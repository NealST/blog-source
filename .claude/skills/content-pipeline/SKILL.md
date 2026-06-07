---
name: content-pipeline
description: 内容生产和分发管线。素材收集→出稿→排版→封面→多平台转换→一键分发。涵盖公众号写作排版、小红书轮播图、Chrome CDP 自动发布。
---

# 内容管线 Content Pipeline

> 本技能默认使用墨筝品牌色。你可以在 `references/` 目录下修改为自己的品牌色，或在 `local/SKILL.local.md` 中覆盖路径和个人设定。

一条龙：素材收集 → 写文章 → 排版 → 多平台内容 → 一键分发。

---

## 存储位置

博客文章与自媒体产物分开存放，支持两种内容形态：

```
source/_posts/                      # 博客长文（Hexo 管理，只放 .md）
├── [文章标题].md
└── ...

content/[slug]/                     # 自媒体产物（content-pipeline 管理）
├── post.md                         # 短资讯源文件（仅短资讯有，长文的 .md 在 source/_posts/）
├── preview.html                    # 公众号排版预览
├── cover.html                      # 公众号头图
├── illustrations.html              # 文章配图
├── manifest.json                   # 分发清单
├── [主题]-小红书版.html            # 小红书轮播图
├── video/                          # HyperFrames 视频（Path C）
│   ├── design.md                   # 视频设计规范（从墨筝品牌衍生）
│   ├── index.html                  # 视频合成源文件
│   ├── bgm.mp3                     # 背景音乐（统一复制）
│   └── output.mp4                  # 渲染输出
└── drafts/
    └── current.json                # 当前素材列表
```

**两种内容形态：**
- **博客长文**（发博客 + 多平台分发）：`.md` 在 `source/_posts/`，`content/{slug}/` 只放产物
- **短资讯**（只做平台分发，不发博客）：`.md` 在 `content/{slug}/post.md`，产物同目录

**slug** = Markdown 文件名去掉 `.md`（如 `kimi-vs-opus.md` → `content/kimi-vs-opus/`）。

输出目录默认为 `content/[slug]/`。用户可指定其他路径，或在 `local/SKILL.local.md` 中配置默认路径。未指定目录时，多平台产出放 `/tmp/`。

### 命名规范

| 项目 | 规则 | 示例 |
|------|------|------|
| 文章 slug | Markdown 文件名去掉 `.md` | `kimi-vs-opus` |
| 产物目录 | `content/{slug}/` | `content/kimi-vs-opus/` |
| 短资讯源文件 | `post.md`（仅短资讯） | `content/ai-weekly-0512/post.md` |
| 排版预览 | `preview.html` | `content/kimi-vs-opus/preview.html` |
| 头图 | `cover.html` | `content/kimi-vs-opus/cover.html` |
| 配图 | `illustrations.html` | `content/kimi-vs-opus/illustrations.html` |
| 分发清单 | `manifest.json` | `content/kimi-vs-opus/manifest.json` |
| 小红书轮播 | `{主题}-小红书版.html` | `kimi-vs-opus-小红书版.html` |
| 视频目录 | `content/{slug}/video/` | `content/claude-code-tips-best-practices/video/` |
| 视频文件 | `video/index.html` | `content/claude-code-tips-best-practices/video/index.html` |
| 视频设计 | `video/design.md` | `content/claude-code-tips-best-practices/video/design.md` |
| 视频 BGM | `video/bgm.mp3`（统一复制） | `content/claude-code-tips-best-practices/video/bgm.mp3` |

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
| "转小红书" + 微信链接 | 同上 |
| "做成小红书" + 微信链接 | 同上 |
| "多平台分发" + 微信链接 | 一次生成所有平台内容 |
| "转小红书并发布" + 微信链接 | 生成 + 自动触发分发 |

### 文章阅读

| 触发词 | 说明 |
|-------|------|
| `/read-gzh` + 微信链接 | 抓取并总结公众号文章 |
| "帮我读一下这篇公众号" | 同上 |
| "总结一下这篇文章" | 同上 |

### 排版与配图

| 触发词 | 说明 |
|-------|------|
| "排版" | 用墨筝主题排版 Markdown → 公众号 HTML |
| "做头图" / "封面图" | 生成公众号头图 HTML（浏览器下载 PNG） |
| "头图提示词" / "封面提示词" | 生成贴合墨筝品牌的 DALL-E/Midjourney 极简生图 Prompt（见 cover-template.md） |
| "做竖版封面" / "竖版头图" | 从公众号封面 → 生成 3:4 竖版封面（1080×1440），适合小红书/视频号 |
| "做配图" / "准备配图" | 生成文章配图 HTML（浏览器下载 PNG） |
| "排版+配图" / "全套排版" | 排版 + 头图 + 配图一起生成 |

### 视频生成（Path C）

| 触发词 | 说明 |
|-------|------|
| "做视频" / "生成视频" / "video" | 博客文章 → HyperFrames 视频 |

### 分发

| 触发词 | 说明 |
|-------|------|
| `/distribute` | 读取 manifest 一键发布 |
| "一键发布" | 全平台发布 |
| "全平台发布" | 同上 |
| "发布到小红书" | 单平台发布 |
| "发布到公众号" | 单平台发布 |

---

## 三条输入路径

### Path A：出稿

```
写文章 → 排版 → 封面图 → manifest
```

适用场景：写完 Markdown 后继续排版/封面/分发流程。写作时参考写作 skill（`../writing/SKILL.md`）的方法论和 AI 模式检测。

### Path B：微信链接 → 小红书内容

```
微信链接 → 抓取文章 → 分析结构 → 生成小红书轮播图 → manifest → 分发
```

适用场景：已有公众号文章，一键转为小红书内容并发布。

### Path C：博客文章 → 视频

```
文章 → 提取核心内容 → 生成 design.md → HyperFrames 视频（含品牌+BGM）→ 渲染
```

适用场景：将博客文章转化为短视频，用于视频号/抖音等视频平台分发。调用 hyperframes skill 生成视频，自动继承墨筝品牌规范和 BGM。

