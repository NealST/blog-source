---
title: Apple HIG Skills 让 AI Agent 真正懂 Apple 设计规范
date: 2026-09-23 14:00:00
tags:
  - Apple
  - Human Interface Guidelines
  - Agent Skills
  - AI 辅助开发
  - 设计系统
categories:
  - 研发洞察
---

> TL:DR: 我最近在开发苹果 app 的时候，就顺手蒸馏了整套苹果官方的 Human Interface Guidelines，即 **Apple HIG Agent Skills**。它将 Apple 官方 HIG 全面解构成高密度、结构化、具备精准路由机制的 Agent Skills，这样 agent 写出来的代码就自动符合 apple 设计规范和最佳实践。

在 AI 辅助编程（如 Claude Code、Cursor、Codex 等）席卷客户端开发的当下，只要给出一个清晰的需求，Agent 几秒钟就能生成一整套 SwiftUI 视图代码。

然而，一旦进入真实交付场景，很多开发者都会发现：**AI 懂代码语法，但缺乏 Apple 的“平台直觉”与设计底线。**

Apple 官方的人机界面指南（Human Interface Guidelines, HIG）固然权威且全面，但它本质上面向人类设计师与开发者撰写，篇幅浩瀚且层级分散。如果直接把几十个网页文档扔进提示词或依赖全网检索，往往会导致灾难性的 Token 膨胀与上下文漂移（Context Drift）。

为了解决这个问题，**Apple HIG Agent Skills** 将庞大的官方 HIG 重构成专为 AI Agent 定制的结构化知识库。

---

## 核心价值：为什么 Agent 需要专属的 HIG 知识库？

### 1. 告别上下文膨胀与检索污染
让大语言模型处理海量平台规范时，最常见的两个极端是：
- **全文常驻上下文**：把成千上万行设计规范全写进规则文件（如 `AGENTS.md`），不仅迅速挤占宝贵的工作窗口，还会导致模型注意力涣散，关键业务逻辑频繁遗忘；
- **盲目全网搜索**：让 Agent 联网搜索或依靠粗粒度向量检索，经常会抓取到陈旧过时的非官方博客，把 iOS 14 的旧方案套进 iOS 18+ 的现代工程里。

Apple HIG Agent Skills 采用 **Agent Skills 标准架构**，将庞大的 HIG 拆分为 9 个原子化领域模块。每个模块均包含严格定义的语义触发边界与反向排除规则（`Do not use for`）。Agent 仅在遇到特定设计决策时才精准激活对应模块，实现“用时即调、查完即走”，保持主上下文的纯净与高效。

### 2. 直击 App Review 拒审红线
AI 生成的代码能编译通过，并不代表能通过 App Store 审核。很多客户端团队在接入 AI 编程后，最大的痛点变成了“送审被打回”。

诸如：
- 应用刚启动就无脑触发隐私权限弹窗，直接撞上 App Tracking Transparency (ATT) 的审核红线；
- 界面手势滥用，阻断了系统核心的屏幕边缘返回与控制中心手势；
- 违规缩放或擅自修改 Apple Pay、Sign in with Apple 的官方标志；
- 在播放音频或视频时，完全忽略系统音频会话中断（Audio Interruption）的恢复链路。

本项目在梳理每一项规范时，专门提炼了**避免（反模式）**清单，将这些极易引发体验翻车与审核被拒的常见误区直接前置，相当于在 Agent 生成代码的第一时间就内嵌了一套合规审查雷达。

### 3. 保留硬核设计规格与官方 API 语境
普通的人工摘要或大模型通用知识，往往会把关键数值模糊为“注意尺寸适中”或“保持可读性”。而在本知识库中，所有具有确定性标准的硬指标被全量保留：
- **触控与人体工学**：点击热区底线（iOS/iPadOS 最小 $44 \times 44\text{ pt}$、visionOS 空间凝视与直接手势最小 $60 \times 60\text{ pt}$）；
- **平台特性差异**：明确标注不同系统边界（如 visionOS/watchOS 无独立深色模式切换、tvOS 十英尺 UI 焦点寻径机制）；
- **材质与排版**：Dynamic Type 全平台字阶与行高映射表、Liquid Glass 材质层级与 35% 变暗层规范、Display P3 广色域与系统语义色阶；
- **新型硬件适配**：iPhone 16 Camera Control 覆盖层交互规范、Apple Pencil Pro 滚转与轻捏响应逻辑。

更关键的是，所有组件与交互模式均紧密对齐 SwiftUI、UIKit、AppKit 的原生 API 术语，使 Agent 在提供设计决策的同时，能直接落地为最地道的系统原生代码。

---

## 知识库全景解构：覆盖 6 大平台的 9 大领域

整个项目结构严密，涵盖 9 大领域模块、64 个原生 UI 组件、29 项核心技术集成、27 项设计基础、25 类用户交互流程与 13 种输入交互形态，横跨 iOS、iPadOS、macOS、visionOS、watchOS 和 tvOS（并涵盖 CarPlay 与 iPhone Duo 等扩展形态）：

