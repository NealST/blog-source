---
title: 聊聊 Claude 新推出的 Agent Skills
date: 2025-10-21 21:10:00
tags: "AI"
---

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

初始化时，agent 会提取 YAML 格式描述的元信息，将其内置到系统提示词中，当大模型收到任务指令且根据元信息判断该 skill 与当前任务有关时，agent 会进一步加载 skill.md 文件中的内容描述部分并将其添加到上下文中。

## Skills 的工作机制

Skill.md 文件中的内容分为三级，其内容分级和上下文加载策略以及 token 消耗如下所示：
| 等级 | 内容类型 | 模型上下文 | Tokens |
  |----------|----------|----------|----------|
  | L1 | 元数据（YAML metadata）| 初始化时加载 | ~100 |
  | L2 | 内容主体（markdown body） | 请求 skill 时加载 | <5k |
  | L3 | 外链文件（markdown 引用） | 模型处理内容主体时按需加载 | 无限制 |

## 一个简单的示例

## 与 MCP 的比较

## Skills 的局限性与关键优势

## 总结


