# 渣打银行 Lead Software Engineer 面试准备

## 一、JD 与简历匹配度分析

### 强匹配项（核心优势）

| JD 要求 | 你的经验 | 匹配度 |
|---------|---------|--------|
| 5-8 years Software Development | 10 年前端经验（2016 至今），超出要求 | ★★★★★ |
| React Preferred | React 生态深度用户（Redux, Zustand, shadcn/ui），淘宝详情页 React Streaming SSR 落地 | ★★★★★ |
| Performance Optimization | P95 FSP 3.95s→1.2s，低端机 5.68s→1.4s，SDK 146KB→36.7KB | ★★★★★ |
| Mentor junior developers | 带领 60+ 人前端团队做工程规范化，具备 Tech Lead 经验 | ★★★★★ |
| Build tools (Vite, Webpack) | Webpack 进度条插件开发经验，前端基建背景 | ★★★★★ |
| RESTful APIs & async programming | 流式数据帧协议设计，Node.js 生态（Koa/Express/Nest.js） | ★★★★★ |
| Agile environment | 阿里大厂敏捷研发流程经验 | ★★★★ |
| Code reviews & coding standards | 主导 60+ 人团队代码规范建设 | ★★★★★ |
| AI coding assistant (preferred) | AI Agent 应用设计经验，LLM/RAG/Tool-calling 实战 | ★★★★★ |
| Micro-frontend (preferred) | 淘宝详情页多技术栈统一（隐含微前端思维） | ★★★★ |

### 需补强的领域

| JD 要求 | 当前状态 | 准备建议 |
|---------|---------|---------|
| CSS preprocessors / Tailwind | 简历未突出，但实际工作中必然涉及 | 准备 Tailwind 核心概念、utility-first 理念，能聊 design token 体系 |
| Testing (Jest, Cypress, Selenium) | 提到 100% 测试覆盖率但未展开 | 准备 testing pyramid、单元/集成/E2E 测试策略的回答 |
| Accessibility (WCAG) | 简历未提及 | 了解 WCAG 2.1 AA 级标准、aria 属性、键盘导航、屏幕阅读器适配，银行对无障碍要求高 |
| Banking/Financial domain | 无金融行业经验 | 了解渣打银行业务（global financial market），金融前端常见需求（实时数据、图表、安全合规） |
| CI/CD pipelines | 简历未突出 | 准备 Git workflow、CI/CD pipeline 设计、canary release 的经验描述 |
| Cross-browser compatibility | 简历侧重跨平台（H5/小程序/Weex） | 可将跨平台经验迁移表述为兼容性能力 |

---

## 二、自我介绍（建议 90 秒）

**策略：结果开场 → 两个锚点 → 精准共鸣 → 留一个意外**

**核心原则：不讲完整故事，只抛钩子。让面试官想追问，并把追问引导到你最擅长的领域。**

---

### English Version（~60 sec）

I’ve spent the last seven years at Alibaba, /
building and optimizing web apps /
that serve hundreds of millions of people every day.
My focus has always been on performance, reliability, /
and building a strong engineering culture. //

Two achievements I’m really proud of.
First, / I helped speed up Taobao’s product detail page, /
cutting its 95th-percentile First Contentful Paint /
from 4 seconds down to 1.2 seconds, /
which boosted conversion by 2%. //

Second, / I built engineering standards /
for our 60-person frontend team —
no top-down rules, /
just tools and culture people actually wanted to use. //

Outside of work, / I built my own products:
a note-taking app with Tauri and React, /
an AI diet app I published on the App Store, /
and I am also keeping a tech blog. //

As for why Standard Chartered?
I love that you do the right thing, /
never settle, /
and better together.This is how I have always worked
Your focus on learning, sabbaticals, and flexible work patterns /
shows you really care about the growth of employees, not just delivery.
That’s exactly the kind of trusted, supportive environment /
I want to be part of it.

---

### 中文版（~250 字，≈90 秒）

> 过去 7 年我在阿里巴巴做的事可以总结为三个关键词：性能、可靠性、工程文化。我负责的产品日活数亿。
>
> 两件最自豪的事：第一，我把淘宝商品详情页的 P95 首屏从 4 秒干到了 1.2 秒，直接推动转化率提升 2%。第二，我给一个 60 人的前端团队建立了工程规范，没用任何行政命令——靠的是做出让人自愿用的工具和文化。
>
> 工作之外我也在做自己的产品——用 Tauri + React 写了一个开源笔记应用，独立上架了一款 AI 饮食决策 App，同时持续维护个人技术博客。
>
> 为什么选渣打：你们的 "Do the right thing, Never settle, Better together" 正好是我一直以来的做事方式。另外你们提供持续学习文化、sabbatical、弹性工作方式——这说明公司是真的在投资人的成长，不只是消耗产出。这是我想要的下一站。

