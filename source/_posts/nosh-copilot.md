---
title: 从 0 到 1 Vibe Coding 上架一款 iOS 应用的复盘
date: 2025-03-22 20:00:00
tags: "AI"
---

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdtNpv96Yt5yTNXxZvJmUZYTKj-L94AACqQtrG1ewAUan7aEaQhgMvQEAAwIAA3cAAzoE.png)

## 前言
从 2025 年起，vibe coding 的概念大行其道，全行业基本上都在讨论如何用 AI 提升研发效率，社交媒体上也充斥着各种无需研发背景就能 vibe coding 出各种应用的宣传。而我主要在思考两件事情：一是 AI 在帮助我们写代码之外，是否还能产品化应用到一些日常生活中解决一些现实的决策问题；二是我想用一个产品开发的全生命周期（从开发到上架）来完整体验一下 vibe coding，看看这个过程存在什么坑点，AI 到底能做什么以及能做到什么程度，未来工程师与 AI 协作应该是怎样的。纸上得来终觉浅，绝知此事要躬行，尽信书不如无书，与其每天被各种外部宣传轰炸，不如自己动手实操一把，有了体感才有依据。

本文回顾了产品设计和开发过程，并总结了 vibe coding 过程中使用 AI 的一些技巧和感受，同时也提出了笔者在实践之后对于 AI 时代的一些想法。

## idea 缘起

我大概苦恼了一个多月的时间去想到底做什么比较好，又贴近生活又解决问题还得是没有人做过的，直到有一天我干完活摸鱼时在一个钉钉群里看到一条消息
![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBcx9ptVtcq2K1B2WxTZ8Z7Gdo25qspgACtQtrG3dMqEUkBT7KV-cn2gEAAwIAA3gAAzoE.jpg)
于是乎，灵感一下就击中了我，吃什么喝什么是人类每天都要高频决策的一件事情，这件事情关乎健康和情绪，可以说极其重要。但这件事情的决策因子其实也较为复杂（不然人类也不会每天都会为此烦恼），考虑因素是多样的，包括当天的心情，最近的生活模式（比如节食，享乐，斋戒等），身体健康特征（比如糖尿病患者或者孕妇），口味偏好（吃辣或清淡），饮食忌口（不吃猪肉或不吃内脏等）以及之前几顿吃了什么（比如前面吃的过于油腻，这顿想要清淡一点）都有关系。但人类的大脑由于日常已经被工作和生活占去大半，已经很难再有多余的带宽来记忆和综合处理这些复杂的信息，但这恰好是机器和 AI 擅长做的事情，机器可以记忆之前的饮食数据和你的各种特征偏好快速形成上下文信息，AI 则擅长综合分析并快速给出决策意见。

## 产品构想

我并不想做一个很大而全复杂的产品，对于这款饮食决策应用来说，我核心希望它具备的功能有三个：
* 能够根据我的饮食偏好，健康状况，当日的摄入记录以及当天的心情等因素帮我决策这一顿吃什么比较好，且这顿吃完以后下一次摄入应该在什么时间点进行以及该吃点什么或者喝点什么。比如说我这顿吃了比较油腻的大餐（火锅或者烤肉），然后它能告诉我我应该在 30 分钟或一个小时内喝点普洱茶或熟红茶（其中的茶褐素等成分能有效包裹脂肪，加速油脂排出），亦或是温柠檬水（柠檬中的有机酸能刺激胃酸和胆汁的分泌，可以更快消化脂肪，并让口腔里的油腻感瞬间消失）
* 能够自动帮我识别某个饮食摄入后对我的健康会有什么直观的影响，比如说我的心脏，大脑，肠胃代谢甚至睡眠等等，而不仅仅是停留在冷冰冰的抽象的卡路里数字上。这份饮食可以是 AI 决策后给我推荐的，也可以是我随手一拍的日常。
* 能够依据我的饮食记录和我的心情轨迹来帮我分析我这一周或者一个月的身心和谐度，并能给出下个阶段我的饮食改进建议。在这里我并没有跟很多传统的饮食记录 APP 一样，只是单纯计算卡路里数字然后给你一个你应该做一些减脂瘦身这种没什么实际用处的建议。我的产品理念是减脂瘦身并不是健康的标准，身心和谐才是，即你的饮食需要切合你当下的心情和近期的生活状态，如果你今天心情很抑郁感到压力很大，那么吃一顿高糖高热量食物来减压就非常身心和谐。