---

## Path A 流程：出稿

### 写文章

写 Markdown 文章。写作时参考写作 skill（`../writing/SKILL.md`）的 5 步方法论和 30 类 AI 模式检测。

### 出稿后续步骤

7. **排版** — 调用排版工具生成 HTML 预览（墨筝主题）
8. **头图 + 配图** — 生成可下载的 HTML 文件（→ 读 `references/cover-template.md`）
   - **竖版封面（可选）**：用户说"做竖版封面"时，从已生成的公众号头图 HTML 转换 → 读 `references/cover-vertical-spec.md`
   - **配图与排版 HTML 的关联**：生成配图后，用 Playwright 截图为 PNG，然后运行 `python3 ${SKILL_DIR}/scripts/insert_image_placeholders.py <preview.html> <illustrations.html>` 自动在排版 HTML 的对应章节位置插入 `<!-- IMAGE:配图-N.png -->` 占位符。分发脚本会自动将配图上传到微信 CDN 并替换占位符为 `<img>` 标签。
   - **图片必须不透明（RGB，无 alpha）**：所有 html2canvas 导出的 PNG 必须在导出前调用 `flattenAlpha(canvas, bgColor)` 消除透明通道。详见 `references/cover-template.md` 中的 helper 函数。原因：微信等平台在白底上渲染透明 PNG，暗底封面会变白。
9. **manifest** — 生成 manifest.json，供 `/distribute` 使用。

   **WeChat 发布流程（全自动）**：
   1. 写文章（Markdown）
   2. 排版（`md2wechat_formatter.py` 生成 `_preview.html`）
   3. 生成配图 HTML → Playwright 截图为 PNG
   4. 在 `_preview.html` 中插入图片占位符 `<!-- IMAGE:文件名.png -->`
   5. 生成 manifest.json（包含所有路径）
   6. 执行 `/distribute --platforms wechat`（API 自动：上传封面→上传配图→替换占位符→推送草稿箱）

   wechat 部分字段说明：
   - `wechat.html`（**必填**）：排版后的 `_preview.html` 路径（配图位置用 `<!-- IMAGE:文件名.png -->` 标记）
   - `wechat.cover_image`（**必填**）：封面 PNG 路径
   - `wechat.title`（**必填**）：文章标题
   - `wechat.author`：作者名（默认 `墨筝`）
   - `wechat.digest`：文章摘要（120 字内）
   - `wechat.images`：配图 PNG 路径列表（按文章中出现的顺序排列，分发脚本会上传并插入到对应占位符位置）
   - `wechat.markdown`（可选）：文章 Markdown 路径（仅作记录，不再用于转换）
10. **询问** — 是否清空当前素材

### 排版命令（**仅公众号 preview.html**）

> **Scope 警告**：本节规则只针对公众号产物 `preview.html`，由 `md2wechat_formatter.py` 渲染，使用 `<section>` 标签 + 内联 CSS 适配微信 API。
>
> 公众号默认正文字号 `large = 16px` / `medium = 15px`，与小红书的 18-19px 完全不同。**不要把 Path B 第 3-4 步里小红书的 `.slide` 卡片结构、27/22/19px 标题层级、html2canvas 下载工具栏混入公众号 preview.html**。

```bash
cd "$MD_FORMATTER_DIR"
python3 md2wechat_formatter.py [文章路径] -o content/[slug]/preview.html
# 可选参数：--font-size large（默认 16px）或 medium（15px）
```

> `$MD_FORMATTER_DIR` 需在 `local/.env` 或环境变量中配置。
> `-o` 参数指定输出到 `content/[slug]/` 目录，保持博客文章与产物分离。
> CSS 自动内联到 style 属性，适配微信 API 推送。输出的 `preview.html` 使用 `<section>` 标签确保微信兼容。

使用统一的「墨筝」主题——墨色 #1C1C1E + 筝弦金 #C4956A + 宣纸底 #F2EDE3，融合 Medium 排版精华。
推荐字号：`large`（16px，默认）、`medium`（15px）

### 排版避坑：视觉元素的"金色左竖线"冲突

H2 标题使用 `border-left:4px solid #C4956A` 时，正文中的引用块（blockquote / 提示词卡片）**不要再用同款金色左竖线**，否则两块紧挨时视觉重复，H2 的"分章"地位被削弱。

**正确分工**：
- **H2 标题**：金色左竖线（4px）+ 12px 左 padding —— 负责"分段锚点"
- **引用 / 提示词卡片**：四面浅边框 + 浅米底 + 圆角 —— 负责"信息容器"，安静不抢戏

**推荐的引用卡片内联样式**（已验证）：
```html
<blockquote style="margin:0 0 16px; padding:14px 18px; border:1px solid #e8dfd0; background:#f5efe4; border-radius:6px; font-size:14px; line-height:1.7; color:#444">
  <!-- 内容 -->
</blockquote>
```

**双语提示词约定**：中文用正常样式，英文原文紧跟一行，颜色 `#7a6952` + `font-style:italic`，作为可静音的参考信息。

---

## Path B 流程：微信链接 → 小红书内容

### 第 1 步：抓取文章

使用 Python 抓取脚本（微信有反爬验证，WebFetch 会被拦）：

```bash
python3 "${SKILL_DIR}/scripts/fetch_wechat_article.py" "<URL>" --json
```

超时 30 秒。失败则提示用户手动复制文章正文。

如果用户只是说"帮我读一下这篇公众号"（`/read-gzh` 触发），执行抓取后直接生成结构化总结，不进入后续内容生成流程。总结格式：

```markdown
# 文章总结
## 基本信息（标题/作者/类型/配图数）
## 核心观点（3条）
## 关键信息
## 金句摘录
## 图片内容（下载并识别配图中的文字）
## 思考/迭代点
```

### 第 2 步：分析文章结构

提取：标题、副标题/金句、核心概念、关键数据、步骤/流程、亮点/特色、方法论/金句、行动召唤。

### 第 3 步：拆分为卡片（**仅小红书**）

