---
name: content-pipeline
description: 内容生产和分发统一管线。素材收集→出稿→排版→封面→朋友圈文案→多平台转换→一键分发。涵盖公众号写作、小红书轮播图、即刻文案、播客音频、品牌视频、Chrome CDP 自动发布。
---

# 内容管线 Content Pipeline

> 本技能默认使用墨筝品牌色。你可以在 `references/` 目录下修改为自己的品牌色，或在 `local/SKILL.local.md` 中覆盖路径和个人设定。

一条龙：素材收集 → 写文章 → 排版 → 多平台内容 → 一键分发。

---

## 存储位置

博客文章与自媒体产物分开存放，支持两种内容形态：

```
source/_posts/                      # 博客长文（Hexo 管理，只放 .md）
├── [文章标题].md
└── ...

content/[slug]/                     # 自媒体产物（content-pipeline 管理）
├── post.md                         # 短资讯源文件（仅短资讯有，长文的 .md 在 source/_posts/）
├── preview.html                    # 公众号排版预览
├── cover.html                      # 公众号头图
├── cover_medium.html               # Medium 风格头图（可选）
├── illustrations.html              # 文章配图
├── illustrations_medium.html       # Medium 风格配图（可选）
├── manifest.json                   # 分发清单
├── [主题]-小红书版.html            # 小红书轮播图
└── drafts/
    └── current.json                # 当前素材列表
```

**两种内容形态：**
- **博客长文**（发博客 + 多平台分发）：`.md` 在 `source/_posts/`，`content/{slug}/` 只放产物
- **短资讯**（只做平台分发，不发博客）：`.md` 在 `content/{slug}/post.md`，产物同目录

**slug** = Markdown 文件名去掉 `.md`（如 `kimi-vs-opus.md` → `content/kimi-vs-opus/`）。

输出目录默认为 `content/[slug]/`。用户可指定其他路径，或在 `local/SKILL.local.md` 中配置默认路径。未指定目录时，多平台产出放 `/tmp/`。

### 命名规范

| 项目 | 规则 | 示例 |
|------|------|------|
| 文章 slug | Markdown 文件名去掉 `.md` | `kimi-vs-opus` |
| 产物目录 | `content/{slug}/` | `content/kimi-vs-opus/` |
| 短资讯源文件 | `post.md`（仅短资讯） | `content/ai-weekly-0512/post.md` |
| 排版预览 | `preview.html` | `content/kimi-vs-opus/preview.html` |
| 头图 | `cover.html` | `content/kimi-vs-opus/cover.html` |
| 配图 | `illustrations.html` | `content/kimi-vs-opus/illustrations.html` |
| 分发清单 | `manifest.json` | `content/kimi-vs-opus/manifest.json` |
| Medium 变体 | 后缀 `_medium` | `cover_medium.html` |
| 小红书轮播 | `{主题}-小红书版.html` | `kimi-vs-opus-小红书版.html` |

---

## 触发词

### 素材收集（Path A）

| 触发词 | 说明 |
|-------|------|
| `/story` | 查看当前素材状态 |
| "看看素材" | 查看已记录的素材 |
| "出稿" | 生成文章 + 排版 + 封面图 |
| "清空素材" | 清空当前素材 |
| "记一笔：xxx" | 手动添加素材 |
| "素材+1：xxx" | 手动添加素材 |
| "写个朋友圈" | 根据素材/文章生成朋友圈文案 |

### 内容生成（Path B）

| 触发词 | 说明 |
|-------|------|
| `/xiaohongshu` + 微信链接 | 微信文章转小红书轮播图 |
| "转小红书" + 微信链接 | 同上 |
| "做成小红书" + 微信链接 | 同上 |
| "转即刻" + 微信链接 | 生成即刻文案 |
| "转播客" + 微信链接 | 生成播客脚本 + AI 语音 |
| `/podcast` + 链接/文章/书名 | 小宇宙播客全流程（15分钟百家讲坛风格） |
| "做播客" + 链接/文章/书名 | 同上 |
| "录播客" + 链接/文章/书名 | 同上 |
| "讲书播客" + 书名/链接 | 百家讲坛风格讲书播客 |
| `/shiji` + 文章/素材 | 史记罗生门栏目播客（AI侦探×史源追踪） |
| "史记罗生门" + 文章/素材 | 同上 |
| "做史记播客" + 文章/素材 | 同上 |
| "做视频" + 微信链接 | 触发品牌视频管线 |
| "做视频画布" + 网址列表 | 生成录屏画布（全屏网页演示 + 露脸 + 提词器） |
| "录屏画布" + 网址列表 | 同上 |
| "录屏" + 网址列表 | 同上 |
| "多平台分发" + 微信链接 | 一次生成所有平台内容 |
| "转小红书并发布" + 微信链接 | 生成 + 自动触发分发 |

### 文章阅读

| 触发词 | 说明 |
|-------|------|
| `/read-gzh` + 微信链接 | 抓取并总结公众号文章 |
| "帮我读一下这篇公众号" | 同上 |
| "总结一下这篇文章" | 同上 |

### 排版与配图

| 触发词 | 说明 |
|-------|------|
| "排版" | 用墨筝主题排版 Markdown → 公众号 HTML |
| "做头图" / "封面图" | 生成公众号头图 HTML（浏览器下载 PNG） |
| "头图提示词" / "封面提示词" | 生成贴合墨筝品牌的 DALL-E/Midjourney 极简生图 Prompt（见 cover-template.md） |
| "做竖版封面" / "竖版头图" | 从公众号封面 → 生成 3:4 竖版封面（1080×1440），适合小红书/视频号 |
| "做配图" / "准备配图" | 生成文章配图 HTML（浏览器下载 PNG） |
| "排版+配图" / "全套排版" | 排版 + 头图 + 配图一起生成 |

### 分发

| 触发词 | 说明 |
|-------|------|
| `/distribute` | 读取 manifest 一键发布 |
| "一键发布" | 全平台发布 |
| "全平台发布" | 同上 |
| "发布到小红书" | 单平台发布 |
| "发布到即刻" | 单平台发布 |