结合这三个核心功能以及移动端产品的用户习惯，我设计了 5 个 tab 来承接和串联这些功能。
* tab1 - 首页：信息流为状态控制栏（心情与饮食模式），ghost card（AI 推荐与规划卡片，展示 AI 推荐的饮食与下一餐的摄入计划），以及饮食记录 timeline 记录列表。其中，ghost card 支持用户对于 AI 的推荐结果进行对话式调整。
* tab2 - Body Impact 页：展示当前的摄入（ghost card 的推荐或者是用户当天记录的饮食综合）对身体带来的影响，由 AI 分析得出。
* tab3 - 相机拍摄页：支持用户随手拍摄饮食，然后利用 AI 能力进行饮食分析计算营养数据和身体影响，并支持用户一键加入 timeline 记录。
* tab4 - Insight 页：负责进行数据洞察，分析用户饮食记录表中的历史数据，进行周维度和月维度的规律统计，并通过图表的形式给出可视化结果。
* tab5 - Profile 页：承接用户个人信息的展示和编辑，比如忌口，身体健康状况等等，同时提供登出和账户删除等账号管理操作。

## 产品展示
<video src="https://im.gurl.eu.org/file/BAACAgEAAxkDAAEBdFtpvU1I6etkQxvSgWLpoy2W8aNFJwACsQUAAv178EVCKY3rHalqGToE.mp4" control></video>

以上是基础的效果展示视频，目前产品主要上架在海外 App Store，如果有海外账号的可以去下载体验一下，这里再放几张额外的截图：
![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdstpv8-igJl4knsYYzHHMUa2UuTztAACngtrG1ewAUY__D82a_I-7QEAAwIAA3cAAzoE.jpg)
<center>拍照分析</center>

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBds1pv8_-MhC7g4lEOcuY09bbq8oJuwACoAtrG1ewAUZn948_I9M5ogEAAwIAA3cAAzoE.jpg)
<center>Insight 分析</center>

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBds5pv9A9onWQU9cgqTGhwzzm-NXfjQACoQtrG1ewAUbzUHt5DnVy_wEAAwIAA3cAAzoE.jpg)
<center>评分逻辑与标准</center>

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdtBpv9BccXIScxtyG9pgJUF4Ie1nUgACogtrG1ewAUYy_HVc3zklqAEAAwIAA3cAAzoE.jpg)
<center>身体影响面板</center>

## 开发过程

整个产品由我与 AI 共同完成，我负责产品和 UX 设计，前后端技术选型，数据库的表设计，技术基建的搭建以及 AI 大模型的选择和接入，AI 则主要负责帮我写代码。整个过程实践下来并非外界宣称的那样，Vibe Coding 有多么多么丝滑，即使完全没有技术背景也能轻松 cover。如果有人这么跟你说要么是他做的东西极其简单，要么就是他在给你传播焦虑。

### 我的技术背景

我有近 10 年的开发经历，最早是做前端，后来逐渐涉猎客户端和服务端，算是一名全干工程师，在公司的组织架构里仍然归类为前端，但我给自己的定位是一名产品工程师。

### 技术选型

