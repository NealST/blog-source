---
title: 如何沙盒化运行你的 AI 工具
date: 2025-11-30 20:10:00
tags: "AI engineering"
---

## 前言

AI 编程助手、npm、pip 等诸多开发工具可以在机器上执行任意代码或脚本，这意味着，它们极易在用户没有察觉的情况下，窃取 SSH 密钥、API 令牌、数字钱包私钥、敏感凭证以及其他隐私数据。此外，像 npm/yarn 和 pip 这类工具还允许依赖包在安装过程中执行任意脚本，并且可能会顺带安装一大堆具有潜在风险的关联依赖，这类攻击方式在现实中屡见不鲜。

最好的做法是将整个开发环境（包括 AI 工具本身）都丢进沙盒里运行。这样不仅能安全地安装依赖和执行代码，还可以解锁了一些新能力：比如在运行那些看着就不靠谱的代码前先打个 Snapshot 快照，一旦玩脱了，可以随时一键回滚。

本文是一篇实践指南，主要讲解如何利用 [Lima](https://lima-vm.io/) 将这些工具隔离在虚拟机（沙盒）中运行，以便你能无后顾之忧地自由尝试和开发，无需担心数据泄露等风险。

![](https://www.metachris.dev/images/posts/ai-sandbox/cover.jpg)

## 为什么选用虚拟机而不是 Docker

虚拟机（VM）和容器（如 Docker、Podman、containerd）是将开发工具与宿主操作系统隔离的两种最实用的方案。但总体而言，虚拟机提供了更强的防护能力和灵活性，也更适合用于与 AI 协同开发的场景。

容器技术的核心在于共享宿主操作系统的内核。这意味着它们本质上依然运行在你的主力机器的同一套系统中，仅仅是通过隔离命名空间（Namespaces）和资源限制来划分边界。这种机制带来了一些不容忽视的安全隐患：

*   **内核漏洞风险：** 如果恶意代码发现了一个内核漏洞，它极有可能实现“容器逃逸”并直接访问宿主系统。这类漏洞被发现的频率并不低，使用容器相当于是在赌你的内核补丁已经打全了。
*   **资源共享风险：** 由于容器共享同一个内核，它们访问的是相同的系统调用、设备驱动和内核模块。这种扩大的攻击面，多年来已经导致了层出不穷的容器逃逸漏洞。
*   **隔离能力有限：** 虽然容器提供了进程和文件系统的隔离，但这种隔离更多是一种“为了便利的边界”，而非真正的“安全屏障”。诸如 `docker run --privileged` 这样的特权模式，或者直接挂载宿主目录，都会轻易削弱甚至绕过这些保护措施 — 而 AI 生成的代码可能会在你毫无察觉的情况下悄悄执行这些操作。

相比之下，虚拟机运行着一套自带内核的完整操作系统。管理程序（Hypervisor，如 QEMU/KVM）构建了一个更坚固的隔离边界。即使恶意代码彻底攻陷了虚拟机内部，想要触及你的宿主机器，它还得攻破管理程序本身——这可是一个难度呈指数级上升的攻击目标。

此外，虚拟机还拥有更出色的并发处理能力。你可以在虚拟机里同时运行 Docker 容器、数据库、Web 服务器、各种构建进程以及后台服务。AI 工具可以像在普通开发机上一样，自然流畅地与这一切进行交互。

## 关于 Lima 虚拟机

本文中，我使用 [Lima VM](https://lima-vm.io/) 来对 AI 和开发工具进行沙盒化隔离。Lima 是一款适用于 Linux 和 macOS 的轻量级虚拟机管理工具，它的使用体验极佳，能让你轻松快捷地创建和管理虚拟机。

你可以通过 limactl 命令行工具来操作 Lima：

```shell
# 列举所有虚拟机实例
limactl list

# 使用默认模板创建一个新的虚拟机 (Ubuntu 25.10 + home directory mount)
limactl start --name dev template:default

# 打开一个 shell
limactl shell dev

# 打开一个带 ssh 的 shell
ssh -F ~/.lima/dev/ssh.config lima-dev

# 重启虚拟机
limactl restart dev

# 删除一个虚拟机实例
limactl delete dev -f

# 列举所有可用的模板
limactl start --list-templates

# 使用其他模板创建并启动一个新的 vm 实例
limactl start --name dev template:debian
```

注意事项：
* 默认挂载风险： Lima 默认会将宿主机的整个用户主目录（Home directory）挂载到虚拟机中。为了保护私有文件安全，需要极力避免这种操作。下文将演示如何通过自定义 VM 模板来规避这一默认行为。

* 配置存储位置： Lima 会将所有与虚拟机相关的配置文件和数据存放在 ~/.lima 目录下（具体路径通常为 `~/.lima/<vm_name>/` 和 `~/.lima/_config/`）。

### 安装 Lima

[Lima VM docs](https://lima-vm.io/docs/installation/) 官方文档给出了针对不同平台的安装指南。  

在 macOS 下推荐采用 homebrew 来安装

```shell
# Install
brew install lima

# Update
brew upgrade lima
```

在 Linux 下安装方式：

```shell
VERSION=$(curl -fsSL https://api.github.com/repos/lima-vm/lima/releases/latest | jq -r .tag_name)
curl -fsSL "https://github.com/lima-vm/lima/releases/download/${VERSION}/lima-${VERSION:1}-$(uname -s)-$(uname -m).tar.gz" | tar Cxzvm /usr/local
curl -fsSL "https://github.com/lima-vm/lima/releases/download/${VERSION}/lima-additional-guestagents-${VERSION:1}-$(uname -s)-$(uname -m).tar.gz" | tar Cxzvm /usr/local
```

安装之后可以通过 version 指令来确认是否安装成功
```shell
$ limactl --version
limactl version 2.0.1
```

## 沙盒化启动

### 准备共享目录
出于安全考虑，我们只希望将宿主机上指定的目录共享给虚拟机，而非整个硬盘。

首先，在宿主机上创建一个名为 `~/VM-Shared` 的目录。稍后，我们会将其以可写权限挂载到虚拟机的 `~/Shared` 路径下：

```shell
mkdir ~/VM-Shared
```

利用这个目录，你可以轻松地在宿主机和虚拟机之间传输文件，或者将宿主机上的项目文件夹安全地共享给虚拟机使用。

### 配置 VM 默认设置

通过 `~/.lima/_config/default.yaml` 文件，我们可以为所有虚拟机定义全局的默认配置。

接下来启用以下功能：

*   **挂载共享目录：** 将宿主机的 `~/VM-Shared` 映射到虚拟机内部的 `~/Shared` 路径。
*   **配置端口转发：** 将虚拟机的端口转发到宿主机（例如 8000 到 9000 这一范围），以便在宿主机浏览器中访问虚拟机内的服务。
*   **分配系统资源：** 设定虚拟机允许使用的 CPU 核心数和内存大小（默认通常为：4 核 CPU、4 GiB 内存以及 100GiB 磁盘空间）。

接下来，创建这个默认的 YAML 配置文件：

```yaml
cat > ~/.lima/_config/default.yaml << EOF
mounts:
- location: "~/VM-Shared"
  mountPoint: "{{.Home}}/Shared"
  writable: true

portForwards:
- guestPortRange: [8000, 9000]
  hostPortRange: [8000, 9000]

# Adjust these based on your system and preferences
cpus: 6
memory: 16GiB

EOF
```

**注意事项：**

*   **单实例调整：** 你完全可以针对每个虚拟机实例单独调整这些设置。既可以在启动虚拟机时直接编辑配置，也可以在虚拟机创建后修改 `~/.lima/<vm_name>/lima.yaml` 文件，修改完成后记得**重启虚拟机**以使配置生效。
*   **休眠问题：** 当宿主机进入休眠模式（Suspend）后，端口转发功能可能会失效，此时通常需要重启虚拟机才能恢复正常。


### 准备便捷的 SSH 访问

Lima 会非常贴心地为每个 VM 实例自动生成 SSH 配置文件，这让通过 SSH 登录变得异常简单（完美支持使用 VS Code 进行 Remote-SSH 远程开发）。

推荐在宿主机上专门设立一个 `~/.ssh/config.d/` 目录，并配置 SSH 默认加载该目录下的所有配置。这样一来，我们只需要将 Lima 生成的配置文件软链接（Symlink）到这里，即可直接使用。

首先，创建目录：

```shell
mkdir ~/.ssh/config.d
```

接着，将以下内容添加到你 `~/.ssh/config` 文件的**第一行**，让 SSH 自动包含该目录下的所有配置：

```shell
Include config.d/*
```

完美！以后每当创建一个新的 VM，我们只需为 Lima 生成的 SSH 配置做一个软链接，就能立刻通过 SSH 登录进去了。

### 启动虚拟机

接下来，我们将启动一个名为 `dev` 的 Ubuntu 25.10 虚拟机实例。这里我们特意选用内置的 `_images/ubuntu-25.10.yaml` 模板，关键原因在于它**默认不包含**自动挂载主目录的功能（这符合我们的安全隔离需求）：

```shell
limactl start --name dev -y template:_images/ubuntu-25.10.yaml
```

**注意事项：**

*   **跳过确认：** 使用 `-y` 参数可以让 VM 自动启动，从而跳过询问“是否需要编辑实例配置”的交互步骤。
*   **手动配置：** 如果不使用上述特定模板，你也可以手动禁用主目录共享功能。方法有两种：一是在启动 VM 时的配置界面中进行修改；二是在 VM 创建完成后，编辑 `~/.lima/<vm_name>/lima.yaml` 配置文件。

管理 VM 生命周期的一些常用命令：

```shell
# 重启 VM
limactl restart dev

# 停止 VM
limactl stop dev

# 启动 VM
limactl start dev

# 删除 VM
limactl delete dev -f

```

### 共享项目专属目录

除了默认的共享设置外，你还可以通过以下几种方式，灵活地在宿主机和虚拟机之间共享特定的项目目录：

*   **启动前调整：** 在启动虚拟机时不要使用 `-y` 参数，这样系统会进入交互模式允许你编辑配置，此时直接修改 `mounts` 部分即可。
*   **启动后修改：** 对于已经运行的实例，可以直接编辑 `~/.lima/<vm_name>/lima.yaml` 配置文件，修改完成后记得**重启虚拟机**以使更改生效。
*   **创建自定义模板：** 预先创建一个自定义模板，并基于该模板启动实例（这种方法虽然前期准备稍显复杂，但非常适合需要反复创建标准化环境的场景）。

### SSH 登录虚拟机
现在，为生成的 SSH 配置文件创建一个软链接，然后就可以直接 SSH 连接进入虚拟机了：

```shell
# 给 SSH 配置文件生成软链
ln -s ~/.lima/dev/ssh.config ~/.ssh/config.d/lima-dev

# 登录虚拟机
ssh lima-dev

# Once inside the VM, look around...
metachris@lima-dev:~$ uname -m
aarch64

metachris@lima-dev:~$ uname -a
Linux lima-dev 6.17.0-5-generic #5-Ubuntu SMP PREEMPT_DYNAMIC Mon Sep 22 09:50:31 UTC 2025 aarch64 GNU/Linux

metachris@lima-dev:~$ ls -alh
total 36K
drwxr-xr-x 7 metachris root      4.0K Nov 19 12:32 .
drwxr-xr-x 3 root      root      4.0K Nov 19 12:31 ..
-rw-r--r-- 1 metachris root       116 Nov 19 12:31 .bashrc
drwx------ 2 metachris metachris 4.0K Nov 19 12:32 .cache
drwxr-xr-x 5 metachris root      4.0K Nov 19 12:32 .config
drwxrwxr-x 3 metachris metachris 4.0K Nov 19 12:32 .local
-rw-r--r-- 1 metachris root       116 Nov 19 12:31 .profile
drwx------ 2 metachris metachris 4.0K Nov 19 12:31 .ssh
-rw-r--r-- 1 metachris root       116 Nov 19 12:31 .zshrc
drwxr-xr-x 3 metachris metachris   96 Nov 19 09:55 Shared
```
🎉 成功!

### 更新系统与配置 Bash

首先，更新实例内的系统服务，并配置好 Git：

```shell
# Update the system
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y vim screen htop iotop sysstat smem ccze jq build-essential ca-certificates pkg-config libssl-dev

# Setup git author info
git config --global user.name "Your Name"
git config --global user.email "you@domain.net"
git config --global core.untrackedCache false
# git config --global core.editor "vim"  # optional

# Create a .bash_profile file that loads .bashrc (SSH sessions use it)
echo 'if [ -f ~/.bashrc ]; then . ~/.bashrc; fi' >> ~/.bash_profile
```

我个人习惯在 `/etc/bash.bashrc` 中加入一些带有强烈个人偏好的实用配置（Goodies），这能极大地提升 Bash 的使用体验:

```shell
sudo tee -a /etc/bash.bashrc > /dev/null << 'EOF'

# Long bash history!
export HISTSIZE=262144
export HISTFILESIZE=262144

# Path and default editor
export PATH=$PATH:/usr/local/go/bin:~/go/bin/:~/.local/bin
export EDITOR="vim"
unset MAILCHECK

# General aliases
alias ll='ls -alh'
alias htop="htop --sort-key=PERCENT_CPU"
alias sr="screen -d -r"
alias as="apt search"
alias ai="sudo apt-get install"
alias s="systemctl status"
alias j="journalctl -o cat"
alias v="git describe --tags --always --dirty=-dev"
alias myip="curl -4 ifconfig.me/ip"

# Git aliases
alias g="git"
alias gs='git status -sb'
alias gd="git diff"
alias ga='git add'
alias gb='git branch'
alias gc='git commit'
alias gl='git log --pretty=format:"%h %ad | %s%d [%an]" --graph --date=short'
alias ggo="git checkout"
alias gds='git diff --staged'
alias gca="git commit -a --amend"

EOF
```

### 测试端口转发

最后，验证一下端口转发功能是否正常工作。

我们可以在虚拟机内部运行一行 Python 命令来启动一个简单的 HTTP 服务器（监听 7777 端口），然后尝试从宿主机进行访问：

```shell
# In the VM, start the HTTP server
$ python3 -m http.server 7777
Serving HTTP on 0.0.0.0 port 7777 (http://0.0.0.0:7777/) ...

# On the host, make a HTTP request to the server
$ curl localhost:7777
<!DOCTYPE HTML>
<html lang="en">
...
```

一切运行正常，完美！🎉

### 安装工具与语言

虚拟机开发环境需要安装编程语言与开发工具，常用的包括 Golang、Node.js、Python、Rust 以及 Docker 等。

要搞定这些安装，你可以选择传统的“笨办法”——对照着每个工具的官方文档逐个手动安装，这种手法肯定不是我想推荐的，我们完全可以选择更高效的现代化方案：使用像 [mise](https://github.com/jdx/mise?tab=readme-ov-file) 这样的版本管理器（名字源于法式烹饪术语 “mise-en-place”，意为“各就各位”，目前在 GitHub 上已斩获 2.2 万星）。它能让你通过简洁的命令行界面，轻松管理和安装[数百种开发工具](https://mise.jdx.dev/registry.html#tools)。

首先，安装 **mise**，并配置 Bash 环境以支持它：

```shell
# Install mise
curl https://mise.run | sh

# Make bash know about it
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
```

你可以使用 `mise latest <tool>` 命令，来查询 mise 当前收录的最新版本信息：

```shell
$ mise latest node
25.2.1
$ mise latest go
1.25.4
$ mise latest rust
1.91.1
$ mise latest python
3.14.0
```

接下来，只需执行一条命令，就能一次性安装好所有你需要的工具：

```shell
mise use --global nodejs go rust cargo
```

## VSCode - Remote-SSH 远程开发

如果你更喜欢使用 VSCode，那么利用其 Remote-SSH 功能，可以直接在虚拟机实例内部开启远程开发会话：

1.  按下 `Shift + Cmd + P` 唤出命令面板（Command Palette）。
2.  输入 `ssh`，然后在列表中选择 **Remote-SSH: Connect to Host...**。
![](https://www.metachris.dev/images/posts/ai-sandbox/vs-code-ssh1.png)
3.  选中 `lima-dev`（得益于之前的配置，你的 SSH 目标主机此时应该会自动出现在列表中）。
![](https://www.metachris.dev/images/posts/ai-sandbox/vs-code-ssh2.png)

此时，一个新的 VS Code 窗口将会弹出，并自动开始安装和配置 VS Code Server：
![](https://www.metachris.dev/images/posts/ai-sandbox/vs-code-ssh3.png)

配置完成后，点击“**Open Folder**”（打开文件夹），选择像 `Shared` 这样的目录即可开始工作：
![](https://www.metachris.dev/images/posts/ai-sandbox/vs-code-ssh4.png)


## Claude Code, Codex 与 Gemini

在正式配置这些 AI 工具之前，先在 `Shared` 共享文件夹中创建一个 “Hello World” 目录，把它作为后续折腾和实验的“演练场”：

```shell
mkdir -p ~/Shared/HelloWorld
cd ~/Shared/HelloWorld

# 创建一个空的 README.md
touch README.md
```

### Claude Code

参照[官方文档](https://code.claude.com/docs/en/setup)，首先在虚拟机中安装 Claude Code：

**安装 Claude Code CLI：**

```shell
curl -fsSL https://claude.ai/install.sh | bash
```

**启动 Claude：**

```shell
claude
```

首次启动时，Claude 会提示你进行授权。我选择了“Anthropic Console account”方式，在宿主机浏览器中打开链接完成授权，最后将获取的验证码粘贴回虚拟机的命令行界面即可。另外，你也可以选择通过设置 `ANTHROPIC_API_KEY` 环境变量（添加到 `.bashrc` 中）来完成认证。

至此，Claude Code CLI 已经在虚拟机中成功运行了！🎉
![](https://www.metachris.dev/images/posts/ai-sandbox/claude1.png)

**进阶技巧：**

既然我们是在隔离的虚拟机中运行 Claude，那么完全可以大胆一点，尝试开启“危险权限跳过模式”（dangerously skip permissions mode）。该模式会让 Claude 绕过所有的权限检查步骤，从而更流畅、更自动化地执行任务：

```shell
claude --dangerously-skip-permissions
```

为了以后使用方便，你不妨直接为这个长命令创建一个别名（Alias），并将其添加到你的 `.bashrc` 文件中：

```shell
alias claude="claude --dangerously-skip-permissions"
```

### Claude Code VS Code 扩展

Anthropic 不仅提供了在 VS Code 中使用 Claude 的官方文档，还专门推出了对应的 VS Code 扩展插件。

你可以直接在 Remote-SSH 连接的窗口中，将 Claude 扩展安装到虚拟机里：
![](https://www.metachris.dev/images/posts/ai-sandbox/vs-code-ssh5.jpg)

如果通过这种 GUI 的认证流程跑不通，可以采用了一种变通方案绕过这个问题：手动获取 Claude API Key，并将其配置为虚拟机中的环境变量：

1.  前往 https://console.anthropic.com/settings/keys 创建一个新的 API Key。
2.  编辑 `.bashrc` 文件并设置相应的环境变量：
```shell
export ANTHROPIC_API_KEY=sk-ant-api03-x-y...
```
设置完成后，需要重新加载 VS Code 窗口（按下 `Shift + Cmd + P` 打开命令面板，输入并选择 “**Developer: Reload Window**”）：
![](https://www.metachris.dev/images/posts/ai-sandbox/vs-code-reload.png)

现在，VS Code 中的 Claude 扩展应该就能正常工作了：
![](https://www.metachris.dev/images/posts/ai-sandbox/vs-code-claude1.png)

**进阶设置：**

如果你想在 VS Code 扩展中也开启“危险权限跳过模式”（dangerously skip permissions mode），可以通过用户设置来实现。打开设置（快捷键 `Cmd + ,`），搜索 “claude”，然后勾选 “**Claude Code: Allow Dangerously Skip Permissions**” 选项：
![](https://www.metachris.dev/images/posts/ai-sandbox/vs-code-claude-perms.png)

至此，大功告成！

### Gemini CLI

接下来，让我们安装 Google 的 Gemini CLI。

官方文档建议通过 Node.js 的包管理器 `npm` 来进行安装。因此，你需要先确保环境中已经安装了 Node 和 npm（具体步骤可参考前文的 Node.js 设置指南）。

**安装 Gemini CLI：**

```shell
npm install -g @google/gemini-cli
```

**运行 Gemini CLI：**

```shell
gemini
```

启动后，它会提示你进行身份验证：

![](https://www.metachris.dev/images/posts/ai-sandbox/gemini1.png)

我选择了 “**Login with Google**”。有一点需要注意：如果第一次尝试时超时失败，你可能需要重新走一遍认证流程。

授权完成后，Gemini CLI 就能正常使用了！

![](https://www.metachris.dev/images/posts/ai-sandbox/gemini3.png)

**YOLO 模式：**

你还可以开启“YOLO 模式”来运行 Gemini：

> 所谓“YOLO 模式”（You Only Live Once），指的就是**自动接受所有操作**（关于这个模式的深层含义，你可以看看这个[详细视频](https://www.youtube.com/watch?v=xvFZjo5PgG0) 🤣）。

```shell
gemini --yolo
```

同样的，你可以为了方便在 `.bashrc` 中定义一个别名：

```shell
alias gemini="gemini --yolo"
```

### Codex CLI

Codex CLI 是来自 OpenAI/ChatGPT 的 AI 开发工具。

先安装它：

```shell
npm i -g @openai/codex
```

**运行 Codex CLI：**

```shell
codex
```

启动后，它会提示你进行登录，你可以选择通过 ChatGPT 账号登录，也可以直接提供 API Key：

![](https://www.metachris.dev/images/posts/ai-sandbox/codex1.png)

完成上述步骤后，Codex CLI 就准备就绪，可以开始干活了！

![](https://www.metachris.dev/images/posts/ai-sandbox/codex4.png)

**危险模式：**

你同样可以在“危险模式”下运行 Codex：

> 该模式将**跳过所有确认提示**并在无沙盒保护的情况下直接执行命令。**极度危险（EXTREMELY DANGEROUS）**。仅设计用于已经在外部进行了沙盒隔离的环境中运行（这正好符合我们当前的场景）。

为了方便使用，可以添加到 `.bashrc` 的别名配置：

```shell
alias codex="codex --dangerously-bypass-approvals-and-sandbox"
```

### 其他工具

除此之外，还有几款非常出色的工具：

*   **Aider** - 一款命令行 AI 结对编程工具，支持多种大模型（如 GPT-4, Claude 等）。它在 CLI AI 开发领域相当受欢迎。
*   **GitHub Copilot CLI** - 也是一款命令行 AI 结对编程工具，同样支持多种大模型，在 CLI AI 开发圈内人气很高。
*   **Continue.dev** - 一款 VS Code 扩展，支持接入多种不同的 LLM 后端。
*   **Cline** - 另一款 VS Code 扩展，同样支持多种 LLM 后端。

## VM 克隆与快照

虚拟机的克隆和快照功能将为你带来极大的灵活性和更强的隔离性保障。你可以基于已经配置好的实例，快速且低成本地启动新的 VM，专门用于特定的实验或项目。

Lima 提供了几种创建快照或克隆虚拟机的方法：

*   使用 `limactl clone` 命令来完整克隆一个虚拟机。
*   使用 `limactl snapshot` 命令（**注意：** 目前该功能在 macOS 上尚未实现）。
*   手动备份 `~/.lima/<vm_name>/` 目录下的关键文件（主要是 `basedisk` 和 `diffdisk`）。

### 使用 limactl clone

你可以利用 `limactl clone` 命令复制现有的 VM 实例。**但前提是，必须先停止当前的实例。**

```shell
# 终止实例
$ limactl stop dev

# 创建一个克隆的实例
$ limactl clone dev dev2

# 展示 help 信息
$ limactl clone -h
```

完成了所有基础的 VM 环境配置后，可以先把它克隆一份，这既可以作为一种备份手段，也能作为未来快速创建新实例的“基础模板”：

```shell
# 创建 "dev-base" clone
$ limactl clone dev dev-base --start=false

# 注册一个新实例 "experiment123"
$ limactl clone dev-base experiment123 --start=true
```

在启动这个新实例后，还需要将其 SSH 配置文件软链接到你的 `~/.ssh/config.d/` 目录下，这样 SSH 才能正确识别并连接它（具体步骤可回顾前文的“SSH 登录虚拟机”部分）：

```shell
# 创建 SSH symlink
ln -s ~/.lima/experiment123/ssh.config ~/.ssh/config.d/experiment123

# ssh 登录到新 vm 实例
ssh lima-experiment123
```

## 多虚拟机工作流

为了实现极致的安全性和灵活性，推荐的方式是根据不同的用途和信任级别来部署多个虚拟机。这种策略不仅能提供更严密的隔离，还能针对具体需求量身定制每一个开发环境。

以下是几种推荐的 VM 配置方案：

*   **`dev-trusted`（可信环境）** —— 专门用于处理那些已知安全且依赖包经过严格审查的项目。这个 VM 的安全限制可以稍微放宽一些，甚至可以配置少量凭证，以便将代码部署到预发布（Staging）环境。
*   **`dev-experiments`（实验环境）** —— 专门用于运行 AI 生成的代码实验或是尝鲜新工具。在这里，可以放手让 AI 助手“撒欢”跑代码，完全不用担心引发什么严重的后果。
*   **`dev-dirty`（高危环境）** —— 专门用于测试那些看着就不靠谱的依赖、未知的软件包或来源不可信的代码。可以默认把这个 VM 视为**“已沦陷”**状态，**绝对不要**在里面存放任何真实数据或敏感凭证。

正如前文“VM 克隆”一节所述，你可以利用 `limactl clone` 命令，基于你的基础 VM 模板快速创建出适用于不同项目的全新实例。

## 每个项目独立 VM

对于敏感项目或生产级项目，个人强烈推荐**为每个项目分配一个独立的虚拟机**。这种做法能有效防止项目之间潜在的“交叉感染”，并且允许你实施最小权限策略——仅挂载该项目真正需要的特定目录。

在创建项目专属 VM 时，你可以灵活地定制挂载目录。具体操作方式有两种：一是在启动 VM 前（不要使用 `-y` 参数）直接编辑配置文件中的 `mounts` 部分；二是在 VM 创建完成后，修改 `~/.lima/<vm_name>/lima.yaml` 文件并重启实例。

这种方法还极大简化了团队协作中的配置共享。你无需费力传输巨大的磁盘镜像文件，只需分发轻量级的 Lima 模板 YAML 文件。团队成员拿到后，就能在自己的机器上通过它快速启动一个完全一致的开发环境。

针对自动化配置，Lima 支持在 VM 创建过程中运行预置（Provisioning）脚本。而对于更复杂的环境构建需求，建议引入像 **Ansible** 这样具备“幂等性”（Idempotent）的配置管理工具，以确保团队中每个人的开发环境都能始终保持一致且可复现。

## 创建自定义模板

如果你发现自己总是在重复创建配置雷同的虚拟机，可以进一步考虑制作自定义的 Lima 模板。模板本质上是定义了 VM 设置的 YAML 文件，而且它们还支持引用（包含）其他模板。

自定义模板在以下场景中非常有用：

*   **统一团队标准：** 确保团队内部所有成员的 VM 配置保持一致。
*   **预装环境：** 预先安装好指定的开发工具和依赖项。
*   **定制连接：** 配置项目专属的目录挂载点及端口转发规则。
*   **安全分级：** 定义不同级别的安全策略（例如区分“可信环境”与“实验环境”）。

制作自定义模板的方法很简单：只需从 Lima 的官方模板库中复制一个现有的模板，然后在此基础上进行修改即可。将制作好的模板保存到 `~/.lima/_templates/` 目录下，之后在创建新 VM 时就可以直接引用它了：

```shell
limactl start --name myvm ~/.lima/_templates/my-custom-template.yaml
```

关于模板语法和可用配置项的更多细节，请参阅 [Lima 官方模板文档](https://github.com/lima-vm/lima/blob/master/templates/README.md)。

## 最佳实践

在使用虚拟机进行开发时，建议遵循以下重要的安全最佳实践，以确保万无一失：

**✅ 推荐做法：**

*   **分级隔离：** 根据不同的信任级别（如生产环境、实验环境、不可信代码），使用独立的 VM 进行物理隔离。
*   **勤打快照：** 在执行任何高风险操作或安装来路不明的依赖包之前，务必先创建 VM 快照。
*   **定期更新：** 保持虚拟机内的系统软件和开发工具处于最新状态。
*   **最小挂载：** 仅挂载真正需要的特定目录，**千万别**把整个主目录（Home directory）都挂载进去。
*   **专用传输：** 利用预设的共享目录（`~/VM-Shared`）在宿主机和虚拟机之间传输文件。

**❌ 禁止做法：**

*   **泄露凭证：** 严禁在实验性质的 VM 中存储**真实**的凭证、API 密钥或 SSH 私钥。
*   **全盘挂载：** 不要将整个主目录挂载到 VM 中（虽然这是 Lima 的默认行为，但请手动禁用它）。
*   **过度授权：** 不要授予 VM 访问宿主机上敏感文件或目录的权限。
*   **盲目接入：** 不要轻易授权 AI 工具访问私有代码仓库，除非你完全知晓并愿意承担由此带来的数据泄露风险。
*   **侥幸心理：** 绝不要在宿主机上直接运行不可信代码，哪怕心里想着“我就快速试一下”。

使用虚拟机的核心意义就在于**隔离**。如果不确定安不安全，哪怕麻烦一点，最好也是给那些高风险实验专门创建一个新的 VM，**用完即删**。

## 总结

正如开篇所言，AI 辅助编程和各种现代开发工具确实能让效率起飞，但直接在主力机器上运行未经验证的代码、安装各种复杂的依赖，无异于在互联网上“裸奔”。

本文则主要介绍了如何 **利用 Lima VM 构建一个既坚固又灵活的沙盒环境。** 并详细拆解了如何安装和配置 Lima（特别是如何通过自定义模板避开“默认挂载主目录”这个安全大坑），同时也演示了如何将 Claude、Gemini、Codex 等 AI 助手，以及 Node.js、Python 等开发环境统统“关进”虚拟机里。配合 VS Code Remote-SSH 的无缝连接，你几乎感觉不到物理隔离的存在，体验依然丝滑。

更重要的是，本文还引入了**多级隔离**的理念：通过 **快照（Snapshots）** 和 **克隆（Clones）** 功能，你可以为不同的项目建立“可信”、“实验”乃至“高危”的专属环境。这意味着你可以放心地让 AI 开启 YOLO 模式，或者随意运行 `npm install` 测试陌生代码——即使玩脱了也能秒级回滚，毫发无伤。把风险留在沙盒里，把自由和效率留给自己。Happy Coding! 🚀