---

## 核心原则：全然诚实

**AI 生成的内容必须诚实标注，不装人类，展现真实的创作过程。**

### 诚实标注规范

当 AI 参与内容创作时，必须在文章中明确标注：

```markdown
**调研 & 撰写**：AI（Claude）
**主导 & 审校**：[用户名]
**创作时间**：[实际用时]（调研 X 分钟 + 写作 Y 分钟）
```

### 禁止的虚假表述

❌ **不要写：**
- "我们花了两周时间调研"（实际几分钟）
- "经过深入访谈"（没有访谈）
- "团队经过讨论"（没有团队）
- "作者：XXX / 编辑：AI 助手"（AI 写了全文）

✅ **应该写：**
- "本文基于 N 篇公开信息源，由 AI 调研分析并撰写"
- "素材收集用时 X 分钟，写作用时 Y 分钟"
- "人类主导 + AI 协作"

### 为什么要诚实

1. **建立信任**：读者值得知道内容如何生成
2. **展现价值**：AI 快速高质量创作本身就是价值，不需要掩饰
3. **符合伦理**：AI 生成内容应该透明化
4. **长期主义**：诚实是长期个人品牌的基石

---

## 两条输入路径

### Path A：日常素材收集 → 出稿

```
边干活边记录 → 说"出稿" → 写文章 → 排版 → 封面图 → 朋友圈文案 → manifest
```

适用场景：日常和 cc 协作时，自动积累素材，攒够了一键出稿。

### Path B：微信链接 → 多平台内容

```
微信链接 → 抓取文章 → 分析结构 → 生成小红书/即刻/播客/视频 → manifest → 分发
```

适用场景：已有公众号文章，一键转为多平台内容并发布。

---

## Path A 流程：素材收集 → 出稿

### 自动记录（默认开启）

cc 在对话中**主动识别有料瞬间**并自动记录，无需手动触发。

**识别信号：**

| 类型 | 识别信号 | 示例 |
|-----|---------|------|
| 踩坑翻车 | 预期≠结果、报错、折腾半天 | "试了三种方案都不行" |
| 意外发现 | "没想到"、"原来可以"、意外有效 | "居然这样就解决了" |
| 迭代打磨 | 改了多版、从复杂到简洁 | "200行改成20行还能跑" |
| 搞笑时刻 | 对话金句、AI抽风、神奇bug | "它认真地给我写了一堆错的" |
| 突破时刻 | 卡了很久终于通 | "困扰一周的bug终于找到了" |
| 方法沉淀 | 可复用的技巧、心得 | "以后遇到这种情况就这么办" |

**自动记录时**：不打断对话，段落结尾标记 `（✓ 素材+1）`

### 手动记录

用户说"记一笔：xxx"或"素材+1：xxx"时记录。

### current.json 格式

```json
{
  "topic": "主题（可选，出稿时自动提取）",
  "materials": [
    {
      "time": "2026-01-30 14:30",
      "content": "素材内容",
      "type": "搞笑时刻",
      "context": "可选的上下文备注",
      "auto": true
    }
  ],
  "created": "2026-01-30"
}
```

### 出稿步骤

1. **读取素材** — 读取 `drafts/current.json`
2. **分析提炼** — 提炼主题和故事线
3. **判断内容类型 → 选择写作框架**：

| 内容类型 | 判断信号 | 使用框架 | 参考文件 |
|---------|---------|---------|---------|
| **说明书类** | 开源项目介绍、工具/产品说明、知识库/数据集发布、平台使用指南、"介绍一下 xxx" | 六段式说明书框架 | `references/manual-framework.md` |
| **教程类** | 教人安装/使用/配置工具、Skill 介绍、技术实战、"怎么做 xxx" | 六段式教程框架 | `references/tutorial-framework.md` |
| **深度长文** | 行业分析、人物故事、趋势判断、观点输出、"为什么 xxx" | 四幕式深度框架 | `references/writing-style.md` |

**说明书类文章框架（3000-6000 字）：**
```
项目定义+核心数据（标题即摘要，开头即高潮）
→ 一、核心成果（数据总览表）
→ 二、功能特性（逐一展开，每个一小节+配图）
→ 三、怎么用（按用户分层：零门槛→进阶→开发者→创作者）
→ 四、价值/洞见（超出工具本身的意义）
→ 五、扩展路线（可选）
→ 写在最后（核心价值+愿景+链接）
```

**教程类文章框架（2000-4000 字）：**
```
先看结果（截图+成品+链接）
→ 一、核心概念是什么（表格+一句话定义）
→ 二、怎么安装/使用（分步骤+代码块+配图标记）
→ 三、实战演示（分阶段+表格展示+人机协作）
→ 四、拿走即用（快速安装命令+使用方式表格）
→ 写在最后（升华+CTA）
```

**深度长文框架（8000-12000 字）：**
```
序言（故事先行，700 字不出论点）
→ 01 铺设背景
→ 02 核心论述
→ 03 转折/案例
→ 04 升华/收束
```

4. **读风格指南** — 写文章前**必须先读** `references/writing-style.md`。这是从鱼头头 9 篇已发布文章中逆向工程出的真实写作模式，不是理论指南。核心要点：极短段落（1-3句）、单句成段做"钉子"、口语化动词、"不是A是B"金句句式、数字制造反差、表格优先于段落。
5. **写文章** — 按对应框架 + 风格指南写文章。写完后用风格指南末尾的"按类型写作清单"自检一遍。
6. **保存** — 保存 Markdown 文件
7. **排版** — 调用排版工具生成 HTML 预览（墨筝主题）
8. **头图 + 配图** — 生成可下载的 HTML 文件（→ 读 `references/cover-template.md`）
   - **竖版封面（可选）**：用户说"做竖版封面"时，从已生成的公众号头图 HTML 转换 → 读 `references/cover-vertical-spec.md`
   - **配图与排版 HTML 的关联**：生成配图后，用 Playwright 截图为 PNG，然后运行 `python3 ${SKILL_DIR}/scripts/insert_image_placeholders.py <preview.html> <illustrations.html>` 自动在排版 HTML 的对应章节位置插入 `<!-- IMAGE:配图-N.png -->` 占位符。分发脚本会自动将配图上传到微信 CDN 并替换占位符为 `<img>` 标签。
   - **图片必须不透明（RGB，无 alpha）**：所有 html2canvas 导出的 PNG 必须在导出前调用 `flattenAlpha(canvas, bgColor)` 消除透明通道。详见 `references/cover-template.md` 中的 helper 函数。原因：微信等平台在白底上渲染透明 PNG，暗底封面会变白。