* APP 端采用 Swift + SwiftUI 的搭配，只做 iOS。一是 iOS 客户端上架审核没有相对那么复杂的备案手续（做过独立开发的都懂） ；二是 AI 极度擅长理解这种“所见即描述”的声明式 UI 树结构且苹果官方的 Swift 相关教程极其详细，AI 学习起来毫不费力，而 Flutter 就相对不那么 AI 友好。
* 服务端我选用 Go 作为主力编程语言，一是我熟悉和喜欢 Go;二是我认为 Go 确实就比较适合写这种业务逻辑。
* 数据库选用 PostgreSql, 这个就不多说了，其 PgVector 插件可以很方便的集成向量检索能力，方便后续对接一些外部营养数据。
* 模型方面，综合能力效果，响应延时与 token 成本等多种因素考虑，我最终选择了 Gemini-3-flash-preview 和 Gemini-3-pro-preview 两款模型，前者承接饮食推荐和多模态视觉识别，后者承接 insight 数据分析，通过 openRouter 统一接入。

### 一些技巧

#### 项目上下文管理
在使用 AI 编码时可以把你的前端代码和服务端代码放在一个父目录下，这样当涉及一些需要串联前后端链路的功能时，AI 可以自主分析并进行前后端编码，且由于上下文信息更充分，不管是消费数据的前端代码还是生产协议的服务端代码都会实现的更准确。

#### prompt 生成
在 vibe coding 过程中，很多时候人会出于需求难以描述清楚或者就是觉得麻烦等原因，会直接跟 Cursor 或 Claude Code 提一个比较笼统模糊的需求，比如说：”你给我实现一个相机拍照的功能“。但这种 prompt 其实不确定性极高，AI 不知道你要在哪个页面以怎样的产品流程，用怎样的交互方式和视觉风格来实现这个功能，于是 AI 只能自己先分析你的仓库找到它认为合适的位置，自行决策产品流程和 UX 实现。但这种方式往往效果奇差，开发者需要再跟 AI 对喷好几轮来做效果调整，不仅浪费 token 也浪费时间。

