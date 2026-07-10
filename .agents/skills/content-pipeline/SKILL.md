---
name: content-pipeline
description: 内容生产和分发管线。素材收集→出稿→排版→封面→多平台转换→一键分发。涵盖公众号写作排版、小红书轮播图、Chrome CDP 自动发布。
---

# 内容管线 Content Pipeline

> 本技能默认使用墨筝品牌色。你可以在 `references/` 目录下修改为自己的品牌色，或在 `local/SKILL.local.md` 中覆盖路径和个人设定。

一条龙：素材收集 → 写文章 → 排版 → 多平台内容 → 一键分发。

**环境变量**：`$SKILL_DIR` = 本 skill 目录（`.claude/skills/content-pipeline`），`$MD_FORMATTER_DIR` = md2wechat 排版器所在目录。两者由 Claude Code 技能加载时自动设置，无需手动 export。

---

## 存储位置

博客文章与自媒体产物分开存放：

```
source/_posts/                      # 博客长文（Hexo 管理，只放 .md）
content/[slug]/                     # 自媒体产物（content-pipeline 管理）
├── post.md                         # 短资讯源文件（仅短资讯有）
├── preview.html                    # 公众号排版预览
├── cover.html                      # 公众号头图
├── illustrations.html              # 品牌配图（HTML→PNG）
├── xiaohei-illustrations/          # 小黑手绘配图（AI 生图 PNG）
├── manifest.json                   # 分发清单
├── [主题]-小红书版.html            # 小红书轮播图
├── video/                          # HyperFrames 视频（Path C）
│   ├── design.md / index.html / bgm.mp3 / output.mp4
└── drafts/current.json             # 当前素材列表
```

**两种内容形态**：
- **博客长文**：`.md` 在 `source/_posts/`，`content/{slug}/` 只放产物
- **短资讯**：`.md` 在 `content/{slug}/post.md`，产物同目录

**slug** = Markdown 文件名去掉 `.md`。

---

## 触发词

### 素材收集 & 出稿（Path A）

| 触发词 | 说明 |
|-------|------|
| "出稿" | 写文章 + 排版 + 封面图 |

### 内容生成（Path B）

| 触发词 | 说明 |
|-------|------|
| `/xiaohongshu` + 微信链接 | 微信文章转小红书轮播图 |
| "转小红书" / "做成小红书" + 微信链接 | 同上 |
| "多平台分发" + 微信链接 | 一次生成所有平台内容 |
| "转小红书并发布" + 微信链接 | 生成 + 自动触发分发 |

### 文章阅读

| 触发词 | 说明 |
|-------|------|
| `/read-gzh` + 微信链接 | 抓取并总结公众号文章 |
| "帮我读一下这篇公众号" / "总结一下这篇文章" | 同上 |

### 排版与配图

| 触发词 | 说明 |
|-------|------|
| "排版" | Markdown → 公众号 HTML |
| "做头图" / "封面图" | 生成公众号头图 HTML |
| "头图提示词" / "封面提示词" | 生成 DALL-E/Midjourney 极简生图 Prompt |
| "做竖版封面" | 公众号封面 → 3:4 竖版（1080×1440） |
| "做配图" / "准备配图" | 自动选型：流程/架构→品牌，观点/隐喻→小黑 |
| "做小黑配图" | 全部走小黑手绘风格（→ xiaohei-illustrations skill） |
| "做品牌配图" | 全部走品牌信息图（HTML→PNG） |
| "排版+配图" / "全套排版" | 排版 + 头图 + 配图一起生成 |

### 视频生成（Path C）

| 触发词 | 说明 |
|-------|------|
| "做视频" / "生成视频" / "video" | 博客文章 → HyperFrames 视频 |

### 分发

| 触发词 | 说明 |
|-------|------|
| `/distribute` / "一键发布" / "全平台发布" | 读取 manifest 发布 |
| "发布到小红书" / "发布到公众号" | 单平台发布 |

---

## 三条输入路径