9. **朋友圈文案** — 生成朋友圈推广文案（→ 读 `references/platform-copy.md`）
10. **manifest** — 生成 manifest.json，供 `/distribute` 使用。

   **WeChat 发布流程（全自动）**：
   1. 写文章（Markdown）
   2. 排版（`md2wechat_formatter.py` 生成 `_preview.html`）
   3. 生成配图 HTML → Playwright 截图为 PNG
   4. 在 `_preview.html` 中插入图片占位符 `<!-- IMAGE:文件名.png -->`
   5. 生成 manifest.json（包含所有路径）
   6. 执行 `/distribute --platforms wechat`（API 自动：上传封面→上传配图→替换占位符→推送草稿箱）

   wechat 部分字段说明：
   - `wechat.html`（**必填**）：排版后的 `_preview.html` 路径（配图位置用 `<!-- IMAGE:文件名.png -->` 标记）
   - `wechat.cover_image`（**必填**）：封面 PNG 路径
   - `wechat.title`（**必填**）：文章标题
   - `wechat.author`：作者名（默认 `墨筝`）
   - `wechat.digest`：文章摘要（120 字内）
   - `wechat.images`：配图 PNG 路径列表（按文章中出现的顺序排列，分发脚本会上传并插入到对应占位符位置）
   - `wechat.markdown`（可选）：文章 Markdown 路径（仅作记录，不再用于转换）
11. **询问** — 是否清空当前素材

### 排版命令（**仅公众号 preview.html**）

> **⚠️ Scope 警告**：本节规则只针对公众号产物 `preview.html`，由 `md2wechat_formatter.py` 渲染，使用 `<section>` 标签 + 内联 CSS 适配微信 API。
>
> 公众号默认正文字号 `large = 16px` / `medium = 15px`，与小红书的 18-19px 完全不同。**不要把 Path B 第 3-4 步里小红书的 `.slide` 卡片结构、27/22/19px 标题层级、html2canvas 下载工具栏混入公众号 preview.html**。

```bash
cd "$MD_FORMATTER_DIR"
python3 md2wechat_formatter.py [文章路径] -o content/[slug]/preview.html
# 可选参数：--font-size large（默认 16px）或 medium（15px）
```

> `$MD_FORMATTER_DIR` 需在 `local/.env` 或环境变量中配置。
> `-o` 参数指定输出到 `content/[slug]/` 目录，保持博客文章与产物分离。
> CSS 自动内联到 style 属性，适配微信 API 推送。输出的 `preview.html` 使用 `<section>` 标签确保微信兼容。

使用统一的「墨筝」主题——墨色 #1C1C1E + 筝弦金 #C4956A + 宣纸底 #F2EDE3，融合 Medium 排版精华。
推荐字号：`large`（16px，默认）、`medium`（15px）

### 排版避坑：视觉元素的"金色左竖线"冲突

H2 标题使用 `border-left:4px solid #C4956A` 时，正文中的引用块（blockquote / 提示词卡片）**不要再用同款金色左竖线**，否则两块紧挨时视觉重复，H2 的"分章"地位被削弱。

**正确分工**：
- **H2 标题**：金色左竖线（4px）+ 12px 左 padding —— 负责"分段锚点"
- **引用 / 提示词卡片**：四面浅边框 + 浅米底 + 圆角 —— 负责"信息容器"，安静不抢戏

**推荐的引用卡片内联样式**（已验证）：
```html
<blockquote style="margin:0 0 16px; padding:14px 18px; border:1px solid #e8dfd0; background:#f5efe4; border-radius:6px; font-size:14px; line-height:1.7; color:#444">
  <!-- 内容 -->
</blockquote>
```

**双语提示词约定**：中文用正常样式，英文原文紧跟一行，颜色 `#7a6952` + `font-style:italic`，作为可静音的参考信息。

---

## Path B 流程：微信链接 → 多平台内容

### 第 1 步：抓取文章

使用 Python 抓取脚本（微信有反爬验证，WebFetch 会被拦）：

```bash
python3 "${SKILL_DIR}/scripts/fetch_wechat_article.py" "<URL>" --json
```

超时 30 秒。失败则提示用户手动复制文章正文。

如果用户只是说"帮我读一下这篇公众号"（`/read-gzh` 触发），执行抓取后直接生成结构化总结，不进入后续内容生成流程。总结格式：

```markdown
# 文章总结
## 基本信息（标题/作者/类型/配图数）
## 核心观点（3条）
## 关键信息
## 金句摘录
## 图片内容（下载并识别配图中的文字）
## 思考/迭代点
```

### 第 2 步：分析文章结构

提取：标题、副标题/金句、核心概念、关键数据、步骤/流程、亮点/特色、方法论/金句、行动召唤。

### 第 3 步：拆分为卡片（**仅小红书**）

> **⚠️ Scope 警告**：本步骤及第 4 步内的全部排版规则（卡片尺寸 540×720、字号 18-27px、h1/h2/h3 层级、稀疏页清单、下载工具栏、CORS 修复、avatar base64 内嵌等）**只适用于小红书轮播图**。
>
> **公众号** 的排版完全独立，走 Path A 的 `md2wechat_formatter.py`（正文 16px `large` / 15px `medium`），见 "### 排版命令" 一节。**不要把小红书的字号、`.slide` 结构、`html2canvas` 下载工具栏混入公众号 preview.html**。
>
> **即刻 / 播客 / 视频** 的产物同样不受本节约束。

