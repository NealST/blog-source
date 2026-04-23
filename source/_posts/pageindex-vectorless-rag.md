---
title: 一种新的思路，我把传统向量 RAG 检索准确度从 61% 提升到了 94%      
date: 2026-04-18 16:00
tags:
  - AI
  - AI-engineering
categories:
  - AI
---

最近在做一个文档处理类的产品，我拿了一份 120 页 10-K 的金融年报（约 10 MB 的 PDF，纯文本量 4 万英文单词）做测试。

首先我搭了一套标准 RAG 流程：PyMuPDF 解析，LangChain 分块，OpenAI Embedding 入 Pinecone，余弦相似度检索，GPT 生成答案。整个过程一周搞定。

不出意外的是终究还是出意外了。

当我问"该公司 2025 年总负债是多少"，系统返回了 CEO 致辞里的一句话——"我们在过去一年中大幅降低了负债水平"。

简直离了大谱！事后检查数据我发现这个召回的余弦相似度数字是 0.89，而真正准确的那个结果相似度是 0.71，排第 8，压根儿就没进 top-k，原始信息藏在一张资产负债表中。

于是我又折腾了两周：分块大小从 500 改到 300 又改到 1000，Embedding 换了 Cohere 又换了 Voyage AI，还加了 reranker，也试了 HyDE。准确率从 **52%** 艰难爬到 **61%**，但这个数字在实际应用场景肯定也没法见人。

后来我发现，问题其实不在调参上。而是 RAG 的假设本身就有问题——"语义最相似 = 最相关"。上面那个 case 里，债务策略在语义上跟"总负债"确实是像，但它并不是应有之义，由于资产负债表本身几乎没有叙述性文字，导致向量根本就没捞到。

分块策略也给我帮了倒忙。100 页文档切成几百个碎片之后，"如表 3.2 所示"跟表 3.2 可能就不在同一个块里，"见附录 G"也是虚空索敌。文档本来有结构，切完就没了。

用户问的是"我想知道什么"，答案写的是"信息长什么样"，两边的口径经常是牛头不对马嘴，如同天主教徒与基督教徒讨论节育一般，单纯的语义相似度就解不了这种匹配问题。

**整个思路就不对。**

## 换个思路

