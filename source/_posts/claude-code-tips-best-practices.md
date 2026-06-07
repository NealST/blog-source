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

用了半年多 Claude Code，踩过的坑比写过的提示词还多。这份清单来自三个地方：Anthropic 官方文档、Boris Cherny（Claude Code 核心开发者）的公开分享、以及我自己每天用它干活的教训。48 条，按使用场景分了五组。

## 基础操作

### 1. 设一个 cc 别名

在 `~/.zshrc`（或 `~/.bashrc`）里加一行：

```bash
# --dangerously-skip-permissions 跳过所有权限确认，按需选用
alias cc='claude --dangerously-skip-permissions'
```

跑一下 `source ~/.zshrc` 就生效了。以后敲 `cc` 代替 `claude`。

### 2. 用 ! 前缀直接跑 bash 命令

`!git status`、`!npm test`，加个感叹号命令立即执行，输出自动进入上下文。不要让 Claude 帮你跑原生命令，白白浪费一轮意图识别的 Token。

### 3. Esc 停止，Esc+Esc 回滚

按一次 `Esc` 中途叫停，上下文不会丢。

连按两次 `Esc`（或者 `/rewind`，或者直接说 "Undo that"）弹出检查点列表，四种恢复选项：代码+对话一起恢复、只恢复对话、只恢复代码、从某个检查点开始压缩。

适合放手探索的场景。做成了就留，做砸了就回滚。不过检查点只追踪文件编辑，bash 命令的副作用（数据库迁移、文件系统操作）不在追踪范围内。

顺带一提：
- `claude --continue` 恢复最近一次会话
- `claude --resume` 打开会话选择器

### 4. 给 Claude 一个反馈闭环

提示词里包含测试命令、lint 检查或预期输出：

```text
将 auth 中间件重构为使用 JWT 替代 session tokens。
改完之后运行现有测试套件。
在提交前修复所有失败的用例。
```

Claude 跑测试、看到报错、自己修，不需要你介入。Boris Cherny 说过，光这一点就能带来 2 到 3 倍的质量提升。

UI 类变更可以配 Playwright MCP 服务器，让 Claude 打开浏览器、操作页面、验证行为。这个闭环能抓住单元测试覆盖不到的问题。

### 5. 给编程语言装代码智能插件

LSP 插件会在每次文件编辑后给 Claude 自动诊断：类型错误、未使用的导入、缺失的返回类型。Claude 在你察觉之前就修了。

各语言安装命令：

```text
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install rust-analyzer-lsp@claude-plugins-official
/plugin install gopls-lsp@claude-plugins-official
```

C#、Java、Kotlin、Swift、PHP 等也有对应插件，跑 `/plugin` 切到 Discover 标签页看完整列表。系统上要装好对应的语言服务器二进制，缺了插件会提醒你。

### 6. 善用 gh CLI，教 Claude 学会任意 CLI 工具

`gh` CLI 直接处理 PR、Issue、评论，不需要额外配 MCP 服务器。CLI 工具比 MCP 省上下文，因为它们不会把工具 schema 加载进来。`jq`、`curl` 同理。

Claude 不认识的工具也能学。"先用 `sentry-cli --help` 了解用法，然后找到生产环境最近的一条错误。"Claude 读帮助输出、理解语法、执行命令。团队内部的小众 CLI 工具也适用。

### 7. 用 "ultrathink" 触发深度推理

这个关键词把推理强度拉到最高，触发 Opus 4.6 的自适应推理。Claude 会根据问题复杂度动态分配思考资源。架构决策、疑难调试、多步推理，所有"先想清楚再动手"的场景都适合。

也可以用 `/effort` 永久设定推理强度。简单任务低强度就够了，没必要为一个变量重命名消耗深度推理的算力。

### 8. 用 Skills 实现按需加载知识

Skills 是扩展 Claude 知识的 Markdown 文件，放在 `.claude/skills/` 目录下。跟 CLAUDE.md 的区别：CLAUDE.md 每次会话都加载，Skills 只在跟当前任务相关时才加载，上下文保持精简。

适合承载：API 规范、部署流程、编码范式。也可以跑 `/plugin` 安装内置 Skills 的插件。

### 9. 用手机远程操控 Claude Code

`claude remote-control` 启动会话，然后从 claude.ai/code 或手机上的 Claude 应用连接。会话跑在本地机器上，手机只是个远程窗口。能发消息、审批工具调用、看进度。

配合第 1 条的 `cc` 别名（已跳过权限确认），远程操控很丝滑：启动任务，离开工位，完成或异常时用手机看一眼。