---

## 三、高频行为面试题（STAR 格式准备）

### Q1: Tell me about a time you led a significant technical initiative.

**English Version:**

**Situation:** Taobao's product detail page had poor frontend performance — P95 first screen paint was 3.95 seconds, and even worse on low-end devices at 5.68 seconds. Multiple tech stacks coexisted, driving up maintenance costs.

**Task:** As the Tech Lead, I needed to unify the architecture and dramatically improve performance to support better business conversion.

**Action:**
- Analyzed performance bottlenecks: server-side rendering blocking, oversized JS bundles, and serialized critical-path requests
- Designed a React Streaming SSR solution, shifting first-screen rendering from blocking to streaming
- Created a phased migration plan, progressively decommissioning legacy code, old domains, and long-tail app versions
- Built a performance monitoring system to continuously track percentile metrics

**Result:** P95 FSP dropped to 1.2s (1.4s on low-end devices), driving a 2% uplift in shopping conversion rate, with a dramatic reduction in maintenance overhead.

**中文版：**

**Situation:** Taobao 商品详情页前端性能差（P95 FSP 3.95s），多套技术栈并存，维护成本高。

**Task:** 作为 Tech Lead，需要统一架构并大幅提升性能，支撑业务转化率提升。

**Action:**
- 分析性能瓶颈：服务端渲染阻塞、JS bundle 过大、关键路径请求串行
- 设计 React Streaming SSR 方案，将首屏渲染从阻塞式改为流式
- 制定分阶段迁移计划，逐步下线旧代码/旧域名/长尾版本
- 建立性能监控体系，持续跟踪各分位数据

**Result:** P95 FSP 降至 1.2s（低端机 1.4s），推动购物转化率提升 2%，维护成本大幅下降。

---

### Q2: Describe a time you solved a complex technical problem.

**English Version:**

**Situation:** The merchant rich-text editor for product details suffered severe submission lag — hundreds of daily complaints, with P95 processing time exceeding 6 minutes.

**Task:** Diagnose and resolve the editor performance issue to eliminate user complaints.

**Action:**
- **Identified the Bottleneck:** The root cause of the lag was the heavy computational cost of converting all merchant-uploaded text and image modules into images via `canvas` upon submission, which severely blocked the main thread.
- **Asynchronous Task Sharding (Pre-processing):** Shifted the heavy conversion process from a centralized "on-submit" action to a background process. Tasks were sharded and triggered incrementally immediately after a merchant added or edited each module.
- **Parallel Execution via Task Queues:** Introduced a task queue system and spun up multiple hidden child `iframe` instances to execute these canvas rendering tasks in parallel, bypassing single-thread limitations.
- **Scenario-specific Optimization:** Applied tailored strategies—bulk generation for "create new" scenarios vs. cache-reliant incremental updates for "edit existing" scenarios.

**Result:** P95 for new product editing dropped from 6+ minutes to under 10 seconds; editing existing products to under 3 seconds. Daily complaints went from hundreds to zero.

**中文版：**

**Situation:** 商家富文本编辑器提交卡顿严重，每天数百起投诉，P95 处理时间超过 6 分钟。

**Task:** 定位并解决编辑器性能问题，消除用户投诉。

**Action:**
- **定位瓶颈**：卡顿根源在于提交时需通过 Canvas 将所有图文模块统一转化为图片，巨大的计算量严重阻塞了主线程。
- **异步任务分片（前置处理）**：将集中式的转换过程拆解，前置到商家每次新增或修改模块后，在后台静默增量处理组件转换。
- **任务队列与并行执行**：引入任务队列机制，并通过分配给多个隐藏的子 iframe 实例同时执行任务，实现 Canvas 渲染的多进程/多实例并行处理。
- **场景化优化**：针对“新建”（需批量生成整个长图）和“编辑”（依靠缓存，仅局部增量更新）场景运用不同策略分别优化以避免冗余计算。

**Result:** 新建编辑 P95 从 6+ 分钟降到 10 秒内，编辑场景降到 3 秒内，日投诉量从数百降到零。

---

### Q3: How do you handle code quality and standards in a team?

**English Version:**

**Situation:** A 60+ person frontend team with inconsistent coding styles and varying quality levels.

**Task:** Establish unified engineering standards and raise overall code quality.