> **Scope 警告**：本步骤及第 4 步内的全部排版规则（卡片尺寸 540×720、字号 18-27px、h1/h2/h3 层级、稀疏页清单、下载工具栏、CORS 修复、avatar base64 内嵌等）**只适用于小红书轮播图**。
>
> **公众号** 的排版完全独立，走 Path A 的 `md2wechat_formatter.py`（正文 16px `large` / 15px `medium`），见 "### 排版命令" 一节。**不要把小红书的字号、`.slide` 结构、`html2canvas` 下载工具栏混入公众号 preview.html**。

**小红书图文转换核心原则：严格 1:1 保留原文，绝不压缩**
小红书帖子单篇最多支持 18 张图片（第 1 张为头图，第 18 张为封底，实际内容卡片最多 16 张）。**每一段、每一条列表项、每一个代码块都必须逐字保留原文，禁止概括、缩写、合并语义、省略细节。** 如果原文内容超出 16 张内容卡片的容量，则：
- 按原文顺序 1:1 排版，排到第 17 张自然截止
- 第 17 张底部注明"完整内容请移步微信公众号『墨筝』阅读原文"
- 第 18 张封底放金句总结 + 公众号引导
- **绝不通过压缩、概括、省略段落来把更多内容塞进有限的卡片**

**Markdown 格式转换规则：**
- **文章主标题（h1）**：原文 `title` 字段。使用最显眼的字号 + 衬线字体 + 上下细线点缀，全片仅在第 1 张卡片出现一次。
- **章节标题（h2 `##`）**：金色左竖线 + 较大无衬线字体。
- **子章节标题（h3 `###`）**：深色文字（`#2C2A28`）+ 较小字号，仅作小段引导，绝不能与 h1/h2 撞样式。**不用金色**，避免与 h2 左竖线和正文混在一起造成视觉密度过高。
- **列表项**：将 `-` 或 `*` 替换为有视觉区分度的极简形符号（如 • 或方形），圆点用中性灰（`#999`），杜绝使用 Emoji。嵌套列表用 `-` 显示且左缩进。
- **重点文字（加粗）**：使用黑色加粗（`#1C1C1E` + `font-weight:700`），不可使用 Emoji。**不用金色**——加粗本身已足够强调，金色会与 h2 左竖线视觉冲突。
- **表格**：小红书不能直接展示表格，需转化为卡片内的结构化键值对（Key-Value）排版。
- **图片**：原文 `![]()` 的图片**必须**独占一整张卡片，完全无 Header/Footer/页码，整张卡片就是一张干净的图，便于读者放大查看。
- **Emoji**：严格禁止在生成的纯文本或代码层中自行添加 Emoji 符号。
- **完整性要求**：所有正文段落、列表项、表格行、强调文字、斜体注释（如禁用环境变量提示）**必须 1:1 保留**，禁止抽象、概括、改写。如果一页放不下，应跨多页继续展示。
- **反空白页规则**：严禁出现"过渡页/指引页"，例如只放一个章节标题加一句"下一张图是…"。具体执行：
  - 章节 h2 必须与首段正文 / 首条列表 / 表格放在**同一张卡片**。
  - 一张卡片若有效内容（去掉 Header/Footer 后）占比不足卡片高度的 50%，必须向上合并到前一张或向下吸收下一张的开头。
  - 图片独占卡片（`.slide.img-only`）周围的文字卡片，不需要再写"下一张图为…"之类的衔接句，图与文上下相邻即天然衔接。
  - **段落容量下限**：纯文字卡片至少包含 3 段正文 / 或 1 段正文 + 3 条列表 / 或 1 个 h2 + 2 段正文。单段 1-2 句话且无列表/代码的"小卡片"必须与相邻同主题段落合并。
  - **拆页前先合并同主题**：拆分卡片之前，先将连续的短段落（每段 ≤ 80 字）按主题归并；只有当合并后高度真的超过 720px 才再拆。

#### 稀疏卡片自检清单（每生成完一版都跑一遍）

按顺序检查每张卡片，命中任一就要修：

1. **是否只有一个标题 + 一句过渡语**（如「跑分情况 / 下面是数据」「特性三 / 大概是这样」）→ 删过渡语，把 h2/h3 直接放到下一张内容卡片顶部。
2. **是否只有 2 段短文本**（每段 ≤ 80 字，且无列表/代码/表格）→ 上下合并同主题段落；如果合并后 > 720px 再考虑用粗体小标题（如「**适合场景**：」「**慎用场景**：」）把不同子点拼到一页。
3. **是否一个 h2 + 一个 h3 + 一两段引子独占一页**（典型"章节扉页"，但小红书没有目录页需求）→ 把这块章节起头并到该章节的第一张实质内容卡（列表/表格/图说明）顶部。
4. **是否在表格/list 卡之后还跟一张「举例 + 总结」短卡**（如「举例：High 0.05，Low 0.005，Max 0.4」+「现实情况大家都用 High」）→ 删掉重复的小标题（表格本身已是该主题），把举例和总结压缩为一段并入表格那张卡的页脚位置。
5. **是否在图片独占卡之前/之后留了一张「图 + 一句话说明」短卡** → 文字直接搬到图片的另一侧那张内容卡，让图与文成为天然上下文。

#### 合并时常用的紧凑写法（避免合并后撑爆 720px）

- **两段连写**：用"。"或"；"把两个短段合成一段，去掉过渡词（"另外"、"具体来说"、"现实情况"）。
- **粗体作分隔**：把多个并列子点用 `<strong>子点名</strong>：` 起头放进同一段，省掉每个子点单独成段的空白。
- **list 二合一**：原文若是「子点 A（含解释）」和「子点 A 的备注」两条 list，合成一条 `子点 A：解释。<em>（备注）</em>`。
- **去除重复小标题**：表格上方的「**费用消耗体感参考：**」之类小标题，如果表格本身已经表达了同样意思，直接删。
- **删冗词**：「适合查」「实际上」「比较」「就别用了」这类口语缓冲词在合并时优先精简。

#### 输出前必走一遍 sparse-pass 流程