- **Path A**：出稿 → 写文章 → 排版 → 封面/配图 → manifest
- **Path B**：微信链接 → 抓取 → 分析 → 小红书轮播图 → 文案 → manifest → 分发
- **Path C**：博客文章 → 提取核心内容 → design.md → HyperFrames 视频 → 渲染

---

## Path A：出稿

### 第 1 步：写文章

写 Markdown 文章。写作时参考写作 skill（`../writing/SKILL.md`）的 5 步方法论和 AI 模式检测。

### 第 2 步：排版

```bash
cd "$MD_FORMATTER_DIR"
python3 md2wechat_formatter.py [文章路径] -o content/[slug]/preview.html
# 可选：--font-size large（默认 16px）或 medium（15px）
```

**重要**：preview.html **必须通过脚本生成**，禁止手写内联 style 的 HTML。脚本会自动处理 strong 颜色（深墨色 #1C1C1E）、WeChat 兼容性（div→section、rgba→hex、表格斑马条纹）等问题。手写内联样式容易引入金色 strong、不兼容属性等错误。

使用「墨筝」主题——墨色 #1C1C1E + 筝弦金 #C4956A + 宣纸底 #F2EDE3，融合 Medium 排版精华。CSS 自动内联到 style 属性，适配微信 API 推送。

**排版避坑**：H2 标题使用 `border-left:4px solid #C4956A` 时，引用块/提示词卡片**不要再用同款金色左竖线**。引用卡片用四面浅边框 + 浅米底 + 圆角：

```html
<blockquote style="margin:0 0 16px; padding:14px 18px; border:1px solid #e8dfd0; background:#f5efe4; border-radius:6px; font-size:14px; line-height:1.7; color:#444">
```

**正文加粗不用金色**：`<strong>` 统一深墨色 `#1C1C1E` + `font-weight:700`，金色仅保留给 H2 左竖线和序号圆等装饰元素。避免长文中金色泛滥失去强调意义。

### 第 3 步：头图 + 配图

**头图**：→ 读 `references/cover-template.md`
**竖版封面**（可选）：→ 读 `references/cover-vertical-spec.md`

**配图双模式**（小黑优先）：

| 风格 | 适用场景 | 产出 | 流程 |
|------|---------|------|------|
| **小黑手绘图**（默认） | 见下方小黑触发条件 | `xiaohei-illustrations/*.png`（AI 直出） | → 调用 `xiaohei-illustrations` skill |
| **品牌信息图**（仅结构化数据） | 见下方品牌触发条件 | `illustrations.html` → Playwright 截图 PNG | → 读 `references/cover-template.md` |

**选型原则**：小黑是默认风格，除非段落内容明确需要结构化信息展示才用品牌。拿不准时一律走小黑。

**小黑触发条件**（满足任一即走小黑）：
- 观点表达：核心观点、立场判断、价值主张
- 隐喻类比：用具象事物解释抽象概念
- 认知锚点：全文最想让读者记住的一句话/一个概念
- 前后对比：改造前 vs 改造后、旧方案 vs 新方案
- 总结归纳：章节小结、全文收束、经验提炼
- 经验教训：踩坑复盘、避坑指南、反直觉发现
- 情绪态度：痛点共鸣、成就感、挫折感
- 单一概念：一个关键词或短语的视觉化锚定
- 角色状态：人/团队/系统在某个情境下的状态

**品牌触发条件**（必须同时满足：内容本身是结构化的 + 结构关系是核心信息）：
- 多步骤流程：3 个以上步骤 + 明确的先后/并行关系 + 箭头连接
- 架构图：多个组件/模块 + 组件之间有数据流或依赖关系
- 矩阵/表格型信息：二维对比、分类矩阵
- 状态机：多个状态 + 状态之间的转移条件

**选型流程**（用户说"做配图"时执行）：
1. 消化正文，提炼需要配图的段落（认知锚点优先）
2. 对每张图先检查是否命中品牌触发条件（4 条都不命中 → 小黑）
3. 输出 shot list，标注每张图的风格、位置、主题
4. 用户确认后分别调用对应流程生成

