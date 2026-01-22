---
title: 如何构建一个能让 Claude Code 做记忆检索的 Skill
date: 2026-01-18 18:00:00
tags: "AI,Claude Code"
---

## 前言

> 最近看到一个很有趣且实用的 Claude Skill, 可以让 Claude 进行记忆检索，作者是来自德国的开发者，名为 Alex。

在使用 Claude Code 时，一个常见的 case 是我们曾讨论过某个问题或解决方案，但就是找不到具体的记录。比如说 “上周我们修复那个 xx 错误时，最终的解决方案是什么来着？”或者需要总结一下“昨天我们具体做了哪些工作？”

Claude Code 会将每一次会话都存储在本地，但 Claude 默认情况下不会去搜索这些文件。为了解决这个问题，Alex 构建了一个“技能（Skill）”，让 Claude 能够搜索它自己的对话历史。将 Claude 变成了一个真正拥有持久记忆的编程伙伴，能够记住过去的解决方案并对过去的工作进行总结。

## Claude Code 如何存储对话

每一个 Claude Code 会话都会作为一个 JSONL 文件保存在 `~/.claude/projects/` 目录下。目录结构如下所示：

```text
.claude/
└── projects/
    ├── -Users-alex-Projects-myapp/      # 编码后的项目路径
    │   ├── a1b2c3d4.jsonl               # 会话文件
    │   ├── b2c3d4e5.jsonl
    │   ├── c3d4e5f6.jsonl
    │   ├── e5f6g7h8.jsonl
    │   └── agent-xyz123.jsonl           # 子智能体(subagent)会话
    └── -Users-alex-Projects-blog/
        └── i9j0k1l2.jsonl
```

路径的编码方式很简单：将 / 替换为 -，绝对路径以 - 开头。因此 `/Users/alex/Projects/myapp` 就变成了 `-Users-alex-Projects-myapp`

每个 JSONL 文件中，每一行都是一个 JSON 对象：

```json
/* 用户输入记录 */
{"type": "user", "timestamp": "2026-01-16T10:30:00Z", "gitBranch": "main", "message": {"content": "Fix the EMFILE error"}}

/* 助手回复记录，包含工具调用 */
{"type": "assistant", "timestamp": "2026-01-16T10:30:15Z", "message": {"content": [{"type": "text", "text": "Let me investigate..."}, {"type": "tool_use", "name": "Bash", "input": {"command": "ulimit -n"}}]}}

/* 会话总结记录 */
{"type": "summary", "summary": "Fixed EMFILE error by increasing file descriptor limit"}
```

每个条目包含角色（role）、时间戳、Git 分支、消息内容以及工具的使用情况。当 Claude 生成对话总结时，会出现 summary 类型。

## Skill 文件结构

```text
conversation-search/
├── SKILL.md                 # 定义触发模式和用法
└── scripts/
    └── search_history.py    # 搜索引擎脚本
```

SKILL.md 文件告诉 Claude 何时激活此技能：

```yaml
---
name: conversation-search
description: Search past Claude Code conversation history. Use when asked to recall, find, or search for anything from previous conversations - including content discussed, links shared, problems solved, topics covered, things posted, or work done together. Triggers include "what did we do today", "summary of our work", "what did we work on", "from our conversations", "what did we discuss", "which X was about Y", "recall when we", "find where we talked about", "search history", "what did I share/post/send you about", "how did we fix", or any reference to past sessions or collaborative work.
---
```
比如说当我问“我们昨天做了什么？”时，Claude 会识别出触发条件，并知道要使用这个技能，这解决了何时触发的问题，但还有一个重要的问题：如何优雅的检索历史，也就是 How to do 的问题，这依赖于具体的 python 脚本实现。

## Python 脚本的实现原理

该脚本支持两种模式：用于日常总结的 __摘要模式 (digest)__ 和用于查找特定解决方案的 __搜索模式 (search)__，它没有依赖复杂的向量数据库，而是通过高效的关键词匹配 + 权重评分算法来实现搜索。

### 数据建模
为了处理复杂的 JSON 结构，脚本使用 dataclass 定义了清晰的数据模型：

