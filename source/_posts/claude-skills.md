---
title: 简单聊聊 Claude 新推出的 Agent Skills
date: 2025-10-25 11:00:00
tags: "AI"
---

![](https://img.alicdn.com/imgextra/i3/O1CN01ltegmA1EjINQq9y3k_!!6000000000387-2-tps-1024-1024.png)

## 前言

Claude 系列模型的母公司 Anthropic 近期新推出了一种为大模型赋予专业领域知识和任务执行能力的实现模式，即 agent skills，其核心思想是让大模型层次递进地读取结构化组织好的文档，脚本等资源以获取上下文。在笔者看来，这种 skills 的方案因其更好的简洁性和扩展性，相比 MCP 会更有潜力成为未来的通用方案。

## Agent Skills 是什么

简单来说，agent skills 是一个文件夹目录，该目录的入口为 SKILL.md 文件，SKILL.md 中需要有一个描述其元信息的 YAML 格式头，其中必须包括 name 和 description 两个字段，来描述其名称和内容与功能的简介。以一个告知大模型如何提取 pdf 内容的 skills 为例，其 skill.md 如下所示：

```markdown
---
name: pdf
description: Comprehensize PDF toolkit for extracting text and tables, merging/splitting documents, and filling-out forms
---

## Overview
This guide covers essential PDF processing operations using Python libraries and command-line tools
```

初始化时，agent 会提取 YAML 格式描述的元信息，将其内置到系统提示词中，当大模型收到任务指令且根据元信息判断该 skill 与当前任务有关时，agent 会进一步加载 skill.md 文件中的 markdown 内容主体部分并将其添加到上下文中。

所以，Skills 的本质其实极其简单，它就是一个告诉大模型一些专业背景知识和 markdown 文档。

## Skills 的工作机制

Skill.md 文件中的内容分为三级，各级对应的上下文加载策略以及 token 消耗如下所示：
| 等级 | 内容类型 | 模型上下文 | Tokens |
  |----------|----------|----------|----------|
  | L1 | 元数据（YAML metadata），包含名称和描述| 初始化时加载 | ~100 |
  | L2 | 内容主体（markdown body），包含专业知识等 | 请求 skill 时加载 | <5k |
  | L3 | 外链文件（markdown 引用） | 模型处理内容主体时按需加载 | 无限制 |

初始化时，L1 的内容会被内置为系统提示词，当模型判断需要使用该 skills 时，L2 的内容会被加载到上下文中。除了这两种类型外，还有 L3 的外链文件。随着知识积累和迭代，skill.md 文档内容会逐渐膨胀，除了正常的文本内容，我们可能还会在文档中嵌入一些脚本内容以支持大模型执行实际任务。为了让 skill.md 文件整洁清晰易维护，我们需要将一些比较独立的内容拆成单独的文件，并通过外链的形式嵌入到 skill.md 中。还是以上述 pdf 的 skills 为例，假设我们把表单填写的专业知识和具体的执行脚本拆开为独立的文件，如下所示：

```plain
pdf/
├── SKILL.md (main instructions)
├── FORMS.md (form-filling guide)
├── REFERENCE.md (detailed API reference)
└── scripts/
    └── fill_form.py (utility script)
```
在 Skill.md 文件中引用 forms.md 文件的示例如下：

![](https://img.alicdn.com/imgextra/i1/O1CN01uKq0qs1cG1qXXZI1A_!!6000000003572-2-tps-1914-1238.png)

当大模型处理 L2 内容主体时，模型会根据内容相关性的判断按需加载 L3 的外链文件。从 L1 到 L2 再到 L3，这种渐进式展开的加载策略就是 skills 的核心设计理念，下图可以帮助你更加具象化的理解这种设计，看看 skills 如何随着用户提问动态加载到模型上下文中：

![](https://img.alicdn.com/imgextra/i1/O1CN01npAehs1urjXJ9YhRe_!!6000000006091-2-tps-1894-1050.png)

## 如何编写 Skills

Anthropic 官方也给出了一些编写 Skills 的实践建议，包括：

* 始于评测：先定义清楚 agents 当前的能力缺陷，然后根据缺陷补充对应 skills。
* 模块化设计：尽量将文档进行模块化拆分，即较为独立的内容拆成单独的文件，通过外链的方式进行引用，以保持 skills.md 文件的简洁些并减少 token 消耗。
* 关注元信息：尽可能完整和严谨的编写 name 和 description，模块会根据元信息来判断是否要加载 skills。
* 在使用模型的过程中逐步打磨：skills 的编写不太可能一蹴而就，而是需要在与模型的交互中逐步观察任务的完成质量，让模型自己反馈还需要哪些上下文信息，然后逐步打磨完善。

## Skills 与 MCP 的比较

MCP 自从去年十一月份首次发布以来吸引力大量关注，目前业界已经有大量的 MCP server 存在，质量也是参差不齐。MCP 的缺陷在实际使用过程中也逐渐突显，最大的问题在于其对上下文 token 的占用和消耗，在添加一定数量的 MCP 工具后，留给上下文的剩余空间就会捉襟见肘，很多实际没有用到的工具其 MCP 描述都会在初始化时被加载到上下文中。

而 Skills 的渐进加载策略则更具优势，初始化时仅加载最少量的 L1 元数据，可以做到 token 消耗最小化。同时，具体的工具执行脚本和命令调用可以通过外链脚本的方式插入到 skills 的 markdown 文档中，让大模型按需加载和执行。

## Skills 的局限性与关键优势

先说局限性，Skills 的设计需要依赖于文件系统的能力支持（读写文件）和本地虚拟机（执行脚本），比较适用于像 Cursor, Claude Code, Codex CLI 和 Gemini Cli 等产品形态的 agent。

再说其优势，笔者认为 Skills 最大的优势就在于其设计足够简单，它没有 MCP 那么复杂的协议设计，需要关注 hosts, clients, servers, resources, prompts, tools, sampling, roots 等。Skills 所需的只有一份 markdown 文件，简单直接又高效。此外，这种简洁性也使其可以快速应用到其他 agent 里，比如说你可以在 Gemini Cli 中输入指令 "读取 pdf/SKILL.md 文件并按照其指导帮我给当前项目创建一份 pdf 格式的描述"，即使 Gemini Cli 当前还不像 Claude 那样支持 skills, 它也可以正常执行这项任务。

不过需要注意的是针对 skills 中的外链脚本需要做好安全防护策略，尽量用沙盒环境来执行，避免出现 prompt 注入攻击，在使用 skills 时需要尽量选择可信的数据源。

## 总结

在 MCP 之外，Skills 提供了另一种给大模型提供专业知识和任务执行能力的模式。这种基于 markdown 文本的设计足够简单高效且节省了上下文 token 的消耗，目前已经在 Claude Code, Claude.ai, Claude Agent SDK 中得到了支持。在笔者看来，skills 会有望超越 MCP，成为新的工具实现标准。