每次生成 HTML 后，**必须**逐张卡片估算高度占比（mental: header 80 + footer 50 + padding 60 = 190px 固定，剩 530px 留给正文）。任一卡 < 270px（50%）就回到上面 5 项清单走一遍合并，重新生成。该流程在产出"第一版"和每次大改后都要执行。

节奏参考（最多 18 张，按原稿长度自然分页，不要擅自精简）：

| 位置 | 卡片类型 | 内容 |
|------|---------|------|
| 第 1 张 | 头图/开场 | 标题 + 核心 Hook + 背景交代 |
| 中间各张 | 纵深展开 | 逐字逐句排版原文内容（包括通过样式转化的表格/列表），单章可跨多页，保持单页 720px 高度内不拥挤溢出 |
| 第 18 张(若截断) | 未完待续 | "因篇幅限制，完整长文及更多细节，请移步微信公众号『墨筝』继续阅读" |
| 尾页(若未截断) | 封底 | 金句总结 + 统一 footer |

footer 每张都带 `[图标] 微信搜索公众号「墨筝」查看更多精彩内容` 提示，无需额外加微信号 CTA 盒子。

#### 页数由内容决定，而非预先设定

**禁止**在生成前预定"生成 N 张卡片"。正确流程：
1. 先按 1:1 还原要求，逐段估算所有内容需要多少张卡片（每张正文区 530px 可用高度）。
2. 估算结果即为总页数（上限 18 张）。
3. 按估算结果生成所有卡片，生成过程中如发现某页溢出则拆页、某页过空则合并，总页数随之浮动。

**反模式**：先拍一个"大概 12 页"的数字，再把内容往里塞——这会导致裁剪、概括、跳段。

#### 生成后内容完整性验证（必做）

每次完成小红书 HTML 生成后，**必须**执行以下验证流程：

1. **逐段对照**：打开源 Markdown（去掉 frontmatter 和开头引用声明），逐段检查每一段落 / 列表项 / 表格行是否出现在某张卡片中。
2. **列出映射**：mental check 格式 — "第 X 段 → slide N"，确认无遗漏。
3. **标记缺失**：任何未能映射到卡片的段落即为内容丢失，必须补入（拆页或追加卡片）。
4. **仅在验证通过后**才输出最终文件路径并告知用户"生成完成"。

该流程是**程序性约束**（procedural），不能靠"已经在 SKILL 中要求了 1:1 还原"这一声明性规则（declarative）替代——声明性规则无法防止 LLM 在长内容生成过程中无意识地概括或跳段。

#### 封底视觉克制原则

封底是全文收束，应安静、有呼吸感，**禁止整段大字加粗**。具体规则：

- **字号/字重**：`.q` 引文使用正文级字号（18px）+ 正常字重（400），颜色用深灰 `#2C2A28` 而非纯黑。仅最后一句 punchline 可用 `.punch`（20px, 600）轻提收束，其余句子保持安静。
- **金色高亮**：`<span class="hl">` 最多 **1 处**，选全文最具收束力的短语。多处金色会让封底视觉密度过高。
- **行高**：封底引文 `line-height: 1.7`，比正文卡片（1.6）略松，营造留白。
- **无 END 标识**：封底不放"— END —"等结束标记，quote-card + footer 本身已构成自然收束。
- **反模式**：整段 22px + font-weight 700 会让三句话挤成一块黑色方块，丧失层次感。

### 第 4 步：生成图片 HTML（**仅小红书**）

输出路径：文章同目录下 `[简短主题]-小红书版.html`，未指定目录放 `/tmp/`。浏览器自动打开预览。

头像路径：生成在 `content/[slug]/` 下的 HTML 中，头像引用用 `../_shared/avatar.jpg`（回退 1 级到 `content/_shared/avatar.jpg`）。`<img>` 配 `onerror` 回退为「墨」字头像，确保加载失败时仍有视觉占位。

**重要：生成前必读范例**

**首选范例**：`references/xiaohongshu-examples/markdown-faithful-范例.html`（Markdown 1:1 还原版式，含 h1/h2/h3 区分 + 图片独占卡片 + 下载工具栏）。
**旧版范例**：`references/xiaohongshu-examples/文字卡片-范例.html`（仅作回顾，新出稿一律用 v2）。

**卡片设计要求**
- 卡片尺寸固定 `540 × 720`（导出 SCALE=2 即 1080×1440，比例 3:4）。
- 同源配色：宣纸底 `#F2EDE3` + 筝弦金 `#C4956A` + PingFang SC 无衬线，公众号同款。
- **筝弦金克制使用**：金色仅用于 h2 左竖线（章节分隔的唯一视觉锚点）。h3 标题、加粗文字、列表圆点均不用金色，防止页面金色密度过高、喧宾夺主。
- **标题三级层次必须视觉可区分**，且**严格大于正文字号**：
  - `h1`（文章主标题）：**27px** 黑色衬线字体 + 上下黑色细线，全文仅第 1 张出现一次。
  - `h2`（章节）：**22px** 黑色无衬线 + 4px 金色左竖线。
  - `h3`（子节）：**19px** 深色（`#2C2A28`）无衬线，与 h2 通过字号和形态区分，**不用金色**。
- **正文字号下限（手机实测过的）**：DOM 是 540×720，但在小红书 App 里图片宽度约等于手机屏宽 360-400px，所以字号要按"实际显示 ~70%"反推。**经多轮 iPhone 实测，最终基线如下（兼顾可读性与单页容量）**：
  - 正文段落 `p` / 一级 `list-item`：**18px**，`line-height: 1.6`（保持舒适，不再继续收紧），`margin-bottom: 7-8px`。
  - 嵌套子项 `list-item.sub`：**16px**。
  - 表格 row：**15.5px**，key 加粗 **16px**，`padding: 6px 0`。
  - 头部 meta 名字：15px，日期：13px。
  - 底部 footer brand / page：12px（信息密度低、可弱化）。
  - **正文（p / list-item）禁止低于 17px**，表格不低于 15px。若卡片放不下，应优先合并稀疏卡或拆页，**绝不通过缩字号或压行高（< 1.5）来塞内容**。
  - **行高底线**：正文 `line-height` 不得低于 **1.55**，低于这个值阅读会发挤。
  - **层级关系硬规则**：h1 > h2 > h3 > 正文 > 子项 > 表格 > footer，相邻层级至少差 1-2px。h3 必须严格大于正文（≥1px），否则标题失去引导作用。