```python
@dataclass
class Message:
    uuid: str                # 消息唯一标识
    parent_uuid: Optional[str] # 父消息标识
    role: str                # 角色：'user' (用户), 'assistant' (助手)
    content: str             # 消息文本内容
    timestamp: str           # 时间戳
    tool_uses: list          # 工具使用记录列表
    tool_results: list       # 工具执行结果列表

@dataclass
class Conversation:
    session_id: str          # 会话 ID
    file_path: str           # 文件存储路径
    summary: Optional[str]   # 会话摘要（如果有）
    messages: list           # 消息对象列表
    project_path: str        # 项目路径
    git_branch: Optional[str]# Git 分支
    timestamp: str           # 会话时间

@dataclass
class SearchResult:
    conversation: Conversation # 关联的会话对象
    score: float             # 相关性得分
    matched_messages: list   # 匹配到的消息列表
    problem_excerpt: str     # 问题摘录
    solution_excerpt: str    # 解决方案摘录
    commands_run: list       # 执行过的命令列表

```

### 搜索算法：基于权重的相关性评分
为了让搜索结果更精准，脚本不是简单地匹配关键词，而是根据内容的重要性赋予不同的权重：

* Summary (摘要): 3.0 倍权重。如果关键词出现在摘要中，说明这是会话的主题。
* User Message (用户消息): 1.5 倍权重。用户通常在这里描述“问题”或“Bug”。
* Tool Use (工具使用): 1.3 倍权重。如果包含工具调用（如执行命令、修改文件），通常意味着这是“解决方案”的一部分。

```python
def calculate_relevance_score(query: str, conversation: Conversation) -> tuple:
    """计算会话与查询的相关性得分"""
    # 1. 对查询语句进行简单的分词（转小写，提取单词）
    query_tokens = tokenize(query)
    if not query_tokens:
        return 0.0, []

    total_score = 0.0
    matched_messages = []

    # 2. 检查会话摘要 (Summary) - 权重最高 (3.0)
    if conversation.summary:
        summary_tokens = tokenize(conversation.summary)
        # 计算重叠词比例
        summary_overlap = len(query_tokens & summary_tokens) / len(query_tokens)
        total_score += summary_overlap * 3.0

    # 3. 遍历每一条消息
    for msg in conversation.messages:
        msg_tokens = tokenize(msg.content)
        overlap = len(query_tokens & msg_tokens)

        if overlap > 0:
            # 基础分：重叠词比例
            msg_score = overlap / len(query_tokens)

            # 策略：提升用户消息的权重 (1.5x)
            # 原因：用户通常在消息中描述具体的问题或报错信息
            if msg.role == 'user':
                msg_score *= 1.5

            # 策略：提升包含工具使用的消息权重 (1.3x)
            # 原因：包含代码执行或文件修改的消息通常是解决方案所在
            if msg.tool_uses:
                msg_score *= 1.3

            total_score += msg_score
            matched_messages.append(msg)

    return total_score, matched_messages
```

### 信息提取：复现记忆的关键

搜索不仅要找到会话，还要提取出具体的解决方案。脚本通过分析 tool_uses 字段，精准提取出运行过的 Bash 命令和修改过的文件。

```python
def extract_bash_commands(conversation: Conversation) -> list:
    """提取会话期间运行的所有 Bash 命令"""
    commands = []
    for msg in conversation.messages:
        for tool in msg.tool_uses:
            # 过滤出 'Bash' 类型的工具调用
            if tool.get('name') == 'Bash':
                cmd = tool.get('input', {}).get('command', '')
                if cmd:
                    commands.append(cmd)
    return commands

def extract_files_touched(conversation: Conversation) -> list:
    """提取被读取、写入或编辑的文件列表"""
    files = set()
    for msg in conversation.messages:
        for tool in msg.tool_uses:
            name = tool.get('name', '')
            inp = tool.get('input', {})

            # 关注文件操作类的工具
            if name in ('Read', 'Write', 'Edit'):
                path = inp.get('file_path', '')
                if path:
                    # 仅保留文件名，保持输出简洁
                    files.add(Path(path).name)
    return sorted(files)[:10]
```

### 每日摘要模式的实现

脚本还支持 --digest 参数，用于生成日报。它会按日期过滤会话，并生成 Markdown 格式的报告。这对于每日站会（Standup）非常有用。

