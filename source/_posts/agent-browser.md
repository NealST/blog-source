---
title: 我用 agent-browser 做了一个自动化截屏和标注网站的 skill
date: 2026-04-05 20:00:00
tags:
  - AI
  - AI-engineering
  - tooling
categories: tools
---

这个 skill 的核心能力在于，你只需要给 AI agent 说一句"帮我截图并标注这个网站"并扔给它一个网站地址，它会自己打开浏览器、逛完所有页面、每页加上标注、写好文档，整个过程都不需要人工参与。

## 先看成品：一条六步的自动化文档流水线

以 claude code 官网为例，我给了它一条 document this website 的指令，它就帮我生成了整个网站的说明文档并有配图说明和标注。
<video >

整个 skill 执行流程分为 6 步，流程如下：

| 阶段 | AI 干了什么 | 用到的命令 |
|------|-----------|-----------|
| 判断目标 | 本地 dev server 还是线上网站？自动识别 | `open`、端口探测 |
| 勘测站点 | 拍一张带编号的全局勘测图，读导航发现所有页面 | `screenshot --annotate`、`snapshot -i -s "nav"` |
| 逐页截图 | 验证选择器 → 注入 SVG 标注 → 截图 → 质量检查 | `eval --stdin`、`get count`、`scrollintoview` |
| 生成文档 | 输出 Markdown，每张截图配编号交叉引用 | — |
| 对比环境 | 可选：staging vs production 像素级对比 | `diff url`、`diff screenshot` |
| 清理 | 移除网络拦截，关掉浏览器 | `network unroute`、`close` |

### 细节说明

**标注不是截图上画圈圈。** 它通过 `agent-browser eval --stdin` 把一个 297 行的 SVG 标注脚本**注入到页面 DOM 里**，直接在页面上画圆、画框、画箭头。三种标注类型：`click`（按钮用实心圆+箭头）、`box`（区域用虚线框）、`circle`（通用标注）。5 种颜色自动轮换，自动编号，标签位置自动避开重叠。每张截图最多 3 个标注——多了就拆图。

**线上站点的脏活它也处理。** Cookie 弹窗？`find text "Accept" click`，一条命令语义定位关掉。懒加载？先滚到底再滚回来触发。广告追踪脚本弹浮层？`network route "**/*.doubleclick.net/**" --abort`，在网络层直接拦截。反爬？换 User-Agent，或者 `--headed` 模式让你手动过 CAPTCHA。

**怎么用？两行命令。**

```bash
npm install -g agent-browser && agent-browser install
```

装完，对你的 AI Agent 说：

```
"Screenshot the app"
"Document otto.de with screenshots"
"给我一份 checkout 流程的截图文档"
```

它就开始干活了。

**手动截图标注写文档？不存在的。**

这条流水线底下跑的，就是 agent-browser。

## agent-browser 是什么

Vercel Labs 开源的浏览器自动化 CLI，由 rust 编写，不依赖 Node.js，不依赖 Playwright，专门给 AI Agent 用。

一张表看全貌：

| 类别 | 数据 |
|------|------|
| Star | 27.1k |
| 版本 | v0.24.1（74 个 Release） |
| 架构 | 纯 Rust client-daemon，零 Node.js 依赖 |
| CLI 命令 | 50+，浏览 / 操作 / 截图 / 调试 / 网络拦截 |
| 选择器 | 4 种：Ref / CSS / Text+XPath / 语义定位 |
| 认证方案 | 6 种：Profile 复用 / Session 持久化 / State 文件 / Auth Vault / 自动连接 / Header 注入 |
| 云浏览器 | 5 家：Browserbase / Browserless / Browser Use / Kernel / AWS AgentCore |
| AI Agent 集成 | Claude Code / Codex / Cursor / Gemini CLI / Windsurf / OpenCode / Goose |
| 平台 | macOS / Linux / Windows，ARM64 + x64 |
| 语言 | Rust 85.9% + TypeScript 10.9% |
| 协议 | Apache-2.0 |