### 10. 把上下文窗口扩到 100 万 Token

Sonnet 4.6 和 Opus 4.6 都支持 100 万 Token 上下文。Max、Team、Enterprise 套餐下 Opus 自动升级到 100 万。也可以在会话中用 `/model opus[1m]` 或 `/model sonnet[1m]` 手动切。

更大的上下文意味着压缩触发得更晚，但输出质量因任务而异。如果不放心，从 50 万开始试。`CLAUDE_CODE_AUTO_COMPACT_WINDOW` 控制压缩触发时机，`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` 设百分比阈值。

## 工作流优化

### 11. 拿不准时先进 Plan 模式

多文件变更、陌生代码、架构决策，Plan 模式前期多花几分钟，能阻止 Claude 认认真真地解决一个完全错误的问题。

小范围、目标明确的任务直接跳过。`Shift+Tab` 在 Normal、Auto-Accept、Plan 三种权限模式间切换，不用离开当前对话。

### 12. 切换任务前先 /clear

一个干净的会话加精准的提示词，远胜累积了三小时上下文的混乱对话。

原因很简单：前序任务的上下文逐渐淹没当前指令。花五秒钟 `/clear` 再写一段清晰的起始提示词，能省掉后续 30 分钟的质量递减。

### 13. 不要替 Claude 解读 Bug，直接贴原始数据

用文字描述 bug 又慢又容易走样。直接粘贴错误日志、CI 输出，然后说"修"。二次解读会丢掉 Claude 定位根因需要的关键细节。

CI 失败也一样。"去修 CI 上挂掉的测试"加上 CI 输出的粘贴，非常稳。也可以贴 PR URL 或编号让 Claude 检查失败的 check 并修复，配合第 6 条的 `gh` CLI 一条龙。

管道传入也行：

```bash
cat error.log | claude "解释这个错误并给出修复建议"
npm test 2>&1 | claude "修复失败的测试"
```

### 14. 用 /btw 提旁支问题

`/btw` 弹出一个浮层让你快速提问，内容不进主对话历史。"你为什么选这个方案？""另一个方案的代价是什么？"回答显示在可关闭的浮层中，主上下文不受影响。

### 15. 用 --worktree 隔离并行开发

`claude --worktree feature-auth` 创建隔离的工作副本和新分支。Claude 自动处理 git worktree 的创建和清理。

Claude Code 团队说这是他们最大的生产力提升点之一。同时开 3 到 5 个 worktree，每个跑独立的 Claude 会话，各自有自己的分支和文件系统状态。上限取决于你的机器，多个开发服务器、构建进程和 Claude 会话会争抢 CPU。

### 16. Ctrl+S 暂存提示词

写了一半长提示词，突然要先问一个问题。`Ctrl+S` 暂存当前草稿，提完问题后自动恢复。类似 `git stash`。

### 17. Ctrl+B 将长任务放入后台

Claude 启动了一个耗时的 bash 命令（测试套件、构建、迁移），按 `Ctrl+B` 送入后台。Claude 继续工作，你也可以继续聊天。完成后结果自动呈现。

### 18. 添加实时状态栏

状态栏是一段 shell 脚本，每次 Claude 响应后执行，在终端底部显示实时信息：当前目录、git 分支、上下文使用量（按充满程度着色）。

最快的方式：在 Claude Code 里跑 `/statusline`。它会问你想显示什么，然后生成脚本。

### 19. 用子 agent 保持主上下文清爽

子 agent 有独立的 Claude 实例和上下文窗口。用它处理开销大的任务（比如代码搜索和调研），这些工作隔离在主会话之外，主会话有充足空间做实际编码。

### 20. Agent Teams 做多会话协同

