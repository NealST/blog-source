---
title: 解读 Loop Engineering
date: 2026-06-10 12:00:00
tags:
  - AI
  - Claude-Code
  - Agent
categories:
  - AI
---

人类在使用 Agent 时，主要在做两件事：告诉它要干啥，以及在它给出结果后判断结果是否符合预期。

Loop Engineering 的思路是把这两件事从人身上移走，交给 Agent 自己来完成。一个 Maker Agent 决定干什么，一个 Check Agent 评估产出质量，二者通过磁盘上的状态文件来做串联。

这个概念来源于 Claude Code 核心开发者 Boris Cherny，据传他已经不再手动提示 Claude，而是编写"循环"来替他完成提示工作。

<!-- 配图：Manual Run vs Self-running Loop
左侧 Manual Run 三步循环：① 你决定执行什么 → ② Agent 执行并返回结果 → ③ 你检查产出，每一轮都需要你在场
右侧 Self-running Loop 四步循环：① 调度决定执行什么 → ② Maker Agent 产出结果 → ③ Checker Agent 评估质量 → ④ 状态写入磁盘文件，下一轮从磁盘读取状态继续
核心对比：人的工作从"每轮都参与"变成"设计一次，持续运行"
-->
![Manual Run vs Self-running Loop](TODO:上传图片后替换为CDN链接)

## 一个 Loop 由六个部分组成

整体包括五个组件加一层记忆，Claude Code 和 Codex 目前均已内置。

**自动化调度（Automations）**：按计划触发，自主完成发现和分类工作。

**工作树（Worktrees）**：每个 Agent 在自己的目录副本里工作，并行运行时不会相互覆盖。常见的坑是 Agent 跑完后没有删除工作树，日积月累磁盘上会留下一堆“死文件”。

**技能（Skills）**：存放项目知识，包括代码规范、构建命令、Review 标准等。Agent 按名称调用技能即可，省去每次从零推导或搬运大段指令的开销。

**连接器（Connectors）**：通过 MCP 协议将 Agent 接入外部工具，如 Issue 跟踪系统、数据库、Slack。

**子 Agent（Sub-agents）**：拆分职责，一个 Agent 负责执行变更，另一个负责审查变更。

**记忆（Memory）**：一个独立于对话之外的知识图谱（比如 supermemory 之类），记录已完成和 todo 事项。

这六个部分是搭建 Loop 的基座，但核心的设计还是 Maker 与 Checker 分离。

## 单次迭代内部怎么跑

六个部分描述的是 Loop 的外部骨架，而每一轮迭代内部也有自己的运转逻辑。

<!-- 配图：The internals of Loop Engineering
上层 Trigger/Input：Message、Event、API Call、Schedule 四种触发方式
中层 Cognitive Core（Agent Loop）：Think(推理、规划、反思) → Act(选择工具、构造调用) → Observe(解析结果、更新状态、检测错误)，循环直到完成/达到最大轮次/预算耗尽
左下 Memory：Working Memory(当前轮上下文) + Long-Term Memory(向量存储、知识库、历史片段，通过语义检索召回)
中下 Safety Layers：每个动作执行前经过四道策略门控 Validate(校验意图) → Scope(权限边界) → Budget(成本限额) → Allow(放行执行)，不通过则 Reject + Replan
右下 Tool Execution：工具类型(搜索、代码执行、API、文件、浏览器) → Dispatch 分发 → 结果返回 Observe
-->
![The internals of Loop Engineering](TODO:上传图片后替换为CDN链接)

每轮迭代由一个触发信号启动，可以是定时任务、外部事件、API 调用或人工消息。进入执行后，Agent 内部仍然是 Think → Act → Observe 三步循环：先推理和规划，再选择工具并发起调用，最后解析执行结果并更新状态。如果任务未完成且预算没有耗尽，就回到 Think 继续下一轮。

