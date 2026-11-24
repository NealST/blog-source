# 原文插图审核清单

所有原图均保存在 `source-images/`，处理结果保存在 `localized-images/`。处理动作均为 `localize`：原图信息结构清晰，只翻译影响理解的自然语言，并做克制的墨筝配色适配；公式、变量、产品名、数值和单位保持原样。

| # | 正文用途 | 主要中文化内容 | 输出 | 验收 |
|---|---|---|---|---|
| 01 | 预训练与指令微调 | 流程标题、节点、样例问答 | `01-pretraining-instruction.png` | 通过 |
| 02 | 预训练模型的四项局限 | 标题、四项问题及说明 | `02-pretrained-limitations.png` | 通过 |
| 03 | 微调目标 | 行为改变、知识补充、两者兼有 | `03-finetuning-impact.png` | 通过 |
| 04 | 全量微调的存储成本 | 场景说明、服务器 | `04-full-finetuning-cost.png` | 通过 |
| 05 | 原权重加更新量 | 权重名称；公式与矩阵维度保留 | `05-lora-update.png` | 通过 |
| 06 | 低秩矩阵分解 | 权重名称、Rank；公式与维度保留 | `06-low-rank-matrices.png` | 通过 |
| 07 | 共享基座与多适配器 | 适配器、任务和权重名称 | `07-shared-base-adapters.png` | 通过 |
| 08 | LoRA 工程收益 | 服务器、精度、维护、成本、延迟 | `08-deployment-benefits.png` | 通过 |
| 09 | QLoRA 第一步 | 压缩冻结权重、量化说明 | `09-compress-weights.png` | 通过 |
| 10 | QLoRA 第二步 | 存储、计算、反量化、显存公式说明 | `10-store-small-compute-big.png` | 通过 |
| 11 | LoRA 与 QLoRA 显存对比 | 标题、硬件要求、质量说明 | `11-lora-vs-qlora.png` | 通过 |
| 12 | 权重大小与方向 | 标题、两项属性和图下注释 | `12-magnitude-direction.png` | 通过 |
| 13 | 全量微调与 LoRA 转向对比 | 两行流程及结果说明 | `13-full-vs-lora-direction.png` | 修正残留英文后通过 |
| 14 | LoRA 耦合与 DoRA 解耦 | 标题、问题、解法和向量说明 | `14-lora-dora-coupling.png` | 通过 |
| 15 | DoRA 完整流程 | 分解、方向适配、归一化、重组 | `15-dora-pipeline.png` | 通过 |

验收项：译文完整；数字、单位、公式和品牌名无变化；节点数量和箭头关系保持；中文可读；无意外裁切或拉伸；无新增事实、Logo 或水印。