实验性功能。先在设置或环境变量中启用 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`，然后说"创建一个 3 人团队来并行重构这些模块。"一个 Team Lead 分配任务，每个 Teammate 有独立上下文窗口和共享任务列表，Teammate 之间可以直接通信协调。

建议从 3 到 5 个 Teammate 起步，每人 5 到 6 个任务。避免让不同 Teammate 改同一文件，会互相覆盖。先从研究和审查类任务（PR Review、Bug 调查）开始试水。

### 21. 用指令引导上下文压缩

系统在自动压缩或你手动 `/compact` 时，不知道哪些信息对你当前任务重要。一次没有引导的压缩可能丢掉花了很久才梳理清楚的文件修改列表，或者直接忘了某个约束。

解决办法是压缩时附带指令：

```text
/compact 聚焦于 API 变更和已修改的文件列表
```

如果会话经常很长，可以在 CLAUDE.md 里写一条常驻规则：

```text
When compacting, preserve the full list of modified files and current test status.
```

这样每次压缩都会自动遵守。

### 22. 用 /loop 实现轮询监控

`/loop 5m 检查部署是否成功并汇报`，后台定时执行。间隔可选（默认 10 分钟），支持 s、m、h、d 单位。也可以对其他命令用：`/loop 20m /review-pr 1234`。

任务绑定当前会话，3 天后自动过期。适合监控部署状态、CI 流水线、轮询外部服务。

### 23. 用语音输入丰富提示词

`/voice` 启用按键说话，按住空格键录入。语音实时转写为提示词文本，可以在同一条消息中混用语音和键盘。口述的提示词天然包含更多上下文，因为人说话不会为了省打字而精简内容。

这个功能需要 Claude.ai 账号（非 API Key）。默认热键是长按空格，但空格本身也用于打字，系统需要几百毫秒判断你是想说话还是打空格，导致录音不能立刻开始。在 `~/.claude/keybindings.json` 里改成 `meta+k` 等组合键就没有歧义，录音即时启动。

### 24. 同一问题纠缠两次后果断重开

和 Claude 在同一个问题上反复修正却解决不了时，上下文已经充斥了失败尝试，这些信息会拖累后续质量。

直接 `/clear` 重开，写一段更好的起始提示词，把之前学到的经验融进去。干净的会话加更精准的提示词，比一段充满失败记录的对话好得多。

## 上下文与提示词

### 25. 精确告知 Claude 要看哪些文件

用 `@` 前缀引用文件：`@src/auth/middleware.ts 里有 session 处理逻辑`。`@` 前缀自动解析为文件路径，Claude 直接定位目标。

Claude 也能自己 grep 搜索代码库，但每一步搜索都消耗 Token 和上下文。一开始就指向正确的文件，跳过整个检索过程。

### 26. 探索陌生代码时用开放式提问

"这个文件你觉得有什么可以改进的？"是一个很好的探索性提示词。不是所有提示词都需要精确具体。当你想用新视角审视现有代码时，开放的问题给了 Claude 空间去发掘你想不到的东西。

我在上手陌生项目时经常这么干。Claude 能指出设计和实现上的改进点，初次阅读代码时很容易遗漏这些。

### 27. Ctrl+G 编辑 Claude 的计划

Claude 接到复杂任务时通常会先输出执行计划。如果大方向对但细节需要调整，按 `Ctrl+G`，计划文本会在系统默认编辑器（VS Code、vim 等）中打开。直接在编辑器里改，删行、加约束、重写某一步，保存关闭后修改版回传给 Claude 执行。

类似 `git rebase -i` 让你调整 commit 列表。计划有 10 步你只想改 2 步，在编辑器里定位修改比在对话里打字描述精确得多，也不浪费上下文。

### 28. 用 /init 生成 CLAUDE.md，然后按需精简

CLAUDE.md 是项目根目录下的 Markdown 文件，为 Claude 提供持久化指令：构建命令、编码规范、架构决策、仓库约定。每次会话开始时 Claude 都会读它。

`/init` 根据项目结构生成初始版本，自动提取构建命令、测试脚本和目录布局。

生成后要审视每一行。判断标准：没有这行，Claude 还能不能正常干活？如果它自己就能读到（比如目录结构），那这条指令就是噪音，删掉。不要让多余的指令占据上下文，稀释真正重要的部分。

一条量化参考：系统提示词本身大约占 50 条指令的预算，CLAUDE.md 有效指令上限大约在 150 到 200 条，超出后遵从度明显下降。

### 29. 出错后让 Claude 自己更新 CLAUDE.md

Claude 犯了错，告诉它"更新 CLAUDE.md，确保以后不再犯同样的错误。"它会自己写规则，下次会话自动遵守。

时间长了，CLAUDE.md 会变成一份由真实错误塑造的活文档。防止膨胀的方法：用 `@imports`（第 31 条）引用独立文件（如 `@docs/solutions.md`）来存具体的模式和修复方案。主文件保持精简，Claude 按需读细节。

### 30. .claude/rules/ 下放条件规则

`.claude/rules/` 目录下的 Markdown 规则文件默认会话开始时全部加载。要让规则仅在处理特定文件时加载，添加 paths 前置声明：

```yaml
---
paths:
  - "**/*.ts"
