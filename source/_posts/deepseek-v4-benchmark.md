---
title: 同一套工作流规范再战：DeepSeek V4 Pro/Flash 对决 Claude Opus 4.7 与 Kimi 2.6
date: 2026-05-14 12:00
tags: "AI"
---

> Kilo Code 团队继上次用 FlowGraph 规范对比 Claude Opus 4.7 与 Kimi 2.6 之后，又将同一套测试施加在刚发布的 DeepSeek V4 Pro 和 DeepSeek V4 Flash 上。四款模型同台竞技，结果拉开了从 $0.02 到 $17.89 的成本光谱。原文地址：https://blog.kilo.ai/p/we-tested-deepseek-v4-pro-and-flash，之前 Claude Opus 4.7 与 Kimi 2.6 对比的内容地址：https://mp.weixin.qq.com/s/PmXDL54ugRk0Iyy0l2mxDg

**TL;DR：** DeepSeek V4 Pro 拿到 77/100 分，花费 $2.25，位居 Claude Opus 4.7（91 分）和 Kimi 2.6（68 分）之间。DeepSeek V4 Flash 以 $0.02 的惊人低价拿到 60/100 分，但构建失败且关键功能缺失。

---

DeepSeek V4 Pro 和 DeepSeek V4 Flash 于 2026 年 4 月 24 日同步发布，均采用 MIT 开源协议。这是 DeepSeek 继 V3 之后首次推出全新架构，也是他们第一次以双档阵容（Pro 为旗舰，Flash 为轻量级）同时发布开源权重模型。