偶然间我看到了 [PageIndex](https://github.com/VectifyAI/PageIndex)，VectifyAI 团队在去年 9 月份做的一个开源框架。

框架的核心思路一句话总结：**不把文档变向量，而是变成一棵树，让 LLM 在树上推理找答案。不需要 Embedding 和向量数据库，不做分块，可以称之为"无向量 RAG"。**

这套方案在 FinanceBench（一个专门评估金融文档问答系统的 benchmark 数据集）上达到了 **98.7%** 的准确率，而传统向量 RAG 大约 **50%**。

最开始我是不大信的。但仔细研究后，确有其 make sense 的地方，跟传统 RAG 问"哪些片段跟查询长得像"的搜索策略不同，它走的是一种仿生学的路子："人类分析师会怎么翻文档找答案"。

人类拿到一份 200 页的报告时不会从头读，会先看目录，判断"大概在财务报表部分"，再翻到目录所在页码，如果判断有误就再回来找下一章。

PageIndex 本质就是把这个过程自动化了。

## 揭开面纱

出于好奇，我去翻了它的源码，它的执行步骤可以总结为两步。

### 第一步：给文档建一棵目录树

文档进来后，PageIndex 先读文档的结构——标题、子标题、章节——然后构建一棵层级树。每个节点是一个章节，带有 LLM 生成的标题和摘要。

以前文的 10-K 年报为例，这棵树大致长这样：

```
Annual Report 2023
├── Business Overview
│   ├── Products and Services
│   └── Market Position
├── Risk Factors
│   ├── Financial Risks
│   └── Operational Risks
├── Financial Statements
│   ├── Balance Sheet
│   │   ├── Assets
│   │   └── Liabilities
│   └── Income Statement
└── Notes to Financial Statements
    ├── Note 1: Accounting Policies
    └── Note 12: Long-term Debt
```

文档从一堆扁平碎片变成了可以导航的结构。

### 第二步：在树上推理式搜索

当查询到来时，PageIndex 跑的是一个迭代循环，不是一次性的向量查找：

1. 把查询和目录树交给 LLM，让它理解文档的整体布局。
2. LLM 判断："长期负债的问题，应该去 Financial Statements，大概率在 Notes 里。"返回一个节点 ID。
3. 展开那个节点，提取对应页面的原始文本。
4. LLM 评估：信息是否足够准确和充分。
5. 不够——带着已有上下文回到目录树，选下一个节点。
6. 够了——生成答案。

这个循环设计让它能处理跨章节的问题。即使数字在资产负债表里，解释在附注里，PageIndex 的推理循环也会分两次把它们都找到。

到这里思路不错，但还不算特别惊艳。深入翻源码才发现，真正撑起这个系统的是一堆工程细节。

## 工程细节

### 不是所有文档都有目录——三条路径自动降级

PageIndex 建树不是只有一条路。源码里有三条处理路径：

1. **`process_toc_with_page_numbers`**——文档有目录、有页码。最理想的情况，直接解析。
2. **`process_toc_no_page_numbers`**——有目录但没页码，LLM 逐段扫描正文，给每个标题定位物理页码。
3. **`process_no_toc`**——完全没目录，按 Token 上限分组页面，让 LLM 从正文中推断出结构，本质上是让模型自己发明一份目录。

PageIndex 的执行路径是：先跑最优路径，如果验证准确率低于 **60%**，自动退到下一级重试。即使文档完全没有结构化标题，PageIndex 也不会直接失败——效果会降级，但不大会崩。

### PDF 页码不可信——投票校准

做过 PDF 解析的人都知道这个坑：目录标注的页码和物理页码经常对不上。前言用罗马数字，正文从 1 重新开始，但 PDF 的物理页码可能已经到了 15。

PageIndex 的做法：从已定位的标题中，同时拿到 TOC 标注的页码和 LLM 从正文中识别的物理页码，算差值，然后用投票机制取出现次数最多的偏移量作为全局校正值，简单且实用。

### 不信任 LLM 的第一次输出——验证修复循环

这个设计我觉得是整个系统里最值得学的。给文档建完树之后，PageIndex 不直接用，先跑一套并发验证。

对每个节点，LLM 会检查：这个标题真的出现在它声称的那个页面上吗？如果不对就缩小范围重新查找。为了避免模型异常导致无限循环，这个"修复→验证"的 loop 最多跑 3 轮。
 
```
生成树 → 并发验证所有节点 → 准确率 100%？→ 直接使用
                                    ↓ 否
                            准确率 > 60%？→ 修复错误节点（最多 3 轮）
                                    ↓ 否
                            降级到下一种处理路径，重来
```

**98.7%** 的准确度不是 LLM 一次蒙对的，是系统反复校验逼出来的。

### 树的深度是自适应的

如果某个节点太大（超过 **10 页**且 **20000 Token**），PageIndex 会在内部递归跑一次 `process_no_toc`，生成更细的子树。

一份 200 页的报告里，"Financial Statements"只有 5 页就保持叶子节点，"Notes to Financial Statements"有 80 页就自动拆分成深层子树。根据内容量进行动态调整。

反过来也有优化：对 Markdown 文档，如果一个节点及其子节点加起来不到 **5000 Token**，就把子节点合并回父节点。避免树碎得太细，减少 LLM 推理的层级。

### 还有两个细节

一个是 Vision RAG。PageIndex 可以跳过 OCR，直接把 PDF 页面当图片丢给多模态 LLM。表格密集的文档特别受益，文本提取经常把行列关系搞混，多模态模型直接"看"布局反而更准。

另一个是双模型策略。配置里分了 `model`（建索引，默认 GPT-4o）和 `retrieve_model`（做检索，默认 GPT-5.4，如果是当前最强的 Claude Opus 4.7 效果会更好）。

索引要的是文本理解和结构化输出，检索要的是推理能力，需求不一样，拆开用不同模型也合理。底层可以随时切换 LiteLLM，OpenAI、Anthropic、Google 等不同的厂商。

## 自己跑一遍

看完源码之后我决定自己写一个简化版，用 Gemini API 跑通核心流程。下面是完整的五步实现。

### 第 1 步：解析文档

用 PyMuPDF 逐页提取文本：

```python
import fitz  # pip install pymupdf

def parse_pdf(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append({"page_num": i + 1, "text": text})
    doc.close()
    return pages
```

然后把连续页面按章节分组。跟随意分块不一样，这里按页面自然边界走：

```python
def group_pages_into_sections(pages, per_section=3):
    sections = []
    for i in range(0, len(pages), per_section):
        batch = pages[i : i + per_section]
        section_id = f"S{str(i // per_section + 1).zfill(3)}"
        combined_text = "\n\n".join(p["text"] for p in batch)
        sections.append({
            "section_id": section_id,
            "start_page": batch[0]["page_num"],
            "end_page": batch[-1]["page_num"],
            "text": combined_text,
        })
    return sections
```

### 第 2 步：构建树索引（LLM 驱动）

不算 Embedding，直接让 Gemini 读每个章节的预览、生成结构化摘要。
出来的是一棵 JSON 树，每个节点带标题、摘要和关键主题。

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

def index_section(section: dict) -> dict:
    preview = section["text"][:1500]
    prompt = f"""Read this section from a document and summarize it.
Section pages: {section['start_page']} to {section['end_page']}
Text:
{preview}
Respond with ONLY valid JSON:
{{
  "title": "short descriptive title (5-8 words)",
  "summary": "2-3 sentence summary of what this section covers",
  "key_topics": ["topic1", "topic2", "topic3"]
}}"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0),
    )
    parsed = json.loads(response.text.strip())
    return {
        "node_id": section["section_id"],
        "title": parsed["title"],
        "pages": f"{section['start_page']}-{section['end_page']}",
        "summary": parsed["summary"],
        "key_topics": parsed["key_topics"],
    }
```

对每个章节运行上述函数，就能得到一棵完整的树，存储为 JSON 文件。

```python
def build_tree_index(sections):
    nodes = [index_section(s) for s in sections]
    return {
        "title": "Your Document Title",
        "total_sections": len(nodes),
        "nodes": nodes,
    }

# 保存以供复用
with open("tree.json", "w") as f:
    json.dump(tree, f, indent=2)
```

### 第 3 步：树搜索（推理，而非相似度）

这一步是脱离传统 RAG，彻底不走寻常路的地方。问题来了之后不查数据库，把整棵树丢给 LLM，让它判断哪些章节最可能有答案。

```python
def retrieve_sections(tree: dict, query: str) -> dict:
    tree_text = f"Document: {tree['title']}\n\n"
    for node in tree["nodes"]:
        tree_text += f"[{node['node_id']}] Pages {node['pages']} | {node['title']}\n"
        tree_text += f"  Summary: {node['summary']}\n"
        tree_text += f"  Topics: {', '.join(node['key_topics'])}\n\n"

    prompt = f"""You are a document retrieval expert.
Given this document tree, identify which sections most likely answer the question.
Think step by step about where a human expert would look.

{tree_text}

QUESTION: {query}

Respond with ONLY valid JSON:
{{
  "reasoning": "your step-by-step reasoning about where to look",
  "selected_ids": ["S001", "S004"],
  "confidence": "high/medium/low"
}}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0),
    )
    return json.loads(response.text.strip())
