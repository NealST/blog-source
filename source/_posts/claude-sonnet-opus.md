---
title: Claude Sonnet 5.5 对比 Opus 5.5 与 Sonnet 5
date: 2026-10-13 10:00:00
tags:
  - AI
  - Claude
  - 模型选型
  - LLM
  - AI工程
---

前不久，Anthropic 发布了 Claude Opus 5.5。因为它省 Token、指令遵循能力也很强，很多开发者拿它来写复杂代码和大型项目，评价甚高，甚至有人感叹那个熟悉的 Claude 又回来了。

之后 Anthropic 紧接着推出了 Claude Sonnet 5.5。

官方在发布公告里称：“单价与前代 Sonnet 5 相同，但单任务成本最高降低 30%，输出速度提升 30% 以上，是迄今最快的 Sonnet 模型。”

不过我们在实际接入后发现了一个反常现象：在特定场景（尤其是高强度思考）下，单价更便宜的 Sonnet 5.5，最终跑完一个任务的开销，反而比顶级旗舰 Opus 5.5 还要贵。

为什么单价便宜，做起事来反而可能更贵？两代 Sonnet 到底迭代了什么，与顶级旗舰 Opus 相比该如何抉择？

---

## 先看结论：核心规格与价格

Claude Sonnet 5.5 定位是中端主力，主打速度快、单价便宜；Claude Opus 5.5 则是顶级旗舰，适合处理那些逻辑复杂、步骤多的大任务。

Sonnet 5.5 与 Opus 5.5 的基础标称定价如下：
- **Sonnet 5.5**：输入每百万 Token 2 美元，输出每百万 Token 10 美元（与前代 Sonnet 5 定价完全一致）；
- **Opus 5.5**：输入每百万 Token 4 美元，输出每百万 Token 20 美元；
- **Prompt 缓存读取（Cache Read）**：Sonnet 5.5 与 Opus 5.5 完全相同，都是每百万 Token 0.20 美元；
- **Batch API 批处理**：Sonnet 5.5 与 Opus 5.5 均支持 50% 的价格折扣。

以下是两代 Sonnet 以及与 Opus 系列的核心参数对照：

