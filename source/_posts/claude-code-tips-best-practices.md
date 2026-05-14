---
title: "Claude Code 的 48 条实用技巧与最佳实践"
date: 2026-05-13 22:00:00
tags:
  - AI
  - Claude-Code
  - CLI
categories:
  - AI
---

结合 [Anthropic 官方文档](https://code.claude.com/docs/en/best-practices)、Boris Cherny（Claude Code 核心开发者）的分享、社区经验，以及最近半年多的日常使用心得，我整理了 48 条 Claude Code 使用技巧与最佳实践，分为：基础操作、工作流优化、上下文与提示词、权限与安全、高阶技巧

## 基础操作篇

### 1. 设置 cc 别名

在 `~/.zshrc`（或 `~/.bashrc`）中添加：

```bash
# --dangerously-skip-permissions 标识跳过所有权限确认提示，可选
alias cc='claude --dangerously-skip-permissions'
```

然后运行 `source ~/.zshrc` 生效配置。之后就可以用 `cc` 替代 `claude` 启动 claude code。

### 2. 用 ! 前缀内联执行 bash 命令
对于原生 bash 命令来说，加一个 `!` 的前缀会让执行更高效，比如 `!git status` 或 `!npm test`，这样命令会立即执行。同时，命令本身及其输出也会加入到上下文，Claude 能直接看到结果。

不要让 Claude 帮你跑命令，这样会浪费意图识别的 token 和时间。

### 3. Esc 停止，Esc+Esc 回滚

按 `Esc` 可以中途停止 Claude 的操作而不丢失上下文。

按 `Esc+Esc`（或输入 `/rewind`，亦或是直接说"Undo that"）可以打开一个可滚动的 checklist，并提供四种恢复选项：同时恢复代码和对话、仅恢复对话、仅恢复代码、或从某个检查点开始做摘要。

比较适合大胆尝试探索的场景，如果 AI 做成了就留着，不行就回滚，没有损失。

但要注意：检查点只追踪文件编辑，bash 命令产生的副作用（数据库迁移、文件系统操作等）不在追踪范围内。

与此相关的两个命令：
* `claude --continue` 可以恢复最近一次会话
* `claude --resume` 打开一个会话选择器，选择其中一个会话恢复执行。

### 4. 给 Claude 提供反馈循环

给 Claude 一个反馈闭环，让它自己发现并修正错误。在提示词中包含测试命令、lint 检查或预期输出：

```text
将 auth 中间件重构为使用 JWT 替代 session tokens。
改完之后运行现有测试套件。
在提交前修复所有失败的用例。
```

Claude 会执行测试、观察失败、自行修复，无需人类介入。Boris Cherny 认为，单凭这一点就能带来 2–3 倍的质量提升。

对于 UI 类型的变更，可以配置 Playwright MCP 服务器，让 Claude 打开浏览器、与页面交互并验证 UI 行为是否符合预期——这个反馈闭环能捕获单元测试覆盖不到的问题。

### 5. 给编程语言安装代码智能插件

LSP 插件会在每次文件编辑后为 Claude 提供自动诊断：类型错误、未使用的导入、缺失的返回类型等。Claude 则会在你察觉之前就发现并修复这些问题，高效且舒适。

各语言的安装命令如下：

```text
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install rust-analyzer-lsp@claude-plugins-official
/plugin install gopls-lsp@claude-plugins-official
```

C#、Java、Kotlin、Swift、PHP、Lua、C/C++ 等语言也有对应插件。运行 `/plugin` 并切换到 Discover 标签页可浏览完整列表。

ps:需要确保系统上安装了对应的语言服务器二进制文件（插件会在缺失时提醒你）。

### 6. 善用 gh CLI，并教 Claude 学会任意 CLI 工具

`gh` CLI 可以直接处理 PR、Issue 和评论，无需额外配置 MCP 服务器。相比 MCP 服务器，CLI 工具更节省上下文——它们不会把工具 schema 加载到上下文窗口中。`jq`、`curl` 等标准 CLI 工具同理。

对于 Claude 尚未掌握的工具，可以这样引导它："先用 `sentry-cli --help` 了解用法，然后用它找到生产环境最近的一条错误。"Claude 会阅读帮助输出、理解语法、执行命令。即便是团队内部的小众 CLI 工具，这种方法也适用。

### 7. 用 "ultrathink" 触发深度推理

这是一个关键词，能将推理强度设为最高并触发 Opus 4.6 的自适应推理能力。Claude 会根据问题复杂度动态分配思考资源。适用于架构决策、疑难调试、多步推理，以及一切需要"先想清楚再动手"的场景。

也可以用 `/effort` 永久设定推理强度。对于简单任务，低强度既快又省 Token——比如说，你就没必要为一个变量重命名消耗深度推理的算力。

### 8. 利用 Skills 实现按需加载知识

Skills 是扩展 Claude 知识的 Markdown 文件。与每次会话都加载的 CLAUDE.md 不同，Skills 仅在与当前任务相关时才会加载，保持上下文的精简。

在 `.claude/skills/` 目录下创建 Skills 文件，或安装内置 Skills 的插件（运行 `/plugin` 浏览）。适合用来承载专业领域知识：API 规范、部署流程、编码范式等

### 9. 用手机远程操控 Claude Code

运行 `claude remote-control` 启动会话，然后从 claude.ai/code 或 iOS/Android 上的 Claude 应用连接。会话在本地机器上运行，手机或浏览器只是一个远程窗口。你可以发送消息、审批工具调用、监控进度。

如果配合第 1 条的 `cc` 别名使用，Claude 已经拥有完整权限，不会再逐一请求确认。这样远程操控会更加顺畅：启动任务、离开工位，然后仅在 Claude 完成或遇到异常时用手机查看一下即可。

### 10. 将上下文窗口扩展到 100 万 Token

Sonnet 4.6 和 Opus 4.6 均支持 100 万 Token 的上下文窗口。在 Max、Team 和 Enterprise 套餐下，Opus 会自动升级到 100 万上下文。也可以在会话中用 `/model opus[1m]` 或 `/model sonnet[1m]` 手动切换。

如果担心大上下文下的输出质量，可以从 50 万开始逐步增加。更大的上下文意味着压缩触发的时机更晚，但响应质量可能因任务而异。通过 `CLAUDE_CODE_AUTO_COMPACT_WINDOW` 控制压缩触发时机，`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` 设定百分比阈值，找到适合自己工作流的平衡点。

## 工作流优化篇

### 11. 拿不准时先进 Plan 模式

Plan 模式适用于多文件变更、陌生代码和架构决策。前期确实多花几分钟，但能阻止 Claude 浪费时间一本正经地解决一个完全错误的问题。

但如果是小范围、目标明确的任务可以直接跳过。使用时可以随时用 `Shift+Tab` 在 Normal、Auto-Accept 和 Plan 三种权限模式之间切换，无需离开当前对话。

### 12. 切换任务前先 /clear

一个干净的会话搭配精准的提示词，远胜于累积了三小时上下文的混乱对话。所以，如果是完全不同的任务，先 `/clear` 一把。

会话退化的根源在于：前序任务的上下文逐渐淹没当前指令。花个五秒钟 `/clear` 再写一段清晰的起始提示词，就可以避免后续 30 分钟的边际效益递减。

### 13. 不要替 Claude 解读 Bug，直接贴原始数据

用文字描述 bug 既慢又容易走样。你看着 Claude 猜测、纠正、再猜测，反复循环。

直接粘贴错误日志、CI 输出，然后说"修"就行了。Claude 擅长阅读分布式系统的日志并追踪断裂点。

二次解读会引入抽象层，往往会丢失 Claude 定位根因所需的关键细节。直接把原始数据交给它，然后等待结果即可。

这对 CI 同样适用。"去修 CI 上挂掉的测试"加上 CI 输出的粘贴，是最稳定可靠的模式之一。也可以贴一个 PR URL 或编号，让 Claude 检查失败的 check 并修复。配合第 6 条的 `gh` CLI，Claude 能自行完成后续操作。

还可以通过管道直接从终端传入：

```bash
cat error.log | claude "解释这个错误并给出修复建议"
npm test 2>&1 | claude "修复失败的测试"
```

### 14. 用 /btw 提旁支问题

`/btw` 会弹出一个浮层供你快速提问，内容不会进入主对话历史。适合用来澄清当前会话中的疑问："你为什么选择这个方案？""另一个方案的代价是什么？"回答显示在可关闭的浮层中，主上下文保持精简，Claude 继续原来的工作。

### 15. 用 --worktree 进行隔离式并行开发

`claude --worktree feature-auth` 会创建一个隔离的工作副本和新分支。Claude 会自动处理 git worktree 的创建和清理。

Claude Code 团队称这是最大的生产力提升点之一。同时开 3–5 个 worktree，每个运行独立的 Claude 会话，每个 worktree 拥有独立的会话、分支和文件系统状态。

本地 worktree 的上限取决于你的机器——多个开发服务器、构建进程和 Claude 会话会竞争 CPU 资源。

### 16. Ctrl+S 暂存提示词

写了一半长提示词，突然发现需要先问一个问题。用 `Ctrl+S` 就可以暂存当前草稿，提完问题后，暂存内容自动恢复，功能上比较类似于 `git stash` 操作。

### 17. Ctrl+B 将长时间任务放入后台

当 Claude 启动了一个耗时的 bash 命令（测试套件、构建、迁移），按 `Ctrl+B` 将其送入后台。Claude 继续工作，你也可以继续聊天。进程完成后结果会自动呈现。

### 18. 添加实时状态栏

状态栏是一段 shell 脚本，在 Claude 每次响应后执行，在终端底部显示实时信息：当前目录、git 分支、上下文使用量（按充满程度进行着色）。

最快的配置方式是在 Claude Code 内运行 `/statusline`。它会询问你想显示什么，然后生成对应脚本。

### 19. 用子 agent 保持主上下文清爽

子 agent 具有独立的 Claude 实例和上下文窗口，用子 agent 来单独处理一些比较复杂的任务，比如 research 之类，就可以将这些开销隔离在主会话之外，让主会话保持清爽，有充足空间来实际编码。

### 20. Agent Teams 做多会话协同

这是一个实验性功能，但能力不容小觑。需要先在设置或环境变量中启用 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`，然后告诉 Claude："创建一个 3 人团队来并行重构这些模块。"一个 Team Lead 负责分配任务，每个 Teammate 拥有独立的上下文窗口和共享的任务列表，Teammate 之间还可以直接通信协调。

建议从 3–5 个 Teammate 起步，每人 5–6 个任务。避免给不同 Teammate 分配修改同一文件的任务以免相互覆盖。

可以先从研究和审查类任务（PR Review、Bug 调查）开始试水。

### 21. 用指令引导上下文压缩

系统在自动触发压缩或手动通过`/compact`来压缩上下文时，并不知道哪些信息对你当前的任务至关重要。一次不加引导的压缩可能会丢掉花了很久才梳理清楚的文件修改列表，或者直接忘记某个关键约束。

解决方法是在触发压缩时附带指令，告诉 Claude 哪些信息必须保留：

```text
/compact 聚焦于 API 变更和已修改的文件列表
```

这样 Claude 在做摘要时会优先保留你指定的内容。

如果你的会话经常很长，也可以在 CLAUDE.md 中写一条常驻规则，这样每次压缩都会自动遵守：

```text
When compacting, preserve the full list of modified files and current test status.
```

### 22. 用 /loop 实现轮询监控

可以通过 `/loop` 指令调度一个在后台定时执行的循环提示词，比如 `/loop 5m 检查部署是否成功并汇报`。间隔可选（默认 10 分钟），支持 s、m、h、d 单位。也可以对其他命令使用：`/loop 20m /review-pr 1234`。

任务绑定在当前会话，3 天后自动过期，不用担心忘记关闭。比较适合用来监控部署状态、CI 流水线、或轮询外部服务。

### 23. 用语音输入丰富提示词内容

运行 `/voice` 启用按键说话功能，按住空格键即可录入。语音实时转写为提示词文本，可以在同一条消息中混用语音和键盘输入。口述的提示词天然包含更多上下文——人类说话会更自然地交代背景、提及约束、描述需求，不会为了省打字而精简内容。

这个功能需要 Claude.ai 账号（非 API Key）才能用。默认热键是长按空格，但由于空格本身也用于打字，系统需要几百毫秒来判断你是"按住想说话"还是"按一下想输入空格"，这个判断等待会导致录音不能立刻开始。如果在 `~/.claude/keybindings.json` 中将热键改为 `meta+k` 等组合键，就不存在歧义，录音可以即时启动。

### 24. 同一问题纠缠两次后，果断重开

当你和 Claude 在同一个问题上反复修正却始终没有解决时，上下文中会充斥很多失败的尝试，这些信息会拖累下一次尝试的质量。

这个时候就应该直接 `/clear` 重开，然后写一段更好的起始提示词——把之前学到的经验融入其中。一个干净的会话加上更精准的提示词，效果会比一段失败的经历好得多。

## 上下文与提示词篇

### 25. 精确告知 Claude 要看哪些文件

用 `@` 前缀直接引用文件：`@src/auth/middleware.ts 里有 session 处理逻辑`。`@` 前缀会自动解析为文件路径，Claude 可以直接定位目标。

Claude 当然也能自己 grep 搜索代码库，但搜索的每一步都消耗 Token 和上下文。从一开始就指向正确的文件，就能跳过整个检索过程。

### 26. 探索陌生代码时用开放式提问

"这个文件你觉得有什么可以改进的？"是一个很好的探索性提示词。不是每个提示词都需要精确具体。当你想用新视角审视现有代码时，一个开放的问题给了 Claude 空间去发掘你想象不到的东西。

我在上手陌生项目时就经常使用这种方式。Claude 能指出一些设计和实现上的改进地方——这些是初次阅读代码时很容易遗漏的。

### 27. Ctrl+G 编辑 Claude 的计划

当你给 Claude 一个复杂任务时，它通常会先输出一份执行计划（"第一步做 X，第二步做 Y，第三步做 Z"）。如果你觉得大方向对但细节需要调整，按 `Ctrl+G`，Claude Code 会把这份计划文本丢进系统默认的文本编辑器（VS Code、vim 等）中打开。你可以直接在编辑器里修改——删行、加约束、重写某一步，保存关闭后修改版会回传给 Claude，它按编辑后的版本执行。

就比较类似于 `git rebase -i` 打开编辑器让你调整 commit 列表。好处在于：如果计划有 10 步、你只想改其中 2 步，直接在编辑器里定位修改比在对话里打字描述"把第 3 步改成……第 7 步删掉"要精确得多，也不会浪费上下文。

### 28. 用 /init 生成 CLAUDE.md，然后按需精简

CLAUDE.md 是项目根目录下的 Markdown 文件，为 Claude 提供持久化指令：构建命令、编码规范、架构决策、仓库约定。Claude 在每个会话开始时都会读取它。

你可以用 `/init` 指令根据项目结构生成一个初始版本，自动提取构建命令、测试脚本和目录布局。

生成后并非万事大吉，你需要审视每一行，判断标准是：**没有这行，Claude 还能不能正常干活？** 如果 Claude 本身就能正确处理（比如它能自己读到的目录结构），那这条指令就是噪音，直接删掉，不要多余的指令占据宝贵的上下文，稀释真正重要的部分。

有一条量化参考：系统提示词本身大约占用 50 条指令的预算，CLAUDE.md 的有效指令上限大约在 150–200 条，超出后 Claude 的遵从度就会明显下降。

所以原则就是：削减冗余，补充 Claude 无法自行推断的关键规则。

### 29. 出错后让 Claude 自己更新 CLAUDE.md

当 Claude 犯了错，告诉它："更新 CLAUDE.md，确保以后不再犯同样的错误。"Claude 会自己编写规则。下次会话开始时，它会自动遵守。

随着时间推移，CLAUDE.md 会成为一份由真实错误塑造的活文档。为防止无限膨胀，可以用 `@imports`（第 31 条）引用独立文件（如 `@docs/solutions.md`）来存放具体的模式和修复方案。主配置文件保持精简，Claude 按需读取细节。

### 30. .claude/rules/ 下放置条件规则

默认情况下，`.claude/rules/` 目录下放置的 Markdown 规则文件在会话开始时都会全部加载。要让规则仅在 Claude 处理特定文件时加载，可以添加 paths 前置声明：

```yaml
---
paths:
  - "**/*.ts"
---
```

这样 TypeScript 规则只在 Claude 读取 `.ts` 文件时加载，Go 规则只在读取 `.go` 文件时加载。

主 CLAUDE.md 得以保持精简，Claude 就不需要遍历当前语言无关的所有 rules。

### 31. 用 @imports 保持 CLAUDE.md 精简

用 `@docs/git-instructions.md` 引用文档。还可以引用 `@README.md`、`@package.json`，甚至 `@~/.claude/my-project-instructions.md`。

Claude 在需要时才读取这些文件。把 `@imports` 理解为"如果需要的话这里有更多上下文"——不会让每次会话都加载的主文件变得臃肿。

## 权限与安全篇

### 32. 用 /permissions 指定白名单命令

对于一些命令，可以用 `/permissions` 将其加入到可信白名单，这样就不用反复确认，可以保持工作流畅，比如 `npm run lint`。未在白名单上的操作仍然需要确认。

### 33. 用 /sandbox 让 Claude 放手干活又不怕出事

使用 Claude Code 时有一个纠结点：又想让它自主执行不要老来问我确认，又担心它误操作到项目之外的东西（比如改了系统文件、往外发奇怪的网络请求）。

`/sandbox` 就是解决这个问题的。它在操作系统层面给 Claude 画地为牢：文件写入只能发生在项目目录内，网络请求只能访问你明确批准的域名。Claude 生成的所有子进程都受这个限制约束（macOS 底层用 Seatbelt 实现，Linux 用 bubblewrap）。

开启沙箱后，你可以放心地搭配 auto-allow 模式，Claude 不再逐一请求权限确认，但它能做的事被严格限定在安全范围内。既不会被频繁打断，也不用担心越界。

如果需要无人值守的长时间运行（通宵迁移、实验性重构），可以更进一步：在 Docker 容器中运行 Claude。容器提供完全隔离和便捷回滚，即便出了问题也能一键恢复。

### 34. 为常驻任务创建自定义子 agent

与第 19 条讲的用完即弃的临时子 agent 不同，自定义子 agent 是预先配置好的、可以反复调用的"专职角色"，保存在 `.claude/agents/` 目录下。

举几个实际的例子：
- **安全审查员**：指定用 Opus 模型、只给只读工具权限，专门 Review 代码中的安全隐患
- **快速搜索助手**：指定用 Haiku 模型追求速度，只负责在代码库中查找信息并汇报
- **测试编写员**：指定关注测试目录，专门为新增功能补充测试用例

用 `/agents` 可以浏览和创建这些 agent。如果某个 agent 需要修改文件但你不想它影响当前工作区，可以设置 `isolation: worktree` 让它在独立的 git worktree 中运行，改完后你再决定是否合并。

### 35. 为你的技术栈选择合适的 MCP 服务器

可以考虑默认集成的 MCP 服务器：Playwright（浏览器测试和 UI 验证）、PostgreSQL/MySQL（直接查询 schema）、Slack（读取 Bug 报告和消息线程上下文）、Figma（设计稿转代码工作流）。

需要注意的是，每配置一个 MCP 服务器，它暴露的工具列表（名称、描述、参数定义）都会被加载进上下文，占用一部分窗口空间。配置得越多，留给实际工作的上下文就越少。所以原则是：只挂载当前项目真正需要的服务器，而不是把能找到的全部堆上去。如果某个 MCP 服务器只是偶尔用到，可以考虑用对应的 CLI 工具替代（参考第 6 条），CLI 不会常驻占用上下文。

### 36. 设置你偏好的输出风格

运行 `/config` 选择偏好风格。内置选项有 Explanatory（详细逐步解释）、Concise（简洁行动导向）和 Technical（精确专业术语）。

也可以在 `~/.claude/output-styles/` 下创建自定义输出风格文件。

### 37. 用 PostToolUse Hook 实现自动格式化

每次 Claude 编辑文件后，格式化工具都应自动运行。在 `.claude/settings.json` 中添加 PostToolUse Hook，对 Claude 编辑或写入的文件自动运行 Prettier（或你使用的格式化工具）：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

`|| true` 防止 Hook 失败阻塞 Claude。也可以添加 `npx eslint --fix` 作为第二个 Hook 条目来链式执行。

如果在 claude code 之外你的编辑器同时打开了相同文件，建议在 Claude 工作期间关闭编辑器的保存时格式化功能。有开发者反馈编辑器的保存操作可能会使 prompt cache 失效，迫使 Claude 重新读取文件，让 Hook 来处理格式化即可。

### 38. 用 PreToolUse Hook 拦截危险命令

通过 PreToolUse Hook 拦截 `rm -rf`、`drop table` 和 `truncate` 等模式。Hook 在 Claude 执行工具之前触发，危险命令在造成破坏之前就会被阻止：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "type": "command",
        "command": "if echo \"$TOOL_INPUT\" | grep -qE 'rm -rf|drop table|truncate'; then echo 'BLOCKED: destructive command' >&2; exit 2; fi"
      }
    ]
  }
}
```

将此配置添加到项目的 `.claude/settings.json` 中。可以通过 `/hooks` 交互式设置，或直接告诉 Claude："添加一个 PreToolUse Hook 拦截 rm -rf、drop table 和 truncate 命令。"

### 39. 在长会话中用 Hook 保持关键上下文

长会话中上下文压缩时，Claude 可能会丢失对当前工作重点的追踪。一个配置了 compact matcher 的 Notification Hook 可以在每次压缩时自动重新注入关键上下文。

告诉 Claude："设置一个 Notification Hook，在压缩后提醒自己当前任务、已修改的文件和所有约束条件。"Claude 会在设置中创建 Hook。适合重新注入的内容包括：当前任务描述、已修改的文件列表、硬性约束（"不要修改迁移文件"）。

这在多小时深入开发某个功能的场景中尤其有价值——Claude 中途丢失线索是一件很令人恼火的事情。

### 40. 始终手动审查认证、支付和数据变更逻辑

Claude 写代码很强，但这些决策需要人类把关：认证流程、支付逻辑、数据变更、破坏性数据库操作。无论其他部分看起来多好，这些都必须人工审查。一个错误的认证范围、一个配置有误的支付 Webhook、或一个悄悄删掉某列的迁移——代价可能是用户、收入或信任。再完备的自动化测试也无法百分百覆盖这些场景。

## 高阶技巧篇

### 41. 用 /branch 在不丢失现有进展的前提下尝试新思路

`/branch`（或 `/fork`）会在当前节点复制你的对话。在分支中尝试高风险的重构，成功就保留，失败了原来的对话也不受影响，比较类似于 git 的分支创建功能。

### 42. 让 Claude 采访你来完善功能规格

你知道要做什么，但感觉缺少足够的细节让 Claude 做好。可以让 Claude 来主导提问：

```text
我想做 [简要描述]。用 AskUserQuestion 工具详细采访我。
问技术实现、边界情况、顾虑和取舍。
不要问显而易见的问题。
持续采访直到覆盖所有方面，
然后输出一份完整的规格文档到 SPEC.md。
```

规格文档完成后，另开一个新会话来执行——干净的上下文加上完整的规格。

### 43. 让一个 Claude 写代码，另一个 Claude 做 Review

第一个 Claude 实现功能，第二个从全新上下文出发做 Review，像一个资深工程师一样审查。审查者对实现过程中的妥协一无所知，会对每一处提出质疑。

同样的思路也适用于 TDD：Session A 写测试，Session B 写代码让测试通过。

### 44. 以对话方式进行 PR Review

不要只让 Claude 做一次性的 PR 审查。在会话中打开 PR，然后与 Claude 对话式地讨论："走一遍这个 PR 中风险最高的改动。""如果这段代码并发执行会出什么问题？""错误处理和代码库其他部分一致吗？"

对话式审查能捕获更多问题，因为你可以深入挖掘真正重要的区域。一次性审查往往只会指出风格问题，而忽略架构层面的隐患。

### 45. 为会话命名和设置颜色

用 `/rename auth-refactor` 在提示栏上标注名称，方便分辨不同会话。还可以用 `/color red` 或 `/color blue` 设置提示栏颜色。可用颜色包括：red、blue、green、yellow、purple、orange、pink、cyan。

当你同时开着 2–3 个并行会话时，这些命名和着色可以让你快速识别会话，避免干错地方。

### 46. Claude 完成时播放提示音

添加一个 Stop Hook，在 Claude 完成响应时播放系统音效。启动任务后切换到其他工作，完成时会听到一声提示：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/afplay /System/Library/Sounds/Glass.aiff"
          }
        ]
      }
    ]
  }
}
```

Linux 上替换为 `paplay` 或 `aplay`。macOS 上其他好听的音效：`Submarine.aiff`、`Purr.aiff`、`Pop.aiff`。

### 47. 用 claude -p 进行批量操作

平时我们用 Claude Code 都是交互式的——你打一句，它回一句。但 `claude -p` 是非交互模式：传入一段提示词，Claude 执行完就退出，不会等你继续输入。这使得它可以被当作一个普通的命令行工具嵌入到 shell 脚本中。

典型场景：你有 20 个文件需要做同样的重构（比如从 class 组件迁移到 hooks）。一个一个手动处理太慢，但它们之间互相独立、互不依赖。这时可以写一个循环，每个文件启动一个 `claude -p` 进程并行处理：

```bash
for file in $(cat files-to-migrate.txt); do
  claude -p "将 $file 从 class 组件迁移为 hooks" \
    --allowedTools "Edit,Bash(git commit *)" &