**Github**：https://github.com/vercel-labs/agent-browser
**官网**：https://agent-browser.dev

安装：

```bash
# npm（推荐）
npm install -g agent-browser
agent-browser install  # 下载 Chrome for Testing

# Homebrew（macOS）
brew install agent-browser

# Cargo（Rust）
cargo install agent-browser
```

`agent-browser install` 只在第一次跑——从 Google 官方的 Chrome for Testing 渠道下载 Chrome。Chrome for Testing 是 Google 专门给自动化测试出的 Chrome 版本，和你日常用的 Chrome 几乎一样，但关掉了自动更新——普通 Chrome 会在后台偷偷升级，版本号一变，跑自动化的脚本可能就挂了。Chrome for Testing 版本锁死，每个 Chrome 发布版本都有对应的下载，跑一百次结果都一样。已有的 Chrome、Brave、Playwright、Puppeteer 的 Chrome 也能自动检测到。

## 为什么不是 Playwright

你可能会问：AI 操作浏览器，Playwright 或 Puppeteer 不行吗？

行。但不好。

| 维度 | Playwright / Puppeteer | agent-browser |
|------|----------------------|---------------|
| 交互方式 | CSS selector / XPath | **snapshot → ref 编号** |
| AI 理解成本 | 高——需要理解 DOM 结构 | 低——无障碍树 + 编号，直接操作 |
| 依赖 | Node.js + 浏览器二进制 | **纯 Rust daemon，零 Node.js** |
| 使用方式 | 写代码调 API | **CLI 命令，任何 Agent 框架都能调** |
| 认证 | 自己写登录逻辑 | `--profile Default` 一行复用 Chrome 登录态 |
| 截图标注 | 自己画 | `--annotate` 自动标注交互元素编号 |
| 注入自定义逻辑 | 写 Node.js evaluate 脚本 | `eval --stdin` 管道注入任意 JS |
| 线上站点处理 | 自己写 cookie / 反爬逻辑 | 内置语义定位 + 网络拦截 |

核心差异在第一行——**交互方式**。

Playwright 要求你靠 CSS selector 或 XPath 定位元素。对人来说没问题，对 AI 来说就是灾难。DOM 结构复杂、class name 被混淆、动态生成的 ID 每次不一样。AI 需要先理解整个 DOM 树，然后猜一个 selector，然后试，然后发现不对，然后换一个再试。

agent-browser 的做法完全不同：先拿到页面的无障碍树（accessibility tree）——浏览器在渲染页面时，除了你看到的视觉界面，还会在内部把每个元素翻译成"这是一个按钮""这是一个输入框""这是一个链接，文字叫'提交'"这样的结构化描述，本来是给屏幕阅读器（盲人辅助软件）用的。agent-browser 把这棵树拿过来，给每个元素分配一个稳定的 ref 编号，AI 直接用编号操作。不用翻 DOM，不用猜 selector，一张"人话写的页面清单"就够了。

而且它比纯无障碍树还多做了一层——很多网站用 `<div>` 做按钮，这种元素在 ARIA 树里是隐形的。agent-browser 会额外跑一段 JS，把所有带 `cursor:pointer`、`onclick`、`tabindex` 的元素也捞出来分配 ref。Playwright 的 `page.accessibility.snapshot()` 底层用的是同一个 Chrome CDP 接口，但没有这层补充检测，遇到 div 按钮就漏了。

**不是 Playwright 不好，是 AI 不应该用人类的方式操作浏览器。**

## 核心工作流：snapshot → ref

这是 agent-browser 最核心的设计。走一遍：