```

`reasoning` 字段不是装饰品，它会告诉你模型为什么选了那些章节。你能看到检索决策的过程，不只是一个相似度分数。这是向量搜索做不到的。

### 第 4 步：内容提取

拿到章节 ID 之后，直接从解析好的章节里取原始文本。就是一次字典查询，没有向量计算。

```python
def retrieve_content(selected_ids: list, sections: list) -> str:
    section_map = {s["section_id"]: s for s in sections}
    context_parts = []
    for sid in selected_ids:
        if sid in section_map:
            sec = section_map[sid]
            context_parts.append(
                f"--- Pages {sec['start_page']}-{sec['end_page']} ---\n"
                + sec["text"][:3000]
            )
    return "\n\n".join(context_parts)
```

### 第 5 步：生成答案

把提取到的文本和问题一起丢给 Gemini 生成答案：

```python
def generate_answer(query: str, context: str) -> str:
    prompt = f"""Answer the question using only the provided context.
Be specific. Include exact numbers, technical terms, and cite page numbers.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1),
    )
    return response.text.strip()
```

## 我的评价

| 维度 | 传统向量 RAG | PageIndex |
|---|---|---|
| 检索方式 | 向量相似度搜索 | LLM 推理式树搜索 |
| 索引方式 | Embedding + 向量数据库 | 层级树结构 (JSON) |
| 分块策略 | 固定大小分块 | 保留文档自然结构 |
| 准确率 (FinanceBench) | ~50% | 98.7% |
| 可解释性 | 低（只有相似度分数） | 高（完整推理链 + 页码引用） |
| 延迟 | 低（单次向量查询） | 较高（多次 LLM 调用） |
| 适用场景 | 大规模文档集合的语义搜索 | 单篇复杂文档的精确问答 |

PageIndex 并非万能。

它擅长处理单篇长文档，尤其适合金融报告、法律合同、技术手册、学术论文这种有层级结构、有交叉引用、对准确率要求高的东西。

如果你的用户需要知道答案来自哪一页，PageIndex 给得了，向量 RAG 给不了。

但它不适合从一千份文档里找到相关的那几份，向量 RAG 做这个好得多。而且每次查询要跑多轮 LLM 调用，大规模用的话成本和延迟都是问题。

对于短文档、纯叙述类的东西（聊天记录、会议纪要），没有层级概念，也发挥不出优势。

我现在的做法是采用混合架构：先用向量搜索从文档集合中锁定对的文档，再上 PageIndex 从那份文档里提取准确答案。

## 写在最后

对于文章开头的那个 case，我用 PageIndex 重新做了检索实现。之前卡在 **61%** 的准确率，一路蹿升到了 **94%**。剩下的 6% 基本都是文档本身信息不完整所致。

PageIndex 做的事情说到底就一件：**模拟人类读文档的方式，把检索从相似度问题变成推理问题。**

Claude Code 其实也是类似的路子，用模型推理驱动的 `glob` 和 `grep` 搜索命令来查找本地文件系统中的相关内容，在检索效率和质量上相较于最早 cursor 的向量检索都取得了更好的效果。

**当任务需要理解结构、追踪逻辑的时候，推理确实比相似度好使。**

### 参考资料

- 完整开源代码：[github.com/VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex)