**小红书图文转换核心原则：保留原文，不压缩、不杜撰**
小红书帖子单篇最多支持 18 张图片。请充分利用这 18 张图的额度来展示原文内容。如果原文极长，18 张图排满后仍有剩余，则在第 18 张图及正文末尾提示：「由于篇幅限制，完整内容请移步微信公众号『墨筝』阅读」。

**Markdown 格式转换规则：**
- **文章主标题（h1）**：原文 `title` 字段。使用最显眼的字号 + 衬线字体 + 上下细线点缀，全片仅在第 1 张卡片出现一次。
- **章节标题（h2 `##`）**：金色左竖线 + 较大无衬线字体。
- **子章节标题（h3 `###`）**：金色文字 + 较小字号，仅作小段引导，绝不能与 h1/h2 撞样式。
- **列表项**：将 `-` 或 `*` 替换为有视觉区分度的极简形符号（如 • 或方形），杜绝使用 Emoji。嵌套列表用 `-` 显示且左缩进。
- **重点文字（加粗）**：使用主题色（如 #C4956A）显示，或在两侧加特殊符号（如【】），不可使用 Emoji。
- **表格**：小红书不能直接展示表格，需转化为卡片内的结构化键值对（Key-Value）排版。
- **图片**：原文 `![]()` 的图片**必须**独占一整张卡片，完全无 Header/Footer/页码，整张卡片就是一张干净的图，便于读者放大查看。
- **Emoji**：严格禁止在生成的纯文本或代码层中自行添加 Emoji 符号。
- **完整性要求**：所有正文段落、列表项、表格行、强调文字、斜体注释（如禁用环境变量提示）**必须 1:1 保留**，禁止抽象、概括、改写。如果一页放不下，应跨多页继续展示。
- **反空白页规则**：严禁出现"过渡页/指引页"，例如只放一个章节标题加一句"下一张图是…"。具体执行：
  - 章节 h2 必须与首段正文 / 首条列表 / 表格放在**同一张卡片**。
  - 一张卡片若有效内容（去掉 Header/Footer 后）占比不足卡片高度的 50%，必须向上合并到前一张或向下吸收下一张的开头。
  - 图片独占卡片（`.slide.img-only`）周围的文字卡片，不需要再写"下一张图为…"之类的衔接句，图与文上下相邻即天然衔接。
  - **段落容量下限**：纯文字卡片至少包含 3 段正文 / 或 1 段正文 + 3 条列表 / 或 1 个 h2 + 2 段正文。单段 1-2 句话且无列表/代码的"小卡片"必须与相邻同主题段落合并。
  - **拆页前先合并同主题**：拆分卡片之前，先将连续的短段落（每段 ≤ 80 字）按主题归并；只有当合并后高度真的超过 720px 才再拆。

#### 稀疏卡片自检清单（每生成完一版都跑一遍）

按顺序检查每张卡片，命中任一就要修：

1. **是否只有一个标题 + 一句过渡语**（如「跑分情况 / 下面是数据」「特性三 / 大概是这样」）→ 删过渡语，把 h2/h3 直接放到下一张内容卡片顶部。
2. **是否只有 2 段短文本**（每段 ≤ 80 字，且无列表/代码/表格）→ 上下合并同主题段落；如果合并后 > 720px 再考虑用粗体小标题（如「**适合场景**：」「**慎用场景**：」）把不同子点拼到一页。
3. **是否一个 h2 + 一个 h3 + 一两段引子独占一页**（典型"章节扉页"，但小红书没有目录页需求）→ 把这块章节起头并到该章节的第一张实质内容卡（列表/表格/图说明）顶部。
4. **是否在表格/list 卡之后还跟一张「举例 + 总结」短卡**（如「举例：High 0.05，Low 0.005，Max 0.4」+「现实情况大家都用 High」）→ 删掉重复的小标题（表格本身已是该主题），把举例和总结压缩为一段并入表格那张卡的页脚位置。
5. **是否在图片独占卡之前/之后留了一张「图 + 一句话说明」短卡** → 文字直接搬到图片的另一侧那张内容卡，让图与文成为天然上下文。

#### 合并时常用的紧凑写法（避免合并后撑爆 720px）

- **两段连写**：用"。"或"；"把两个短段合成一段，去掉过渡词（"另外"、"具体来说"、"现实情况"）。
- **粗体作分隔**：把多个并列子点用 `<strong>子点名</strong>：` 起头放进同一段，省掉每个子点单独成段的空白。
- **list 二合一**：原文若是「子点 A（含解释）」和「子点 A 的备注」两条 list，合成一条 `子点 A：解释。<em>（备注）</em>`。
- **去除重复小标题**：表格上方的「**费用消耗体感参考：**」之类小标题，如果表格本身已经表达了同样意思，直接删。
- **删冗词**：「适合查」「实际上」「比较」「就别用了」这类口语缓冲词在合并时优先精简。

#### 输出前必走一遍 sparse-pass 流程

每次生成 HTML 后，**必须**逐张卡片估算高度占比（mental: header 80 + footer 50 + padding 60 = 190px 固定，剩 530px 留给正文）。任一卡 < 270px（50%）就回到上面 5 项清单走一遍合并，重新生成。该流程在产出"第一版"和每次大改后都要执行。

节奏参考（最多 18 张，按原稿长度自然分页，不要擅自精简）：

| 位置 | 卡片类型 | 内容 |
|------|---------|------|
| 第 1 张 | 头图/开场 | 标题 + 核心 Hook + 背景交代 |
| 中间各张 | 纵深展开 | 逐字逐句排版原文内容（包括通过样式转化的表格/列表），单章可跨多页，保持单页 720px 高度内不拥挤溢出 |
| 第 18 张(若截断) | 未完待续 | "因篇幅限制，完整长文及更多细节，请移步微信公众号『墨筝』继续阅读" |
| 尾页(若未截断) | 封底 | 金句总结 + 统一 footer |