```python
def format_digest(conversations: list, target_date: datetime, project_filter: Optional[str]) -> str:
    """格式化每日摘要报告"""
    date_str = target_date.strftime('%B %d, %Y')
    
    # ... (省略头部构建)

    lines = []
    for i, conv in enumerate(conversations, 1):
        # 自动提取问题描述作为标题
        problem = extract_problem_excerpt(conv)
        commands = extract_bash_commands(conv)
        files = extract_files_touched(conv)

        # 截取前60个字符作为标题
        title = problem[:60].replace('\n', ' ')
        
        # 构建 Markdown 输出
        lines.append(f"### {i}. {title}")
        lines.append(f"   Session: `{conv.session_id[:8]}`")
        if conv.git_branch:
            lines.append(f"   Branch: `{conv.git_branch}`")
        
        # 列出涉及的关键文件和命令数量
        if files:
            lines.append(f"   Files: {', '.join(files[:5])}")
        if commands:
            lines.append(f"   Commands: {len(commands)} executed")
        
        lines.append("")

    return '\n'.join(lines)
```

## 使用指南

配置好 SKILL.md 后，你可以直接用自然语言与 Claude 交互，或者在终端直接运行脚本。

### 场景一：找回丢失的解决方案

用户: “Recall how we fixed the EMFILE error last week.” (回忆一下上周我们是怎么修复 EMFILE 错误的。)

Claude (调用脚本):
```shell
python3 search_history.py "EMFILE error" --days 7
```

输出结果:
```text
============================================================
Result #1 (Score: 4.25)
============================================================
Project: /Users/alex/Projects/fitness-app
Session: a1b2c3d4...
Branch: main
Date: 2026-01-10

PROBLEM:
Getting EMFILE error when running tests, too many open files

SOLUTION:
The issue was too many file watchers. Fixed by increasing the limit...

COMMANDS RUN (3 total):
  $ ulimit -n
  $ ulimit -n 10240
  $ echo "ulimit -n 10240" >> ~/.zshrc
```

此外，该脚本支持按照日期范围和特定项目进行过滤：
```shell
# 仅今天的会话
python3 search_history.py --today "newsletter"

# 昨天
python3 search_history.py --yesterday "bug fix"

# 过去 7 天
python3 search_history.py --days 7 "refactor"

# 自特定日期以来
python3 search_history.py --since 2026-01-01 "feature"

# 仅搜索指定项目
python3 search_history.py "vitest config" --project ~/Projects/fitness-app
```

### 场景二：回忆工作内容

用户: “What did I work on yesterday?” (我昨天做了什么？)

Claude (调用脚本):
```shell
python3 search_history.py --digest yesterday
```

输出内容：
```text
## January 16, 2026 - 32 sessions

### 1. Set Context Menu Feature Spec
   Session: `1498ff91`
   Branch: `fitnessFunctions`
   Files: set-context-menu.md, SetContextMenu.vue, SetContextMenuPO.ts
   Commands: 12 executed

### 2. Fix Pipeline: Missing i18n, Unused Exports
   Session: `23351e77`
   Branch: `fitnessFunctions`
   Files: de.json, en.json, claude-qa.yml
   Commands: 6 executed

### 3. Adding AI Coding Articles to Second Brain
   Session: `5c909423`
   Branch: `main`
   Files: article.md, dex-horthy.md, diagrams-guide.md
   Commands: 1 executed
```

## 总结

在这个技能出现之前，我们可能会浪费很多时间去重新解决之前已经解决过的问题。“我知道我们讨论过这个问题，但我找不到记录了。” 现在，我们只需要问 Claude 即可。
这样做的好处包括：
* 不再重复解决问题 - Claude 可以立即找到过去的解决方案。
* 每日摘要助力站会 - “我们昨天做了什么？” 可以提供现成的总结。
* 保留操作命令 - 你可以使用相同的命令复现确切的解决方案。
* 跨项目搜索 - 从你参与过的任何项目中查找解决方案。

这个 Skill 将 Claude 从一个无状态的助手转变为更接近于一个拥有持久记忆的编程伙伴，让它记得你们一起做过的事情。

## 参考

* Skill 地址：https://github.com/alexanderop/dotfiles/blob/main/claude/skills/conversation-search/SKILL.md