- **间距收紧规则（字号大了就要收 margin）**：字号上调以后，标题 margin-bottom 控制在 10-16px、正文/list-item margin-bottom 控制在 7-8px、`post-header margin-bottom: 14px`、表格 padding 收到 10px 14px，行高保持 ≥ 1.55 不要为了塞内容继续压缩。
- **内联 `<code>` 不可拆**：CSS 必须给 `code { white-space: nowrap; }`，否则带 ASCII 空格的命令（如 `/effort ultracode`、`git commit -m`、`docker run -it`）会在空格处换行，把 `/effort` 留上一行、`ultracode` 挤下一行，中间撑出巨大空白。中文之间夹的 inline `<code>` 也建议在命令内部用 `&nbsp;` 拼接，双保险。
- **长命令独立成块**：超过半行的命令/代码片段，单独用 `<code class="cmd-block">`，CSS 配 `display:block; white-space:pre-wrap; word-break:break-word; padding:8px 12px;`，让它正常换行展示，而不是塞回行内 `<code>` 撑爆布局。
- **图片独占卡片**：原文 `![]()` 必须独占一整张 `.slide.img-only`，黑底 + `object-fit:contain` 全图展示，**无 Header / Footer / 页码 / 金色光晕**。
- **每张卡片 Header**：头像 + 「墨筝」+ MM/DD 自动写入（脚本兜底）。日期统一使用**生成当天的日期**，不使用原文 frontmatter 中的发布日期。
- **每张卡片 Footer**：左 `微信搜索公众号「墨筝」查看更多内容`，右 `当前页 / 总页数`。

**下载工具栏（必带）**：
- 顶部 fixed 工具栏含两个按钮：`全部下载 (ZIP)` + `下载当前`，外加一个 `#progress` 进度文本。
- 引入 `html2canvas@1.4.1` + `jszip@3.10.1` + `file-saver@2.0.5`（jsDelivr CDN）。
- `flattenAlpha()` 把透明通道展平为底色，避免微信白底渲染时暗底变白。
- 图片独占的 slide 走 `#1C1C1E` 底色路径，其余 slide 走 `#F2EDE3`。
- **跨域图片必须先 inline**：远端图床（如 `im.gurl.eu.org`、telegram 图床等）通常不返回 CORS 头，直接被 html2canvas 渲染会把 canvas 标 tainted，`toBlob` 抛 SecurityError 静默失败、点按钮没反应。必须在每次下载前先跑一遍 `inlineRemoteImages()`：
  - 先尝试直连 `fetch(src, { mode: 'cors', cache: 'force-cache' })` → `blob()` → `FileReader.readAsDataURL` → 写回 `img.src`，等 `img.decode()`。
  - 直连失败必须 fallback 到图片代理：依次尝试 `https://wsrv.nl/?url=<去掉协议头>`、`https://images.weserv.nl/?url=<去掉协议头>`、`https://corsproxy.io/?<完整URL>`，任一成功即可。
  - 所有源都失败时把 `img.src` 替换为 1x1 透明 GIF 占位符（`data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7`），避免污染 canvas 让整个下载流程崩溃。
- **本地图片（如头像）必须在生成期直接 base64 内嵌**：用户多半通过 `file://` 双击打开 HTML，此时本地图片在 canvas 里仍被视为 cross-origin、`fetch()` 也无法读取本地文件，导致跟跨域图床一样的 tainted canvas。**生成脚本**应当读取 `content/_shared/avatar.jpg` 等本地资源，转 base64 后通过占位符（如 `__AVATAR__`）替换到 HTML 里，不要保留任何 `src="../../xxx"` 这种相对路径写法。
- **错误必须暴露**：`downloadAll/downloadOne` 必须用 `try/catch` 包裹，失败时把错误写到 `#progress` 并 `alert()`，否则用户只会看到"点了没反应"。
- 检查 `toBlob` 返回值非空：返回 null 即说明仍被污染，应抛错而不是塞 null 进 zip。

**文案质量要求（硬规则）**：
- **严禁压缩、总结、改写、杜撰**：原文所有段落、列表项（含嵌套子项）、表格行、加粗、斜体注释（如禁用环境变量）必须 1:1 逐字保留。
- 一页装不下就跨多页继续展示，宁可多张卡片也不可裁剪文字。
- **容量溢出时截止而非压缩**：内容超出 18 张卡片时，按原文顺序排到放不下为止，末尾提示跳转公众号。绝不通过概括、省略段落、合并语义来强行塞入更多内容。
- 卡片外的小红书正文描述可适度口语化，但卡片内严格忠于原文。

生成的内容应达到 v2 范例的专业水准。

### 第 5 步：生成小红书发布文案

**根据内容类型选择风格：**

- **个人 IP 风格**（真人分享、产品开发、踩坑记录）
  - → 读 `local/SKILL.local.md` 中指定的个人品牌风格文件（如有）
  - 流水账式真实感 + 具体时间细节 + 口语化表达
  - 300-350字，8-12个标签
  - 人设：在 `local/SKILL.local.md` 中自定义

- **墨筝风格**（方法论总结、深度分析）
  - → 读 `references/platform-copy.md` 的小红书部分
  - 结构化拆解 + 干货密度高
  - 适合转载公众号文章

### 第 6 步：输出 manifest.json

所有内容生成完毕后，自动输出 manifest.json 到输出目录。格式：

```json
{
  "version": "1.0",
  "created": "<ISO时间戳>",
  "source": "<微信链接>",
  "title": "<文章标题>",
  "outputs": {
    "xiaohongshu": { "html": "...", "copy": { "title": "...", "body": "...", "tags": [...] } },
    "wechat": {
      "html": "...",
      "cover_image": "...",
      "title": "...",
      "author": "墨筝",
      "digest": "...",
      "images": [...]
    }
  }
}
```