footer 每张都带 `[图标] 微信搜索公众号「墨筝」查看更多精彩内容` 提示，无需额外加微信号 CTA 盒子。

### 第 4 步：生成图片 HTML（**仅小红书**）

输出路径：文章同目录下 `[简短主题]-小红书版.html`，未指定目录放 `/tmp/`。浏览器自动打开预览。

头像路径：生成在 `content/[slug]/` 下的 HTML 中，头像引用用 `../_shared/avatar.jpg`（回退 1 级到 `content/_shared/avatar.jpg`）。`<img>` 配 `onerror` 回退为「墨」字头像，确保加载失败时仍有视觉占位。

**📚 重要：生成前必读范例**

**首选范例**：`references/xiaohongshu-examples/markdown-faithful-范例.html`（Markdown 1:1 还原版式，含 h1/h2/h3 区分 + 图片独占卡片 + 下载工具栏）。
**旧版范例**：`references/xiaohongshu-examples/文字卡片-范例.html`（仅作回顾，新出稿一律用 v2）。

✅ **卡片设计要求**
- 卡片尺寸固定 `540 × 720`（导出 SCALE=2 即 1080×1440，比例 3:4）。
- 同源配色：宣纸底 `#F2EDE3` + 筝弦金 `#C4956A` + PingFang SC 无衬线，公众号同款。
- **标题三级层次必须视觉可区分**，且**严格大于正文字号**：
  - `h1`（文章主标题）：**27px** 黑色衬线字体 + 上下黑色细线，全文仅第 1 张出现一次。
  - `h2`（章节）：**22px** 黑色无衬线 + 4px 金色左竖线。
  - `h3`（子节）：**19px** 金色无衬线，与 h2 颜色形态完全错开。
- **正文字号下限（手机实测过的）**：DOM 是 540×720，但在小红书 App 里图片宽度约等于手机屏宽 360-400px，所以字号要按"实际显示 ~70%"反推。**经多轮 iPhone 实测，最终基线如下（兼顾可读性与单页容量）**：
  - 正文段落 `p` / 一级 `list-item`：**18px**，`line-height: 1.6`（保持舒适，不再继续收紧），`margin-bottom: 7-8px`。
  - 嵌套子项 `list-item.sub`：**16px**。
  - 表格 row：**15.5px**，key 加粗 **16px**，`padding: 6px 0`。
  - 头部 meta 名字：15px，日期：13px。
  - 底部 footer brand / page：12px（信息密度低、可弱化）。
  - **正文（p / list-item）禁止低于 17px**，表格不低于 15px。若卡片放不下，应优先合并稀疏卡或拆页，**绝不通过缩字号或压行高（< 1.5）来塞内容**。
  - **行高底线**：正文 `line-height` 不得低于 **1.55**，低于这个值阅读会发挤。
  - **层级关系硬规则**：h1 > h2 > h3 > 正文 > 子项 > 表格 > footer，相邻层级至少差 1-2px。h3 必须严格大于正文（≥1px），否则标题失去引导作用。
- **间距收紧规则（字号大了就要收 margin）**：字号上调以后，标题 margin-bottom 控制在 10-16px、正文/list-item margin-bottom 控制在 7-8px、`post-header margin-bottom: 14px`、表格 padding 收到 10px 14px，行高保持 ≥ 1.55 不要为了塞内容继续压缩。
- **内联 `<code>` 不可拆**：CSS 必须给 `code { white-space: nowrap; }`，否则带 ASCII 空格的命令（如 `/effort ultracode`、`git commit -m`、`docker run -it`）会在空格处换行，把 `/effort` 留上一行、`ultracode` 挤下一行，中间撑出巨大空白。中文之间夹的 inline `<code>` 也建议在命令内部用 `&nbsp;` 拼接，双保险。
- **长命令独立成块**：超过半行的命令／代码片段，单独用 `<code class="cmd-block">`，CSS 配 `display:block; white-space:pre-wrap; word-break:break-word; padding:8px 12px;`，让它正常换行展示，而不是塞回行内 `<code>` 撑爆布局。
- **图片独占卡片**：原文 `![]()` 必须独占一整张 `.slide.img-only`，黑底 + `object-fit:contain` 全图展示，**无 Header / Footer / 页码 / 金色光晕**。
- **每张卡片 Header**：头像 + 「墨筝」+ MM/DD 自动写入（脚本兜底）。
- **每张卡片 Footer**：左 `微信搜索公众号「墨筝」查看更多内容`，右 `当前页 / 总页数`。

✅ **下载工具栏（必带）**：
- 顶部 fixed 工具栏含两个按钮：`全部下载 (ZIP)` + `下载当前`，外加一个 `#progress` 进度文本。
- 引入 `html2canvas@1.4.1` + `jszip@3.10.1` + `file-saver@2.0.5`（jsDelivr CDN）。
- `flattenAlpha()` 把透明通道展平为底色，避免微信白底渲染时暗底变白。
- 图片独占的 slide 走 `#1C1C1E` 底色路径，其余 slide 走 `#F2EDE3`。
- **跨域图片必须先 inline**：远端图床（如 `im.gurl.eu.org`、telegram 图床等）通常不返回 CORS 头，直接被 html2canvas 渲染会把 canvas 标 tainted，`toBlob` 抛 SecurityError 静默失败、点按钮没反应。必须在每次下载前先跑一遍 `inlineRemoteImages()`：
  - 先尝试直连 `fetch(src, { mode: 'cors', cache: 'force-cache' })` → `blob()` → `FileReader.readAsDataURL` → 写回 `img.src`，等 `img.decode()`。
  - 直连失败必须 fallback 到图片代理：依次尝试 `https://wsrv.nl/?url=<去掉协议头>`、`https://images.weserv.nl/?url=<去掉协议头>`、`https://corsproxy.io/?<完整URL>`，任一成功即可。
  - 所有源都失败时把 `img.src` 替换为 1x1 透明 GIF 占位符（`data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7`），避免污染 canvas 让整个下载流程崩溃。