每个动作在执行前都会经过一层安全验证：先校验调用意图是否合法，是否有相应权限，再判断成本是否超出限额，全部通过才可执行。

memory 分两层运作：工作记忆是当前轮次的上下文窗口，用完即丢；长期记忆是外挂的向量存储或知识库，通过语义检索召回历史决策和经验，让 Agent 不必每次都从零开始推理。

## 核心设计：Maker 与 Checker 分离

<!-- 配图：Maker-Checker 分离流程
① Maker（蓝色）：执行变更、产出结果 —hands off the output→ ② Checker（绿色）：独立 Agent，最好用不同模型，依据独立信号（tests、lint、static analysis）评分
→ 评估通过 → comes back clean, loop ends
→ 评估不通过 → findings become the next instruction，虚线箭头回到 Maker 开启下一轮
-->
![Maker-Checker Split](TODO:上传图片后替换为CDN链接)

让同一个模型给自己打分，结果会偏宽松，它倾向于放过自己的 Bug。

Maker-Checker 分离的做法是：执行变更的 Agent（Maker）和评估变更的 Agent（Checker）必须是两个独立的实例，最好使用不同的模型，且 Checker 的评判依据应该是独立信号（测试结果、Lint 输出、类型检查），而非 Maker 的自述。

Checker 的评估结论会作为下一轮指令回传给 Maker，循环往复，直到评估结果全部通过。

## 在启动之前定义退出条件

Loop 没有终止条件时会无限循环、持续消耗 Token。运行时间越长、调用的子 Agent 越多，成本攀升越快。

实操中可以这样定义退出条件：只修复严重问题，最终执行一轮验证 pass，两轮循环后强制停止，以"全部测试通过且 Lint 干净"作为明确的退出标志。

关键原则：**退出条件在 Loop 运行之前确定，而非运行过程中临时追加。**

## 状态放在磁盘里

<!-- 配图：跨运行的状态持久化
顶部时间轴：separate runs, hours or days apart
Run 1 / Run 2 / Run 3 三次独立运行，相邻运行之间标注 "agent forgets between runs"
底部 State 层：a markdown file or a knowledge graph, holds what's done and what's still open, persists, does not reset
每次运行：reads it first（向上箭头从 State 到 Run）→ writes back last（向下箭头从 Run 到 State）
-->
![State persists across runs](TODO:上传图片后替换为CDN链接)

模型在两次运行之间会遗忘所有信息，所以状态必须持久化到 session 之外。

如果想要简单一点，一份 Markdown 文件或知识图谱就足以承载"已完成"和"待处理"的清单。每次运行开始时先读取这份状态，结束时再写回更新。

Agent 会遗忘，但这份文件不会。

## Loop 适合干啥

Loop 天然适合那些"答案明确、验证成本低"的工作。比如检查版本号是否过期、新代码有没有配套测试、依赖有没有已知漏洞。这类任务的共同特征是 Checker 能拿到一个二元信号（通过/不通过），不需要理解上下文就能判定结果。

反过来，如果工作质量标准模糊、需要结合业务背景才能判断好坏，Loop 就容易出问题。因为 Checker 没有可靠的评判锚点，要么误判通过，要么反复打回陷入死循环。

在 Loop 工作过程中要确保 Checker 是独立实例且依赖客观信号（测试、Lint），而非 Maker 的自述
，以及每轮产出都有人来质检，不是只看 CI 状态，否则几轮下来代码就失控了。

## 写在最后

Loop Engineering 并不是什么很复杂的工程概念，核心思想其实也没有脱离思考、行动、反馈的 Agent Loop 范畴。变化在于人的角色，你不再编写提示词，而是设计三件事：由谁来提示，用什么信号验证，在什么条件下停止。

角色变了，但责任不会消失。

设计 Loop 的人必须持续理解 Loop 的产出并有衡量产出质量的能力，否则这套自动化流程最终会变成一个黑盒，批量输出越来越平庸的结果。