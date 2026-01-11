---
title: Claude Code 定制化指南：详解 CLAUDE.md、Skills 与 Subagents
date: 2026-01-11 19:20:00
tags: "AI"
---

在使用 Claude Code 进行开发时，我们常常面临一个两难困境：AI 模型拥有广博的通用知识，但往往缺乏项目特定的上下文，或者对某些库的最新版本（如 Dexie.js 的最新 API）缺乏了解。

虽然 Claude Code 允许我们通过提示词（Prompt）来补充信息，但如何优雅地管理这些上下文？是该把规则写在文件里，还是做成一个工具？

本文通过解决同一个问题——**“如何让 Claude Code 准确掌握第三方库（Dexie.js）的最新文档与开发规范”**——来深度解析 Claude Code 四种核心定制机制：**CLAUDE.md**、**Slash Commands**、**Subagents** 和 **Skills**。

## 核心痛点：上下文污染与知识过时

假设我们正在开发一个使用 Dexie.js（IndexedDB 封装库）的应用。由于训练数据的滞后，Claude 可能会建议过时的 API，或者忽略了 `liveQuery()` 这样现代的响应式用法。

我们需要“教会”Claude Code 获取最新文档。Claude Code 提供了四种截然不同的方式来实现这一点，每种方式都有其特定的适用场景和权衡。

---

## 1. CLAUDE.md：常驻的项目记忆

### 机制解析
`CLAUDE.md` 是 Claude Code 的“项目宪法”。每当你启动 Claude Code 或开始新对话时，这个 Markdown 文件的内容会被**自动加载**到上下文的最前端。

*   **存放位置**：项目根目录或 `.claude/CLAUDE.md`。
*   **嵌套特性**：Claude Code 支持目录级上下文。例如，`tests/CLAUDE.md` 只有在 Claude 访问测试目录时才会被读取，这有助于保持主上下文的精简。

### 实战应用
在 `CLAUDE.md` 中，我们可以这样写：

```markdown
## Database Guidelines
我们使用 Dexie.js。在编写任何数据库代码前：
1. 必须先从 https://dexie.org/llms.txt 获取最新文档索引。
2. 使用 `liveQuery()` 进行响应式数据绑定。
3. 遵循 `src/db/` 中的 Repository 模式。
```

### 优劣分析
*   **优点**：零操作成本，自动生效；通过 Git 共享，团队规范统一。
*   **缺点**：**上下文漂移（Context Drift）**。随着对话变长，模型可能会逐渐“遗忘”初始的指令，优先关注最近的对话历史。它没有独立的上下文窗口，会占用宝贵的 Token 空间。

---

## 2. Slash Commands：可手动触发的快捷指令

### 机制解析
Slash Commands 是你通过 `/command` 在终端显式调用的指令。它不仅是 Prompt 的快捷键，更是**工作流的编排者**。

你可以在命令定义中明确要求 Claude 调用特定的工具、执行一系列步骤，甚至并发启动多个 Subagents（子智能体）来处理任务。

### 实战应用
创建一个 `.claude/commands/dexie-help.md`：

```markdown
---
description: 获取 Dexie.js 指导并查询最新文档
allowed-tools: Read, WebFetch
---

首先，从 https://dexie.org/llms.txt 获取文档索引。
然后，根据用户的问题抓取相关页面。
最后，基于最新文档回答用户问题：$ARGUMENTS
```

使用时，只需在终端输入：
```bash
/dexie-help 如何创建复合索引？
```

### 优劣分析
*   **优点**：**控制权在用户手中**，明确何时触发；支持参数传递；非常适合“阅后即焚”的一次性查询任务。
*   **缺点**：必须记住命令名称；它通常是一次性的交互，不会持久化改变 Claude 的长期记忆。

---

## 3. Subagents：拥有独立上下文的专家

### 机制解析
这是 Claude Code 最强大的特性之一。**Subagent（子智能体）** 是一个独立的 Claude 实例，拥有**完全独立的上下文窗口**。

当主对话中的任务过于复杂（例如需要阅读大量文档、扫描整个代码库）时，主 Agent 可以委派一个 Subagent 去执行。Subagent 完成工作后，只将**最终结果（摘要）**返回给主对话。

> **关键洞察**：Subagents 是保持主上下文（Main Context）清洁的秘诀。在 Plan Mode 中，Claude Code 默认就会启动一个 Explore 类型的 Subagent 来扫描代码库，从而避免将成吨的文件内容直接倾倒进你的主会话中。

### 实战应用
定义一个 `.claude/agents/dexie-specialist.md`。在这个定义中，你可以强制要求该 Agent 在回答任何问题前，必须先联网读取最新文档。

当你在主对话中问：“帮我设计一个包含外键的 Dexie Schema”时：
1. 主 Claude 识别任务，委派给 `dexie-specialist`。
2. **Subagent** 启动，在一个全新的上下文中联网下载文档、阅读、思考。
3. **Subagent** 将精炼后的 Schema 代码和解释返回给主 Claude。
4. 主 Claude 将结果展示给你。

### 优劣分析
*   **优点**：**彻底隔离上下文噪音**；适合重型任务（阅读、研究、全库扫描）；可以为特定任务配置不同的模型（如 Opus）。
*   **缺点**：启动较重；用户无法直接与 Subagent 对话（中间隔了一层）。

---

## 4. Skills：自动发现的能力包

### 机制解析
Skills 是结构化的能力封装。与 Slash Commands 不同，Skills 通常是**自动发现**的。Claude 会根据 `description` 判断当前任务是否需要调用某个 Skill。

Skills 通常以目录形式存在（如 `.claude/skills/dexie-expert/`），可以包含 `SKILL.md` 定义文件、辅助脚本、模板文件等。

### 实战应用
Claude 会在后台通过 `<available_skills>` 标签感知到这些能力。当你问“帮我优化一下数据库查询”时，Claude 可能会自动决定：“这需要使用 `dexie-expert` Skill”，并按照 Skill 中定义的最佳实践来执行，甚至运行 Skill 目录下的验证脚本。

### 优劣分析
*   **优点**：**智能触发**，无需用户记忆命令；可以封装复杂的、包含代码脚本的逻辑；体验上更像是增强了 Claude 本身的能力。
*   **缺点**：与主对话共享上下文；触发与否取决于模型的判断（有时可能不触发）。

---

## 总结：该如何选择？

在定制 Claude Code 时，请参考以下决策矩阵：

| 场景需求 | 推荐方案 | 核心理由 |
| :--- | :--- | :--- |
| **项目铁律、代码规范** | **CLAUDE.md** | 启动即加载，确保基准对齐。 |
| **手动触发的工作流** | **Slash Commands** | 明确的 `/` 入口，支持参数，适合定向任务。 |
| **重型研究、文档阅读** | **Subagents** | **关键推荐**。拥有独立上下文，防止主对话被撑爆。 |
| **复杂的自动化能力** | **Skills** | 模型自动决策调用，可包含脚本与辅助文件。 |

**最佳实践建议**：
对于需要大量阅读外部文档或扫描代码库的任务，优先考虑 **Subagents**，这是让你的 Claude Code 在长时间开发会话中保持“清醒”和高效的关键。