**Action:**
- Defined and rolled out coding conventions with unified ESLint/Prettier configurations
- Designed a CLI scaffolding tool to ensure every new project started compliant from day one
- Drove adoption of unit testing and established a code review culture
- Built developer tools (VS Code extension, Chrome extension) to lower the friction of following standards

**Result:** Significant improvement in code consistency, shorter onboarding time for new hires, and reduced production incident rate.

**中文版：**

**Situation:** 60+ 人前端团队代码风格不一致，质量参差不齐。

**Task:** 建立统一工程规范，提升整体代码质量。

**Action:**
- 制定并推行代码规范（ESLint/Prettier 配置统一）
- 设计 CLI 脚手架工具，确保项目初始化即符合规范
- 推动单元测试落地，建立 code review 文化
- 开发效率工具（VS Code 插件、Chrome 插件）降低规范执行成本

**Result:** 团队代码一致性显著提升，新人上手时间缩短，线上故障率下降。

---

### Q4: Tell me about a time you mentored someone or shared knowledge.

**English Version:**

**Situation:** While driving engineering standardization for a 60+ person team, I found that many developers struggled not with willingness but with knowing *how* to follow best practices.

**Task:** Lower the barrier to adopting good practices and help the team grow collectively.

**Action:**
- Ran internal tech talks and brown-bag sessions on topics like testing strategies, performance debugging, and code review best practices
- Provided one-on-one guidance for junior developers on architectural thinking and problem decomposition
- Built CLI tools and project templates that embedded best practices by default — a form of "mentoring at scale"
- Maintained a personal tech blog, sharing insights on React, performance optimization, and engineering culture

**Result:** Team members became more autonomous in making sound technical decisions. New hires ramped up faster with less hand-holding. Several junior engineers I coached were promoted within a year.

**中文版：**

**Situation:** 在推动 60+ 人团队工程规范化的过程中，我发现很多同学不是不愿意做好，而是不知道怎么做。

**Task:** 降低最佳实践的执行门槛，帮助团队整体成长。

**Action:**
- 组织内部技术分享，覆盖测试策略、性能调试、code review 方法论等主题
- 对初级开发者做一对一辅导，重点培养架构思维和问题拆解能力
- 通过 CLI 工具和项目模板把最佳实践内置其中——一种"规模化 mentor"方式
- 持续维护个人技术博客，分享 React、性能优化、工程文化相关内容

**Result:** 团队成员在技术决策上更加自主，新人上手更快，我辅导的几位初级工程师在一年内得到晋升。

---

### Q5: How do you handle disagreements with product managers or stakeholders?

**English Version:**

**Situation:** Marketing complained slow page loads were wasting ad budgets, but Product Managers refused to pause features for a root-level codebase refactoring.

**Task:** Align cross-functional priorities and secure buy-in for a complete codebase overhaul.

**Action:**
- **Linked Tech to Business Impact:** Quantified how maintaining legacy codebases caused high latency and killed ad ROI, uniting Marketing, Product, and Engineering around a shared revenue goal.
- **Refused Quick Fixes:** Explained there was no viable "band-aid." Advocated firmly for the painful but correct path: converging scattered codebases and dropping legacy versions to fix the root cause.
- **Zero-Downtime Rollout:** Designed a phased migration strategy, allowing us to swap the architecture safely ("change the engine in flight") without blocking new feature releases.

**Result:** Secured full buy-in. We achieved a 1.2s P95 load time, driving a 2% conversion lift that resolved Marketing's complaints. The converged codebase doubled future delivery speed.

**中文版：**

**Situation:** 广告端投诉详情页变慢浪费预算，但产品端拒绝为“纯技术重构”暂停新功能迭代，导致优先级冲突。

**Task:** 调和分歧，争取资源进行彻底的底层代码重构。

**Action:**
- **技术债务业务化**：用数据证明维护老旧代码是如何拖垮 FCP 和广告 ROI 的，将三方目标统一到“提升整体营收”上。
- **拒绝苟且重本求源**：明确指出没有“快速止血”捷径。顶住压力推动正确但痛苦的抉择：收敛多套零散代码库、坚决下线长尾历史版本，彻底拔除性能和维护痛点。
- **平滑演进打消顾虑**：设计精细的灰度迁移方案，在不中断核心业务迭代的前提下“开着飞机换引擎”，打消了产品侧对断档发版的担忧。

**Result:** 成功拿到了完整重构的排期。最终 P95 降至 1.2s，转化率提升 2% 终结了客诉，且统一后的代码库让后续研发提速一倍。

---

## 三（续）、简历项目 STAR 详解（中英对照）

> 以下按简历项目逐一展开。项目 2（详情页架构优化）和项目 4（富文本编辑器）已在上方行为面试题 Q1/Q2 中覆盖，此处不再重复。