如果用户说"转小红书并发布"，生成 manifest 后自动执行 `/distribute`。

### 第 7 步：用户微调

告知用户所有产出物路径，提示可调整，输入 `/distribute` 可一键发布。

**公众号同步提示**：封面 PNG 从浏览器下载后，直接 `/distribute --platforms wechat` 即可同步到草稿箱（API 模式，无需打开 Chrome）。

**一次性产出：**
1. 小红书图片 HTML（含一键下载工具栏）
2. 小红书发布文案（标题 + 正文 + 标签）
3. manifest.json（供 `/distribute` 一键发布）

---

## Path C 流程：博客文章 → 视频

将博客长文转化为 HyperFrames 视频合成。视频输出到 `content/[slug]/video/` 目录，自带墨筝品牌水印和 BGM。

**视频定位：导流型（teaser）**。目的是精选文章亮点，引导观众到公众号阅读全文，不是完整呈现所有内容。

### 时长与内容决策规则

| 文章规模 | 时长 | 场景数 | 内容策略 |
|----------|------|--------|----------|
| 短文（<2000字，<10个要点） | 30-45s | 4-5 | 每个要点给标题+一句描述 |
| 中文（2000-5000字，10-20个要点） | 45-60s | 5-7 | 精选 8-12 个最有吸引力的要点 |
| 长文（>5000字，>20个要点） | 60-90s | 7-9 | 精选 12-15 个最有吸引力的要点，按章节分组展示 |

**每个要点的停留时间**：标题+描述至少 4-5 秒可读时间。宁可少选几个要点，也不要为了塞更多内容而缩短每个要点的停留时间。观众读不完的信息等于没有。

**内容选择原则**：
- 选最具"钩子感"的要点——让人想知道更多细节的
- 每个章节至少选 1-2 个代表性要点，保持全文结构的覆盖感
- 最后一个场景明确引导"完整内容请关注公众号「墨筝」"

### 第 1 步：定位文章 & 创建输出目录

从 `source/_posts/[slug].md` 读取博客文章，提取标题、章节结构和核心内容。

创建输出目录 `content/[slug]/video/`（slug = Markdown 文件名去掉 `.md`）。

### 第 2 步：生成视频 design.md

写入 `content/[slug]/video/design.md`，供 hyperframes skill 的 Step 1（Design system）读取。

**品牌衍生规则**：墨筝品牌色体系（宣纸底 `#F2EDE3`、墨色 `#1C1C1E`、筝弦金 `#C4956A`）是为静态博客/小红书设计的，不能直接照搬到视频。视频 design.md 需要**衍生**：

- **背景**：保持暗色基调（墨色精神），但不限定于 `#1C1C1E`。可根据文章内容主题调整色相——偏蓝（tech）、偏暖（editorial）、偏深蓝（data）等
- **强调色**：保留筝弦金的暖金调性，但饱和度和亮度可提升至视频级别（`#D4A76A`-`#E8A850` 范围）。可根据内容引入第二强调色
- **文字色**：保持高对比，`#F2EDE3` 或更亮的 `#F0F6FC` 均可
- **字体**：必须从 hyperframes 内置字体列表中选择（Oswald, Montserrat, DM Sans, JetBrains Mono, IBM Plex Mono, Source Code Pro 等），不使用 PingFang SC 等系统字体

design.md 格式参考 `content/ai-code-review-benchmark/video/design.md`：

```markdown
# Design

## Mood
[根据文章内容决定，如 Dark tech、Editorial calm 等]

## Colors
- Background: `#XXXXXX` (从墨色衍生的暗底)
- Foreground: `#XXXXXX` (高对比文字色)
- Accent 1: `#XXXXXX` (从筝弦金衍生的主强调色)
- Accent 2: `#XXXXXX` (内容主题相关的第二强调色)
- Muted: `#XXXXXX` (面板/卡片背景)
- Border: `#XXXXXX` (结构线)

## Typography
- Headlines: [内置字体], [weight]
- Body: [内置字体], [weight]
- Data/Code: [等宽内置字体], [weight]

## Constraints
- All text in Chinese except technical terms
- [其他内容相关约束]
```

### 第 3 步：准备 BGM

将 `content/ai-code-review-benchmark/video/bgm.mp3` 复制到 `content/[slug]/video/bgm.mp3`。所有视频统一使用同一首 BGM。

### 第 4 步：调用 hyperframes 生成视频

进入 `content/[slug]/video/` 目录，调用 hyperframes skill 生成 `index.html`。hyperframes 会自动读取同目录下的 `design.md`。

**竖版视频布局规则（1080×1920）：**

| 元素 | 字号 | 说明 |
|------|------|------|
| 场景分类标签 | 36px | 如"基础操作""工作流优化"，等宽字体，粗体 |
| 卡片编号 | 24px | 等宽字体，accent 色 |
| 卡片标题 | 38px | 核心信息，800 字重 |
| 卡片正文/描述 | 28px | 辅助信息，75% 透明度 |
| 代码/命令 | 26px | 等宽字体，accent-blue 色 |
| 角标/页码 | 16px | 装饰性，不影响阅读 |
| 水印文字 | 28px | 含 36px 图标 |

- **平台安全区**：竖版顶部留 170px（视频号/抖音顶部 UI 遮挡区域），底部和右侧也有平台 UI 占用。
- **内容密度**：列表/技巧类视频，每个 scene 放 4 条内容。
- **scene-content padding**：竖版用 `330px 64px 80px`（含 170px 平台安全区 + 水印 + 水印与内容间距），横版用 `80px 120px`。
- **卡片间距**：gap `24px`，卡片内 padding `20px 24px`。

**品牌元素必带项**（参照 `content/ai-code-review-benchmark/video/index.html` 的实现）：

**a) 常驻水印**：

```html
<div class="watermark" id="watermark">
  <div class="watermark-icon">M</div>
  <div class="watermark-text">公众号：墨筝</div>