我的方式是，我会在 idea 形成的一开始就在 Google AI studio 中跟 AI 一起做头脑风暴和产品设计的讨论，这样每做一个新的功能点都可以基于前序的对话记录来延续整个产品的设计风格，当功能点讨论完毕后可以直接让 AI studio 给出一份用于生成代码的 prompt ，内容涵盖 UX 设计，业务流程，用户故事甚至数据结构等。然后再把这份 prompt 直接扔给 Cursor 或 Claude Code 等工具来写代码实现，还是以相机功能为例：
![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdo9pvp6z9qKOiXZIuNaEPwKqqv471gAC5AxrG6J48UXqURNa0BbRiwEAAwIAA3cAAzoE.png)
它会生成非常详细的 prompt:
```markdown
# Task: Implement "Snap Tab" (AI Food Scanner)

## 1. Feature Context
**Goal:** Create a frictionless, AR-style camera interface for capturing food logs.
**UX Philosophy:** "Shoot, Slide, Save". No navigating to new screens. Edit everything inline.
**Design Style:** Organic Futurism (Dark Mode, Glassmorphism, Neon Mint Accents).

---

## 2. Tech Stack Requirements (iOS)
-   **Camera:** Use `AVFoundation` wrapped in `UIViewControllerRepresentable` (for full control) OR `Camera` (SwiftUI 18+ if targeting latest). *Recommendation: AVFoundation for stability.*
-   **State Management:** MVVM (`CameraViewModel`).
-   **Haptics:** `UIImpactFeedbackGenerator`.

---

## 3. UI Implementation Specifications

**Root View:** `CameraContainerView`

### State 1: The Viewfinder (Active Camera)
**Layout:** Full-screen `ZStack`.

**Layer A: Camera Preview**
-   Fill entire screen (`.ignoresSafeArea`).
-   **Tech:** Display the video feed from `AVCaptureSession`.

**Layer B: The HUD Overlay (AR Feel)**
-   **Center:** A "Focus Reticle" widget.
    -   *Visual:* Four corner brackets `L` shape, disconnected.
    -   *Animation:* "Breathing" (Scale up/down slightly) to show AI is active.
    -   *Color:* `AppColors.primaryMint`.
-   **Bottom Label:** Small capsule text: *"AI Scanning..."* or *"Point at food"*.

**Layer C: Controls Dock (Bottom Aligned)**
-   **Background:** Gradient Black (Transparent top -> Opaque bottom).
-   **Layout:** `HStack` with 3 elements.
    1.  **Left:** `GalleryButton` (Icon: `photo.on.rectangle`).
    2.  **Center:** `ShutterButton` (The Hero).
        -   *Outer Ring:* White, Stroke 4px, Diameter 80px.
        -   *Inner Circle:* Primary Mint, Diameter 60px.
        -   *Interaction:* Scale down to 0.9 on press. Trigger heavy haptic.
    3.  **Right:** `FlashButton` (Icon: `bolt.slash / bolt.fill`).
-   **Top Left:** `CloseButton` (`xmark`). Dismisses the view.

### State 2: The Analysis (Processing)
**Trigger:** User taps Shutter.
**Visuals:**
1.  **Freeze Frame:** The camera feed stops on the captured image.
2.  **Scan Effect:** A horizontal "Laser Line" (Gradient Mint) moves from top to bottom of the screen repeatedly.
3.  **Loader:** Show text "Analyzing..." with a shimmering effect.

### State 3: The Result Sheet (Smart Receipt)
**Trigger:** AI returns data (or Mock success).
**UI:** A Modal Bottom Sheet (custom height ~60% of screen), overlaying the frozen photo.
**Background:** `Material.ultraThin` (Glass) + Dark Tint.

**Component Structure (`VStack`):**

**A. Header (Identity)**
-   **Widget:** `TextField`.
-   **Style:** `Title2`, Bold, White. No border.
-   **Logic:** Pre-filled with AI result (e.g., "Avocado Toast"). User can tap to type corrections.

**B. Macros Visuals (The Rings)**
-   **Layout:** `HStack` of 3 `RingChart` widgets.
-   **Data:** Protein (Blue), Carbs (Green), Fat (Orange).
-   **Center Text:** Display gram value (e.g., "20g").
-   **Logic:** These values scale dynamically with the Slider.

**C. The Portion Slider (Core Interaction)**
-   **Label:** "Portion Size: **1.0x**".
-   **Widget:** `Slider(value: $portionMultiplier, in: 0.25...2.0, step: 0.25)`.
-   **Logic:**
    -   `displayedCalories = baseCalories * portionMultiplier`
    -   `displayedMacros = baseMacros * portionMultiplier`
    -   *UX:* Updating the slider updates the Calorie count and Macro rings *instantly*.

**D. Meta Data**
-   **Time:** A small Chip showing "🕒 Now".
    -   *Tap:* Opens a picker for "15m ago", "30m ago".
-   **Calories:** Large Display: **"450 kcal"**.

**E. Action Footer**
-   **Layout:** `HStack`.
-   **Left:** Text Button "Retake" (Grey).
-   **Right:** Large Solid Button **[ ✅ Add to Log ]**.
    -   *Action:* Save to `TimelineViewModel`, Dismiss Camera, Trigger "Success" animation.

---

## 4. Logic & ViewModel Specifications

**Class:** `CameraViewModel`

**Properties:**
-   `cameraPermission: Bool`
-   `capturedImage: UIImage?`
-   `analysisState: Enum` (idle, scanning, success, error)
-   `foodResult: FoodLog?` (The AI result)
-   `portionMultiplier: Double` (Default 1.0)

**Core Functions:**

1.  **`takePhoto()`**
    -   Capture frame.
    -   Set state to `scanning`.
    -   Call `AIService.analyze(image)`.

2.  **`processAIResult(json)`**
    -   Parse JSON to `FoodLog` model.
    -   Set state to `success`.
    -   Initialize `baseCalories` and `baseMacros` for slider logic.

3.  **`saveLog()`**
    -   Create final `FoodLog` object with modified portion/calories.
    -   Append to Global Timeline.
    -   **Trigger:** Refresh Ghost Card (for "Next Meal" forecast).

---

## 5. Animation & Polish Guidelines

-   **Scanner:** Use `GeometryReader` to animate a `Rectangle` (height 2px) moving `offset(y)`.
-   **Transition:** Use `.transition(.move(edge: .bottom))` for the Result Sheet appearing.
-   **Haptics:**
    -   `style: .heavy` on Shutter tap.
    -   `style: .light` when AI analysis finishes.
    -   `style: .selection` when dragging the Portion Slider.

---
```