---

### 项目 1：Store AI Shopping Assistant — Edge-side Implementation

**English Version:**

**Situation:** Alibaba wanted to launch an AI shopping assistant for Taobao stores — a conversational LUI (Language User Interface) that needed to work across multiple platforms (PC, H5, mini programs) with real-time streaming responses.

**Task:** Design and deliver the edge-side (client + frontend) architecture for the AI assistant from scratch (0 to 1), balancing high performance with cross-platform adaptability.

**Action:**
- Designed an edge Client + Frontend architecture that decoupled the AI interaction layer from platform-specific rendering, enabling one codebase to run across platforms
- Defined streaming data frame and card protocols for server communication, enabling dynamic Agent rendering — the UI could progressively display different card types as the Agent decided what to show
- Solved a key UX problem: streaming Markdown rendering caused visual jumps when syntax chunks were partially returned; built a buffering and reconciliation mechanism to ensure smooth, flicker-free rendering

**Result:** Successfully launched the AI shopping assistant from zero to production. The architecture supported multiple platforms without code duplication, and the streaming rendering delivered a smooth conversational experience comparable to native chat applications.

**中文版：**

**Situation:** 阿里巴巴要在淘宝店铺上线 AI 导购助手——一个对话式 LUI 交互产品，需要跨平台（PC、H5、小程序）运行，且支持实时流式响应。

**Task:** 从零设计并交付 AI 助手的端侧（Client + 前端）架构，兼顾高性能和多平台适配。

**Action:**
- 设计了 edge Client + 前端的分层架构，将 AI 交互层与平台渲染层解耦，实现一套代码多平台运行
- 定义了流式数据帧和卡片协议，用于与服务端 Agent 通信，支持动态卡片渲染——UI 可以根据 Agent 的决策逐步展示不同类型的卡片
- 解决了流式 Markdown 渲染的跳动问题：当 Markdown 语法块被截断返回时，通过缓冲和协调机制确保渲染平滑无闪烁

**Result:** AI 导购助手顺利从 0 到 1 上线。架构支持多平台无需重复开发，流式渲染体验接近原生聊天应用的流畅度。

---

### 项目 3：Protocol Engine SDK Refactoring

**English Version:**

**Situation:** The Protocol Engine SDK — used across Taobao's core consumer links (product detail, cart, checkout) — was a 146 KB black box. When issues occurred, developers had no way to debug it; troubleshooting could take hours with no clear root cause.

**Task:** Refactor the SDK to reduce bundle size, make the execution pipeline observable, and provide business teams with flexible customization without breaking any existing integrations.

**Action:**
- Rewrote the SDK architecture with a cleaner abstraction layer, separating the core protocol engine from business-specific logic — this gave teams the flexibility to customize behavior and adopt different tech stacks
- Aggressively optimized the bundle: tree-shook unused code paths, replaced heavy dependencies, and restructured module boundaries — cutting size from 146 KB to 36.7 KB
- Built comprehensive observability into the execution pipeline: added structured logging, trace points, and diagnostic tools so developers could pinpoint anomaly root causes within 5 minutes
- Ensured zero-fault migration: wrote 100% test coverage for the refactored SDK and enforced rigorous canary release mechanisms for each consuming application

**Result:** Bundle size reduced by 75% (146 KB → 36.7 KB). Developer troubleshooting experience went from "black-box guessing" to "root cause in 5 minutes." All business migrations completed with zero production incidents.

**中文版：**

**Situation:** 协议引擎 SDK 被淘宝核心消费链路（商品详情、购物车、下单）广泛使用，体积 146 KB，且是一个黑盒——出问题时开发者无法调试，排查可能耗费数小时且找不到根因。

**Task:** 重构 SDK，缩减体积、使执行链路可观测，并为业务团队提供灵活的定制能力，同时不能破坏任何现有集成。

**Action:**
- 重新设计 SDK 架构，引入更清晰的抽象层，将核心协议引擎与业务逻辑分离——让各团队可以灵活定制行为、支持不同技术栈
- 极致优化包体积：tree-shaking 无用代码路径、替换重依赖、重构模块边界——从 146 KB 减到 36.7 KB
- 在执行管线中内置全链路可观测性：结构化日志、埋点追踪、诊断工具，让开发者可以在 5 分钟内定位异常根因
- 保障零故障迁移：编写 100% 测试覆盖率，对每个接入应用执行严格的灰度发布机制

**Result:** 包体积缩减 75%（146 KB → 36.7 KB），排障体验从"黑盒猜测"变为"5 分钟定位根因"，所有业务迁移零线上故障。

---