</div>
```

- 横版位置 `bottom:36px;right:48px`，竖版 `top:218px;left:60px`（顶部 170px 平台安全区 + 48px 内边距，底部和右侧被平台 UI 遮挡；右上角留给页码角标）
- `opacity: 0.7`，z-index 高于所有场景
- 图标：accent 色圆角方块 + 白色 M 字母
- 动画：1.5s 时 `gsap.from("#watermark", { opacity: 0, duration: 1.0, ease: "power1.out" }, 1.5)`

**b) BGM 音频轨**：

```html
<audio id="bgm" data-start="0" data-duration="[视频总时长]" data-track-index="10" src="bgm.mp3" data-volume="0.3"></audio>
```

- `data-volume="0.3"`（背景级别，不抢内容）
- `data-track-index="10"`（与视觉轨道分开）

**c) 尾屏 CTA（推荐）**：

最后一个场景包含公众号导流提示，如"更多内容请关注公众号「墨筝」"。

### 第 5 步：校验 & 渲染

```bash
cd content/[slug]/video/
npx hyperframes lint && npx hyperframes validate
npx hyperframes inspect
npx hyperframes render --output output.mp4
```

**一次性产出：**
1. `content/[slug]/video/design.md` — 视频设计规范
2. `content/[slug]/video/index.html` — HyperFrames 视频合成源文件
3. `content/[slug]/video/bgm.mp3` — 背景音乐
4. `content/[slug]/video/output.mp4` — 渲染输出（可选，需 hyperframes CLI）

---

## 分发流程（/distribute）

读取 manifest.json，通过 API 或 Chrome CDP 自动化发布到各平台（→ 读 `references/distribute-platforms.md`）。

### 用法

```bash
# 全平台发布
npx -y bun "${SKILL_DIR}/scripts/distribute/distribute.ts" --manifest /path/to/manifest.json

# 选择平台
npx -y bun "${SKILL_DIR}/scripts/distribute/distribute.ts" --manifest /path/to/manifest.json --platforms wechat,xhs

# 预览模式（不提交，只预填内容）
npx -y bun "${SKILL_DIR}/scripts/distribute/distribute.ts" --manifest /path/to/manifest.json --platforms xhs --preview
```

### 平台缩写

| 缩写 | 平台 | 状态 |
|------|------|------|
| `wechat` | 公众号 | 可用 |
| `xhs` | 小红书 | 可用 |

### 执行顺序

公众号 → 小红书（顺序执行，避免 Chrome 端口冲突）

### 四级降级

| 级别 | 模式 | 触发条件 |
|------|------|---------|
| L0 | API 直推 | 公众号 API 直接推草稿箱，无需 Chrome |
| L1 | 自动发布 | CDP 完全自动化 |
| L2 | 辅助发布 | 登录态失效/选择器失效/`--preview` |
| L3 | 手动模式 | CDP 连接失败 |

公众号优先 L0（API），凭证缺失或失败时自动降级 L3（手动）。

### 公众号 API 模式说明

**凭证来源**（按优先级）：
1. 环境变量 `WECHAT_APPID` + `WECHAT_APPSECRET`
2. 配置文件 `~/.config/wechat-api/config.json`

**Token 缓存**：
- 缓存位置：`~/.config/wechat-api/token-cache.json`
- 有效期 2 小时，提前 5 分钟刷新
- 无需手动管理，脚本自动处理

**执行流程**：
1. 获取 access_token（优先读缓存）
2. 从 `_preview.html` 提取文章内容（`extractArticleContent`，兼容 `<div>` 和 `<section>` 容器）
3. 修复 WeChat 不兼容的 HTML 结构（`fixHtmlForWechat`）
4. 扫描并上传本地图片到微信 CDN（`uploadLocalImagesInHtml`）
5. 下载远程图片并上传到微信 CDN（`uploadRemoteImagesInHtml`，跳过已在 `mmbiz.qpic.cn` 上的图片）
6. 上传封面图获取 `thumb_media_id`
7. 调用 `draft/add` 创建草稿

---

## 品牌设计规范

**统一品牌色体系：**
- **墨筝（mozheng）**：所有平台统一使用——墨色+筝弦金体系（公众号、小红书等）

> **单一真相源**：在 `local/SKILL.local.md` 中指定你的品牌色文档路径。
> 如果色值冲突，以品牌文档为准。以下色板作为默认示例。

### 墨筝色板（墨色+筝弦金体系）

> 公众号「墨筝」专属配色。取意：墨——墨汁近黑微暖；筝——古筝丝弦哑光金。

**比例法则**（按场景区分）：

| 场景 | 比例 | 说明 |
|------|------|------|
| 暗底（头图、配图、封面） | 墨色 80% : 筝弦金 8% : 宣纸 10% : 其余 2% | 公众号头图、文章配图等暗底产物 |
| 浅底（小红书文字卡片） | 宣纸 75% : 灰文字 18% : 筝弦金 5% : 墨色 2% | 小红书轮播图，与公众号正文同源配色，禁用朱红等其它强调色 |

| 名称 | 色值 | 用途 |
|------|------|------|
| 墨色（主暗色） | `#1C1C1E` | 暗底卡片背景、标题、表头 |
| 筝弦金（重点色） | `#C4956A` | 强调色、重点文字、链接、分割线（仅点睛） |
| 宣纸底 | `#F2EDE3` | 暗底上的主文字、浅底卡片组件背景（**配图浅底页用 `#FFFFFF` 纯白**） |
| 浓墨 | `#2C2A28` | 渐变暗端、hover 态 |
| 淡墨 | `#7A7876` | 次要文字 |
| 半透白 | `rgba(255,255,255,0.5)` | 暗底上的品牌名 |
| 半透墨 | `rgba(28,28,30,0.4)` | 浅底上的品牌名 |

### 墨筝代码块配色（语法高亮）

代码块使用墨色暗底 `#1C1C1E` + 宣纸白文字 `#F2EDE3`，筝弦金淡边框 `rgba(196,149,106,0.15)`。语法高亮基于 Pygments，色彩从墨筝体系延伸：

