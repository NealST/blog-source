---
title: 10 个前端任务实测 Qwen3.8-Max VS Claude Fable 5
date: 2026-08-22 13:00:00
tags:
  - AI
  - Claude
  - Token
  - Qwen
categories:
  - AI
---

**TL;DR**：在全部十项测试任务中，Qwen3.8-Max 的表现与 Claude Fable 5 难分伯仲（我们的统计结果为：Fable 胜出 4 项，Qwen 胜出 3 项，平局 3 项）。而且，Qwen3.8-Max 展现出了自己的视觉审美。在成本方面，运行完整的十项任务，Qwen3.8-Max 耗费 3.05 美元，而 Fable 5 花费了 8.44 美元。

长期以来，“设计工作该用哪个模型？”的答案始终是 Anthropic 的 Claude 系列模型。无论是控制台、落地页、演示文稿、推介页面，还是任何需要向人类展示内容的界面，开发者都倾向于Claude。然而，Claude 属于闭源模型，且 Fable 5 是目前排名前五的模型中成本最高的一款。

OpenAI 的模型在前端领域一直处于追赶状态，尽管经历了从 GPT-5.4、5.5 到 5.6 Sol 的逐步迭代，但始终未能缩小差距。在我们的测试中，Kimi K3 是首个在表现上比肩 Fable 5 的开源模型，且完成十项测试任务的成本仅为 Fable 5 的 29%。

阿里于 8 月 2 日发布了 Qwen3.8-Max，该模型在 Arena.ai 的前端代码排行榜上首次入榜便位列第四，排名甚至比 Claude Fable 5 高出一位，而 Qwen3.8-Max 的单位 Token 成本甚至低于 Kimi K3。