### 项目 5：Cross-platform UI Component Library — DiDi

**English Version:**

**Situation:** At DiDi, multiple business lines were independently building their own UI components, leading to inconsistent user experience, duplicated effort, and high maintenance costs across platforms.

**Task:** Design and implement a unified cross-platform UI component library and a shared materials center to serve multiple business lines.

**Action:**
- Led the architecture design of the component library, establishing a clear API contract and theming system that worked across platforms
- Built a shared materials center where teams could discover, preview, and reuse components — reducing duplication
- Defined contribution guidelines and review processes to maintain quality as the library scaled across teams

**Result:** Unified the UI layer across multiple DiDi business lines, significantly reducing duplicated component development and improving visual consistency across products.

**中文版：**

**Situation:** 在滴滴，多条业务线各自独立开发 UI 组件，导致用户体验不一致、重复劳动、跨平台维护成本高。

**Task:** 设计并实现统一的跨平台 UI 组件库和共享物料中心，服务多条业务线。

**Action:**
- 主导组件库架构设计，定义清晰的 API 规范和主题系统，确保跨平台一致性
- 搭建共享物料中心，支持组件发现、预览和复用，减少重复开发
- 制定贡献规范和 review 流程，保障组件库在多团队接入后的质量

**Result:** 统一了滴滴多条业务线的 UI 层，显著减少重复组件开发，提升产品间的视觉一致性。

---

### 项目 6：Login SDK & Membership System — MOGU Inc.

**English Version:**

**Situation:** At MOGU, each internal business unit handled login and membership integration independently. Every new integration took about 2 weeks, with duplicated logic and inconsistent implementations across the group.

**Task:** Independently manage the frontend of the group's point/membership system and design a reusable Login SDK to dramatically speed up integrations.

**Action:**
- Analyzed the login and membership flows across different business units, identifying common patterns and unit-specific variations
- Designed an abstract Login SDK that encapsulated shared logic while exposing configuration hooks for business-specific traits — enabling each unit to integrate without writing boilerplate
- Independently owned the full frontend of the point/membership system, handling both the consumer-facing and admin-facing interfaces

**Result:** Integration time for new business units dropped from 2 weeks to 3 days — an 80%+ reduction. The SDK became the standard login solution across all MOGU business units.

**中文版：**

**Situation:** 在蘑菇街，各内部业务线独立对接登录和会员体系，每次新接入大约需要 2 周，逻辑重复且实现不一致。

**Task:** 独立负责集团积分/会员系统的前端开发，并设计可复用的 Login SDK，大幅加速接入效率。

**Action:**
- 分析各业务线的登录和会员流程，提炼共性逻辑和业务差异点
- 设计抽象 Login SDK，封装通用逻辑的同时暴露业务特征配置钩子——让各业务线无需重写样板代码即可接入
- 独立负责积分/会员系统全端前端开发，覆盖 C 端和管理后台

**Result:** 新业务线接入时间从 2 周降到 3 天，缩减 80% 以上。该 SDK 成为蘑菇街所有业务线的标准登录方案。

---

## 四、技术面试高频考点

### 4.1 React 深度

**准备要点：**
- React 18/19 新特性：Concurrent Mode、Suspense、Server Components、useTransition、use() hook
- React Streaming SSR 原理（renderToPipeableStream），你有实战经验，务必讲清楚
- 状态管理方案对比：Redux vs Zustand vs Jotai vs Context，什么场景用什么
- React 性能优化：React.memo、useMemo、useCallback、虚拟列表、代码分割
- Fiber 架构和调度机制

**加分项——你的独特经验：**
- 流式 SSR 在淘宝详情页的落地实践
- 流式 Markdown 渲染防跳动的技术细节
- AI Agent 动态卡片渲染方案