done
wait
```

其中 `--allowedTools` 限定了 Claude 在这个任务中只能使用哪些工具（这里只允许编辑文件和执行 git commit），防止它在无人监督的批量模式下做出意料之外的操作。`&` 让每个进程在后台并行跑，`wait` 等待全部完成。

适用于：批量格式转换、大规模 import 路径更新、逐文件的重复性迁移——前提是每个文件的处理互相独立。

### 48. 自定义等待动画的提示词

当 Claude 思考时，终端会显示带有动词的旋转动画，比如"Flibbertigibbeting..."和"Flummoxing..."。你可以换成任何你喜欢的内容：

```text
把我的 spinner 动词替换为这些：
Hallucinating responsibly, Pretending to think, Confidently guessing, Blaming the context window
```

也不必自己提供列表。告诉 Claude 你想要的风格就行："把 spinner 动词换成哈利波特的咒语。"Claude 会自己生成。这是一个小细节，但能让等待变得愉快一些。

---

## 写在最后

使用 Claude Code 半年多下来，我最大的体会是：**投入在提示词和上下文管理上的时间，回报率远高于投入在具体编码上的时间。** 一段精准的起始提示词、一份维护良好的 CLAUDE.md、一个恰到好处的反馈闭环——这些"元工作"决定了 Claude 输出质量的上限。

另外就是：不要试图让 Claude 一次性完成过于庞大的任务。把大任务拆成明确的小步骤，每步给出清晰的验收标准，比扔一个模糊的大需求然后祈祷它能搞定要靠谱得多。

工具在迭代，技巧也在演化。如果你有好用的实践没有被本文覆盖到，欢迎评论区交流。
