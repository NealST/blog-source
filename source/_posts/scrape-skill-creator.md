# Scrape Skill Creator，把任意文档网站变成 AI 编程助手的 skill

最近在公司内部做一些 agent 基建，但遇到一个问题：公司内部很多技术框架和组件的资料只提供了网站可以查看，没有任何可被 AI 消费的文档素材。

这就导致 agent 无法写出与内部框架和组件相契合的代码，达不到生产级的水准。于是，我写了一个 Skill —— Scrape Skill Creator

## 它能帮你做什么？

一句话：**只需要给一个网站 URL，它就能自动生成一个 AI Agent 可调用的 Skill。**

具体来说：

**场景 1：内部 API 文档 → AI 技能**

公司有一套内部 RPC 框架，文档在内网 Wiki 上。装上这个 skill 后：

```
/scrape-skill-creator https://wiki.internal.com/rpc-api
```

AI 助手就能直接调用正确的 API，知道入参、返回值、错误码，不再瞎编。

**场景 2：第三方 SDK 文档 → AI 技能**

某个 SDK 刚发了新版本，Claude 的训练数据还没覆盖到：

```
/scrape-skill-creator https://docs.newservice.io/v3/api
```

几分钟后，你的 AI 助手就掌握了最新版的用法。

**场景 3：一整套文档站 → 多个专项技能**

一个文档站有十几个模块？它会自动识别侧边栏结构，按模块拆分，每个模块生成独立的 skill，互不干扰。

---

## 为什么不直接把文档丢给 AI？

你可能会想：我直接把网页内容粘到对话里不就行了？

问题是：

1. **上下文窗口有限** —— 一个完整的 API 文档有可能动辄几万字，塞不进去
2. **每次对话都要重复** —— 下次开新会话又得重新粘贴
3. **格式混乱** —— 网页直接复制的文本夹杂导航栏、页脚、广告
4. **没有结构** —— AI 很难从一坨文字里精确定位到你要的那个方法

Scrape Skill Creator 可以自动解决这些问题：

- 自动过滤导航、页脚、弹窗等噪音内容
- 结构化为逐方法的 Markdown（参数表格、代码示例、错误码）
- 生成标准 Skill 格式，AI 助手按需加载，不占用对话上下文
- 一次生成，永久可用，团队共享

---

## 它是怎么工作的？

整个流程分五步，全自动：

```
发现站点结构 → 爬取页面 → 解析内容 → 生成 Skill → 校验输出
```

**第一步：智能发现**

给定一个 URL，它不只爬这一页。它会分析侧边栏，找出整个文档的结构树：

```
发现 23 个页面：
  Router 模块（当前）: createRouter, useRoute, useRouter
  Store 模块: createStore, defineStore, storeToRefs
  Composables: useFetch, useHead, useState
建议爬取: Router 模块（3 页）。其他模块可作为独立 skill。
继续？
```

支持 Docusaurus、VitePress、Nextra、GitBook、Mintlify 等主流文档框架。

如果发现有不支持的，可以在 issue 中贴反馈。

**第二步：深度爬取**

不是简单的 `fetch` 请求。它用 agent-browser 模拟真实浏览器：

- 自动展开折叠的 `<details>` 区块
- 点击所有 Tab 面板，抓取每个标签页的内容
- 关闭 Cookie 弹窗、登录遮罩
- 滚动到底部触发懒加载
- 智能重试 + 限速，不会被封 IP

**第三步：结构化解析**

把原始文本变成 AI 友好的格式：

```markdown
### Router.push

异步方法，导航到指定路由。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| to | RouteLocationRaw | 是 | 目标路由 |

​```ts
import { useRouter } from 'vue-router'
const router = useRouter()
await router.push('/users/1')
​```
```

**第四步：生成标准 Skill**

输出兼容 Claude Code 和 GitHub Copilot 两套体系的文件结构：

```
.claude/skills/vue-router/
├── SKILL.md
└── references/
    └── api.md

.agents/skills/vue-router/
├── SKILL.md
└── references/
    └── api.md
```

**第五步：自动校验**

`doctor.py` 会检查：frontmatter 格式、文件编码、链接有效性、内容是否过期。有问题直接告诉你哪里要修。

---

## 怎么安装？

### 1. 安装依赖

```bash
# agent-browser（用于爬取网页）
brew install agent-browser && agent-browser install
# 或
npm install -g agent-browser && agent-browser install
```

### 2. 安装 Skill

```bash
# 安装为项目级 skill
git clone https://github.com/NealST/scrape-skill-creator.git \
  .claude/skills/scrape-skill-creator

# 或安装为用户级 skill（所有项目通用）
git clone https://github.com/NealST/scrape-skill-creator.git \
  ~/.claude/skills/scrape-skill-creator
```

安装完成，重启 Claude Code 即可使用。

---

## 怎么用？

### 最简单的方式：交互式向导

```bash
python3 scripts/wizard.py
```

向导会一步步引导你完成全部流程。

### 在 Claude Code 中直接调用

```
/scrape-skill-creator https://docs.example.com/api my-api-skill
```

或者用自然语言触发：

- "从这个网站做一个 skill"
- "把这个文档变成 skill"
- "scrape this site into a skill"

### 手动精细控制

```bash
# 发现
python3 scripts/discover.py https://docs.example.com/api --out discovered.json

# 爬取
python3 scripts/crawl.py urls.json --out /tmp/pages --qps 1.0

# 生成
python3 scripts/gen_skills.py manifest.json --pages /tmp/pages --out ./skills/

# 校验
python3 scripts/doctor.py ./skills/
```

---

## 一些使用建议

1. **不要只爬一页** —— 工具会自动发现侧边栏结构，让它帮你决定爬取范围
2. **锁定版本号** —— 用 `/v3/api` 而不是 `/latest/api`，避免内容过期
3. **大站点拆分** —— 超过 20 页的模块建议拆成多个 skill，每个职责清晰
4. **定期更新** —— 文档更新后重新跑一次流水线，保持 skill 与源站同步
5. **不用局限于特定网站** —— 比如你可以把看到的一些优质踩坑和实践总结的博客也提取下来变成 skill。

---

## 写在最后

AI 编程助手的能力边界，除了模型本身，还取决于它能获取到的知识。

Scrape Skill Creator 做的事情很简单：把网上的知识，变成 AI 能用的 Skill。

项目开源，欢迎 Star 和贡献：

GitHub: https://github.com/NealST/scrape-skill-creator

---

*如果觉得有用，欢迎转发给你的团队。有问题可以在 GitHub Issues 中反馈。*