```
apple-hig-skills/
├── apple-hig-foundations/                  # 设计基础与各平台专属指南
├── apple-hig-patterns/                     # 用户交互流程与交互模式
├── apple-hig-inputs/                       # 硬件与输入交互机制
├── apple-hig-components-content-layout/    # 内容与布局组件
├── apple-hig-components-menus-actions/     # 菜单、操作与导航组件
├── apple-hig-components-presentation-input/# 展示与输入控件
├── apple-hig-components-status-system/     # 状态指示与系统体验组件
├── apple-hig-technologies-domain/          # 商业、支付、健康与媒体技术
└── apple-hig-technologies-system/          # 系统服务、AI 与深度集成技术
```

### 1. 设计基础与全平台指南 (Foundations & Platform Guides)
不仅涵盖 Apple 的九大通用设计原则（Purpose、Agency、Delight 等），更针对 8 种形态提供了针对性的平台指引：
- **visionOS**：Shared Space 与 Full Space 的切换原则、前庭眩晕防护（$0.2\text{ Hz}$ 运动敏感频段）；
- **tvOS**：专注“十英尺体验”，焦点寻径引擎与视差分层规范；
- **macOS**：多窗口层级、窗口尺寸恢复与菜单栏规范；
- **无障碍与包容性**：5 类无障碍需求、动态类型适配、减弱动态效果与高对比度支持；
- **最新材质体系**：Liquid Glass 玻璃质感层级与 Vibrancy 视觉层次。

### 2. 用户交互流程与模式 (Patterns)
聚焦真实产品中最复杂的闭环交互链路：
- **启动与引导**：极速冷启动、推迟登录机制、TipKit 智能调度与字符数边界；
- **数据与任务闭环**：行内即时校验、无限撤销（Undo Stack）语义、iOS 18+ 文档启动器；
- **系统级反馈**：AVAudioSession 类别与中断响应、语义触觉模式、4 级通知中断级别（Passive 到 Critical）。

### 3. 全模态交互与输入方式 (Inputs)
超越单纯的触控屏幕，全面覆盖 Apple 生态的 13 种软硬件输入：
- **新硬件交互**：iPhone 16 Camera Control 覆盖层与参数滑块、Action Button 的 3 词动词规范；
- **手写与触感**：Apple Pencil Pro 滚转与轻捏响应、触觉反馈匹配；
- **空间与体感**：visionOS 视线注视与微手势（$16\text{ pt}$ 间距 / $60\text{ pt}$ 中心距）、watchOS 双指互点；
- **传统与外设**：全键盘访问（FKA）快捷键标准、iPadOS 指针磁吸效果、MFi 游戏手柄映射。

### 4. 64 个原生 UI 组件深度拆解 (Components)
将系统组件划分为 4 大类，杜绝跨平台滥用：
- **内容与布局**：图表、集合视图、macOS 专用分栏与大纲视图、tvOS Lockups；
- **菜单与操作**：标准按钮层级与热区标准、visionOS Ornaments 装饰栏、上下文菜单与 Dock 菜单；
- **展示与输入**：Alerts 提醒框、Sheets 表单面板（Detents 与抓手交互）、Pickers 选择器与颜色井；
- **状态指示与系统级体验**：灵动岛三种展示形态（极简态、紧凑态、展开态）、实时活动（Live Activities）、Apple Watch 复杂功能与表盘。

### 5. 商业闭环与前沿系统技术集成 (Technologies)
打通系统底层能力与商业变现管道：
- **商业与生态**：Apple Pay 按钮标准规格、StoreKit 2 应用内购买与订阅退订流程、CarPlay 模版体系、SharePlay 空间 Persona 模版；
- **Apple Intelligence 与系统服务**：负责任生成式 AI 交互（幻觉应对、置信度归因呈现）、App Intents 语义与 Siri 对话规范、VoiceOver 转盘集成、iCloud 静默无冲突数据同步。

---

## 统一的排查结构：让规范即查即用

项目中的每一篇参考文档，均摒弃了冗长的叙述性说明，全部按照统一且高效的“五步链路”组织：

$$\text{一句话定位} \longrightarrow \text{最佳实践} \longrightarrow \text{常见误区/避免（拒审红线）} \longrightarrow \text{平台差异} \longrightarrow \text{关键数值与 API 术语}$$

这种高信息密度的组织形式，使得无论是作为 AI Agent 的外部检索源，还是作为工程师与设计师在代码提交、设计走查时的参考清单，都能在数秒内获得确定性的答案。

---

## 开源项目地址

Apple HIG Agent Skills 基于 MIT 协议开源，欢迎体验与共同完善：

- **GitHub 仓库**：[NealST/apple-hig-skills](https://github.com/NealST/apple-hig-skills)