- **本地图片（如头像）必须在生成期直接 base64 内嵌**：用户多半通过 `file://` 双击打开 HTML，此时本地图片在 canvas 里仍被视为 cross-origin、`fetch()` 也无法读取本地文件，导致跟跨域图床一样的 tainted canvas。**生成脚本**应当读取 `content/_shared/avatar.jpg` 等本地资源，转 base64 后通过占位符（如 `__AVATAR__`）替换到 HTML 里，不要保留任何 `src="../../xxx"` 这种相对路径写法。
- **错误必须暴露**：`downloadAll/downloadOne` 必须用 `try/catch` 包裹，失败时把错误写到 `#progress` 并 `alert()`，否则用户只会看到"点了没反应"。
- 检查 `toBlob` 返回值非空：返回 null 即说明仍被污染，应抛错而不是塞 null 进 zip。

✅ **文案质量要求（硬规则）**：
- **严禁压缩、总结、改写、杜撰**：原文所有段落、列表项（含嵌套子项）、表格行、加粗、斜体注释（如禁用环境变量）必须 1:1 保留。
- 一页装不下就跨多页继续展示，宁可多张卡片也不可裁剪文字。
- 卡片外的小红书正文描述可适度口语化，但卡片内严格忠于原文。

生成的内容应达到 v2 范例的专业水准。

### 第 5 步：生成小红书发布文案

**根据内容类型选择风格：**

- **个人 IP 风格**（真人分享、产品开发、踩坑记录）
  - → 读 `local/SKILL.local.md` 中指定的个人品牌风格文件（如有）
  - 流水账式真实感 + 具体时间细节 + 口语化表达
  - 300-350字，8-12个标签
  - 人设：在 `local/SKILL.local.md` 中自定义

- **墨筝风格**（方法论总结、深度分析）
  - → 读 `references/platform-copy.md` 的小红书部分
  - 结构化拆解 + 干货密度高
  - 适合转载公众号文章

### 第 6 步：生成即刻发布文案

→ 读 `references/platform-copy.md` 的即刻部分。

### 第 7 步：生成播客脚本

**根据触发词选择播客模式：**

| 触发词 | 模式 | 时长 | 风格 |
|--------|------|------|------|
| "转播客" | 标准模式 | 5-8 分钟 | AI搭档聊天风 → 读 `references/platform-copy.md` 播客部分 |
| `/podcast` / "做播客" / "录播客" / "讲书播客" | **百家讲坛模式** | **15 分钟** | **讲书人风格** → 读 `references/xiaoyuzhou-podcast.md` |

**百家讲坛模式**是小宇宙播客的主力模式，适合把文章/书籍改编为有故事感、有节奏感的深度音频内容。

### 第 8 步：AI 语音生成

通过 SSH 连接 Ubuntu 机器，使用 IndexTTS2 本地生成（零样本声音克隆）（→ 读 `references/tts-config.md`）。

**百家讲坛模式的 TTS 调整**：15 分钟脚本约 4000 字，分段大小 600 字（更短分段带来更好的语音节奏），预计 6-7 段。

文件命名：`[播客标题].mp3` + `[播客标题]-播客脚本.md`

### 第 8.2 步：生成播客封面（百家讲坛模式）

→ 读 `references/podcast-cover-template.md`

生成 3000×3000 正方形封面 HTML，墨筝体系，浏览器下载 PNG 后上传小宇宙。

文件命名：`[播客标题]-播客封面.html`

### 第 8.5 步：输出 manifest.json

所有内容生成完毕后，自动输出 manifest.json 到输出目录。格式：

```json
{
  "version": "1.0",
  "created": "<ISO时间戳>",
  "source": "<微信链接>",
  "title": "<文章标题>",
  "outputs": {
    "xiaohongshu": { "html": "...", "copy": { "title": "...", "body": "...", "tags": [...] } },
    "jike": { "copy": { "body": "...", "circles": [...] } },
    "xiaoyuzhou": { "audio": "...", "script": "...", "cover": "...", "copy": { "title": "EP01丨...", "description": "...", "show_notes": "..." } },
    "video_canvas": { "html": "...", "teleprompter_md": "...", "cover_html": "..." }
  }
}
```

如果用户说"转小红书并发布"，生成 manifest 后自动执行 `/distribute`。

### 第 9 步：品牌视频生成（可选）

仅当用户提到"视频"、"抖音"、"视频号"或"品牌视频"时执行：

**A. Remotion 品牌片头片尾**

```bash
cd "$REMOTION_DIR"
npx remotion render src/index.ts Intro --output /tmp/brand-intro.mp4
npx remotion render src/index.ts Outro --output /tmp/brand-outro.mp4
```

> `$REMOTION_DIR` 需在 `local/.env` 或环境变量中配置。

**B. AI 视频 Prompt** — 为 Seedance 2.0 或 Google Veo 生成 4 段视频 prompt

**C. ffmpeg 拼接指令** — 生成拼接命令供用户手动执行

### 第 9B 步：录屏画布生成（可选）

仅当用户说"做视频画布"、"录屏画布"、"录屏"时执行。用户提供**要演示的网址列表 + 简短主题**。

1. **获取输入** — 用户提供：要演示的网址列表 + 简短主题
2. **生成提词器脚本** — 每个网址对应一段口播（80-150 字），含 `[提示]` cue 标记
3. **输出提词器脚本 md** — `[主题]-提词器脚本.md`，用户可直接编辑
4. **组装 HTML** — 读取 `references/video-canvas-template.md` 获取完整 CSS+JS 模板，网址预填 `WEB_URLS` + 提词器脚本填入 `SCRIPTS`
5. **输出文件** — `[主题]-视频画布.html`，保存到用户指定目录或 `/tmp/`
6. **生成封面图** — `[主题]-封面.html`，暗底 + 人像圆框，浏览器下载 PNG
7. **提示用户** — 先检查提词器脚本 md，再在浏览器中打开 HTML 录制。16:9 固定比例，各平台直接上传

### 第 10 步：用户微调

