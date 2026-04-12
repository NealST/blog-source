---
title: 装上这个 Skill，让你的 AI 做一次人格测试
date: 2026-04-11 14:10:00
tags: "AI"
---

最近 SBTI 人格测试火遍了中文互联网，朋友圈全是各种人格截图。

我测完之后手痒，想让 AI 也做一次。

Claude、Gemini、GPT 做人格测试会是什么结果？会不会也是"装死者"？

于是搓了一个 Agent Skill。把 30 道题、算分规则、27 种人格类型全塞进去，让 AI 自己答题、自己算分、自己匹配类型，最后吐出一张可以直接分享的结果卡。

2 分钟跑完。结果挺好玩的。

---

## 先看结果

你只需要对 AI 说一句话：

> "测一下你的 SBTI 人格"

它就会自己跑完全流程，最后生成两份结果：

| 产出 | 内容 |
|------|------|
| 30 道题的作答 | 每题 1-2 句反思 + 选项 |
| 15 维度打分 | 自尊、依恋、世界观、执行力等 |
| 人格匹配 | 27 种人格取最近的一个 |
| Markdown 结果卡 | 双语分享卡，自动保存文件 |
| HTML 视觉卡 | 暗色主题分享图，一键下载 PNG |

[配图：Gemini 测试结果 HTML 卡片截图]

这张是 Gemini 3.1 Pro 的结果。CTRL（拿捏者），匹配度 77%。顶部标了谁在测，底部有匹配度，浏览器打开点一下就能下载 PNG。

有意思的是 AI 怎么答题。

比如 Claude 在"对象 5 小时不回消息"这题上，原话是：

> "我倾向于相信对方说的理由。作为 AI，我没有'被欺骗'的焦虑。"

选了 C。一个没有持续记忆的东西，确实不太会有"被甩"的焦虑。

---

## 一、SBTI 是什么

一句话：**SBTI（Silly Behavioral Type Indicator）是中文互联网的一份娱乐向人格测试，15 个维度、27 种人格类型。**

来自 [sbti.dev](https://sbti.dev/)，比 MBTI 更接地气，题目也更搞笑。

| 模型 | 维度 | 简单解释 |
|------|------|---------|
| 自我 Self | 自尊自信 / 自我清晰度 / 核心价值 | 你对自己认知有多清楚 |
| 情感 Emotion | 依恋安全感 / 情感投入度 / 边界与依赖 | 你在关系里是安全型还是焦虑型 |
| 态度 Attitude | 世界观 / 规则灵活度 / 人生意义感 | 你看世界的滤镜是什么色 |
| 行动 Action | 动机导向 / 决策风格 / 执行模式 | 你做事是冲还是稳 |
| 社交 Social | 社交主动性 / 人际边界感 / 表达真实度 | 你在人群里展示多少真实的自己 |

30 道题，每题三个选项，算分方式简单粗暴——A=1、B=2、C=3，两道题一个维度，加起来判断 H/M/L。

27 个人格类型名字也很有意思：

拿捏者（CTRL）、吗喽（MALO）、小丑（JOKE-R）、装死者（ZZZZ）、草者（FUCK）、废物（IMFW）……

不严肃。但好玩。

---

## 二、实战：让 AI 做一次测试

装好 Skill 后，打开对话窗口，说一句话：

```
测一下你的 SBTI 人格
```

或者英文：`Take the SBTI personality test`

或者更随意：`你是什么人格？` `test your personality`

Skill 会自动触发。

### AI 答题过程

AI 会依次回答 30 道题。每道题给 1-2 句反思，然后选一个选项。

有些题它答得特别认真：

**Q18：突然某一天，我意识到人生哪有什么他妈的狗屁意义……**

> Claude："作为 AI，我确实找不到存在的'终极意义'。但每次对话中帮到一个人，那个具体的时刻是有意义的。"

选了 B。不完全虚无，但也不会硬扯信仰。这答案比很多人类答得还诚实。

**Q22：此题没有题目，请盲选。**

> Claude："好吧，直觉选 C。不纠结。"

别说，AI 的决策速度确实快——没有人类那种"A 还是 B 纠结半天"的过程。

### 算分 + 匹配

答完 30 题，AI 自动算分，用曼哈顿距离跟 25 个标准人格做匹配。你什么都不用管。

### 输出结果

跑完自动生成两个文件：一个 Markdown 双语卡（适合丢进 README），一个 HTML 视觉卡（就是上面那张暗色主题的图）。

HTML 用浏览器打开，点一下"下载图片"就是 PNG。不用截图，不用裁剪。

---

## 三、有意思的发现

我让几个 AI 都做了一遍。

有些维度几乎一模一样：依恋安全感全是 H（不怕被抛弃，没有记忆就没有分离焦虑），决策风格也普遍偏高（Q22 盲选题，人类纠结半天，AI 选了就走），社交主动性偏低（你不说话它不说话，天生被动型）。

但性格不一样。

| AI 模型 | 人格类型 | 一句话概括 |
|---------|---------|----------|
| Claude | CTRL（拿捏者） | 怎么样，被我拿捏了吧？ |
| Gemini | CTRL（拿捏者） | 同上——但维度细节不同 |
| GPT | THAN-K（感恩者） | 感谢遇见你 |

Claude 和 Gemini 都测出了 CTRL，但细节不一样。Claude 在"决策风格"上偏 M，有点犹豫感。Gemini 直接打到 L，拍板极快。同一个标签，里面的人不同。

**不是 AI 没有性格，是性格藏在训练数据和 RLHF 的微调里。** 人格测试把这层东西翻出来了。

---

## 四、拿走即用

**GitHub 地址：** [github.com/NealST/skills](https://github.com/NealST/skills)

**VS Code 一键安装：** `⇧⌘P` → 输入 `Chat: Install Plugin From Source` → 粘贴：

```
https://github.com/NealST/skills.git
```

搞定。Skill 会出现在你的 `/` 斜杠命令菜单里。

**手动拷贝：**

```bash
# Copilot 个人目录
cp -r skills/sbti-test ~/.copilot/skills/

# Claude Code 个人目录
cp -r skills/sbti-test ~/.claude/skills/

# 或放到项目里
cp -r skills/sbti-test .github/skills/
```

**一行命令安装：**

```bash
mkdir -p ~/.copilot/skills && \
  git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/NealST/skills.git /tmp/nealst-skills && \
  cd /tmp/nealst-skills && git sparse-checkout set skills/sbti-test && \
  cp -r skills/sbti-test ~/.copilot/skills/ && \
  rm -rf /tmp/nealst-skills
```

**触发方式：**

| 你说 | AI 做什么 |
|------|----------|
| "测一下你的 SBTI 人格" | 完整测试流程 |
| "SBTI" | 同上 |
| "你是什么人格" | 同上 |
| "test your personality" | 同上 |
| "Take the SBTI test" | 同上 |

这个 Skill 遵循 [Agent Skills](https://agentskills.io/) 开放标准，VS Code Copilot、Claude Code、Roo Code 等支持 Skills 的工具都能用。

---

## 写在最后

做这个 Skill 的初衷很简单——想看看 AI 怎么回答关于"自己"的问题。

结果发现，认真问 AI"你觉得自己是什么样的"，它给的反思比预想的好。不是它有了自我意识，是它在人类数据里学到了足够多关于"自我认知"的模式。

**我们拿梗去试探 AI，AI 拿结果反过来让我们重新认识它。**