这样做的好处有：
* 你不需要绞尽脑汁去写很详细的提示词，同时 Agent 编码还可以减少很多不确定性，产出质量和效果离预期的 gap 会很小，大大提升效率。
* 产品的功能设计和实现可以做到一以贯之，不会有显著的割裂感。
* 产品从 0 到 1 的整个对话过程会形成一段完整的记忆，这段记忆在未来会很宝贵，比如当你的产品要上架时，你可以基于这份记忆让 AI 帮你判断和总结上架流程中需要填写的各种材料和表单，生成产品卖点，总结心路历程，做产品宣发等等。![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdpBpvqHKLGdeIORmM9W93f6fx50RoQAC5gxrG6J48UVgT2ACLqOeDgEAAwIAA3cAAzoE.png)

#### 如何高效解决 bug

AI 生成的代码并不总是功能正确且运行正常，当你在体验过程中遇到一些 bug 的时候，比如说由于服务端接口跪了导致某个服务不可用，客户端莫名 crash 或者内存使用很高导致应用被系统回收，这个时候如果是完全没有技术背景的人，可能会跟 AI 说：”xx 功能怎么不能正常使用了，你帮我修一下“，”app 闪退了，你赶紧修一下“。然后 AI 会开始动手扫描各种代码文件进行一通分析，在消耗了大量 token 以后大概率最后会给你列一些似是而非的几大问题，然后你也没得选只能让 AI 自己动手去修这些它排查出来的问题，但是凑巧它可能就会在修复问题的过程中改坏了一些代码，然后引入新的问题。

AI 可以低成本生成大量代码以后，这种问题在 vibe coding 的过程中会时有发生且随着项目复杂度越高这类问题发生的概率也就越高，但让人类去逐行分析 debug AI 写的代码显然也是劳神费力且效率低下。面对这种问题，比较好的解法是你可以先让 AI 针对某条功能链路添加上完整的前后端日志，然后再走一遍功能，在控制台中看到疑似错误的相关日志以后再把错误日志结合你的问题描述一起丢给 AI，这个时候它就能精准定位到问题所在，高效解决问题。

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdrlpv6LhW_iqHkKRQTFDgoSkpMCcNAACggtrG1ewAUYTRLT1OMfi9QEAAwIAA3kAAzoE.png)

#### 先探讨再行动：善用 plan 模式

Agent 模式下的 AI 编码工具在拿到你的 prompt 之后会倾向于立刻开始干活，看起来似乎执行力拉满，但实际往往问题颇多。打个现实的比方就是你是一个面试官，Agent 是一位面试者，你给它出了一道题以后它并没有跟你对焦清楚题目内容和问题边界或者它自以为它搞清楚了，然后就直接上手写代码了，写出来的代码最后总是差强人意，这种面试者一般很难通过面试。

更好的做法是当你提出一个任务时，先开启 plan 模式，并在 prompt 中附赠一句“如果有不确定的地方告知我来做决策”，这样 AI 会先分析代码仓库，查找和阅读相关文件输出并主动提出澄清性问题和人类决策要求，最后形成一份规格明确的执行方案，并以 markdown 的形式保存下来，然后再使用 Agent 模式上手干活就可以大幅提升任务的成功率和准确度。