---
```

TypeScript 规则只在读 `.ts` 文件时加载，Go 规则只在读 `.go` 文件时加载。主 CLAUDE.md 保持精简，Claude 不用遍历当前语言无关的 rules。

### 31. 用 @imports 保持 CLAUDE.md 精简

`@docs/git-instructions.md` 引用文档。还能引 `@README.md`、`@package.json`，甚至 `@~/.claude/my-project-instructions.md`。

Claude 需要时才读这些文件。把 `@imports` 理解为"如果需要的话这里有更多上下文"，不会让每次会话都加载的主文件变臃肿。

## 权限与安全

### 32. 用 /permissions 指定白名单命令

`/permissions` 把常用命令加入可信白名单，比如 `npm run lint`，不用反复确认。未在白名单上的操作仍需确认。

### 33. 用 /sandbox 让 Claude 放手干活又不怕出事

用 Claude Code 有一个纠结点：想让它自主执行别老来问我，又怕它误操作到项目之外的东西。

`/sandbox` 在操作系统层面给 Claude 画地为牢：文件写入只能在项目目录内，网络请求只能访问你明确批准的域名。所有子进程都受限制（macOS 用 Seatbelt，Linux 用 bubblewrap）。

开沙箱后搭配 auto-allow 模式，Claude 不再逐一请求确认，但能做的事被严格限定。不会被打断，也不用担心越界。

如果需要无人值守的长时间运行（通宵迁移、实验性重构），可以更进一步：Docker 容器。完全隔离加便捷回滚，出了问题一键恢复。

### 34. 为常驻任务创建自定义子 agent

跟第 19 条那种用完即弃的子 agent 不同，自定义子 agent 是预先配好的，可以反复调用的角色，保存在 `.claude/agents/` 目录下。

几个实际的例子：
- 安全审查员：指定 Opus 模型，只给只读权限，专门 Review 安全隐患
- 快速搜索助手：指定 Haiku 模型追求速度，只负责查找信息并汇报
- 测试编写员：关注测试目录，为新增功能补测试用例

`/agents` 浏览和创建。如果某个 agent 需要改文件但你不想影响当前工作区，设 `isolation: worktree` 让它在独立的 git worktree 中运行。

### 35. 为你的技术栈选合适的 MCP 服务器

可以考虑的默认集成：Playwright（浏览器测试和 UI 验证）、PostgreSQL/MySQL（直接查 schema）、Slack（读 Bug 报告和消息线程上下文）、Figma（设计稿转代码）。

每配一个 MCP 服务器，它暴露的工具列表（名称、描述、参数定义）都会加载进上下文。配得越多，留给实际工作的空间越少。只挂当前项目真正需要的服务器，不是能找到的全部堆上去。偶尔才用到的考虑用 CLI 工具替代（参考第 6 条），CLI 不常驻占上下文。

### 36. 设置偏好的输出风格

`/config` 选风格。内置有 Explanatory（详细逐步解释）、Concise（简洁行动导向）、Technical（精确专业术语）。

也可以在 `~/.claude/output-styles/` 下创建自定义风格文件。

### 37. 用 PostToolUse Hook 自动格式化

每次 Claude 编辑文件后格式化工具都应该自动跑。在 `.claude/settings.json` 里添加 PostToolUse Hook：

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

`|| true` 防止 Hook 失败阻塞 Claude。也可以加 `npx eslint --fix` 作为第二个 Hook 条目链式执行。

如果编辑器也打开了同一文件，建议 Claude 工作期间关掉编辑器的保存时格式化。有开发者反馈编辑器的保存操作可能让 prompt cache 失效，迫使 Claude 重新读文件。让 Hook 来处理格式化就好。

### 38. 用 PreToolUse Hook 拦截危险命令

PreToolUse Hook 在 Claude 执行工具之前触发。拦截 `rm -rf`、`drop table`、`truncate`：

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

加到项目的 `.claude/settings.json` 里。可以通过 `/hooks` 交互式设置，或者直接告诉 Claude 帮你加。

### 39. 在长会话中用 Hook 保持关键上下文

长会话压缩时 Claude 可能丢失对当前工作的追踪。配一个 compact matcher 的 Notification Hook，每次压缩时自动重新注入关键上下文。

告诉 Claude"设置一个 Notification Hook，在压缩后提醒自己当前任务、已修改的文件和所有约束条件。"它会在设置里创建 Hook。适合重新注入的内容：当前任务描述、已修改文件列表、硬性约束（"不要修改迁移文件"）。

多小时深入开发某个功能时特别有用。Claude 中途丢失线索很让人恼火。

### 40. 认证、支付和数据变更逻辑必须手动审查

Claude 写代码很强，但这些决策需要人把关：认证流程、支付逻辑、数据变更、破坏性数据库操作。无论其他部分看起来多好，这些都必须人工审查。一个错误的认证范围、一个配置有误的支付 Webhook、一个悄悄删掉某列的迁移，代价可能是用户、收入或信任。

## 高阶技巧

### 41. 用 /branch 在不丢失现有进展的前提下尝试新思路

`/branch`（或 `/fork`）在当前节点复制对话。在分支里尝试高风险重构，成功就保留，失败了原来的对话不受影响。类似 git 的分支创建。

### 42. 让 Claude 采访你来完善功能规格

你知道要做什么，但细节不够让 Claude 做好。让它来主导提问：

```text
我想做 [简要描述]。用 AskUserQuestion 工具详细采访我。
问技术实现、边界情况、顾虑和取舍。
不要问显而易见的问题。
持续采访直到覆盖所有方面，
然后输出一份完整的规格文档到 SPEC.md。
```

规格文档写完后，另开一个新会话来执行。干净的上下文加完整的规格。

### 43. 让一个 Claude 写代码，另一个做 Review

第一个 Claude 实现功能，第二个从全新上下文出发审查，像一个资深工程师一样。审查者对实现过程中的妥协一无所知，会对每一处提出质疑。

同样的思路也适用于 TDD：Session A 写测试，Session B 写代码让测试通过。

### 44. 以对话方式做 PR Review

不要只让 Claude 做一次性的 PR 审查。在会话中打开 PR，然后对话式地讨论："走一遍这个 PR 中风险最高的改动。""如果这段代码并发执行会出什么问题？""错误处理跟代码库其他部分一致吗？"

对话式审查能抓到更多问题，因为你可以深入挖掘真正重要的区域。一次性审查往往只会指出风格问题，忽略架构层面的隐患。

### 45. 为会话命名和设置颜色

`/rename auth-refactor` 在提示栏上标注名称。`/color red` 或 `/color blue` 设提示栏颜色。可用颜色：red、blue、green、yellow、purple、orange、pink、cyan。

同时开着 2 到 3 个并行会话时，命名和着色让你快速识别，避免干错地方。

### 46. Claude 完成时播放提示音

Stop Hook，Claude 完成响应时播系统音效：

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

Linux 上换成 `paplay` 或 `aplay`。macOS 上其他好听的：`Submarine.aiff`、`Purr.aiff`、`Pop.aiff`。

启动任务后切去干别的，完成时听到一声提示就行。

### 47. 用 claude -p 批量操作

平时用 Claude Code 都是交互式的，你打一句它回一句。`claude -p` 是非交互模式：传入提示词，执行完就退出，可以当普通命令行工具嵌入 shell 脚本。

典型场景：20 个文件做同样的重构（比如 class 组件迁到 hooks），互相独立。写个循环并行跑：

```bash
for file in $(cat files-to-migrate.txt); do
  claude -p "将 $file 从 class 组件迁移为 hooks" \
    --allowedTools "Edit,Bash(git commit *)" &