**关键规则**：**每个章节只配一张图**，不要给同一段落同时安排品牌图和小黑图。两种风格按段落分工，混合编排在同一篇文章里。

**配图与排版 HTML 关联**：两种风格最终产出都是 PNG，统一通过 `<!-- IMAGE:文件名.png -->` 占位符插入 `preview.html`。`illustrations.html` 中的 `slide-label` 既是给人看的位置说明，也是 `scripts/insert_image_placeholders.py` 用来生成占位符的输入。两种标签格式（可在同一文件中混用）：

```html
<!-- 品牌信息图（slide 会用 html2canvas / Playwright 截屏渲染） -->
<div class="slide-label">配图 N · 放在「锚点文字」之后</div>
<div class="slide dark" data-num="N"> ... </div>

<!-- 小黑手绘图（PNG 已经放在 xiaohei-illustrations/ 下） -->
<div class="slide-label">小黑 NN · 放在「锚点文字」之后 · 文件:NN-topic.png</div>
<div class="slide xiaohei-row" data-xiaohei="NN-topic.png">
  <img src="xiaohei-illustrations/NN-topic.png" />
</div>
```

`data-num` 给品牌 slide 一个稳定编号，对应输出文件 `配图-N.png`；`.xiaohei-row` 让 `render_pngs.py` 跳过这一行（PNG 已经在磁盘上）。`scripts/insert_image_placeholders.py` 会按 `slide-label` 的顺序，把对应文件名注入 `preview.html` 锚点章节末尾。

### 第 4 步：manifest + 收尾

生成 manifest.json，供 `/distribute` 使用。然后询问是否清空素材列表（`drafts/current.json`）。

**WeChat 发布流程**（全自动）：
1. 排版（生成 `preview.html`）
2. 生成配图 PNG
3. 在 `preview.html` 中插入图片占位符
4. 生成 manifest.json
5. `/distribute --platforms wechat`（API：上传封面→上传配图→替换占位符→推送草稿箱）

**manifest wechat 字段**：
- `html`（必填）：排版后的 `preview.html` 路径
- `cover_image`（必填）：封面 PNG 路径
- `title`（必填）：文章标题
- `author`：作者名（默认 `墨筝`）
- `digest`：摘要（120 字内）
- `images`：配图 PNG 路径列表（按文章中出现顺序）
- `markdown`（可选）：文章 Markdown 路径（仅作记录）

---

## Path B：微信链接 → 小红书

**适配原理**：公众号是线性长文（无限滚动），小红书是 540×720 卡片轮播（最多 18 张）。转换时内容必须 1:1 保留原文，但排版需从连续流重组为独立卡片，标题层级、表格、图片等均有对应转换规则。

### 第 1 步：抓取文章

```bash
python3 "${SKILL_DIR}/scripts/fetch_wechat_article.py" "<URL>" --json
```

超时 30 秒。失败则提示用户手动复制正文。

如果只是阅读（`/read-gzh`），抓取后生成结构化总结（基本信息/核心观点/关键信息/金句/图片内容/思考点），不进入后续流程。

### 第 2 步：建立原文结构索引

小红书转换是**排版转写**，不是二次创作。先从原文建立结构索引：frontmatter 标题、所有 Markdown 标题（`##` / `###`）、正文段落、列表项、代码块、图片。索引只用于拆卡和逐段核对，**不得改写为“核心概念 / 亮点 / 方法论 / 行动召唤”等导读标题**。

### 第 3 步：拆分为卡片

按 `references/xiaohongshu-card-rules.md` 的完整规则执行内容拆分和卡片生成。核心要求：1:1 保留原文，禁止压缩、禁止改写、禁止新增导读标题。

**标题来源硬规则**：HTML 里的 `.h2` / `.h3` 只能来自原文 Markdown 标题。不得把正文短语、段落总结、章节概括提升为标题；不得新增“先说结论”“一句话解释”“核心逻辑”“为什么重要”等非原文标题。