### 挑战 AI，质疑 AI，不能当甩手掌柜

AI coding 固然已经很强，但是并不意味着你就给它一个任务以后就可以完全放手开始刷手机了。AI 在执行任务的过程中会存在一种我称之为“目标自聚焦”的现象，通俗一点说就是只看当下，不管以后，只看局部不看整体，在解决一些 bug 时这种现象尤为明显。它经常会只聚焦于当下你提出的这个问题怎么解决，以及怎么让它的改动通过编译器编译和单元测试，但是这个改动是否有什么后续影响或者全局影响，甚至这个改动或者方案本身是否合理可能都不一定。比如：

![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdrppv6bnfadtkYzWKdW2eR0x8gX-HQAChgtrG1ewAUaB65WCUvMYUQEAAwIAA3kAAzoE.jpg)

当 AI 完成某项任务后我们最好要多看看它最后输出的信息，挑出你比较存疑的地方质疑它，挑战它，多问一些为什么，有没有更好的解法等，而不是无脑信任它。即使你前序使用了 plan 模式来生成执行方案，也不可大意略过，毕竟那一段执行方案对于 AI 来说也只是一段 prompt 而已，并不代表他会百分百遵循。

### 模型使用体感

整个开发过程中我主要使用了 4 个模型来辅助编程，分别是 Claude Sonnet 4.6, Claude Opus 4.6, Gemini 3.1 pro 以及 GPT 5.4。

在使用体感上：
* Gemini 3.1 pro 的视觉能力最强，ux 实现比较可靠可以拿 90 分，但做业务逻辑的质量比较一般，大概只有 70 分。
* Claude Sonnet 4.6 和 Claude Opus 4.6 基本上旗鼓相当，这两模型在业务逻辑（比如服务端实现和前后端串联）的实现质量上比较牢靠，经常能做到一步到位，可以拿 90 分。但视觉实现上比较一般，经常会出现页面布局不和谐 & 配色不协调的问题，只有 70 分的水平。
* GPT 5.4 在拟人化上做的很好，解答问题的思路非常接近人类同时输出的回答文案可读性也最好，但是干活的质量相对比较中庸，ux 视觉和功能逻辑都只能拿到 80 分

### 用到的工具与周期成本

* Github Copilot & Claude Code: 仓库初始化 & 编程工具，copilot 我开了 Pro+ 的会员（$39/月，$390/年），额度为 1500 requests/月，各种最强的模型随便用且模型上新速度极快，搭配 claude code，对于个人来说等于不限量 token。
* Railway: go 服务端应用部署，成本为 $5/月。
* Supabase: 数据库存储 & 图片存储，成本为 $25/月
* Termly: 隐私协议 & eula 服务协议生成，上架审核需要
* Unsplash: 免费且优质的图片服务，用来做 AI 推荐饮食的背景图，提升视觉吸引力。免费版本可以承接 5000/小时 的请求吞吐量，很够用了。
* Firebase: ios 应用的用户统计埋点
* Revenuecat: 集成 App 商业化订阅状态和 paywall 的管理

整个产品从项目初始化到提交上架大概花了一个月的时间，主要是下班之后&周末空余&春节期间（刚好春节前腿骨折了动不了，只好在书房肝），最终赶在春节假期最后一天提交了审核，这是我首次做 iOS 应用，不出意外第一次提交审核就被拒了。
![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdsFpv8S5w0vLAqnTURI_gVQkYTSpMwACkwtrG1ewAUaRoGHqnKxldQEAAwIAA3cAAzoE.png)
后面修改了一版以后再次提交就顺利通过了审核。这里有个小技巧是尽量选在晚上 9 点或者 10 点左右提交审核，这样你提交之后美国那边正好是审核员开始上班的时间，然后在审核资料中填写好各种给审核员使用的测试账号，如果是复核最好是在上次审核意见中添加一个回复详细说明你这次提交解决了哪些问题，这样你的审核效率会更高。我是晚上 9 点半提交的审核，然后凌晨 4 点就收到了苹果的回复邮件。