done
wait
```

`--allowedTools` 限定 Claude 在这个任务中只能用哪些工具，防止无人监督的批量模式下出意料之外的操作。`&` 后台并行，`wait` 等全部完成。

适用于批量格式转换、大规模 import 路径更新、逐文件的重复性迁移，前提是每个文件的处理互相独立。

### 48. 自定义等待动画的提示词

Claude 思考时终端会显示带动词的旋转动画，比如 "Flibbertigibbeting..." 和 "Flummoxing..."。可以换成你喜欢的：

```text
把我的 spinner 动词替换为这些：
Hallucinating responsibly, Pretending to think, Confidently guessing, Blaming the context window
```

也不用自己提供列表。"把 spinner 动词换成哈利波特的咒语。"Claude 自己生成。一个小细节，但等待时会愉快一些。

---

## 写在最后

用了半年多，我最大的体会是：花在提示词和上下文管理上的时间，回报率远高于花在具体编码上的时间。一段精准的起始提示词、一份维护良好的 CLAUDE.md、一个恰到好处的反馈闭环，这些决定了 Claude 输出质量的上限。

另一个教训是不要试图让 Claude 一次性完成过大的任务。拆成明确的小步骤，每步给清晰的验收标准，比扔一个模糊的大需求然后祈祷它能搞定靠谱得多。

工具在迭代，技巧也在变。如果你有好用的实践没被这篇覆盖到，欢迎评论区交流。
