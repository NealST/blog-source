---
name: content-pipeline
description: 内容生产和分发管线。素材收集→出稿→排版→封面→多平台转换→一键分发。涵盖公众号写作排版、小红书轮播图、视频生成，Chrome CDP 自动发布。正文配图按语义选型：观点与隐喻调用 xiaohei-illustrations，架构、流程、状态、关系与数据图表调用 diagram-design。
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
├── diagrams/                       # diagram-design 单图源文件（自包含 HTML）
├── xiaohei-illustrations/          # 小黑手绘配图（AI 生图 PNG）
├── manifest.json                   # 分发清单
├── [主题]-小红书版.html            # 小红书轮播图
├── video/                          # 视频产物（Path C，按后端分目录）
│   ├── hyperframes/                # design.md / index.html / bgm.mp3 / output.mp4
│   └── handdraw/                   # job.json / inputs / work / outputs/film.mp4
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
| "做头图" / "封面图" | 根据文章内容生成 TopView 公众号头图 |
| "头图提示词" / "封面提示词" | 生成 DALL-E/Midjourney 极简生图 Prompt |
| "做竖版封面" | 公众号封面 → 3:4 竖版（1080×1440） |
| "做配图" / "准备配图" | 自动选型：结构/数据→diagram-design 品牌图，观点/隐喻→小黑 |
| "做小黑配图" | 全部走小黑手绘风格（→ xiaohei-illustrations skill） |
| "做品牌配图" / "做架构图" / "做流程图" | 结构化图调用 diagram-design（HTML→PNG）；不适合成图的列表保留文字或表格 |
| "优化原图" / "统一插图风格" / "图片中文化" | 审核文章已有插图；必要时用 Topview image edit 统一风格并翻译图中文字 |
| "排版+配图" / "全套排版" | 排版 + 头图 + 配图一起生成 |

### 视频生成（Path C）

| 触发词 | 说明 |
|-------|------|
| "做视频" / "生成视频" / "video" | 博客文章 → 视频；默认 HyperFrames |
| "手绘视频" / "白板动画" / "边画边讲" | 博客文章 → Sweety Handdraw Video |

### 分发

| 触发词 | 说明 |
|-------|------|
| `/distribute` / "一键发布" / "全平台发布" | 读取 manifest 发布 |
| "发布到小红书" / "发布到公众号" | 单平台发布 |

---

## 三条输入路径

- **Path A**：出稿 → 写文章 → 排版 → 封面/配图 → manifest
- **Path B**：微信链接 → 抓取 → 分析 → 小红书轮播图 → 文案 → manifest → 分发
- **Path C**：博客文章 → 按内容/意图选择 HyperFrames 或 Handdraw → 渲染与验证

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

**头图**：默认使用 `scripts/topview_image_gen.py` 根据文章内容直接生图，再裁切为公众号头图比例。仅当用户明确要求可编辑模板时，才生成 `cover.html`。完整提示词策略见 `references/cover-template.md`。
**竖版封面**（可选）：→ 读 `references/cover-vertical-spec.md`

**TopView 头图生成流程**：
1. 提炼文章最有吸引力的单一矛盾、结果或视觉隐喻，优先使用具体数字、强反差或明确动作，不要把文章摘要直接画成图。
2. 设计一个占据画面 40%-60% 的核心视觉主体，并为标题预留稳定的负空间；画面必须在缩略图尺寸下仍能一眼识别。
3. 提示词应明确主体、动作、空间关系、光线、材质、主辅色和禁忌。默认要求无文字、无 Logo、无 UI 小字，避免生成错误文字；文章标题由公众号后台叠加或通过摘要承担。
4. 技术内容默认采用墨色背景、暖金关键光，可根据产品识别色加入一种高对比辅助色。避免常见的发光球、抽象网络、无主体数据流和堆叠界面截图。
5. 使用 TopView 生成 16:9、2K 原图，保存为 `content/[slug]/cover-source.png`，同时把完整提示词保存为 `content/[slug]/cover-prompt.txt`。
6. 将原图居中裁切为 2.35:1，再缩放到 `1800×766`，输出 `content/[slug]/cover.png`。不得直接拉伸 16:9 原图。
7. 生成后必须检查：主体是否被裁断、缩略图是否仍有视觉焦点、画面是否有错误文字、是否与文章主题直接相关。未通过则调整提示词重生成。

