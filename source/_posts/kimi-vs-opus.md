---
title: 同一套工作流评测规范：深度对比 Claude Opus 4.7 与 Kimi 2.6
date: 2026-04-22 12:00
tags: "AI"
---

> Kilo Code 团队用一份硬核的工作流编排规范（1042行）同时考察了刚刚发布的 Kimi K2.6 和前沿模型 Claude Opus 4.7。评测方法很客观，结果和观点值得分享，原文地址：https://blog.kilo.ai/p/we-gave-claude-opus-47-and-kimi-k26。

**TL;DR：** 跑同一套规范，Claude Opus 4.7 拿了 91 分，Kimi K2.6 拿了 68 分，两个模型的测试代码都跑通了。Kimi K2.6 只花了 Claude 五分之一的钱，就实现了 75% 的功能。但丢掉的那 25 分恰好是系统的命门：Worker 崩溃了能不能恢复？排队抢任务会不会搞错优先级？事件流还能不能连上？在这些稍微一踩油门就容易出问题的角落，Kimi K2.6 暴露了 6 处逻辑缺陷，而 Claude Opus 4.7 只有 1 处。

---

[Kimi K2.6](https://www.kimi.com/blog/kimi-k2-6) 在 2026 年 4 月 20 日上线，这个时候离 Anthropic 放出 [Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) 只有四天。我们把同一份名为 FlowGraph 的规范丢给了它们。这是一个要落盘到数据库的工作流引擎，里面涉及到任务的有向无环图（DAG）校验、防并发抢占、租约超时恢复、暂停和取消，还得支持服务端推送（SSE）。等它们各自把代码写完，除了看测试绿不绿，我们还人工做了一遍 code review，专门造了一些极端场景去撞它们的防护网。
![](https://substackcdn.com/image/fetch/$s_!3LI_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19a9dd82-4071-49c4-9392-942df218e832_1944x1220.png)

此外，在定价方面，Claude Opus 4.7 的输入成本大约是 Kimi K2.6 的 5 倍，输出成本更是足足隔了 6 倍。花这几倍的大价钱能不能换来代码质量上的绝对碾压，也是这次“极限施压”想摸清楚的底细。

![](https://substackcdn.com/image/fetch/$s_!CFgp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Facdf3acc-d975-4947-b5ae-d38e4ca523e3_1642x298.png)

## 为什么要用工作流来当考题

一般来说，API 框架的评测都喜欢搞个大杂烩，顺手考察一筐基础技能（搭架构、写鉴权、加过滤、做错误处理）。但这次，我们想选个场景往深了挖，评判的核心基准只有一条：逻辑必须绝对正确。

工作流引擎就是个绝佳的考场。你想想平时跑的自动结算业务：拉取付款记录、执行扣款、发送收据、推送数据报表。几步之间环环相扣，某一步出错了需要触发重试，要是干活的进程跑到一半突然崩溃了，还得能恢复现场。大名鼎鼎的 Temporal、Airflow 或是 AWS Step Functions 其实也都是在各种规模下解决这类痛点的。

选这道题，是因为带有 DAG（有向无环图）校验、原子抢占、租约超时恢复、重试调度以及各种启停控制引擎，**根本没法糊弄人**。两个干活的进程同时抢一个任务，系统它要么锁住了，要么就超卖了；租期到了的旧任务，它要么被系统正确回收，要么就死在了那里；当上游依赖跑通时，下游的待办步骤要么乖乖启动，要么就卡死不动。在这些环节上，代码行就是行，不行就是不行。

此外，这份满编 1,042 行的设计规范里还立了几个规矩：把 SQLite 作为唯一的数据源（source of truth）、保证对所有待办任务执行确定性的调度、以及必须满足“至少执行一次（at-least-once）”的语义。硬生生塞进去了包括工作流定义、运行实例、Worker 流水线、事件推送和健康看板在内的整整 20 个接口。

## 我们怎么测的

我们在 Kilo CLI 里，给两个模型喂了完全相同的 prompt：

> "读取 @SPEC.md，在当前目录下把项目写出来。@SPEC.md 就是你唯一要遵循的标准。别给我整假的 mock 数据，也别写那种玩具一样的增删改查。你要写出所有业务代码、配置文件、Prisma 的 schema、测试套件还要有 README。自己干，直到功能完整闭环。结束前跑一遍你写的测试，有报错就自己修，最后必须保证项目能跑起来。"

Claude Opus 4.7 满血开启了“高强度思考模式”，Kimi K2.6 也打开了它的思考模式。各自在一个干净的目录里开工，互打掩护。

## 它们交出了什么作业？

![](https://substackcdn.com/image/fetch/$s_!1-Kt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F235d6a11-70ea-4fdc-9e2c-cfa06d1e8392_2716x302.png)

Claude Opus 4.7 差不多花了 20 分钟就跑完了全程。Kimi K2.6 在挂钟耗时上确实久一些，但这并不是咱们这次要计较的分数。毕竟在跑测的当天，Kimi K2.6 才刚刚发版，可用的调度节点还紧巴巴的。如果直接拿它和基建早就炉火纯青的 Claude 去比绝对耗时，反而会让测试结果失真。等随后接盘托管的云厂商多起来，这块的响应差距自然也就抹平了。

从交付的东西来看，两边的工程骨架是一点没敷衍，稳稳拿捏了我们的预期：

- 老老实实用 Prisma 糊了底层，把 SQLite 当作唯一的业务状态源
- 用 Hono 把工作流定义、运行实例、Worker 动作、事件流、健康检查和指标监控的接口全都开了出来
- 知道在做任务抢占时，挂上带条件的 `updateMany` 来防并发锁死
- 搞定了重试和租约超时的逻辑调度
- 单独抽排了一张 `RunEvent` 表用来落审计日志
- README 给得也挺利索，配齐了起步指南不说，还煞有介事地交代了下 at-least-once（至少执行一次）机制

## 它们都说自己完美通关了

Claude Opus 4.7 在 6 个文件里跑了 31 个测试，全面绿灯。Kimi K2.6 把 20 个测试塞进了一个独立文件里，也是全部绿灯。

要是测到这里就直接收工，这两份代码看着确实还不相上下。但其实差远了。我们直接上手 review 了源码，外加起个独立的 SQLite 数据库专门跑定向复现测试，一下就把他们打回了原形：Claude Opus 4.7 爆出了 1 个真 bug，而 Kimi K2.6 身上足足查出来 6 个。

## Claude Opus 4.7的翻车点

### 多个任务同时超时，它的恢复机制犯了迷糊

根据规范，假如一个步骤重试到了上限，整个工作流就该宣告失败（`failed`），而其他还在排队的步骤应该被锁死（`blocked`）。Claude Opus 4.7 在只有一个步骤超时的时候，完美做到了这一点。但如果有两个租约同时过期进入恢复流程，它就自己和自己打架了。

我们看它的源码。在 `runRecovery()` 这段逻辑里，它把所有状态是 `running` 并且时间超期的任务一股脑儿读进内存，然后循环处理。

![](https://substackcdn.com/image/fetch/$s_!u_NU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c1d7f06-15bd-4804-84cf-29e47f8aebd5_1994x652.png)

处理第一个任务时，发现重试耗尽了，立刻触发 `failRunDueToDeadStep()`，把工作流置为失败，把别的步骤设为 `blocked`，这一步做的很好。

最大的问题就在第二次遍历。在走完 `failRun` 处理之后，轮到超时任务做回收时（执行 `handleLeaseExpiry()` ），它的 SQL 就只靠任务 `id` 来识别，连个兜底的状态检查都没加：

![](https://substackcdn.com/image/fetch/$s_!pecT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91043bb9-9896-4557-8cf3-7d0f7eaba7a9_1994x492.png)

于是乎，刚刚才被上一个循环设为 `blocked` 的任务，直接就被改回了 `waiting_retry`（等待重试）。

我们在库里塞了任务 a（最多重试 1 次）和任务 b（最多重试 2 次），让它们同时过期重跑。

![](https://substackcdn.com/image/fetch/$s_!kx6e!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52105575-cea2-4065-8e2d-c2ae18964a2a_1994x276.png)

本来工作流已经因为 a 重试耗尽而彻底失败，b 应该被锁住调用。结果 b 居然又活过来了，下一次 Worker 请求一伸手，它会恢复执行。

Claude Opus 4.7 的测试确实没测这个，为了图省事，它自己写的测试场景里永远只有一个步骤孤零零地超时。

（另外我们在代码审查时还揪出 Claude 的两处不严谨，比如拉取任务的列表存在被挤占的风险，SSE 推送在处理未知游标时有点大意，但都没到逻辑崩坏的程度。）

## Kimi K2.6 的 6 个痛点

相比之下，Kimi K2.6 踩到的坑就结结实实扎在命门上了。

**1. 抢任务不顾全局优先级**
规范明确要求：多个任务一起排队时，先看 `priority`（优先级降序），再看 `availableAt`（可用时间升序），跨越所有的工作流进行全局统筹。

但 Kimi K2.6 怎么写的？它只在一个工作流内部排序，然后完全听任数据库查询返回的先后，轮着处理每个工作流。

![](https://substackcdn.com/image/fetch/$s_!qSqZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F969de824-79bf-47e6-9b12-64e756b69c02_1994x1082.png)

我们用两个独立的工作流复现：一个里面留了个优先级 10 的任务，另一个里面留了个优先级 100 的任务。一发送 `/workers/claim`，系统先把那个优先级 10 的任务扔了过来。

**2. 说好的实时数据流，变成了播放录像**
规范要求访问 SSE 事件流接口时，先重播数据库里以往的事件，然后切成保持连接的长连接，推送新产生的也就是 live 的事件。

Kimi K2.6 代码是这么写的：一次性从表里查出旧数据，塞进流里，接着就原地开启一个定时器在那发 keepalive 心跳。没有任何机制去监听后续的事件。它甚至顺手写了一套 `emitAndBroadcast` 的发布订阅工具，但是！路由层压根儿没有去调用。

![](https://substackcdn.com/image/fetch/$s_!G7L1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0c7d956-6690-4f15-b98a-7c586f81efe5_1994x813.png)

客户端看着静悄悄的连接，以为天下太平。更有意思的是，它自己在 README 里大大方方标榜：“支持事件实时流推送”。

**3. 即使已经过期还会当成正常项目结算**
心跳维持接口知道拒绝已经被判定过期的流程，但是 `complete` 和 `fail` 接口没有做校验。

我们把一个任务的 `leaseExpiresAt` 刻意改到了好几天前，再向完成接口发起请求，它直接返回了 `succeeded`。

![](https://substackcdn.com/image/fetch/$s_!Fr-U!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F761cb687-e134-49dc-95c3-10ad448b6690_1994x115.png)

在工作流引擎的语境里，超时等同于出错，本该被收回去重新分发，结果 Kimi K2.6 让一个已经死去的 Worker 把任务又“复活”并通关了。

**4. 找不到版本时，给的 HTTP 码不对**
规范中的声明：如果没有可激活的版本也没有上传指定 `version`，返回 `409`。Kimi K2.6 手一滑，扔了个 `404 (NOT_FOUND)` 出来。

![](https://substackcdn.com/image/fetch/$s_!sIdy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feddd5455-d0e0-41f3-bc21-c466d9dbac36_1994x223.png)

**5. 数据校验太死板，框死了本来可以用得好好的 JSON**
规范本意是允许传递任何格式的 JSON payload（字符串、数字、数组都行）。但 Kimi K2.6 自己用的 Schema 把 `input` 和 `output` 死死限制成了 `z.record(z.any())`，导致合规的数组数据直接被服务器弹开。

**6. 直接执行 `npm run build` 会报错**
代码跑测试 `npm test` 没问题。但是当按照生产要求去跑 `npm run build`，编译就会因为某些隐式类型报错。

![](https://substackcdn.com/image/fetch/$s_!zw-b!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffcee959c-d406-4978-84b3-ea1df77cf582_1994x223.png)

此外，`package.json` 里配的 `npm start` 是直接去跑 `node dist/index.js`，这就导致在一个完全干净的新环境里拉下代码，照着文档走标准的“构建加启动”流竟然是断的。

## 模型是如何给自己的行为做结案陈词的

跑完最后一步后，两家模型都甩出了一份跑测总结，宣称自己彻底完成了代码实现，并且所有测试绿灯通过。从纯字面的技术角度看，这俩都没撒谎，但偏偏谁也没能察觉到上面那些深埋的隐患。

Claude Opus 4.7 的总结大体上十分靠谱。它准确地描述了自己设计的恢复路径、原子抢占模式以及事件的落库机制。唯一漏算的一点，就是多租约同时过期时的交互 bug。

![](https://substackcdn.com/image/fetch/$s_!XtV5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61573fdc-7a07-4b69-a032-2d13a83af77d_1928x2664.png)

Kimi K2.6 的总结报告里，信誓旦旦地说自己整出了确定性的全局调度和实时的 SSE 数据流。这两条大话甚至被它一本正经地写进了 README 里面。但扒开源码一看，压根儿没交付这俩功能。

“测试全都跑通了”和“代码写对了”完全是两码事。这两个模型确实对规范吃得很透，也顺顺利利把绝大部分的工程给搭了出来，但在写测试用例时，谁也没写出能把自身最致命的逻辑缺陷给揪出来的刁钻测试。

![](https://substackcdn.com/image/fetch/$s_!yJJ0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50a961ff-359e-447e-9896-0fd38db22966_1928x2672.png)

## 打个分：Claude 91 分，Kimi 68 分

![](https://substackcdn.com/image/fetch/$s_!QItW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8401fa44-af87-47e1-a9b9-c68f9e769c57_1504x854.png)

Claude Opus 4.7 折损在恢复机制的 bug、搜索列表被截断，和 SSE 抛出游标错误的处理上。
Kimi K2.6 踩的全是雷区：跨流程调度、超时任务的处理判定和实时流。
最终定格，Claude Opus 4.7 拿到 91 分。Kimi K2.6 仅仅拿到 68 分。

## 聊聊钱和现状

![](https://substackcdn.com/image/fetch/$s_!P7SD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89be5073-989b-47ed-9398-62efea3ebc75_1038x300.png)

平摊下来，Kimi K2.6 每拿一分的成本差不多只有 Claude 的四分之一。它丢掉的那 23 分，全栽在了租约管理、跨流程调度和事件流推送上，而这恰恰是整个规范里最难啃的硬骨头。也正是这点差距，决定了一个系统到底是仅仅“接口能调通”，还是“在高负载下依然稳定自如”。

## 开源模型现在到底是个什么身位

这次测试，其实印证了我们一直观察到的一个趋势。在此之前的三段式基准测试中，MiniMax M2.7 的检出率和 Claude Opus 4.6 打平。在任务队列规范测试上，GLM-5.1 也就比 Claude Opus 4.6 落后了 5 分。虽然这次 Kimi K2.6 在更难的测试上差了 23 分，但第一遍跑下来，系统整体骨架是对的。

过去这一年，大家都学聪明了，在“完成基本业务代码”上，开源和闭源的差距已经越来越小。真正的硬核差距，死卡在那些刁钻的代码路径上（比如租约恢复、跨流程调度、流式语义）。对于要在高并发争抢、宕机恢复中见真功的活儿，目前闭源的前沿大模型依然是更稳妥的选择。但如果你只是要个基础脚手架、几张表结构定义、几个接口和一套初始的测试用例，像 Kimi K2.6 这样的开源模型已经做得够好，这时候差距显式的性价比就相当诱人了。

Kimi K2.6 现在 $0.95 / $4 (百万 token) 的定价，只是个起步价，不是底价。月之暗面把权重开源，就意味着必定有大把云厂商抢着提供托管服务，最后价格和延迟肯定会卷到一个极低的状态。其实 MiniMax M2.5 就已经上演过这出戏了——发布没几个月，它就成了 Kilo Code 各个模式里使用量霸榜的头牌。只要加入混战的托管商越来越多，价格战只会越打越凶。

开源权重的另一大爽点是：如果你有数据合规要求、定制化工作流，或者就是单纯用量太大导致接 API 太烧钱，你完全可以拿 Kimi K2.6 自己去跑服务和做微调。花再多钱也买不来 Claude Opus 4.7 给你这个待遇。

这些优势当然没法抹平在上面的技术缺陷，但确实给了我们看问题的新视角。掏 $0.67，换一套初具规模的代码加上你自己的人手 code review，Kimi K2.6 现在绝对是一张能打的牌。掏 $3.56，图个少修点 bug、用着踏实，Claude Opus 4.7 依然是更稳当的选择。选哪条路，全看手头的活儿怎么算账。要知道在一年之前，面对这种复杂度的需求，我们甚至根本没得选。

## 结论

**用来搭复杂后端的脚手架：** Kimi K2.6 干得相当漂亮。大体骨架、库表结构、路由接口全是对的，测试用例也都跑得通。如果是要探探设计思路、快速搭个业务原型测试，或是干脆想要个起手式留着自己仔细 review，这 $0.67 花得绝对超值。

**用来做极其考验状态机的核心系统：** Claude Opus 4.7 明显领先了一个身位。两套代码乍一看长得差不多，但一卷到那些平时很难随手测到的深水区（租约过期、跨批次调度、SSE 流、拒绝过期租约），差距立马就出来了。要是你的项目在租约到期、多个任务疯抢 Worker 时绝不能掉链子，或者必须得给客户端起准实时的事件流，Claude Opus 4.7 给的产物离“直接上线”的门槛要近得多。

**别轻信模型自己的汇报：** 两个模型跑完都没心没肺地报喜说完工了。其中一个大体是对的，另一个却在交出的代码里埋了 6 个无视规范的硬伤。在这种容不得一丁点逻辑错误的活儿里，“测试全绿”只是个入场券，远远不是护身符。只有踏踏实实走一遍 code review，再单拎几个极限场景针对性地跑一跑复现，我们才看清它们“嘴里报的”和“实际写的”到底差多远。
