---
title: 我写了个工具，让 Copilot 和 Cursor 的会话历史做到远程同步
date: 2026-04-11 20:00:00
tags: "AI"
categories: tools
---

事情是这样的。

我在公司用 Copilot 写了一下午代码，跟它聊了很多——架构怎么拆、某个边界情况怎么处理。回到家打开同一个项目，对话面板空空如也。

所有上下文，全丢了。

我得重新跟 AI 解释一遍："这个项目是干什么的、之前试过什么、现在卡在哪里。"每次切机器都来一遍，烦得要死。

这件事非常影响我的开发效率。这些对话里是有真东西的——为什么选了这个方案、中间踩了什么坑。结果它们只在本地存着，换台电脑就没了。

所以我写了 sync-chat。

做一件事：利用 Copilot 和 Cursor 的 hook 机制，在会话结束时自动导出 `.jsonl` 对话记录到仓库的 `.chat-sync/` 目录。git push 之后另一台机器 git pull，打开编辑器就能看到之前的对话。

**对话历史应该和代码一样纳入版本控制。**

**GitHub 地址**
[https://github.com/NealST/sync-chat](https://github.com/NealST/sync-chat)

---

## 工作原理

对话记录就是文件——`.jsonl` 格式，躺在本地某个目录里。sync-chat 把它们复制到仓库的 `.chat-sync/` 目录，之后就是 commit、push、pull。另一台机器 pull 下来，再写回 Agent 本地存储，对话面板里就有了。

这个工具不会做任何 git 操作，什么时候 commit、什么时候 push，还是由用户自己来干。

有两种方式触发这个过程。

### Hook 自动同步

Copilot 和 Cursor 都支持 hook——在特定生命周期事件上执行 shell 命令。sync-chat 安装后会在项目里放四个文件：

```
your-project/
  .github/hooks/sync-chat.json   ← Copilot hook 配置
  .cursor/hooks.json              ← Cursor hook 配置
  scripts/
    export.sh                     ← 会话结束时执行
    restore.sh                    ← 会话开始时执行
```

| 事件 | 触发时机 | 脚本 | 行为 |
|------|---------|------|------|
| 会话结束 | Copilot `Stop` / Cursor `sessionEnd` | `export.sh` | 从 stdin 读取路径，复制 `.jsonl` 到 `.chat-sync/<agent>/` |
| 会话开始 | Copilot `SessionStart` / Cursor `sessionStart` | `restore.sh` | 将 `.chat-sync/<agent>/` 中的文件写回本地存储，跳过未变化文件 |

配一次就不用管了。

### CLI 手动同步

不想用 hook？手动来：

```bash
npx sync-chat export     # 本地对话 → .chat-sync/
npx sync-chat restore    # .chat-sync/ → 本地存储
```

---

## 怎么用

### 安装

```bash
npx sync-chat
```

装到指定目录或强制覆盖：`npx sync-chat install ./my-project --force`

没有 Node.js 也行：`bash <(curl -fsSL https://raw.githubusercontent.com/NealST/sync-chat/main/install.sh)`

安装完提交生成的文件就行：

```bash
git add .github/hooks/ .cursor/hooks.json scripts/
git commit -m "chore: add sync-chat hooks"
git push
```

### 多设备同步

**公司的机器：** 正常用 Copilot / Cursor 干活 → 会话结束自动导出 → 下班前 `git push`

**家里的机器：** `git pull` → 打开编辑器 → 白天聊的全在面板里

### 团队协作

团队成员 push 的不只是代码，还有和 AI 的对话记录。其他成员接手项目，通过 git clone，他们也能看到之前和 AI 聊过什么、试过什么，一些经验可以直接复用，这些内容可能比“员工.skill”更有实际价值。

### 扩展新 Agent

加一个新 Agent 的话：

| 步骤 | 操作 |
|------|------|
| 1 | 新增 hook 配置，调用 `export.sh --agent <name>` 和 `restore.sh --agent <name>` |
| 2 | 在 `restore.sh` 中添加 `elif` 分支，写上新 Agent 的本地存储路径 |
| 3 | 视情况更新 `bin/cli.js` 中的 CLI 子命令 |

> Claude Code 的对话历史存在云端（关联 Anthropic 账号），换设备登录即可恢复，不需要同步。

---

## 参考

**目录结构：**

```
your-project/
  .chat-sync/
    copilot/<session-id>.jsonl
    cursor/<session-id>.jsonl
  .github/hooks/sync-chat.json
  .cursor/hooks.json
  scripts/export.sh
  scripts/restore.sh
```

`.chat-sync/` 不要加到 `.gitignore`——提交到 git 就是这个工具的全部意义。

**Agent 本地存储路径：**

| Agent | 路径 |
|-------|------|
| GitHub Copilot（VS Code） | `~/Library/Application Support/Code/User/workspaceStorage/<hash>/chatSessions/`（macOS） |
| Cursor | `~/.cursor/projects/<encoded-path>/agent-transcripts/` |

---

## 写在最后

sync-chat 的本质就是把会话历史从本机搬到 git 里。本身是一个小工具，出发点主要是解决我自己的设备同步问题，如果这个工具对你也有用，欢迎使用探讨。

---

**整理 & 撰写**：AI（Claude）
**主导 & 审校**：墨筝