**配图双模式**（小黑优先）：

| 风格 | 适用场景 | 产出 | 流程 |
|------|---------|------|------|
| **小黑手绘图**（默认） | 见下方小黑触发条件 | `xiaohei-illustrations/*.png`（AI 直出） | → 调用 `xiaohei-illustrations` skill |
| **品牌结构图与数据图表** | 结构关系或数据分布是核心信息 | `diagrams/NN-topic.html` → 汇入 `illustrations.html` → PNG | → 读 `../diagram-design/SKILL.md` 和 `references/diagram-design-integration.md` |

**选型原则**：小黑是默认风格，除非段落内容明确需要结构化信息展示才用 diagram-design。拿不准时一律走小黑；普通列表或简单表格已经能讲清的内容，不必强行画图。diagram-design 是品牌结构图的设计引擎，不替代 TopView 头图或小黑手绘。

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
- 关系与时序：实体关联、调用先后、跨角色交接、依赖或拓扑变化
- 数据图表：有来源的数值、单位与比较口径，需要展示趋势、分布或数量关系

**冲突处理**：前后对比只表达观点或属性差异时仍走小黑或表格；若核心是组件连接、数据流或状态关系的变化，走 diagram-design。不得为凑图编造数值或关系。

**选型流程**（用户说"做配图"时执行）：
1. 消化正文，提炼需要配图的段落（认知锚点优先）
2. 逐张分析原文已有图片表达的核心语义，建立已有视觉信息清单；同时按 `references/source-image-localization.md` 判断风格适配与中文化价值
3. 对需要处理的原图调用已安装的 `topview-generate` skill，以 `image_edit` 生成主题适配的中文版；不满足条件的原图保持不变
4. 删除与处理后原图语义重复的候选配图；新图必须补充原图没有表达的观点、结构或数据
5. 对每张新图检查是否命中品牌触发条件；未命中 → 小黑，命中 → diagram-design；若表格/文字更清楚则取消该候选图
6. 输出 shot list，标注风格、位置、主题、与原图的差异；原图额外标注 `keep` / `localize` / `restyle+localize` 及判定理由；diagram-design 图额外标注图型、语义模式（如有）、尺寸预设、信息来源与计划删减项
7. 按对应技能生成。原图处理遵循 Topview 的首次计费确认与 MCP 流程；小黑保持原流程；diagram-design 按 `references/diagram-design-integration.md` 执行风格确认、单图设计、验证与 PNG 接入。用户要求直接生成可跳过 shot list 等待，但不能跳过计费确认、diagram-design 的首次品牌确认或覆盖 profile 的授权

**原文插图适配与中文化**：先判断图片的主要价值来自“信息解释”还是“原始证据”，不得见到英文就翻译。只有当自然语言文字是图片的主要信息载体，且中文化能明显降低理解门槛时，才考虑翻译或重绘；产品界面、社交平台原帖、官方文档、论文或基准原图、品牌素材、纪实照片等具有来源和证据价值的图片，默认保留原文，通过中文图注解释。只处理文章中已存在的内容型插图，不把截图、照片和品牌素材一律重绘。风格明显偏离墨筝主题时做视觉适配；图中存在会影响中文读者理解的外语标题、标签、图例、注释或流程节点时翻译为中文。代码、命令、API/产品名、商标、网址、数据和真实 UI 文案默认保留。使用 Topview `image_edit` 时必须保持原图事实、结构、节点关系、数值、单位和宽高比，不新增原文没有的信息；详细判定、提示词和验收规则见 `references/source-image-localization.md`。

处理后文件保存为 `content/[slug]/localized-images/NN-original-name.png`，Markdown、`preview.html`、小红书轮播与 manifest 均引用处理后的同一文件。原始图片不得覆盖；若编辑结果文字错误、关系变化、主体走样或可读性下降，回退原图并报告，不得带病发布。