**推荐材料：**
- 📖 [React 官方文档 — React 19 新特性](https://react.dev/blog/2024/12/05/react-19) — 最权威的一手信息
- 📖 [New Suspense SSR Architecture in React 18](https://github.com/reactwg/react-18/discussions/37) — Dan Abramov 写的 Streaming SSR 设计原理
- 📺 [React Server Components — Talk by Dan Abramov and Lauren Tan](https://react.dev/blog/2020/12/21/data-fetching-with-react-server-components) — RSC 概念来源
- 📖 [Bulletproof React](https://github.com/alan2207/bulletproof-react) — React 项目架构最佳实践，GitHub 30k+ stars
- 📖 [useMemo, useCallback, React.memo 完全指南](https://www.joshwcomeau.com/react/usememo-and-usecallback/) — Josh Comeau 的深度文章

---

### 4.2 JavaScript 深度

**准备要点：**
- Event Loop（宏任务/微任务）、Promise、async/await
- 闭包、原型链、this 绑定
- ES6+ 特性：Proxy、Reflect、WeakMap/WeakRef、Iterator/Generator
- 模块系统：ESM vs CJS，Tree Shaking 原理
- TypeScript 高级类型：泛型、条件类型、infer、模板字面量类型

**推荐材料：**
- 📖 [JavaScript.info](https://javascript.info/) — 最全面的现代 JS 教程，Event Loop / Promise / Proxy 章节必读
- 📺 [Jake Archibald: In The Loop](https://www.youtube.com/watch?v=cCOL7MC4Pl0) — Event Loop 最经典的可视化讲解（JSConf）
- 📖 [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/) — TS 高级类型系统的权威参考
- 📖 [Type Challenges](https://github.com/type-challenges/type-challenges) — TypeScript 类型体操练习，面试前刷中等难度即可
- 📖 [ES modules: A cartoon deep-dive](https://hacks.mozilla.org/2018/03/es-modules-a-cartoon-deep-dive/) — ESM 原理图解

---

### 4.3 CSS & 响应式设计

**准备要点：**
- Flexbox 和 Grid 布局模型
- CSS 变量（Custom Properties）和 Design Token 体系
- Tailwind CSS 原理：utility-first 理念、JIT 编译、与传统 CSS 方案对比
- 响应式设计：media queries、container queries、clamp()
- CSS-in-JS vs Utility CSS vs BEM 的 trade-off

**推荐材料：**
- 📖 [A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) — CSS-Tricks 经典速查
- 📖 [A Complete Guide to CSS Grid](https://css-tricks.com/snippets/css/complete-guide-grid/) — 同上，Grid 版
- 📖 [Tailwind CSS 官方文档 — Core Concepts](https://tailwindcss.com/docs/utility-first) — 重点看 utility-first 理念和 design system 集成
- 📺 [Why I Love Tailwind CSS (and Why You Should Too)](https://www.youtube.com/watch?v=lHZwlzOUOZ4) — 快速理解 Tailwind 的设计哲学
- 📖 [The CSS Container Queries Guide](https://ishadeed.com/article/css-container-query-guide/) — Ahmad Shadeed 的容器查询深度指南

---

### 4.4 性能优化（你的王牌）

**准备要点（结合实际经验）：**
- Core Web Vitals：LCP、FID/INP、CLS 的含义和优化策略
- 首屏性能优化全链路：DNS → TCP → TLS → TTFB → FCP → LCP
- SSR/SSG/ISR 的适用场景和 trade-off
- 代码分割策略：路由级、组件级、动态 import
- 资源优化：图片（WebP/AVIF、lazy loading）、字体（font-display）、Critical CSS
- Bundle 优化：Tree Shaking、Scope Hoisting、chunk 策略
- 运行时性能：长任务分片（requestIdleCallback、scheduler.yield）、虚拟滚动

**推荐材料：**
- 📖 [web.dev — Performance](https://web.dev/learn/performance) — Google 官方性能学习路径，覆盖 Core Web Vitals 全部内容
- 📖 [Interaction to Next Paint (INP)](https://web.dev/articles/inp) — FID 已被 INP 替代，必须了解
- 📺 [The Cost of JavaScript](https://www.youtube.com/watch?v=63I-mEuSvGA) — Addy Osmani 经典演讲，JS 性能成本分析
- 📖 [Rendering on the Web](https://web.dev/articles/rendering-on-the-web) — Google 出品，SSR/CSR/SSG/Streaming 全对比
- 📖 [JavaScript Loading Priorities in Chrome](https://addyosmani.com/blog/script-priorities/) — 资源加载优先级详解
- 📖 [Optimize Long Tasks](https://web.dev/articles/optimize-long-tasks) — scheduler.yield 与长任务优化

---

### 4.5 测试策略

**准备要点：**
- Testing Pyramid：Unit → Integration → E2E 的比例关系
- Jest：单元测试、mock 策略、snapshot testing
- React Testing Library：testing by user behavior 而非 implementation detail
- Cypress/Playwright：E2E 测试策略和最佳实践
- 你的实战经验：SDK 重构 100% 测试覆盖 + canary release 的故事

**推荐材料：**
- 📖 [Testing Library 官方文档 — Guiding Principles](https://testing-library.com/docs/guiding-principles) — "The more your tests resemble the way your software is used, the more confidence they can give you"
- 📖 [Kent C. Dodds — Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications) — 替代传统 Testing Pyramid 的现代测试策略
- 📖 [Playwright Best Practices](https://playwright.dev/docs/best-practices) — 官方 E2E 测试最佳实践
- 📺 [But really, what is a JavaScript test?](https://www.youtube.com/watch?v=r9HdJ8P6GQI) — Kent C. Dodds 从零解释测试本质
- 📖 [Vitest 官方文档](https://vitest.dev/) — 如果面试聊到 Vite 生态的测试方案

---

### 4.6 工程化与 CI/CD

**准备要点：**
- Git 工作流：Git Flow vs Trunk-Based Development
- CI/CD pipeline 设计：lint → test → build → deploy → smoke test
- Canary Release / Blue-Green Deployment
- Monorepo 管理（如果有经验）
- 构建工具：Webpack vs Vite 的差异和选型

**推荐材料：**
- 📖 [Trunk Based Development](https://trunkbaseddevelopment.com/) — 全面介绍 Trunk-Based 工作流及其适用场景
- 📖 [Vite 官方文档 — Why Vite](https://vite.dev/guide/why.html) — Webpack vs Vite 的设计差异
- 📖 [Turborepo Handbook](https://turbo.build/repo/docs/crafting-your-repository) — Monorepo 最佳实践
- 📖 [GitHub Actions 官方文档](https://docs.github.com/en/actions) — CI/CD pipeline 构建参考
- 📖 [Canary Releases — Martin Fowler](https://martinfowler.com/bliki/CanaryRelease.html) — 金丝雀发布概念出处

---

### 4.7 安全与合规（银行业重点）

**准备要点：**
- XSS 防御：CSP、输入转义、DOMPurify
- CSRF 防御：SameSite Cookie、CSRF Token
- CORS 配置最佳实践
- HTTPS / HSTS / Subresource Integrity
- 敏感数据处理：不在前端存储敏感信息、加密传输
- Content Security Policy 在金融场景的应用
- 身份认证：OAuth 2.0 / OIDC / JWT 的前端处理

**推荐材料：**
- 📖 [OWASP Top 10](https://owasp.org/www-project-top-ten/) — Web 安全必知的 10 大漏洞类型，银行面试高频
- 📖 [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) — 按主题分类的安全速查表（XSS/CSRF/Auth 等）
- 📖 [MDN — Content Security Policy (CSP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) — CSP 配置详解
- 📖 [Auth0 — OAuth 2.0 Simplified](https://auth0.com/docs/get-started/authentication-and-authorization-flow) — OAuth/OIDC 流程图解
- 📖 [web.dev — Safe and secure](https://web.dev/secure/) — Google 出的 Web 安全实践指南

---

### 4.8 无障碍（Accessibility）

**准备要点：**
- WCAG 2.1 AA 标准核心原则：可感知、可操作、可理解、健壮性
- 语义化 HTML 的重要性（header/nav/main/section/article）
- ARIA 角色和属性（aria-label、aria-describedby、aria-live）
- 键盘导航和焦点管理
- 颜色对比度要求（4.5:1 / 3:1）
- 屏幕阅读器测试（VoiceOver / NVDA）

**推荐材料：**
- 📖 [web.dev — Learn Accessibility](https://web.dev/learn/accessibility) — Google 出品的无障碍学习路径，结构清晰
- 📖 [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) — W3C 官方 ARIA 模式库，面试能引用这个很加分
- 📖 [The A11Y Project — Checklist](https://www.a11yproject.com/checklist/) — 实用的 WCAG 合规检查清单
- 📖 [Deque University — axe Rules](https://dequeuniversity.com/rules/axe/) — 自动化无障碍测试规则参考
- 📺 [A11ycasts with Rob Dodson](https://www.youtube.com/playlist?list=PLNYkxOF6rcICWx0C9LVWWVqvHlYJyqw7g) — Google Chrome 团队出品的无障碍系列视频

---

## 五、可能的系统设计 / 场景题

### 场景 1：设计一个金融市场实时数据看板

**考察点：** WebSocket、实时数据更新策略、大量数据渲染性能

**回答思路：**
- 数据层：WebSocket 连接管理、断线重连、数据去重和排序
- 渲染层：虚拟列表/虚拟表格处理大量行情数据、requestAnimationFrame 控制更新频率
- 状态管理：区分高频数据（行情）和低频数据（配置），不同更新策略
- 性能：Web Worker 处理数据计算、避免主线程阻塞

**推荐材料：**
- 📖 [TanStack Virtual](https://tanstack.com/virtual/latest) — 虚拟滚动方案，理解大数据量渲染必备
- 📖 [MDN — WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) — WebSocket 基础
- 📖 [High-Performance Real-Time Stock Ticker (System Design)](https://systemdesign.one/real-time-stock-ticker-system-design/) — 直接对口的系统设计案例
- 📖 [Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) — Web Worker 在计算密集场景的应用

### 场景 2：设计一个微前端架构方案

**考察点：** 子应用隔离、通信机制、共享依赖

**回答思路：**
- 方案选型：Module Federation vs qiankun vs single-spa
- JS 沙箱：Proxy-based sandbox
- CSS 隔离：Shadow DOM / CSS Modules / scoped styles
- 通信：Custom Events / Shared State / URL params
- 共享依赖：externals / import maps

**推荐材料：**
- 📖 [Micro Frontends — Martin Fowler](https://martinfowler.com/articles/micro-frontends.html) — 微前端概念的经典文章
- 📖 [Module Federation 官方文档](https://module-federation.io/) — Webpack 5 模块联邦
- 📖 [qiankun 官方文档](https://qiankun.umijs.org/) — 蚂蚁金服出品，JS 沙箱机制值得研究
- 📺 [Micro-Frontends: What, Why, and How — Luca Mezzalira](https://www.youtube.com/watch?v=w58aZjACETQ) — 微前端架构决策的系统讲解

### 场景 3：如何从零搭建一个前端项目并建立工程规范

**考察点：** 你的基建经验

**回答思路：** 直接用你在阿里推动 60+ 人团队工程化的经验

**推荐材料：**
- 📖 [Bulletproof React](https://github.com/alan2207/bulletproof-react) — 从项目结构到测试到状态管理的全套最佳实践
- 📖 [ESLint 官方文档 — Configuration](https://eslint.org/docs/latest/use/configure/) — 规范配置参考
- 📖 [Conventional Commits](https://www.conventionalcommits.org/) — 提交信息规范
- 📖 [Husky + lint-staged](https://github.com/lint-staged/lint-staged) — Git hooks 自动化代码检查

---

## 六、你应该问面试官的问题

1. **团队相关：** What does the frontend team structure look like? How many frontend engineers are on the team, and what's the ratio of senior to junior members?

2. **技术栈：** What's the current tech stack? Are there any ongoing or planned migrations? For example, are you moving from a legacy framework to React?

3. **业务场景：** Could you tell me more about the specific financial market applications I'd be working on? For example, is it trading platforms, risk dashboards, or client-facing portals?

4. **工程实践：** How mature is the current CI/CD pipeline and testing infrastructure? Is there room for improvement that this role would drive?

5. **AI 方向：** The JD mentions AI coding assistants as a plus. Is the team exploring AI-assisted development or any AI-powered features for the products?

6. **成长空间：** What does career progression look like for this role? Is there a path toward a principal engineer or engineering manager track?

7. **工作方式：** The JD mentions hybrid working. What does a typical week look like in terms of office days and remote days?

---

## 七、需要特别注意的点

### 1. 外企面试文化差异
- 强调 **collaboration** 而非个人英雄主义
- 回答问题用 **"we" 多于 "I"**，但在描述自己贡献时清晰表明 "my specific contribution was..."
- 体现 **structured thinking**：回答技术问题先说 approach，再说 detail
- 体现 **trade-off thinking**：不要只说方案好，要说为什么不选其他方案

### 2. 银行业特殊关注点
- **Security first**：每个技术决策都要考虑安全影响
- **Compliance**：金融机构受严格监管，代码变更流程更严谨
- **Stability over innovation**：银行更看重稳定性和可靠性，不要一味强调新技术
- **Accessibility**：WCAG 合规在欧美银行是硬性要求
- **Data sensitivity**：对客户数据的处理要格外谨慎

### 3. 薪资谈判参考
- 渣打 Band 5 对应 Senior/Lead 级别
- 广州 base，外企 package 结构通常包含：base salary + bonus（通常 2-4 个月）+ 补充公积金 + 商业保险
- 可以了解下渣打的 RSU/股票计划

### 4. 英语面试准备
- 技术面很可能是英文进行，准备好用英文描述你的项目经验
- 练习常见技术词汇的英文发音：asynchronous、reconciliation、hydration、serialization
- HR 面基本确定是英文，准备好 behavioral questions 的英文回答

---

## 八、面试当天 Checklist

- [ ] 打印简历英文版 2 份
- [ ] 准备好自我介绍（英文，2-3 分钟）
- [ ] 复习 React 18/19 核心概念
- [ ] 复习 Web 安全知识（XSS/CSRF/CSP）
- [ ] 复习 WCAG 无障碍基本要求
- [ ] 了解渣打银行近期新闻和业务重点
- [ ] 准备 3-5 个问面试官的问题
- [ ] 确认面试地点和到达路线
