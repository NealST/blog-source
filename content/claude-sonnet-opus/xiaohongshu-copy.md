# 小红书发布文案

标题：Sonnet半价却更贵｜Claude选型

Sonnet 5.5 的输入输出单价只有 Opus 5.5 的一半，但把思考档位拉到 Max，单任务总成本反而可能贵一倍多。

问题不在标价，而在隐藏的推理 Token。Sonnet 5.5 在高强度思考下平均输出约 19.3 万 Token，比 Opus 5.5 多近 60%。

日常开发可以从 Sonnet 5.5 起步，用自动化检查把关；任务失败后升级到 Medium 档 Opus，而不是继续硬拉 Sonnet。复杂架构、跨仓库重构和高代价排错，则直接交给 Opus。

完整跑分、接口变化和模型分工见公众号「墨筝」。

.
#AI #Claude #Sonnet #Opus #模型选型 #AI编程 #ClaudeCode #Token成本 #开发者 #人工智能