**关键规则**：**每个章节只配一张图**，不要给同一段落同时安排品牌图和小黑图。两种风格按段落分工，混合编排在同一篇文章里。

**diagram-design 接入约定**：单图保存在 `diagrams/NN-topic.html`；将已验证的内联 SVG 与必要样式汇入 `illustrations.html` 的 `.slide[data-num="N"]`，不得用 iframe。每张图的 SVG ID 和样式作用域必须隔离。继续由 `render_pngs.py` 导出 `配图-N.png`，沿用下方 `slide-label`、占位符与 manifest 规则。默认纯白浅底、静态图，不直接沿用 diagram-design 的出厂配色；完整品牌映射、导出和检查步骤见集成参考。

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

头像路径：`content/[slug]/` 下用 `../_shared/avatar.jpg`，配 `onerror` 回退。真实头像必须绝对定位并完整覆盖底层“墨”字 fallback；头像加载成功时不得露出 fallback。

**关注提示硬规则**：每张文字卡、封面和封底的 Header 右侧必须放置两行右对齐文案：`关注我` / `持续更新 AI 实战`。使用 `margin-left:auto; text-align:right`，第一行金色加粗、第二行弱灰小字；原文图片独占页不添加。Footer 的公众号引导继续保留。

**原文图片硬规则**：Markdown 原图不是 540×720 文字卡的内嵌元素。先按 `references/source-image-localization.md` 完成原图审核与必要的 Topview 中文化，再把最终采用的图片作为独立轮播素材；保持原始宽高比导出，不加 Header/Footer/页码、底色、边框、圆角、阴影或 3:4 留白。

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

将博客长文转化为视频。先选择后端，产物分别输出到 `content/[slug]/video/hyperframes/` 或 `content/[slug]/video/handdraw/`，不得共用中间文件。

**视频定位**：导流型（teaser），精选亮点引导观众到公众号阅读全文。

### 后端选择

- **HyperFrames（默认）**：数据对比、产品演示、UI、代码和快速动效摘要。
- **Sweety Handdraw Video**：故事、观点、机制讲解、寓言，以及用户明确要求手绘视频、白板动画或边画边讲。
- 用户只说“做视频”且两者都适合时使用 HyperFrames；不得同时生成两套昂贵产物。
- 后端一旦确定，不得在失败时静默切换。切换会改变视觉语言，必须告知用户并获得同意。

### 时长与内容决策

| 文章规模 | 时长 | 场景数 | 策略 |
|----------|------|--------|------|
| 短文（<2000字） | 30-45s | 4-5 | 每个要点标题+一句描述 |
| 中篇（2000-5000字） | 45-60s | 5-7 | 精选 8-12 个最有吸引力的要点 |
| 长文（>5000字） | 60-90s | 7-9 | 精选 12-15 个要点，按章节分组 |

每个要点至少 4-5 秒可读时间。宁可少选几个，也不要缩短停留时间。

### HyperFrames 流程

1. **定位文章**：从 `source/_posts/[slug].md` 读取，创建 `content/[slug]/video/hyperframes/`
2. **读取默认视频风格**：完整读取 `references/hyperframes-video-style.md`。除非用户明确指定其他风格，否则使用其中的技术编辑部视觉、固定墨筝色板、非对称信息图构图和动效规则
3. **生成 design.md**：以风格参考中的模板为基线，保留 `#1C1C1E`、`#F2EDE3`、`#C4956A`、`#D8B28C` 等固定色板；标题使用 `ZCOOL XiaoWei`，正文使用 `Noto Sans SC`，技术标签使用 `IBM Plex Mono`
4. **准备共享资产**：复制 `content/_shared/bgm.mp3` 为项目根目录的 `bgm.mp3`；复制 `content/_shared/fonts/zcool-xiaowei.ttf` 和 `content/_shared/fonts/noto-sans-sc.ttf` 到项目的 `fonts/` 目录。若任一共享字体缺失则停止并报告，不得静默退回系统字体
5. **调用 hyperframes 生成视频**：进入目录，hyperframes 自动读取 design.md。品牌元素必带：常驻水印（`公众号：墨筝`，opacity 0.7）、BGM 音频轨（`data-volume="0.3"`）、尾屏 CTA。竖版布局（1080×1920）：顶部留 180px 平台安全区，scene-content padding `340px 64px 80px`，水印 `top:228px;left:60px`
6. **校验 & 草稿验收**：运行 lint 和 check；先渲染 draft，从每个场景中段提取关键帧，实际检查完整画布。工具检查失败时按风格参考中的降级流程执行，不得直接跳到最终渲染
7. **最终渲染**：关键帧通过后运行 `npx hyperframes render --output output.mp4 --quality high`，再用 `ffprobe` 核对时长、1080×1920、视频轨和 AAC 音轨