![](https://substackcdn.com/image/fetch/$s_!sIGP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7893889f-28aa-4a06-977c-dcba5f8070a8_4075x4075.jpeg)

为了验证排名，我们给这两个模型输入了十个相同的 UI 设计提示词，并对它们的输出结果、运行成本以及各自的工作方式进行了对比。

## 定价

![](https://substackcdn.com/image/fetch/$s_!Y-23!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d190e8a-9950-46e8-8523-b44cd64e8e12_1566x362.png)

Fable 5 的输入 Token 价格为 Qwen3.8-Max 的 5 倍，输出 Token 价格为其 8.3 倍。此处引入 Kimi K3 作为参考，目前这三款模型在前端排行榜的头部交替领先。

## 测试设定

两个模型的任务均在一个独立且无共享状态的空目录中启动，且接收完全相同的提示词。我们不做任何多轮对话迭代，文中每一张截图均为单次生成的直接结果。

我们将 Qwen3.8-Max 的推理级别设定为“极大（xhigh）”，Fable 5 的推理级别设定为“高（high）”。考虑到不同厂商间的推理标签不具备直接可比性，我们选择了 Qwen 的最高级别，并依据实际使用量计算成本。

提示词采用“视觉基调 + 基本内容”的约定格式。我们限定了产品名称并列出必要的内容元素，将所有的视觉决策权交予模型。每个模型均生成一个通过 CDN 引入 Tailwind 的独立 `index.html` 文件。

其中九项任务均依此方式运行，唯一的例外是“设置页面”任务：我们向模型提供了一份简明的深色品牌规范（三种十六进制颜色代码、一组字体搭配、无渐变色、无纯黑纯白、圆角半径最大为 8 像素），旨在测试模型执行具体指令的能力，而非单纯的自由发挥。

ps：文中的胜负判定仅代表个人主观偏好。在大多数任务中，两者的输出质量在伯仲之间，最终选择很大程度上取决于个人审美。

## 任务 1（Qwen 更好）：实体产品落地页

我们要求模型为“Murmur”设计一个落地页，这是一款售价 349 美元的直销高端头戴式耳机。

![](https://substackcdn.com/image/fetch/$s_!Gc9v!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dcf0a3b-1eb3-43af-9f96-737159fb6f59_6240x2480.png)

两个模型均使用 SVG 绘制了耳机插图，并在其周围加入了指示发声单元、电池和 USB-C 的悬浮规格标签。Qwen 的插图细节更为丰富，它不仅标注了左右耳罩，为悬浮标签添加了毛玻璃特效，还绘制了从耳机向外辐射的声波。此外，Qwen 还为该品牌设计了一个声波图风格的 Logo，而 Fable 仅在圆圈内放了一个字母 M。Qwen 在排版上也更为用心，主标题的换行处理得当，第二行文字采用金色点缀，使首屏主视觉区更具可读性。在单次生成的限制下，Qwen 的结果呈现出更强的高级感。

![](https://substackcdn.com/image/fetch/$s_!s32x!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8b3c4ca-bfe3-400d-a926-13a3cf36413e_1864x502.png)

## 任务 2（Fable 更好）：电商产品详情页

Talus 是一家户外装备店，此页面用于销售一款名为 Crag 32L 的技术型背包。

![](https://substackcdn.com/image/fetch/$s_!xj0M!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62a3a4f7-7afe-4fe9-9316-5d1d72cdb04d_6240x2480.png)

两者在布局上高度一致，均将带有缩略图选择器的图片库置于左侧，购买详情置于右侧。Qwen 在“加入购物车”按钮旁添加了数量增减控件，而 Fable 则没有。Fable 提供的颜色和尺寸选择器完成度更高，商品描述也蕴含了更多实用的购买信息，包括免邮说明、库存状况以及绳索绑带等产品细节。Fable 采用了米色背景，并将导航链接居中；Qwen 则保留了白色背景，同时将 Logo 靠左对齐、账户控制控件靠右对齐。由于提示词中图片服务商的特性，两者的图片库都加载了通用的占位图片，因此均未能实际展示出背包的样貌。

![](https://substackcdn.com/image/fetch/$s_!Zey6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6eed248b-ed39-4e43-bd38-3b95d47ba889_1864x502.png)

## 任务 3（Qwen 更好）：邮件客户端收件箱

Postline 是一款邮件客户端，提示词要求实现完整的三栏式收件箱布局：文件夹栏、邮件列表栏以及阅读窗格。

![](https://substackcdn.com/image/fetch/$s_!GOvu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd45e8fa3-b870-46fc-9eb9-3f26b9c164ae_6240x2480.png)

两者的局部设计高度相似，主要差异存在于细节。Qwen 的收件箱视觉更为极简，留白间距更合理，邮件列表的信息层级也更清晰。其操作工具栏仅采用等距分布的图标，而 Fable 则为每项操作附加了文本标签。另外，Fable 的“撰写”按钮缺失了水平方向的内边距。不过，Fable 在阅读窗格的功能排布上更胜一筹。它折叠了历史邮件，展开了当前阅读的邮件，并将附件与回复编辑框整合在同一首屏可视区域内；相比之下，Qwen 较高的邮件卡片直接将回复编辑框推至了屏幕可见范围之外。

![](https://substackcdn.com/image/fetch/$s_!66b5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97a17eac-1fc9-4b41-8a09-f7e319eac937_1864x500.png)

## 任务 4（平局）：CRM 数据表格

Cairn 是一款 CRM 系统，要求实现一个包含 12 行联系人数据的表格，并具备筛选、排序、选中行以及批量操作工具栏等功能。

![](https://substackcdn.com/image/fetch/$s_!aiWG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F126723a7-35f3-4562-86e8-3ea0165fabe4_6240x2480.png)

两个模型都选择了绿色作为点缀色（尽管是不同的绿色），并且均将批量操作工具栏以悬浮形式置于表格之上，这是本次测试中最令人惊艳的一致决策。Qwen 侧边栏较宽，每个图标旁均配有文字标签。Fable 则仅采用纯图标侧边栏，从而为表格提供了更多的横向空间。然而，两者的输出都存在数据逻辑上的小纰漏：Qwen 在“交易金额”列上标识了降序排序图标，但其生成的行数据并非按此顺序排列；Fable 显示了一个激活的过滤器，本应排除的交易状态，却依然出现在了表格中。

![](https://substackcdn.com/image/fetch/$s_!5rYS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F184d7ff0-d21b-4ce9-a6c7-3e062859631e_1864x500.png)

## 任务 5（Qwen 更好）：个人财务控制台

Alder 是一款个人财务应用，提示词要求包含账户余额、支出图表、支出类别分析、交易记录、账单和储蓄目标等元素。

![](https://substackcdn.com/image/fetch/$s_!np_n!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2537468-023b-4670-9f33-8e2da032b5f5_6240x2480.png)

两个模型都采用了卡片式的便当盒网格布局。Qwen 将账户余额、月度支出和月度收入统一放置在顶部的一个深绿色卡片中，使得最核心的数据集中于一处，并占据了页面中最抢眼的位置。在支出类别分析的设计上，两者的处理方式出现了分歧：Qwen 为每个类别单独绘制了水平条形图，用户只需扫一眼即可比较各项支出的占比；Fable 则构建了一个单根的堆叠柱状图，每段用不同颜色标识，用户在阅读时需要对照图例才能理解。综合来看，Qwen 在图表设计的表现更为出色。

![](https://substackcdn.com/image/fetch/$s_!KqvH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa98a93c4-177b-410e-b3a7-fb5efa91f550_1864x502.png)

## 任务 6（Fable 更好）：播客播放器

Earshot 是一款播客应用，要求生成包含播放列表和播放控制栏的正在播放界面。

![](https://substackcdn.com/image/fetch/$s_!3F0o!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86a361df-7618-437b-b1ef-bfd143eb0303_6240x2480.png)

两个模型均将播放器置于页面中心，播放队列置于右侧，而固定置顶的节目列表则放置在左侧侧边栏。两者的差异主要体现在控件的风格特征上。Fable 的播放器设计保持极简风格，节目名称使用了衬线字体，整体采用了暖暗色调。Qwen 的设计则更具趣味性，引入了声波图样式的进度条、彩色的暂停按钮，并在控件后方叠加了大面积的橙色光晕。虽然 Qwen 的声波进度条在视觉上很讨喜，但它看起来更像装饰，而非实用的拖拽进度条。此外，Fable 的播放队列还截断了若干长标题。

![](https://substackcdn.com/image/fetch/$s_!BJCf!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcbbe0d8e-b36f-4f71-aa6a-6ab2a804efb9_1864x502.png)

## 任务 7（Fable 更好）：智能家居控制台

Haven 是一款智能家居应用，要求生成包含场景模式、按房间分组的设备、调光滑块、恒温器以及一个离线设备的交互界面。

![](https://substackcdn.com/image/fetch/$s_!1Fnc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe01b3233-9850-46d9-9d0e-466ae51b8213_6240x2480.png)

两个模型都采用了相似的设备卡片网格布局，并配备了开关与滑块，同时都在页头展示了室内外温度。在页头信息的处理上，Fable 的设计更便于快速扫视，而 Qwen 则将温度数值包裹在胶囊状的标签中。Qwen 尝试使用悬浮标签栏作为底部导航，却导致其与部分卡片面板产生了遮挡重叠。此外，Qwen 的图标未能成功渲染——它引用的 Phosphor 图标库 URL 路径无法提供实际的图标字体文件，导致页面上所有图标的位置均显示为空白。相比之下，Fable 针对不同的设备类型定制了专属的控件交互：例如照明设备的色温调节选项、摄像头的录制状态标识，以及与页面级整体警告相呼应的离线扬声器提示。

![](https://substackcdn.com/image/fetch/$s_!gxJ7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcffe46a8-a6fb-460d-82aa-90e51475b088_1864x500.png)

## 任务 8（Fable 更好）：影院在线选座

Marquee 是一款影院票务应用。提示词要求生成一个座位图，包含五种明确的座位状态、状态图例以及订单明细。

![](https://substackcdn.com/image/fetch/$s_!WqJP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf6d4eb4-0e7b-4b44-834c-acfdfbdc5417_6240x2480.png)

两个模型生成的界面都非常接近真实的影院选座系统，屏幕标识位于顶部，座位阵列排布其下。在座位图的构建上，二者表现旗鼓相当，均妥善处理了“可选”、“已售”、“已选”、“无障碍轮椅专属”以及“高级VIP”等状态。两者的差异主要体现在订单明细的处理方式上。Fable 将其集成在一个悬浮卡片中，使得界面紧凑且易于快速总览。Qwen 则采用了一个占据全高的侧边栏，并且其“继续”按钮上的文本发生了折行。此外，状态图例在位置排布上也有所不同，Fable 将图例固定在页面底部，而 Qwen 则将其直接安置于座位图的下方。

![](https://substackcdn.com/image/fetch/$s_!tl4f!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0f41abb-4606-4326-ae6c-2de978f8999f_1864x500.png)

## 任务 9（平局）：新手引导向导

Gantry 是一款项目管理工具，此任务要求生成其四步新手引导中的第二步：工作区设置表单。

![](https://substackcdn.com/image/fetch/$s_!PkJt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14dcbbed-19e8-44ca-a558-58bd76470a48_6240x2480.png)

两个页面呈现出镜像对称的构造。Qwen 将表单置于左侧，视觉展板放在右侧，而 Fable 恰好相反。两者的表单部分几乎一模一样，包含了相同的进度指示器（步骤 1 标记为已完成，步骤 2 为当前激活状态）、相同的表单字段以及相同的“继续”按钮。对于另一侧的视觉展板，两个模型分别创作了不同的产品图例：Fable 在 SVG 网格背景上绘制了路线图时间轴，而 Qwen 则绘制了看板视图的骨架图；同时两者均在面板内补充了用户评价。这一组对比图可谓涵盖了本次测试的整体特征：两个模型展现出相似的构思逻辑，却通过截然不同的视觉审美来付诸实现。

![](https://substackcdn.com/image/fetch/$s_!BCFW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2a8d4c8-0b53-41c5-bca5-32986eb4dacb_1864x502.png)

## 任务 10（平局）：设置页面

这是一项附带严格约束的任务。我们为两个模型提供了有关睡眠监测应用 Nocturne 的相同品牌规范：近黑色的背景（#0B0D10）、暖灰色的文本（#E8E6E0）、烛光般的琥珀色作为点缀（#D4A24E），标题统一使用 Source Serif 4 字体，正文使用 IBM Plex Sans 字体，要求不包含渐变色、不使用纯黑或纯白，且各元素的圆角半径上限需限制在 8 像素。

![](https://substackcdn.com/image/fetch/$s_!k8pY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3655bc43-aad7-4927-a113-3ee51699835a_6240x2480.png)

我们通过 HTML 代码检查了模型是否遵循每项可量化的规则。两者均使用了指定的三种颜色，从 Google Fonts 引入了指定的字体，完全避开了渐变色，且未采用纯黑纯白。分歧出现在圆角半径的限制上，Fable 严格遵循了 8 像素的阈值约束，这在其切换开关的设计中体现得尤为明显——为了不超过圆角上限，它的开关呈现为近似方形，而非通常的药丸状；反观 Qwen，它使用了完全圆角的切换开关，并且用户头像是毫无限制的纯圆形，双双打破了预设规则。

除了品牌规范之外，两个页面的骨架依然类似：左侧为板块导航，右侧为具体的设置内容。Fable 在其导航栏中加入了一条名为“高危操作区”的入口条目，而 Qwen 则未包含此项。此外，在数值自洽层面，Fable 设置的入睡时段（10:30 PM - 11:15 PM）与其标识的 7 小时 30 分钟的固定睡眠目标并不完全吻合。

![](https://substackcdn.com/image/fetch/$s_!kfI7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76949660-bc02-41d6-b670-c0cd6c5e4bbb_1864x502.png)

## 十项任务中的规律

骨架趋同，但审美存异。在多项任务中，两个模型做出了相同的布局选择：左图右文的电商产品页、悬浮的批量操作条、便当盒网格控制台，以及镜像对称的新手引导页。真正的区别在于覆盖在骨架之上的视觉表现。这两个模型在排版、组件形态和装饰元素上不断做出迥异的决策，而这一点在“新手引导向导”任务的对比中体现得最为直白。

Qwen 具有非常固定的色彩偏好特征。在十个页面中，有九个页面 Qwen 都选用了琥珀色、橙色或金色作为主色调，唯一的例外是 CRM 系统中的蓝绿色。Fable 则会根据每次提示词的语境灵活调整其调色板：户外装备店呈现森林绿与焦橙色，CRM 选用橄榄绿，播客播放器采用珊瑚粉与蓝绿色，影院应用则是金色与紫罗兰的组合。

Fable 倾向于在屏幕上呈现更高的信息密度。在收件箱、CRM 系统、财务控制台和智能家居控制台的页面中，Fable 都能在同等的首屏可视区域内容纳更多的有效交互信息。相比之下，Qwen 则采用了更为宽大的组件和更多的留白；这种设计有时显得视觉感受十分沉稳，但有时也会让人觉得空间利用率不足。此外，Fable 在整个测试集中更偏好使用衬线字体进行视觉展示，而 Qwen 则更常选用醒目的几何无衬线字体。

这两个模型生成的界面也都出现了一些明显的瑕疵。在 Qwen 的输出中，智能家居页面的图标库完全未能加载，选座界面的按钮文本发生了折行，且 CRM 系统的排序标识与实际行数据并不匹配。而在 Fable 的输出中，CRM 系统的过滤器状态与实际表格内容存在矛盾，设置页面中的入睡时段与睡眠目标数值出现逻辑偏差，播客的播放队列也对长标题进行了生硬截断。

## 截然不同的智能体执行逻辑

尽管两者的最终输出页面在质量上十分接近，但它们构建这些页面的方式却大相径庭。

Fable 几乎完全依赖于单步直出。在十项任务中有九项，它都是一次性完成 `index.html` 的编写并随之停止运行。它从未主动打开浏览器查看生成的页面，也从未对自身代码进行复查，平均每项任务仅消耗 2 分 11 秒。

Qwen 则是将各项任务当作需要经过多步规划的工作来对待。它在进行实际编码前总会进行长篇的深度推理，在写入完成之后，通常还会对自身的 HTML 进行一次快速的代码语法校验。而在开发播客播放器这一任务中，它的执行步骤甚至走得更远——它主动在沙箱容器内部安装了 Playwright 和 Chromium 浏览器内核，对自己生成的页面进行了真实截图，读取截图结果，随后修改页面代码，并再次进行截图验证。仅这一项任务就消耗了 30 次工具调用以及 15 分 44 秒的运行时间，这也成了唯一一项在成本上使得 Qwen 追平 Fable 的测试任务（0.90 美元对 0.88 美元）。

自查机制并未对其输出结果起到关键作用。在播客播放器测试中，尽管 Qwen 运用了多轮截图循环复验，但我们整体还是略偏好 Fable 的生成结果。而对于那个图标完全缺失的智能家居控制台测试，Qwen 又并未发现自己漏了什么。

此外，Qwen 还会做任务重试，Fable 则不会。在产出最终可用结果前，Qwen 有三项任务遭遇过完全失败，其中一项甚至尝试了四次。在那些失败的尝试中，它要么根本没有创建 HTML 文件，要么把文件写到了错误的嵌套路径中。相比之下，Fable 的十项任务全都是一次性通过的。

## 单任务成本与耗时

十项任务的完整运行中，Qwen3.8-Max 花费 3.05 美元，Fable 5 花费 8.44 美元，Qwen 的成本仅为 Fable 的 36%。不过，其中一项任务的成本占据了不低的比例：除播客播放器外，Qwen 每项任务的开销在 0.13 至 0.34 美元之间，而仅播客播放器的截图检查循环便占据了 Qwen 总支出的 29%。若将该任务从两者的统计中剔除，Qwen 的成本将降至 Fable 的 28%。

PS：
1. 由于统计中未计入重试任务所引发的额外开销，两者的真实成本差距比上述数据看起来的要小一些；
2. 我们在测试中开启了 Qwen 的“极大（xhigh）”推理，这是其五个级别中最昂贵的一档。如果降低推理级别，Qwen 的成本还会进一步下降，尽管我们尚未测定这会在多大程度上削弱其设计输出质量。

在执行时长上，Qwen 平均每项任务耗时 7 分 55 秒，而 Fable 为 2 分 11 秒，核心原因主要是 Qwen 高强度的推理计算以及频繁自查的工作习惯。