告知用户所有产出物路径，提示可调整，输入 `/distribute` 可一键发布。

**公众号同步提示**：封面 PNG 从浏览器下载后，直接 `/distribute --platforms wechat` 即可同步到草稿箱（API 模式，无需打开 Chrome）。

**一次性产出五样东西，不需要额外要求：**
1. 小红书图片 HTML（含一键下载工具栏）
2. 小红书发布文案（标题 + 正文 + 标签）
3. 即刻发布文案（正文 + 圈子标签）
4. 小宇宙播客（录制脚本 + AI 语音 MP3 + 节目封面）
5. manifest.json（供 `/distribute` 一键发布）

**单独触发 `/podcast` 时，产出三样：**
1. 播客脚本 md（15 分钟百家讲坛风格，3800-4200 字）
2. AI 语音 MP3（IndexTTS2 本地生成）
3. 节目封面 HTML（3000×3000，浏览器下载 PNG）
4. 小宇宙发布文案（标题 + 简介 + 完整文稿）
5. manifest.json

**第 9B 步可选追加（说"视频画布"/"录屏"时）：**
6. 录屏画布 HTML（全屏网页演示 + 摄像头露脸 + 录制 + 提词器 + 美颜，16:9 固定）
7. 提词器脚本 md（按网站分段，可编辑，修改后说"更新提词器"同步到 HTML）
8. 封面图 HTML（暗底 + 人像圆框，浏览器下载 PNG）

---

## 分发流程（/distribute）

读取 manifest.json，通过 Chrome CDP 自动化发布到各平台（→ 读 `references/distribute-platforms.md`）。

### 用法

```bash
# 全平台发布
npx -y bun "${SKILL_DIR}/scripts/distribute/distribute.ts" --manifest /path/to/manifest.json

# 选择平台
npx -y bun "${SKILL_DIR}/scripts/distribute/distribute.ts" --manifest /path/to/manifest.json --platforms xhs,jike

# 预览模式（不提交，只预填内容）
npx -y bun "${SKILL_DIR}/scripts/distribute/distribute.ts" --manifest /path/to/manifest.json --platforms xhs --preview
```

### 平台缩写

| 缩写 | 平台 | 状态 |
|------|------|------|
| `wechat` | 公众号 | 可用 |
| `xhs` | 小红书 | 可用 |
| `jike` | 即刻 | 可用 |
| `xiaoyuzhou` | 小宇宙 | 可用 |
| `douyin` | 抖音 | 实验性 |
| `shipinhao` | 视频号 | 待开发 |

### 执行顺序

公众号 → 小红书 → 即刻 → 小宇宙 → 抖音 → 视频号（顺序执行，避免 Chrome 端口冲突）

### 四级降级

| 级别 | 模式 | 触发条件 |
|------|------|---------|
| L0 | API 直推 | 公众号 API 直接推草稿箱，无需 Chrome |
| L1 | 自动发布 | CDP 完全自动化 |
| L2 | 辅助发布 | 登录态失效/选择器失效/`--preview` |
| L3 | 手动模式 | CDP 连接失败 |

公众号优先 L0（API），凭证缺失或失败时自动降级 L3（手动）。

### 公众号 API 模式说明

**凭证来源**（按优先级）：
1. 环境变量 `WECHAT_APPID` + `WECHAT_APPSECRET`
2. 配置文件 `~/.config/wechat-api/config.json`

**Token 缓存**：
- 缓存位置：`~/.config/wechat-api/token-cache.json`
- 有效期 2 小时，提前 5 分钟刷新
- 无需手动管理，脚本自动处理

**执行流程**：
1. 获取 access_token（优先读缓存）
2. 从 `_preview.html` 提取文章内容（`extractArticleContent`，兼容 `<div>` 和 `<section>` 容器）
3. 修复 WeChat 不兼容的 HTML 结构（`fixHtmlForWechat`）
4. 扫描并上传本地图片到微信 CDN（`uploadLocalImagesInHtml`）
5. 下载远程图片并上传到微信 CDN（`uploadRemoteImagesInHtml`，跳过已在 `mmbiz.qpic.cn` 上的图片）
6. 上传封面图获取 `thumb_media_id`
7. 调用 `draft/add` 创建草稿

---

## 品牌设计规范

**统一品牌色体系：**
- **墨筝（mozheng）**：所有平台统一使用——墨色+筝弦金体系（公众号、小红书、即刻等）

> **单一真相源**：在 `local/SKILL.local.md` 中指定你的品牌色文档路径。
> 如果色值冲突，以品牌文档为准。以下色板作为默认示例。

### 墨筝色板（墨色+筝弦金体系）

> 公众号「墨筝」专属配色。取意：墨——墨汁近黑微暖；筝——古筝丝弦哑光金。

**比例法则**：墨色 80% : 筝弦金 8% : 宣纸 10% : 其余 2%

| 名称 | 色值 | 用途 |
|------|------|------|
| 墨色（主暗色） | `#1C1C1E` | 暗底卡片背景、标题、表头 |
| 筝弦金（重点色） | `#C4956A` | 强调色、重点文字、链接、分割线（仅点睛） |
| 宣纸底 | `#F2EDE3` | 暗底上的主文字、浅底卡片组件背景（**配图浅底页用 `#FFFFFF` 纯白**） |
| 浓墨 | `#2C2A28` | 渐变暗端、hover 态 |
| 淡墨 | `#7A7876` | 次要文字 |
| 半透白 | `rgba(255,255,255,0.5)` | 暗底上的品牌名 |
| 半透墨 | `rgba(28,28,30,0.4)` | 浅底上的品牌名 |

### 墨筝代码块配色（语法高亮）

代码块使用墨色暗底 `#1C1C1E` + 宣纸白文字 `#F2EDE3`，筝弦金淡边框 `rgba(196,149,106,0.15)`。语法高亮基于 Pygments，色彩从墨筝体系延伸：