manifest 的 `outputs.video` 增加 `"backend": "hyperframes"`；旧 manifest 没有该字段时保持兼容。

### Handdraw 流程

执行前必须完整读取 `references/handdraw-video-integration.md` 和已安装的 `sweety-handdraw-video/SKILL.md`，由后者控制任务格式和质量门禁。核心顺序：

1. **环境检查**：读取固定安装版本，运行 `setup.sh --check`；确认生图能力和一条可用配音路径。不得静默安装依赖、下载大模型或购买服务。
2. **旁白先行**：从文章改编完整口播，保留事实、数字、来源和限定；真实音频生成 alignment，禁止手写时间戳。
3. **预算与分镜**：写 `design.json`、`storyboard.json`、drawing plan，先按旁白运行预算检查，再生成插画。
4. **素材门禁**：每张图先保存 brief/prompt 并绑定美术记录；先完成一个代表场景，通过看图、缩略图、线稿和部位检查后再扩展。
5. **构建与预览**：依次运行 `doctor`、`build`、`verify --assets-only` 和 15 秒代表段渲染，实际查看描线、填色、字幕和封面衔接。
6. **整片验收**：渲染 `outputs/film.mp4`，运行 `verify`；填写基于实际观察的 `review.json` 后才可 `finalize`。未实际听音必须保留 open check。

manifest 的 `outputs.video` 使用 `"backend": "handdraw"`，`path` 指向 `content/[slug]/video/handdraw/outputs/film.mp4`，并记录 cover、captions、script、verification、job 与 `"aigc": true`。发布时仍须显式声明“AI 生成”。

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
| 生成头图 | `references/cover-template.md` — 头图规范 |
| 原文插图风格适配与中文化 | `../topview-generate/SKILL.md` + `references/source-image-localization.md` — Topview image edit、翻译边界与验收 |
| 生成品牌结构图/数据图表 | `../diagram-design/SKILL.md` + `references/diagram-design-integration.md` — 图型设计、品牌适配、PNG 接入 |
| 生成小黑配图 | `../xiaohei-illustrations/SKILL.md` — 小黑 IP 手绘风格 |
| 横版→竖版封面 | `references/cover-vertical-spec.md` |
| 小红书卡片生成规则 | `references/xiaohongshu-card-rules.md` — 内容拆分逻辑、字号层级、质量控制、下载工具栏 |
| 小红书视觉样式 | `references/xiaohongshu-text-card.md` — 组件 CSS 模板、配色方案、Header/Footer HTML |
| 小红书文案 | `references/platform-copy.md` |
| 生成 HyperFrames 视频 | `references/hyperframes-video-style.md` + hyperframes skill（`../hyperframes/SKILL.md`） |
| 生成手绘视频 | `references/handdraw-video-integration.md` + 已安装的 sweety-handdraw-video skill |
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
| Topview MCP 未连接或未认证 | 原文插图处理 | 停止图片编辑，按 `topview-generate` skill 引导宿主连接 `topview-mcp` 或完成登录；不得改走旧 REST API |
| Handdraw render venv 缺失 | Path C | 报告 `setup.sh` 命令，征得用户同意后安装 |
| Handdraw 无生图或配音能力 | Path C | 停止并说明缺失能力，不生成纯文字片、不静默切换后端 |