![](https://substackcdn.com/image/fetch/$s_!RkaY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb504b56e-63d8-4c77-b957-8bec78d1bfac_1080x742.png)

Kilo 团队沿用了此前测试 Claude Opus 4.7 和 Kimi 2.6 时的那套 FlowGraph 规范，同样的规范文档、同样的 prompt、同样的评分标准，确保处在同一起跑线。

## 四款模型一览

![四款模型对比](https://substackcdn.com/image/fetch/$s_!VI4A!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfc40c6e-2242-4f9a-aa09-9e3ab2e328eb_1456x437.jpeg)

DeepSeek V4 Flash 是本次对比中最便宜的模型，且差距悬殊——输出 token 单价不到 Kimi 2.6 的 1/14，约为 Claude Opus 4.7 的 1/89。

此外，DeepSeek 正在对 V4 Pro 实施七五折促销（截至 2026 年 5 月 31 日）。折后输入价格降至约 $0.036/百万 token，输出降至 $0.87/百万 token，在两个维度上均低于 Kimi 2.6。DeepSeek 还永久下调了全线产品的输入缓存定价，降幅达 90%。

## 测试内容

这是我们在 Opus 4.7 vs Kimi 2.6 评测中使用的同一份 FlowGraph 规范：一个工作流编排后端，包含 20 个接口、持久化状态、租约管理、重试机制和事件流推送。相比常规编码基准测试，它是一份更重型的基础设施考题，旨在将模型推向极限。

我们让 DeepSeek V4 Pro 和 V4 Flash 走完同样的流程，看看 DeepSeek 新阵容在成本和首次生成质量上，与 Claude Opus 4.7 及 Kimi 2.6 之间的差距。

## Prompt

两个 DeepSeek 模型均在 Kilo CLI 中运行，使用与 Opus 4.7 和 Kimi 2.6 完全一致的 prompt：

> "读取 @SPEC.md，然后在当前目录下把项目写出来。@SPEC.md 是你唯一要遵循的标准。不要做假的 mock 数据，也别写那种玩具一样的增删改查。你要写出所有业务代码、配置文件、Prisma schema、测试套件和 README，让项目能跑起来。……"

两个 DeepSeek 模型均开启思考模式，在各自独立的空目录里运行，互不干扰。

## 它们交出了什么作业

![交付物对比](https://substackcdn.com/image/fetch/$s_!qjeS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59fe59f0-563b-4a61-b70d-42ebbdd1133c_1456x377.jpeg)

DeepSeek V4 Pro 的测试套件通过了，但 TypeScript 构建失败。DeepSeek V4 Flash 的测试套件压根没跑起来——它的初始化脚本尝试强制重置数据库时报错，第一个测试用例都没执行到。

如果只看模型自身的总结报告，两个 DeepSeek 实现看上去都更接近 Claude Opus 4.7 的表现。但我们做了代码逐行审查，并在隔离的 SQLite 数据库上做了定向复现，问题就暴露出来了。

## DeepSeek V4 Pro

DeepSeek V4 Pro 把系统的大框架做对了。接口都接上了，测试套件也通过了，项目结构也算合理。问题集中在与 Kimi 2.6 相同的几个地方：租约过期处理、调度逻辑、输入校验，以及构建完整性。
![](https://substackcdn.com/image/fetch/$s_!qSDq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F060370e7-c491-4821-8644-232ff08c74d7_1456x1709.png)

### 超时的 Worker 仍然能完成步骤

当一个 Worker 认领了某个步骤时，系统会为其分配一个租约，到期即视为超时。如果 Worker 卡住或崩溃，租约过期后应该允许其他 Worker 接管。一旦租约过期，原 Worker 就不再是该步骤的所有者，不应该被允许将其标记为完成。

DeepSeek V4 Pro 在心跳续约时做了这个检查，但在任务完成时没有。我们标记了一个步骤，手动将其租约过期时间改到过去，然后调用 API 将该步骤标记为成功完成——API 返回了 200，步骤被记录为已完成。原 Worker 实际上越过了已经过期的租约，强行敲定了一项它不再拥有的工作。

DeepSeek V4 Pro 自己的 README 写道"Worker 在租约过期后不能完成步骤"，但实现并未强制执行这一规则。

### 一个满载的工作流会阻塞其他不相关的工作

一个工作流运行实例可以声明它最多允许多少个步骤并行执行。当达到上限时，这个饱和的实例不应再接受新工作，但共享同一队列的其他实例应该继续正常推进。

DeepSeek V4 Pro 的认领逻辑每次只检查一个候选者。如果这个候选者恰好属于一个已经达到并行上限的实例，函数就直接放弃返回空结果，而不是去检查下一个候选者。

我们用两个共享队列的活跃实例复现了这个问题。实例 A 已达到并行上限，实例 B 有空余容量且有一个更高优先级的步骤等待执行。下一次认领请求却返回为空。在生产环境中，这意味着 Worker 空转，尽管有实际的工作等待处理——仅仅因为队列里第一个实例恰好是满载的。

### 项目无法构建

`npm test` 通过了，但 `npm run build` 不行。即便修复了构建报错，项目依然无法通过 `npm start` 启动。TypeScript 配置被设置为不产出编译文件，而 `package.json` 中的 `npm start` 脚本却依赖这些编译产物。按照 DeepSeek V4 Pro 自己的 README 在新检出的目录中操作，用户得到的只会是一个无法启动的服务。

## DeepSeek V4 Flash

$0.02 完成整个运行——这是一个我们此前从未在这类测试中触及的价位。内部逻辑写得尚可，问题出在对外暴露的 API 层面。
![](https://substackcdn.com/image/fetch/$s_!h1D4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b352196-67a3-4d23-af0c-813abcdb5fe4_1456x1709.png)

### 客户端无法启动工作流

要使用这个系统，客户端首先需要通过调用指定接口来创建一个工作流运行实例。如果这个接口不工作，后面的一切都无从谈起——没有运行实例可供 Worker 认领，没有事件可以推送，没有步骤可以完成。

DeepSeek V4 Flash 写了这个接口的处理逻辑，但把它挂载到了错误的路由前缀下。规范要求的路径是 `/workflows/key/:key/runs`，而 DeepSeek V4 Flash 实际上把它放在了 `/runs/key/:key/runs`。对规范路径发起请求，返回的是 `404 Endpoint not found`。README 里写的是规范路径，但服务器不响应这个路径。

DeepSeek V4 Flash 的测试直接调用内部函数而非走 HTTP API。从测试套件的视角看一切正常，从真实客户端的视角看，系统的入口丢了。

### 已失败的工作流仍然分发任务

一旦工作流运行失败（因为某个步骤用尽了所有重试次数），该运行中的其他步骤都应该停下来。规范要求将剩余步骤置为 `blocked` 状态，这样 Worker 就不会再认领它们。

DeepSeek V4 Flash 的恢复逻辑在开头一次性加载所有过期步骤，然后逐个处理。如果第一个过期步骤耗尽重试次数并导致父运行失败，同一批次中靠后的步骤仍然会被提升为"等待重试"状态——即便它所属的运行已经结束了。

我们用同一个运行下的两个过期步骤做了复现：

- 步骤 a 已无剩余重试次数，被正确标记为死亡
- 父运行被正确标记为失败
- 步骤 b 却进入了 `waiting_retry` 状态而非 `blocked`

此时 Worker 轮询新任务时仍然会收到步骤 b，并为一个已经失败的工作流继续执行它。Claude Opus 4.7 有一个类似的多租约过期恢复 bug，Kimi 2.6 则完全没实现实时事件推送。竞态条件下的恢复逻辑，始终是这份规范中最难一次做对的部分。

### 同样的超时 bug

DeepSeek V4 Flash 也有与 V4 Pro 相同的租约过期完成 bug——过期的租约仍然能最终敲定工作，即便原 Worker 已经不再拥有该步骤。

此外，它还拒绝了合法的请求体。规范声明工作流运行的 input 和 metadata 可以携带任意 JSON，包括数组、字符串和数字。DeepSeek V4 Flash 的校验逻辑却只接受 JSON 对象。客户端发送 JSON 数组作为 input 会收到 400 响应，尽管规范明确允许这么做。

### 工具调用表现超出预期

上面那些 bug 是关于 DeepSeek V4 Flash 产出代码的质量问题。工具调用则是另一个维度：模型在 Kilo CLI 中的操作行为。在这个维度上，它的表现出乎意料地稳健。它在编辑文件前会先读取文件内容，在合适的时机安装依赖和运行测试，没有因为命令出错而陷入死循环。即便产出的代码有缺陷，Agent 循环本身运行得很流畅。

对于这个价位的模型来说算是超出预期了。工具调用的可靠性通常是廉价模型最先崩溃的地方——参数格式错误、幻觉文件路径、或者毫无进展的死循环把 token 烧光。DeepSeek V4 Flash 在我们的测试中成功避免了这些失败模式。

## 评分

我们使用了与 Opus vs Kimi 评测相同的 7 维评分标准。

![评分表](https://substackcdn.com/image/fetch/$s_!67Lg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b201fc2-3474-47ec-9b80-ccc5e61eb982_1456x540.jpeg)

DeepSeek V4 Pro 落位在 Claude Opus 4.7 和 Kimi 2.6 之间。与 Opus 的差距集中在构建质量和租约处理上。DeepSeek V4 Flash 则排在 Kimi 2.6 之后，几乎每个评分维度都有扣分。

## 成本与质量

![成本质量象限](https://substackcdn.com/image/fetch/$s_!nf6m!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59f37c4e-4756-4ce9-b844-04cfdd6bc72e_1090x484.png)

DeepSeek V4 Flash 的每分成本约为 Kimi 2.6 的 1/30，Claude Opus 4.7 的 1/100。分数是低了些，但绝对开销之低使得跑三四次对比择优仍然比跑一次 Kimi 2.6 更便宜。
![](https://substackcdn.com/image/fetch/$s_!-zqd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5d34121-438e-4376-aa15-8ee999507ddd_1356x892.png)
DeepSeek V4 Pro 在本次测试中比 Kimi 2.6 贵，因为我们跑的时候还没叠上官方折扣。如果按七五折促销价重新计算，同一次运行大约花 $0.55，在绝对成本上低于 Kimi 2.6 的同时多拿了 9 分。

## 对开源权重模型意味着什么

前几轮对比中观察到的格局依然稳固：开源权重模型与前沿闭源模型在表面覆盖率上的差距很窄，但在高难度代码路径（租约恢复、跨实例调度、过期租约拒绝）的正确性上仍有差距——虽然也在缩小。

DeepSeek V4 Pro 是相对 Kimi 2.6 的一次实质性进步。故障模式类似，但整体结构更干净，规范级别的遗漏更少。叠加官方折扣后，价格差距与 Kimi 拉开，质量差距依然保持。

DeepSeek V4 Flash 则打开了一个新品类。它不适合在没有人工收尾的情况下独立承担复杂后端构建，但 $0.02 一次的"初版尝试"对于这种量级的后端来说，是此前不存在的价位。如果你能接受不完美的输出再做一轮修正，这个成本结构会改变很多场景的计算方式。

## 总结

**Claude Opus 4.7 依然领跑。** 规范中那些棘手的部分——涉及时序、恢复、多组件协同的逻辑——所有其他模型丢分的地方。Claude Opus 4.7 只有一个可复现的 bug，其余三个模型都不止一个。

**DeepSeek V4 Pro 表现优于 Kimi 2.6。** 高出 9 分，每 token 标价更低，审查后暴露的故障模式也大致相同。叠加 5 月 31 日前的官方折扣后，成本优势更加明显。

**DeepSeek V4 Flash 开辟了新品类。** 它在没有人工清理的前提下不够可靠，但花 $0.02 就能拿到这种体量后端的一份初稿——这个价位前所未有。如果你能消化不完美的产出，这个成本逻辑就很香。