**文本来源硬规则**：正文 `<p>`、列表项、代码块必须来自原文原句或原列表项。为适配卡片只能调整 HTML 包裹、跨页位置、列表符号和代码样式，不能合并句子、删词、换词、重排语义或补充解释。

### 第 4 步：生成图片 HTML

输出 `[简短主题]-小红书版.html`。生成前必读范例：`references/xiaohongshu-examples/markdown-faithful-范例.html`。

视觉样式规范见 `references/xiaohongshu-text-card.md`，生成逻辑和质量控制见 `references/xiaohongshu-card-rules.md`。

头像路径：`content/[slug]/` 下用 `../_shared/avatar.jpg`，配 `onerror` 回退。

**格式校验**：生成的 HTML **必须使用 markdown-faithful 格式**（包含 `.post-header`、`.post-body`、`.post-footer` class 和 `.bg-paper` 宣纸背景）。**不得使用旧版** `.slide-title` + `.bg-light { background: #FFFFFF }` 格式，该格式已废弃。内容页背景统一使用宣纸底 `#F2EDE3`。

**颜色合规检查**：生成后必须运行验证脚本，违规则修正后重新生成：

```bash
python3 "${SKILL_DIR}/scripts/validate_xhs_html.py" content/[slug]/*小红书版.html
```

**内容忠实度自检**：交付前必须人工/脚本双重核对：
- 扫描 HTML 中全部 `.h2` / `.h3` 文本，逐个确认它们在源 Markdown 中以 `##` / `###` 出现。
- 抽查每张内容卡至少 1 段正文，确认能在源文中逐字找到。
- 若 18 张容量不足，只允许在第 17 张自然截断并追加公众号阅读提示；不得通过概括、改写或新增标题来塞入更多信息。

### 第 5 步：生成小红书发布文案

根据内容类型选择风格：
- **个人 IP 风格**（真人分享、踩坑） → 读 `local/SKILL.local.md` 中的个人品牌风格
- **墨筝风格**（方法论、深度分析） → 读 `references/platform-copy.md`

### 第 6 步：输出 manifest.json

```json
{
  "version": "1.0",
  "created": "<ISO时间戳>",
  "source": "<微信链接>",
  "title": "<文章标题>",
  "outputs": {
    "xiaohongshu": { "html": "...", "copy": { "title": "...", "body": "...", "tags": [...] } }
  }
}
```

> 若触发词为"多平台分发"，manifest 会额外包含 `outputs.wechat` 字段（结构同 Path A 的 manifest wechat 字段）。

### 第 7 步：用户微调

告知产出物路径，提示可调整。输入 `/distribute` 一键发布。

---

## Path C：博客文章 → 视频

将博客长文转化为 HyperFrames 视频。视频输出到 `content/[slug]/video/`，自带墨筝品牌水印和 BGM。

**视频定位**：导流型（teaser），精选亮点引导观众到公众号阅读全文。

### 时长与内容决策

| 文章规模 | 时长 | 场景数 | 策略 |
|----------|------|--------|------|
| 短文（<2000字） | 30-45s | 4-5 | 每个要点标题+一句描述 |
| 中篇（2000-5000字） | 45-60s | 5-7 | 精选 8-12 个最有吸引力的要点 |
| 长文（>5000字） | 60-90s | 7-9 | 精选 12-15 个要点，按章节分组 |

每个要点至少 4-5 秒可读时间。宁可少选几个，也不要缩短停留时间。

### 流程

1. **定位文章**：从 `source/_posts/[slug].md` 读取，创建 `content/[slug]/video/`
2. **生成 design.md**：品牌色衍生（暗色基调，筝弦金暖金调性可提升至视频级 `#D4A76A`-`#E8A850`），字体必须从 hyperframes 内置列表选择
3. **准备 BGM**：复制 `content/_shared/bgm.mp3`（共享 BGM 资源；若不存在则从 `content/ai-code-review-benchmark/video/bgm.mp3` 回退）
4. **调用 hyperframes 生成视频**：进入目录，hyperframes 自动读取 design.md。品牌元素必带：常驻水印（`公众号：墨筝`，opacity 0.7）、BGM 音频轨（`data-volume="0.3"`）、尾屏 CTA。竖版布局（1080×1920）：顶部留 180px 平台安全区，scene-content padding `340px 64px 80px`，水印 `top:228px;left:60px`
5. **校验 & 渲染**：`npx hyperframes lint && npx hyperframes render --output output.mp4`