| 名称 | 色值 | Token 类型 | 设计意图 |
|------|------|-----------|----------|
| 筝弦金 | `#C4956A` | 关键字 `if/for/export/const` | 与品牌强调色统一 |
| 苔绿 | `#A8C97F` | 字符串 `"hello"` | 暗底上清新可读 |
| 淡墨 | `#7A7876` | 注释 `# comment` | 低调退后，不分散代码阅读 |
| 暖金 | `#D4A76A` | 数字 `42` | 与筝弦金同色系，微暖 |
| 青瓷 | `#8FBCBB` | 函数名 `func()` | 冷色对比，区分关键字 |
| 藤紫 | `#B48EAD` | 类型 `string/int` | 区分函数名与类型 |
| 淡棕 | `#9A8A7B` | 操作符/标点 `= + {}` | 安静不抢眼 |

**设计原则**：暖色系（金/绿/棕）为主调，冷色（青瓷/藤紫）少量点缀，整体不脱离墨筝「文房器乐」的温暖质感。内联 `code` 保持浅底（`#f0ece4`）不变。

### 品牌选择规则

所有平台统一使用墨筝品牌色体系（墨色 #1C1C1E + 筝弦金 #C4956A + 宣纸底 #F2EDE3），保持跨平台视觉一致性。

### 字体

```css
font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

### 品牌角标

每页左上角品牌 logo + 文字，暗底页用 `.light`，浅底页用 `.dark`。
- 墨筝体系：文字显示 `墨筝`，logo SVG 中强调色使用筝弦金 `#C4956A`

### 页码

右下角 `1/N`，暗底页 `rgba(255,255,255,0.2)`，浅底页 `rgba(28,28,30,0.2)`。

---

## 内容适配原则

微信 → 小红书需要**排版适配**，但**内容必须 1:1 保留**：

| 维度 | 微信（线性长文） | 小红书（卡片轮播） |
|------|------|--------|
| 载体 | 单篇连续阅读 | 540×720 卡片，最多 18 张 |
| 排版 | `md2wechat_formatter.py` 内联 CSS | 文字卡片 HTML + html2canvas 导出 |
| 标题层级 | Markdown h1/h2/h3 | h1 27px / h2 22px / h3 19px 视觉区分 |
| 表格 | 原生 HTML table | 结构化键值对排版（小红书不支持表格） |
| 图片 | 文内嵌图 | 独占整张卡片，黑底全图展示 |

**核心原则**：卡片内严格忠于原文——所有段落、列表项、表格行、加粗、斜体注释必须 1:1 逐字保留，禁止压缩、概括、杜撰。一页放不下就跨多页，宁可多张卡片也不可裁剪文字。内容超出 18 张时按顺序排到放不下为止，末尾提示跳转公众号，绝不压缩来塞入更多内容。卡片外的小红书正文描述可适度口语化。

---

## 完整模板参考

首次生成小红书图片时，参考 `references/xiaohongshu-examples/` 目录下的范例文件获取完整 CSS + JS。

> 如果有额外的本地模板参考，在 `local/SKILL.local.md` 中指定路径。

生成新内容时复用范例文件的 CSS + JS 部分，只替换卡片内容。

---

## Script Directory

**Agent Execution**: Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>`.

| Script | Purpose |
|--------|---------|
| `scripts/fetch_wechat_article.py` | 微信文章抓取（Python，模拟微信 UA） |
| `scripts/insert_image_placeholders.py` | 配图占位符插入（解析 illustrations.html 的 slide-label，在 preview.html 对应章节插入 `<!-- IMAGE:配图-N.png -->`） |
| `scripts/distribute/distribute.ts` | 分发主编排器 |
| `scripts/distribute/cdp-utils.ts` | 共享 CDP 工具 + Manifest 类型定义 |
| `scripts/distribute/wechat-api.ts` | 公众号 API 客户端（token 管理、图片上传、草稿创建） |
| `scripts/distribute/platforms/*.ts` | 各平台发布模块 |
| `scripts/render_pngs.py` | Playwright 渲染 cover.html / illustrations.html 为 PNG（含 bottom-bleed 裁剪） |

---

## Reference 文件索引

cc 按需读取，不要一次性加载所有 reference。

| 场景 | 读取文件 |
|------|---------|
| 出稿写文章 | → 写作 skill（`../writing/SKILL.md`），含 5 步写作方法论 + 30 类 AI 模式检测 |
| 生成头图/配图 | `references/cover-template.md` — 墨筝风格排版规范（头图 + 配图 + 视觉组件） |
| 横版→竖版封面 | `references/cover-vertical-spec.md` — 公众号封面转竖版的 CSS 转换规范 |
| 生成小红书轮播图 | `references/xiaohongshu-text-card.md` — **唯一风格**：公众号同源配色的文字卡片。首选范例：`references/xiaohongshu-examples/markdown-faithful-范例.html`（v2 Markdown 1:1 还原版式）。旧版范例 `文字卡片-范例.html` 仅作回顾。旧多卡片信息图模板 `xiaohongshu-format.md` 已废弃，只作 SVG / 下载脚本存档 |
| 生成小红书文案 | `references/platform-copy.md` — 小红书文案规范 |
| 生成视频 | hyperframes skill（`../hyperframes/SKILL.md`）— HyperFrames 视频合成框架，参照 `content/ai-code-review-benchmark/video/` 已有实现 |
| 分发到各平台 | `references/distribute-platforms.md` — 平台配置 + manifest 格式 + 降级策略 |

---

## 故障处理

| 问题 | 处理 |
|------|------|
| 微信抓取失败 | 提示用户手动复制文章正文 |
| 文章太短（<500字） | 按内容自然分页，可能只需 3-5 张卡片 |
| 文章太长（>5000字） | 充分利用 18 张额度 1:1 排版，第 18 张仍放不下则提示跳转公众号 |
| 导出图片模糊 | 检查 SCALE=2，浏览器缩放 100% |
| manifest 不存在 | 提示先运行内容生成 |
| Chrome 启动失败 | 降级 L3（手动模式） |