![](https://miro.medium.com/v2/resize:fit:1400/1*vKYtuezFbh7eCFcgu2ba2Q.png)
*Sonnet 5.5 与 Sonnet 5 核心参数对比*

![](https://miro.medium.com/v2/resize:fit:1400/1*O3evv1fTRxQ-4B95a213-A.png)
*Sonnet 5.5、Sonnet 5、Opus 5.5 与 Opus 5 规格横向对比*

![](https://miro.medium.com/v2/resize:fit:1400/1*87YZH6oSYCcgPzK2wfjrPQ.png)
*Sonnet 5.5 与 Opus 5.5 选型核心差异*

![](https://miro.medium.com/v2/resize:fit:1400/1*qGQaFqrQB1sqa0YDNyqlhQ.png)
*Sonnet 5.5 与 Opus 5.5 的定价与关键配置细节*

### 为什么标价没变，官方却说更便宜了？

既然输入输出的单价还是 2 美元和 10 美元，官方说的“最高省 30%”是从哪来的？

这并不是因为换了分词器。迁移文档写得很清楚，Sonnet 5.5 沿用了 Sonnet 5 的分词器，相同的文字切出来的 Token 数量一模一样。**它之所以能省钱，是因为模型表达更精炼，完成同一项任务所需要的输出字数变少了**。

此外，Prompt 缓存的最小起步门槛从过去的 1024 Token 降低到了 512 Token。这意味着更短的 System Prompt 现在也能享受到 90% 的缓存读取优惠，这对日常频繁调用的项目是个实打实的好处。

在基础规格上，Sonnet 5.5 与旗舰 Opus 5.5 保持了一致（相比前代 Sonnet 5 的 200K 上下文有了大幅提升）：
- **上下文窗口**：Sonnet 5.5 与 Opus 5.5 均为 100 万（1M）Token（前代 Sonnet 5 为 200K）；
- **单次最大输出**：Sonnet 5.5 与 Opus 5.5 均为 128K Token（Batch API 测试版支持到 300K）；
- **知识库截止时间**：均为 2026 年 6 月。

不过，Sonnet 5.5 与 Opus 5.5 在默认思考强度（Effort）的设定上正好相反：
- **Sonnet 5.5**：在 Claude Code 和 Claude.ai 网页端默认是 Medium（中度），但在直接调用 API 时默认是 High（高）；
- **Opus 5.5**：默认则是 Medium。

也就是说，如果你不做任何调整直接用默认配置拿 Sonnet 5.5 和 Opus 5.5 跑对比，实际上是在拿“全力思考的 Sonnet”去打“克制思考的 Opus”。

---

## Sonnet 5.5 与 Opus 5.5 的跑分对比

Anthropic 官方给出的发布测试数据是最合理的起点。在官方公布的 8 项评测中，Opus 5.5 在 7 项上胜出，但领先幅度都很小，差距大多在 3.2 个百分点以内。而在终端交互评测 Terminal-Bench 4.0 上，Sonnet 5.5 跑出了 70.6%，超过了 Opus 5.5 的 66.4%；在测试实际办公场景的 GDPval-AA 评测中，Sonnet 5.5 拿到 1844 分，与 Opus 5.5 的 1846 分基本打平。

![](https://miro.medium.com/v2/resize:fit:1400/1*7mLrSYf42XNY1_xvuhko_A.png)
*Terminal Bench 评测得分背后的注脚*

不过，在看这些数字时，有几个细节需要客观看待：

1. **前代 Sonnet 5 的基准分偏低**  
   前代 Sonnet 5 在这项测试里的得分只有 10.3%。从 10% 提升到 70% 看上去非常震撼，但有一部分原因是旧模型对这一版测试格式的适配比较吃亏。
2. **Sonnet 5.5 与 Opus 5.5 的测试档位并不一致**  
   仔细看官方图表的附注就会发现：Sonnet 5.5 拿下的 70.6%，是在 Max（最高强度思考）下跑出来的，而 Opus 5.5 的 66.4% 是在 Xhigh（超高强度）下跑出来的。如果拉到完全相同的 Xhigh 档位，官方数据显示 Sonnet 5.5 只有 61.5%，依然低于 Opus 5.5 的 66.4%。更关键的是成本差异：Sonnet 5.5 在 Max 档位单次尝试需要花费 12.54 美元，而 Opus 5.5 在 Xhigh 档位只需 7.35 美元。
3. **独立第三方测试的结论并不一致**  
   独立评测机构 Artificial Analysis 在自己的环境下测试 Terminal-Bench，Sonnet 5.5 得到 64%，Opus 5.5 得到 60%，两者的差距远没有官方图表那么悬殊。而在 Vals 的测试集中，Sonnet 5.5 得分 53.03%，Opus 5.5 则是 61.62%，依然是 Opus 5.5 明显领先。

所以，**不能简单地说 Sonnet 5.5 整体上已经超越了 Opus 5.5**。在各家综合测试中，Opus 5.5 依然保持着微弱的优势；Sonnet 5.5 的核心价值在于，在很多日常评测中它能紧紧咬住旗舰的成绩，但单价只有 Opus 5.5 的一半，吐字速度也更快。

评测中还有两个值得留意的细节：
- 一是思考预算不是越多越好：比如在 FrontierCode 编程测试中，Sonnet 5.5 在 Xhigh 档位能拿到 52.1%，但强行提到 Max 档反而掉到了 46.2%（后面我们会细说原因）。
- 二是早期测试中的插曲：Artificial Analysis 在早期测试时遇到过结构化输出的 Bug，官方表示正式版已修复，当时的数据可能稍微低估了 Sonnet 5.5 的真实表现。

---

## 单任务成本：半价并不总是靠谱

纸面计算下，一笔包含 10 万输入 Token 和 2 万输出 Token 的常规请求，Sonnet 5.5 约花费 0.40 美元，Opus 5.5 约花费 0.80 美元，刚好就是半价。

但一旦引入思考过程（Reasoning Tokens），就不一样了。

Artificial Analysis 在其智能指数（Intelligence Index）中评估了各模型跑完单项任务的实际花费：

![](https://miro.medium.com/v2/resize:fit:2000/1*_dzYCVRx9DKNnSXE3rLJbg.png)
*Artificial Analysis 智能指数综合得分*

Sonnet 5.5 拿下了 56 分，位列榜单第二，仅比 Opus 5.5 低 2 分，大幅超越了前代 Sonnet 5 的 38 分。

但细看单任务的实际花费：**在高强度思考下，Sonnet 5.5 单任务成本甚至明显超过了 Opus 5.5**。

![](https://miro.medium.com/v2/resize:fit:2000/1*9nPMN7xjb4e_qY5DRMmFqg.png)
*Artificial Analysis 智能指数单任务成本实测*

![](https://miro.medium.com/v2/resize:fit:1400/1*8HPKtefvK1aGIIbGq-8kKg.png)
*Sonnet 5.5、Sonnet 5、Opus 5.5 与 GPT-6 系列单任务消耗与定价*

![](https://miro.medium.com/v2/resize:fit:1400/1*HKL0-erp-O-PzGEESFUW5A.png)
*单任务成本必须按目标质量分数看，而不是按档位标签看*

### 为什么单价便宜一半，干活反而更贵？

答案在思考过程产生的 Token 总量上。

在 Max 思考档位下，Sonnet 5.5 平均每个任务输出了大约 19.3 万个 Token，其中有 14.2 万个都是隐藏的推理思考 Token。相比之下，Opus 5.5 平均只用了 11.9 万个，前代 Sonnet 5 也只有 11.8 万个。

这是该机构有测试记录以来的最高输出量：比 Opus 5.5 多了近 60%，更是 GPT-6 Astra 的 7 倍。

单价再便宜，只要 Token 消耗量膨胀数倍，总账单自然就会超纲。在 Max 档位下，Sonnet 5.5 单任务平均花费约为 7.60 美元，不仅明显高于 Opus 5.5（约 5.98 美元），也比前代 Sonnet 5 贵了 50% 左右。

如果我们按照“达成同样的分数”来算账：
- **目标 51~52 分**：Sonnet 5.5 得开到 Xhigh 档；而 Opus 5.5 只要开在 Medium 档就能拿到 51 分，单任务成本只要 1.34 美元。
- **目标 56 分的高质量**：Opus 5.5 在 Xhigh 档花费 3.46 美元；而 Sonnet 5.5 开到 Max 档要花 7.60 美元以上，直接贵了一倍多。

虽然 Vals 在其自测任务集上给出了相反的比例（Sonnet 5.5 $20.80 vs Opus 5.5 $32.77，因为在他们的任务结构中思考 Token 膨胀没那么剧烈），但逻辑是一致的：**Sonnet 5.5 并非在任何情况下都比 Opus 5.5 更省钱**。它的成本优势只存在于低思考和中等思考强度；一旦你把它拉到 Max 试图硬顶出旗舰质量，往往反而比直接调用 Opus 5.5 更贵。

---

## 思考档位：为什么别直接拉到最大？

官方技术文档里专门写了一句话：

![](https://miro.medium.com/v2/resize:fit:1400/1*Vol0djUq02j3ErM_ZqV1rg.png)

> “Sonnet 5.5 的思考档位与 Sonnet 5 并不对等。请重新测试确定档位，不要直接照搬旧设置。”

换句话说：**Sonnet 5.5 的 Medium，并不等于前代 Sonnet 5 的 Medium**。

Sonnet 5.5 在较低档位（如 Low 或 Medium）实际做出来的效果，就已经能赶上前代 Sonnet 5 在高档位的表现了。在 Low 档位下，整个测试仅耗费 2300 万 Token，得分也有 36 分。只有当你把档位往回调时，相比前代 Sonnet 5“节省 30%”的好处才能真正体现出来；如果你原样保留旧代码里的高档位甚至直接开到 Max，账单反而会上涨。

而且，**思考档位拉得过高不仅花钱多，还容易出现“想得太多”的副作用**：
- **Simon Willison 的绘图测试**：在 Max 档位下，Sonnet 5.5 消耗了 12.8 万 Token（约 1.28 美元），最后依然没画好“骑自行车的鹈鹕”；而在 Xhigh 档位下，只用了 41 秒、花费 6 美分就成功画出。
- **FrontierCode 编程测试**：Xhigh 档得分 52.1%，拉到 Max 反而掉到 46.2%，就是因为模型把太多精力浪费在拆分任务和子智能体调度上，反而容易把事情搞砸。

所以，日常使用建议从 Medium 或 High 开始尝试，不要盲目拉到 Max。

---

## 速度与延迟：吐字快不等于干活快

Anthropic 官方表示 Sonnet 5.5 的输出速度比前代 Sonnet 5 提升了 30% 以上。根据 Artificial Analysis 的实测，Sonnet 5.5 的吐字速度大约是每秒 85 至 139 个 Token，而 Opus 5.5 是每秒 74 至 93 个 Token。

但要分清一点：**吐字速度快，不代表任务能更快完成**。因为在高强度思考下，Sonnet 5.5 往往会产生多得多的思考文本，即便每秒流速更快，最终等它完整输出的总耗时也可能更长。

Sonnet 5.5 与 Opus 5.5 在实际使用体验上还有一个明显区别：
- **Opus 5.5**：思考机制是底层常驻的，无法手动关闭；
- **Sonnet 5.5**：允许关闭前置思考。如果你的产品是在线客服、即时聊天等看重首字弹出时间（TTFT）的工具，关闭前置思考的 Sonnet 5.5 能做到秒回。

---

## 接入接口要注意什么？几个容易踩坑的变化

如果你是在 API 上做开发的工程师，在从旧版 Sonnet 5 切换到 Sonnet 5.5 前，有几项改动需要特别留意，避免线上报错：

![](https://miro.medium.com/v2/resize:fit:1400/1*9gzqeDGhJUXFvfNPDjxTxw.png)

1. **不能直接关闭思考功能**  
   在 Sonnet 5.5 上，向接口传入 `thinking: {"type": "disabled"}` 会直接返回 400 报错。现在最低的选项是 `between_tools`，它只在会话最开始跳过前置思考。
2. **移除了强制工具调用（Forced Tool Use）**  
   Sonnet 5.5 不再支持把 `tool_choice` 指定为 `any` 或具体工具名，现在只接受 `auto` 或 `none`。如果之前你的代码依赖强制调用某工具来稳定吐出 JSON，需要做相应调整。
3. **工具间的进度文本可能拿不到**  
   两次工具调用之间较长的推理说明，现在会被归入思考块（Thinking Blocks）。而在默认设置下这些思考块对外是空白的。程序不会崩，但如果你的产品界面原本依赖这些中间文字做进度提示，看起来会像是卡住了一样。
4. **思考过程不能跨模型流转，长任务别中途换模型**  
   如果想在同一轮会话里把 Sonnet 5.5 换成 Opus 5.5，虽然接口不会报错，但前一个模型的思考块会被直接丢弃。新模型看不到之前的推理脉络，只能按对话表面重新接话。Opus 5.5 看不懂 Sonnet 5.5 的思考块，Sonnet 5.5 也看不懂 Opus 5.5 的。因此对于连续的大任务，最好自始至终固定使用同一个模型。
5. **思考块严格绑定账号（防蒸馏保护）**  
   思考块只能在生成它的同一个账号内有效，而且只要修改了上文消息就无法复用。Sonnet 5.5 专门增加了分类器，用来拦截抓取思考过程训练其他模型的行为，还新增了 `frontier_llm` 状态码，直接拒绝可能辅助训练竞品模型的请求。
6. **网络安全审查会自动降级回退**  
   如果请求被判定具有高危安全漏洞利用风险，Sonnet 5.5 会自动回退到旧版 Sonnet 5 处理，Opus 5.5 则会回退到 Opus 4.8。普通的 Bug 修复不受影响，但在安全相关业务上要留意这一机制。
7. **对事实严谨度要求高的场景要多留心**  
   在 Artificial Analysis 的全知评测（Omniscience）中，Opus 5.5 的事实准确率为 66%，Sonnet 5.5 则是 54%。虽然 Sonnet 5.5 的幻觉率测出来是 47%（低于 Opus 5.5 的 59%），但如果是严谨的事实问答或严肃业务，对 Sonnet 5.5 的输出依然建议加上二次核对。
8. **轻量级 Haiku 5.5 即将推出**  
   如果是超大规模、低成本敏感的任务，可以稍等几周，更轻巧的 Haiku 5.5 即将推出。

---

## 怎么选：三款模型各自适合什么场景？

![](https://miro.medium.com/v2/resize:fit:1400/1*VNVwnWf_gdOmYlSRJrf8rQ.jpeg)
*面对长程复杂任务，旗舰模型的持续推断力依然最稳*

![](https://miro.medium.com/v2/resize:fit:1400/1*DLccAPNc1EtatPaS1nJS5Q.jpeg)
*在中等范围工程与创意落地中，Sonnet 5.5 展现出极高的性价比*

### 什么时候该从 Sonnet 5 升级到 Sonnet 5.5？

对于现有的 Sonnet 5 用户来说，只要注意调准思考档位，可以直接升级到 Sonnet 5.5：
- 单价完全一致，但上下文窗口从 200K 跃升到了 1M；
- 输出速度提升了 30% 以上；
- 在完成同一任务时表达更加精炼，往往能少用 20%~30% 的 Token；
- Anthropic 还把 Sonnet 5.5 设为了免费网页端的新默认模型。对于绝大多数中小型项目和日常任务，Sonnet 5.5 完全可以平替前代 Sonnet 5。

### 什么时候应该直接用 Opus 5.5？

Anthropic 官方的态度很直接：面对目标开放、高度依赖持续推导和连贯判断的复杂任务，Opus 5.5 的优势依然无法替代。

官方公布的两个案例很典型：
- 一个测试团队让它在不到 3 小时内，对一个 20 万行代码的大型项目做完了全量审计和修 Bug；
- 另一个团队让它在完全无人的情况下，跨 6 个核心代码仓库连续自主跑了 18 个多小时。

**如果你要进行系统底层架构设计、多文件联动的全局大重构、或者追查非常隐蔽的复杂链路 Bug，Opus 5.5 是最安全稳健的选择**。在这些场景里，做错一次的修复成本，远比省下的 Token 贵得多。

### 什么时候选 Sonnet 5.5 代替 Opus 5.5？

Claude Code 的创造者 Boris Cherny 曾对比过两代 Sonnet 修复同一个 Bug 的表现，Sonnet 5.5 在精准度和响应速度上都有显著进步。

除了日常的代码修改与功能开发，Sonnet 5.5 在做动效设计、SVG 绘图和前端界面布局时，上手体验也相当不错：
- 开发者 Kevin Ngo 分享过他用 Sonnet 5.5 制作 JavaScript 动效的经历，平均只要 3 到 4 次迭代就能做出高质量成果。
- 他的用法很值得参考：**“让 Opus 5.5 负责规划架构并制定创意方向，再交由 Sonnet 5.5 负责具体的编码与落地实现。”** 这个组合既利用了 Opus 5.5 的宏观判断力，又享受了 Sonnet 5.5 便宜一半的执行成本，效果非常理想。
- 此外，CodeRabbit 计划将常规代码审查转移至 Sonnet 5.5；Base44 报告构建应用的原型迭代次数相比 Opus 5 减少了近一半；Unity 则在编辑器评测中取得了 90% 的高任务完成率。

**综合写代码的选型建议很清晰**：对于边界清晰的日常开发、单文件修改、测试用例补全和常规 Bug 修复，Sonnet 5.5 的质量非常接近旗舰，且单价只有 Opus 5.5 的一半，是绝对的首选；而对于宏观架构设计、底层大版本迁移和棘手的排错，交给 Opus 5.5 更稳妥。

---

## 顺便聊聊：便宜的国产与开源模型怎么看？

在讨论 Sonnet 5.5 定价时，Hacker News 上也有不少人提出：现在 DeepSeek V4 Flash、GLM-5.3 这类模型价格极低，Sonnet 5.5 的性价比真的有那么高吗？

![](https://miro.medium.com/v2/resize:fit:1400/1*08966PBWn7Jjpbszx6PIww.png)
*社区用户关于高性价比模型的讨论*

![](https://miro.medium.com/v2/resize:fit:1400/1*4Gr0DvJHYftGE6pQdpRM8Q.png)
*关于开源/区域模型与顶级闭源模型定位的探讨*

确实，在中等难度的日常需求里，很多国产和开源模型已经足够好用，价格也更低。但工程选型必须算总账。

比如 TokenCost 实测过 GLM-5.3 的账单，发现它在某些任务里吐出的 Token 数量是同类模型平均值的 2.4 倍。虽然每百万 Token 标价极低，但写出来的字数一多，最终账单同样会被拉高，这和 Sonnet 5.5 在高思考强度下的道理是一样的。

---

## 推荐的日常分工策略

结合 Sonnet 5.5 与 Opus 5.5 的真实特性，推荐在日常项目中采用一套简单的 5 步分工策略：

1. **默认用 Sonnet 5.5 起步**：常规日常任务默认接入 Sonnet 5.5（平替前代 Sonnet 5）。针对需求明确的 Agent 工具调用设为 Medium 档位，一般编码任务设为 High 档位。
2. **设立自动化检查门禁**：通过单元测试、Schema 校验或自动打分工具把关，一旦结果不符合预期就自动拦截。
3. **梯次升级，不要盲目拉满**：当任务初次失败时，直接将问题升级给处于 Medium 档位的 Opus 5.5，而不是盲目把 Sonnet 5.5 强行开到 Max 档死磕。
4. **复杂核心任务一开始就上 Opus 5.5**：对于目标模糊、涉及跨多个代码库、或者一旦做错代价很大的核心任务，不要走前置试探，从一开始就直连 Opus 5.5。
5. **拿自己的真实数据说话**：持续跟踪任务成功率、单任务消耗的 Token、工具调用频次以及人工修复所花的时间。

别人的评测数据只是参考，只有自己项目里的真实监控，才能给出最准确的答案。