### Vibe Coding 真的完全不需要技术知识吗？

在我看来答案是否定的！至少在当前这个阶段还不行。如果你做的东西足够简单或者只是一次性的演示使用，那么可能不需要。但如果你想要真正做一款商业化有一定复杂度的产品，必要的技术背景还是刚需。因为在开发过程中你会遇到各种技术决策，比如针对产品特点该设计几张数据表，数据表的字段结构该怎么设计，AI 给的结果是否合理，用什么样的技术栈，是否要叠加 redis 缓存，怎么做数据库的读写分离，怎么做分布式等等，这些都需要经验带来的技术判断力。或许你会说这些东西让那些技术专家们写成 skill 不就好了，然后我的 Agent 不就可以自动享有这些专家知识了吗？但 skill 的本质也不过是一段 prompt, AI 大模型的本质也只是一个随机概率的算法，谁也不能保证 AI 的输出就一定是百分百遵循 skill 的，且即使单点是 OK 的，但是当你去串整体业务流程的时候上下游的衔接会存在更多问题。

AI 带来的影响只是不需要那么多初级程序员了，但对于掌握底层技术和系统设计的架构师和资深程序员来说，其实是一个能力放大器。

## 一些想法

* 代码是业务逻辑的表达，软件生产的媒介，而 vibe coding 的本质是将写代码的执行者从人转移到 AI 身上，AI 通常会借助一些编译器工具如 rust 的 cargo 或者 typescript 的 tsc 等来校验其编写的代码是否正确。但编译正确并不等于逻辑正确，逻辑正确也并不等于功能设计的合理性，AI 替代人写代码以后，人应该做的是并不是简单的 accept，而是要多质疑，多问为什么要这么做以及增强自己的判断力，给 AI 设定什么应该做，什么不应该做，怎么做是对的。**人负责设立标准和边界，AI 负责执行**
* AI 时代需要多读一些“无用的闲书”，少读工具书。这个产品的 idea 起源于同事的那一句话，但是也发散于我看过的一本书《你是你吃出来的》，摄入的饮食很大程度上决定了你的健康和心理状态，而这些营养数据的最佳消费方式则是让 AI 处理后来指导我。很多伟大的创意都来自于跨界融合和生活观察，多读闲书会增加你的审美和创意能力，**这个时代会属于一种人：兼具文科生的脑洞情怀&理科生的逻辑思维。**
* AI 时代，最怕的是你不会想更不敢想。移动互联网时代，软件的供给已经极度繁荣，但软件生成的成本很高，有些想法即使很有趣很天马行空但要么很难落地实现，要么落地成本太高让人望而却步。AI 时代软件生成的成本程指数级下降，有趣的想法反而是市场供给的稀缺品，尽管执行力仍然很重要，但我认为未来实际执行层面的比较会越来越少：讨论是咏春拳牛逼还是宫家六十四手更强没有更多意义，反正 AI 都能施展，更多的是看你的的想法是否足够让人眼前一亮。![](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBdGJpvWH5K1xnZJ-9SyyB1OCTNggmhgACzAtrG_178EW5PNOHYDfA7QEAAwIAA3gAAzoE.jpg)
* 引用小说《双城记》的一句话：”这是最坏的时代，也是最好的时代“，AI 既带来了各行业大规模的岗位合并和裁员，但同时也带来了生产力边界的极大拓宽和人类角色身份的转换，人类可以从枯燥的机械化执行的工作中解脱出来，去做更有创造性的事情，让人生的时间丰富度变得更高。AI 在未来应该也会诞生一些新的岗位和机会，对于个体来说，需要做的是降低杠杆，养好身体，先度过这段转折期。**我永远相信悲观的做准备，乐观的看未来是一种更好的生活态度。**