```bash
# 1. 打开页面
agent-browser open example.com

# 2. 拿到交互元素快照——每个元素带一个 ref 编号
agent-browser snapshot -i
# 输出：
# - heading "Example Domain" [ref=e1] [level=1]
# - button "Submit" [ref=e2]
# - textbox "Email" [ref=e3]
# - link "Learn more" [ref=e4]

# 3. 用编号直接操作
agent-browser click @e2                    # 点按钮
agent-browser fill @e3 "test@example.com"  # 填邮箱
agent-browser get text @e1                 # 读标题文字

# 4. 页面变了？重新 snapshot 拿新编号
agent-browser snapshot -i
```

`snapshot -i` 只返回交互元素（按钮、输入框、链接），过滤掉装饰性的 DOM 噪音。一个典型页面完整 DOM 要吃掉 3000-5000 tokens，snapshot 输出只有 200-400 tokens——省了差不多 10 倍的 context window。还能加 `-c`（精简模式）、`-d 3`（限制深度）、`-s "header"`（只看 header 范围内的元素）。

**拿到编号，直接操作。不猜、不试、不翻车。**

### 另一条路：看图操作

`snapshot` 走的是文字路线。如果你的 AI 是多模态的——能看图——还有一条路：

```bash
agent-browser screenshot --annotate page.png
# 输出：
#   [1] @e1 button "Submit"
#   [2] @e2 link "Home"
#   [3] @e3 textbox "Email"

# AI 看截图，找到标注编号，直接操作
agent-browser click @e2
```

`--annotate` 在截图上给每个交互元素叠加一个带编号的标签。AI 看图识别布局和视觉状态，拿到编号后操作。

文字看 snapshot，图片看 annotate。两条路，都指向同一套 ref 编号。

### Batch：一次跑一批

多步操作不想一条条敲？用 batch：

```bash
echo '[
  ["open", "https://example.com"],
  ["snapshot", "-i"],
  ["click", "@e1"],
  ["screenshot", "result.png"]
]' | agent-browser batch --json
```

一次调用，省掉每条命令的进程启动开销。`--bail` 可以在出错时立即停止。

## 登录怎么办

做过浏览器自动化的人都知道——登录是最烦的环节，写登录脚本、处理 2FA、cookie 过期、OAuth 跳转。

agent-browser 给了 6 种方案，从零配置到企业级：

### 最简：复用你的 Chrome 登录态

```bash
# 列出你 Chrome 里的所有 Profile
agent-browser profiles

# 用你默认 Profile 的登录态打开网站
agent-browser --profile Default open https://gmail.com
```

它把你的 Chrome Profile 复制到临时目录（只读快照，不动你的原始 Profile），浏览器启动时就带着你所有的 cookie 和 session。

零配置。你 Chrome 里登录过的网站，agent-browser 都能直接访问。

### 持久化：登一次，以后自动恢复

```bash
# 首次：指定一个 session 名字
agent-browser --session-name twitter open twitter.com
# 手动登录一次...

# 以后：同一个名字，自动恢复
agent-browser --session-name twitter open twitter.com
# cookie 和 localStorage 自动保存和加载
```

状态文件存在 `~/.agent-browser/sessions/`。想加密？设一个环境变量：

```bash
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
# 所有 session 文件自动用 AES-256-GCM 加密
```

### Auth Vault：密码不让 AI 看到

```bash
# 存储凭证（加密）
echo "mypassword" | agent-browser auth save github \
  --url https://github.com/login \
  --username myuser \
  --password-stdin

# 登录——AI 只需调这一行，永远看不到密码
agent-browser auth login github
```

密码始终加密存储在本地，LLM 的上下文里永远不会出现明文密码。

### 安全兜底：防止 Agent 失控

```bash
# 只允许访问特定域名
agent-browser --allowed-domains "example.com,*.example.com" open example.com

# 操作策略文件——限制哪些命令可以执行
agent-browser --action-policy ./policy.json open example.com

# 敏感操作需要确认
agent-browser --confirm-actions eval,download open example.com
```

**说白了就一件事：AI 不碰密码，也能干活。**

## 更多能力一览

