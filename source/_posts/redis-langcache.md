---
title: LangCache 帮你节省 90% 的模型调用成本和延迟耗时
date: 2026-09-12 17:00:00
tags:
  - AI
  - tooling
---

对于大模型应用来说，每次收到的问题可能都不是全新的。

比如，一个客服助手可能会收到下面三个问题：

* “购买月度套餐后可以退款吗？”
* “月度订阅支持退款吗？”
* “我可以取消套餐并拿回已支付的费用吗？”

尽管表述略有不同，但实际问的是同一件事，答案也一样。

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBqipqpQmd6MXVuFs-nBhdJLkwlXJk8AAClQxrG2hYKUV_0hW7LEFiBAEAAwIAA3cAAz0E.png)

对于大模型应用来说通常会把每种问法都当作新的请求，重新组织提示词，再把请求发送给底层模型，最后再生成一篇已经回答过的答案。

前缀缓存可以减少一部分重复计算。

当多个请求使用相同的系统提示词或上下文作为开头时，模型会复用这部分公共前缀已经计算好的 KV 状态。

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBqitqpQnODWUp_KNKxudvgwiku8RUewAClgxrG2hYKUV98W1uakrjJgEAAwIAA3cAAz0E.png)

但模型还是要处理新增的 Token，并解码生成完整答案。

因此，即便命中了前缀缓存，模型仍然要执行一次生成调用。

要进一步减少这类调用，应用层可以额外做一份答案缓存。

当新问题到来时，先使用 embedding 模型将其转换为向量，并与之前回答过的问题进行比较。如果找到相似度匹配的向量结果，就直接返回缓存中的回答，不再调用底层大模型。

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBqixqpQnrB5vcDHNQTSSh0cePbrVprwAClwxrG2hYKUWDRPMBs8evnAEAAwIAA3cAAz0E.png)

一旦命中缓存，这次大语言模型调用所需的输入 Token、输出 Token 和解码时间就都可以省掉。

理论很简单，但在实际落地时，会有很多细节需要考虑，比如 embedding 实现，相似度匹配策略和阈值、过期策略和数据隔离，失败的退避策略，错误匹配的监控等等。

Redis 推出了对应的托管服务 Redis LangCache，可以让你直接在应用中开箱即用。

它会在内部生成向量、搜索以往的回答，并在再次调用模型之前返回匹配的答案。

Redis 还提供了访问范围控制、自定义过滤、TTL、淘汰策略和缓存监控等功能。

我简单测试了一下，对比 Redis LangCache 与直接调用大语言模型的效果：

测试中，面对一个换了表达方式的问题，直接调用模型耗时 2.232 秒，使用了 514 个输入 Token 和 250 个输出 Token。

Redis 在 0.373 秒内返回了之前的回答，没有消耗任何大语言模型的输入或输出 Token。在这次测试中，响应速度约为直接调用模型的 6 倍。

Redis 官方称，LangCache 最多可以节省 90% 的 API 成本，缓存命中时的响应速度最高可提升至 15 倍。

实际效果还是取决于业务请求中有多少内容可以安全复用。

Redis LangCache 上手体验：https://redis.io/langcache/