| 名称 | 色值 | Token 类型 | 设计意图 |
|------|------|-----------|----------|
| 筝弦金 | `#C4956A` | 关键字 `if/for/export/const` | 与品牌强调色统一 |
| 苔绿 | `#A8C97F` | 字符串 `"hello"` | 暗底上清新可读 |
| 淡墨 | `#7A7876` | 注释 `# comment` | 低调退后，不分散代码阅读 |
| 暖金 | `#D4A76A` | 数字 `42` | 与筝弦金同色系，微暖 |
| 青瓷 | `#8FBCBB` | 函数名 `func()` | 冷色对比，区分关键字 |
| 藤紫 | `#B48EAD` | 类型 `string/int` | 区分函数名与类型 |
| 淡棕 | `#9A8A7B` | 操作符/标点 `= + {}` | 安静不抢眼 |

**设计原则**：暖色系（金/绿/棕）为主调，冷色（青瓷/藤紫）少量点缀，整体不脱离墨筝「文房器乐」的温暖质感。内联 `code` 保持浅底（`#f0ece4`）不变。

### 品牌选择规则

所有平台统一使用墨筝品牌色体系（墨色 #1C1C1E + 筝弦金 #C4956A + 宣纸底 #F2EDE3），保持跨平台视觉一致性。

### 字体

```css
font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

### 品牌角标

每页左上角品牌 logo + 文字，暗底页用 `.light`，浅底页用 `.dark`。
- 墨筝体系：文字显示 `墨筝`，logo SVG 中强调色使用筝弦金 `#C4956A`

### 页码

右下角 `1/N`，暗底页 `rgba(255,255,255,0.2)`，浅底页 `rgba(28,28,30,0.2)`。

---

## 内容改写原则

微信 → 小红书不是照搬，需适配：

| 维度 | 微信 | 小红书 |
|------|------|--------|
| 篇幅 | 2000-3000 字 | 每页 50-80 字 |
| 结构 | 线性阅读 | 卡片式跳读 |
| 语气 | 技术向、深度 | 简洁、直观、有冲击力 |
| 视觉 | 文字为主 | 视觉为主、文字点缀 |

改写要点：标题要炸、数字要大、一页一个点、视觉替代文字、保留核心链接。

---

## 完整模板参考

首次生成小红书图片时，参考 `references/xiaohongshu-examples/` 目录下的范例文件获取完整 CSS + JS。

> 如果有额外的本地模板参考，在 `local/SKILL.local.md` 中指定路径。

生成新内容时复用范例文件的 CSS + JS 部分，只替换卡片内容。

---

## Script Directory

**Agent Execution**: Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>`.

| Script | Purpose |
|--------|---------|
| `scripts/fetch_wechat_article.py` | 微信文章抓取（Python，模拟微信 UA） |
| `scripts/insert_image_placeholders.py` | 配图占位符插入（解析 illustrations.html 的 slide-label，在 preview.html 对应章节插入 `<!-- IMAGE:配图-N.png -->`） |
| `scripts/distribute/distribute.ts` | 分发主编排器 |
| `scripts/distribute/cdp-utils.ts` | 共享 CDP 工具 + Manifest 类型定义 |
| `scripts/distribute/wechat-api.ts` | 公众号 API 客户端（token 管理、图片上传、草稿创建） |
| `scripts/distribute/platforms/*.ts` | 各平台发布模块 |

---

## Reference 文件索引

cc 按需读取，不要一次性加载所有 reference。

| 场景 | 读取文件 |
|------|---------|
| 出稿写说明书文章 | `references/manual-framework.md` — 六段式说明书框架（定义+成果→特性→用法→价值→路线→收束，3000-6000 字） |
| 出稿写深度长文 | `references/writing-style.md` — 人设 + 写作规范 + 格式（四幕式，8000-12000 字） |
| 出稿写教程文章 | `references/tutorial-framework.md` — 六段式教程框架（先看结果→概念→操作→实战→拿走即用，2000-4000 字） |
| 生成头图/配图 | `references/cover-template.md` — 墨筝风格排版规范（头图 + 配图 + 视觉组件） |
| 横版→竖版封面 | `references/cover-vertical-spec.md` — 公众号封面转竖版的 CSS 转换规范 |
| 生成小红书轮播图 | `references/xiaohongshu-text-card.md` — **唯一风格**：公众号同源配色的文字卡片。范例：`references/xiaohongshu-examples/文字卡片-范例.html`。旧多卡片信息图模板 `xiaohongshu-format.md` 已废弃，只作 SVG / 下载脚本存档 |
| 生成各平台文案 | `references/platform-copy.md` — 小红书/即刻/播客/朋友圈文案规范 |
| 生成播客音频 | `references/tts-config.md` — IndexTTS2 本地 TTS 配置 + 生成脚本 |
| 小宇宙播客（百家讲坛） | `references/xiaoyuzhou-podcast.md` — 15分钟讲书人风格脚本规范 + 改编流程 + 发布配置 |
| 播客节目封面 | `references/podcast-cover-template.md` — 3000×3000 正方形封面 HTML 模板 |
| 史记罗生门栏目 | `references/shiji-luoshengmen.md` — 栏目品牌设定 + AI侦探风格 + 脚本结构 |
| 分发到各平台 | `references/distribute-platforms.md` — 平台配置 + manifest 格式 + 降级策略 |
| 生成录屏画布 | `references/video-canvas-template.md` — 录屏画布模板（全屏网页演示+露脸+提词器+录制） |

---

## 故障处理

| 问题 | 处理 |
|------|------|
| 微信抓取失败 | 提示用户手动复制文章正文 |
| 文章太短（<500字） | 压缩为 5-6 张卡片 |
| 文章太长（>5000字） | 精选核心，控制 10 张以内 |
| 导出图片模糊 | 检查 SCALE=2，浏览器缩放 100% |
| manifest 不存在 | 提示先运行内容生成 |
| Chrome 启动失败 | 降级 L3（手动模式） |
| IndexTTS2 模型加载失败 | 检查 checkpoints 目录和 infer_v2 导入 |
| TTS 生成失败 | 只输出脚本文本，提示手动录制 |