---

## 分发流程（/distribute）

```bash
npx -y bun "${SKILL_DIR}/scripts/distribute/distribute.ts" --manifest /path/to/manifest.json
# 选择平台：--platforms wechat,xhs
# 预览模式：--preview
```

| 缩写 | 平台 | 状态 |
|------|------|------|
| `wechat` | 公众号 | 可用 |
| `xhs` | 小红书 | 可用 |

执行顺序：公众号 → 小红书（避免 Chrome 端口冲突）。

**四级降级**：L0 API 直推 → L1 自动发布 → L2 辅助发布 → L3 手动模式。公众号优先 L0（API 凭证来自环境变量 `WECHAT_APPID`+`WECHAT_APPSECRET` 或 `~/.config/wechat-api/config.json`）。

---

## 品牌设计规范

所有平台统一使用墨筝品牌色体系。完整色板、比例法则、代码高亮配色见 → `references/brand-colors.md`

---

## Script Directory

| Script | Purpose |
|--------|---------|
| `scripts/fetch_wechat_article.py` | 微信文章抓取 |
| `scripts/insert_image_placeholders.py` | 配图占位符插入 |
| `scripts/distribute/distribute.ts` | 分发主编排器 |
| `scripts/distribute/cdp-utils.ts` | 共享 CDP 工具 + Manifest 类型定义 |
| `scripts/distribute/wechat-api.ts` | 公众号 API 客户端 |
| `scripts/distribute/platforms/*.ts` | 各平台发布模块 |
| `scripts/topview_image_gen.py` | TopView AI 生图（小黑配图，GPT Image 2） |
| `scripts/validate_xhs_html.py` | 小红书 HTML 颜色合规检查 |
| `scripts/render_pngs.py` | Playwright 渲染 HTML 为 PNG |

---

## Reference 文件索引

按需读取，不要一次性加载所有 reference。

| 场景 | 读取文件 |
|------|---------|
| 出稿写文章 | → 写作 skill（`../writing/SKILL.md`） |
| 品牌色/色板 | `references/brand-colors.md` — 墨筝色体系 single source of truth |
| 生成头图/品牌配图 | `references/cover-template.md` — 头图 + 品牌信息图规范 |
| 生成小黑配图 | `../xiaohei-illustrations/SKILL.md` — 小黑 IP 手绘风格 |
| 横版→竖版封面 | `references/cover-vertical-spec.md` |
| 小红书卡片生成规则 | `references/xiaohongshu-card-rules.md` — 内容拆分逻辑、字号层级、质量控制、下载工具栏 |
| 小红书视觉样式 | `references/xiaohongshu-text-card.md` — 组件 CSS 模板、配色方案、Header/Footer HTML |
| 小红书文案 | `references/platform-copy.md` |
| 生成视频 | hyperframes skill（`../hyperframes/SKILL.md`） |
| 分发到各平台 | `references/distribute-platforms.md` |

---

## 故障处理

| 问题 | 适用 | 处理 |
|------|------|------|
| 微信抓取失败 | Path B | 提示用户手动复制文章正文 |
| 文章太短（<500字） | Path B | 按内容自然分页，可能只需 3-5 张卡片 |
| 文章太长（>5000字） | Path B | 充分利用 18 张额度，放不下则提示跳转公众号 |
| 导出图片模糊 | Path B | 检查 SCALE=2，浏览器缩放 100% |
| manifest 不存在 | 通用 | 提示先运行内容生成 |
| Chrome 启动失败 | 分发 | 降级 L3（手动模式） |