snapshot、ref、认证，核心就这几件事。除此之外 agent-browser 还有些实用的零碎：

| 能力 | 怎么用 | 场景 |
|------|--------|------|
| 多 Session | `--session agent1` / `--session agent2` | 多个 AI 同时跑，互不干扰 |
| 网络拦截 | `network route <url> --abort` / `--body <json>` | 拦截请求、mock 接口 |
| 设备模拟 | `set device "iPhone 14"` | 移动端测试 |
| HAR 录制 | `network har start` / `stop` | 抓包分析 |
| 像素级对比 | `diff url <a> <b>` / `diff screenshot` | staging 和 production 找差异 |
| 云浏览器 | `-p browserbase` / `-p browserless` | 没本地浏览器的环境（serverless、CI） |
| iOS Simulator | `-p ios --device "iPhone 16 Pro"` | 真实 Mobile Safari 测试 |
| 可观测 Dashboard | `dashboard start` | 实时看 AI 在浏览器里干什么 |
| Trace / Profiler | `trace start` / `profiler start` | Chrome DevTools 级别的性能分析 |
| 流式预览 | `stream enable --port 9223` | WebSocket 推送浏览器画面 |

Dashboard 值得单独说一句——`agent-browser dashboard start` 启动一个本地 web 页面（端口 4848），实时显示浏览器视口画面 + 命令流 + 控制台日志。你可以"旁观"AI 在浏览器里的一切操作。

## Skill 生态

app-screenshots 只是其中一个。agent-browser 周围已经攒起一圈 Skill 了。

```bash
# 一行命令，让你的 AI Agent 学会用 agent-browser
npx skills add vercel-labs/agent-browser
```

这行命令把 agent-browser 的 Skill 文件装到你的项目里。支持 Claude Code、Codex、Cursor、Gemini CLI、Windsurf、Goose、OpenCode。Skill 从仓库实时拉取，不会过期。

或者更简单——直接告诉你的 AI Agent：

```
Use agent-browser to test the login flow.
Run agent-browser --help to see available commands.
```

`--help` 的输出足够详细，大多数 Agent 看完就会用了。

## 架构：为什么快

agent-browser 采用 client-daemon 架构——daemon 就是一个在后台常驻的进程，你看不见它，但它一直活着，随时等你发号施令。类似 macOS 的 Spotlight 索引服务：你不用的时候它安静待着，你一搜东西它立刻响应。

1. **Rust CLI**——解析命令，和 daemon 通信
2. **Rust Daemon**——直接走 CDP（Chrome DevTools Protocol），不经过 Node.js

daemon 在你第一次跑命令时自动拉起来，之后就常驻后台。所以第一条命令可能要等一下（启动 Chrome），后续命令都是毫秒级响应。Rust daemon 本身只吃 7MB 内存，同样的活儿换 Node.js 跑是 140MB（V8 的锅），20 倍差距。

设置 `AGENT_BROWSER_IDLE_TIMEOUT_MS` 可以让 daemon 在空闲一段时间后自动退出。

浏览器引擎默认用 Chrome（来自 Chrome for Testing），也支持 LightPanda（`--engine lightpanda`）和 Safari（通过 WebDriver，用于 iOS）。

## 写在最后

浏览器自动化这件事，Selenium 搞了 20 年，Playwright 搞了 5 年。它们解决的都是同一个问题："怎么用代码控制浏览器"。

agent-browser 换了个问法："怎么让 AI 控制浏览器"。

答案不是更好的 API——是一棵无障碍树、一组编号、一个 CLI。让 AI 用自己的方式理解页面就行了。

**浏览器自动化的终局，不是让 AI 模拟人类点击，是让 AI 用 AI 的方式操作浏览器。**

**Github**：https://github.com/vercel-labs/agent-browser
**官网**：https://agent-browser.dev
**app-screenshots Skill**：https://github.com/alexanderop/app-screenshots
