# 墨筝风格排版规范

> 公众号头图、文章配图、排版的统一规范。
> 所有图片产出为 HTML 文件，浏览器打开后点击下载按钮导出 PNG。

---

## 一、排版（Markdown → 公众号 HTML）

使用 md-formatter 排版工具（统一墨筝主题，CSS 自动内联）：

```bash
cd "$MD_FORMATTER_DIR"
python3 md2wechat_formatter.py [文章路径] -o [输出HTML路径]
# 可选：--font-size large（默认 16px）或 medium（15px）
```

> `$MD_FORMATTER_DIR` 需在 `local/.env` 或环境变量中配置。

产出 `_preview.html`，浏览器打开 → 全选复制 → 粘贴到公众号编辑器。

---

## 二、公众号头图（HTML 可下载）

### 尺寸

- 主头图：`900 x 383 px`（2.35:1），2x 导出 `1800 x 766`
- 次头图：从主图中心裁出 `200 x 200` 正方形

### 设计规范

- **背景**：墨色暗底 `#1C1C1E`，带微弱径向渐变纹理
- **主标题**：不超过 15 字，宣纸白 `#F2EDE3`，92px，font-weight 900，居中
- **副标题**：28px，`rgba(255,255,255,0.5)`，主标题下方
- **产品名/关键词**：筝弦金 `#C4956A`，带筝弦金边框框住，居中
- **品牌角标**：左上角墨筝 logo SVG + 文字
- **底部标签**：右下角，小字标签（工具名、特性），`rgba(255,255,255,0.35)`
- **装饰元素**：左右两侧可放低透明度（0.12）的主题相关 SVG 图标

### 截图背景指引

当文章涉及具体产品/游戏/工具时，**优先使用产品截图作为头图背景**，增加视觉吸引力：

1. **截图作为背景**：将产品/游戏截图设为 `background-image`，`background-size: cover`
2. **透明度控制**：截图 `opacity: 0.3-0.5`，避免喧宾夺主
3. **暗色渐变遮罩**：在截图上层叠加暗色渐变，确保文字可读
   ```css
   .bg-screenshot { position: absolute; inset: 0; background: url('截图路径') center/cover; opacity: 0.4; }
   .bg-overlay { position: absolute; inset: 0; background: linear-gradient(135deg, rgba(28,28,30,0.85), rgba(15,31,24,0.95)); }
   ```
4. **文字层**：`z-index: 2`，保持宣纸白 `#F2EDE3`，不受背景影响

### 风格选择决策树

| 内容类型 | 推荐风格 | 背景处理 |
|---------|---------|---------|
| 技术教程 / 工具介绍 | 墨色暗底 `#1C1C1E` | 纯色 或 产品截图背景（opacity 0.3） |
| 女性成长 / 温暖话题 | 暖亮风格（见五B色板） | 纯色渐变，柔和暖色 |
| 游戏 / 娱乐类 | 墨色暗底 + 截图背景 | 游戏截图（opacity 0.4-0.5）+ 暗色遮罩 |
| 深度分析 / 行业观察 | 墨色暗底 `#1C1C1E` | 纯色，强调文字内容 |
| 产品测评 / 对比 | 墨色暗底 + 截图背景 | 产品 UI 截图（opacity 0.3）+ 渐变遮罩 |

### HTML 结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  body { background: #111; display: flex; flex-direction: column; align-items: center; padding: 70px 20px 80px; }
  .cover { width: 900px; height: 383px; position: relative; overflow: hidden; border-radius: 8px; }
  .bg-dark { position: absolute; inset: 0; background: #1C1C1E; }
  .content { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 2; }
  /* 工具栏同小红书模板 */
</style>
</head>
<body>
  <div class="toolbar">
    <button onclick="downloadCover('main')">下载头图 (900x383)</button>
    <button onclick="downloadCover('secondary')">下载次图 (200x200)</button>
  </div>
  <div class="cover" id="cover-main">
    <div class="bg-dark"></div>
    <!-- 品牌角标 -->
    <!-- 主标题 + 副标题 + 产品名 -->
    <!-- 底部标签 -->
  </div>
  <!-- html2canvas + FileSaver 下载脚本 -->
</body>
</html>
```

下载脚本：用 `html2canvas` 渲染 cover div，SCALE=2，主图直接导出，次图从中心裁正方形。

> **重要**：`html2canvas` 配置必须设置 `backgroundColor: null`，然后在导出前调用 `flattenAlpha()` 将 canvas 合成到实底色上。背景色优先从子元素 `.bg-light` / `.bg-dark` 获取（因为 `.slide` 本身通常是透明的），fallback `#1C1C1E`。导出前需临时移除 `border-radius` 以避免圆角处出现底色溢出。直接设置 `backgroundColor` 参数会覆盖元素内部渐变层，导致渐变丢失。
>
> 所有导出模板（头图、配图、小红书、播客封面）必须包含以下 helper：
> ```js
> function flattenAlpha(canvas, bgColor) {
>   const isTransparent = !bgColor || bgColor === 'transparent' || bgColor === 'rgba(0, 0, 0, 0)';
>   const flat = document.createElement('canvas');
>   flat.width = canvas.width; flat.height = canvas.height;
>   const ctx = flat.getContext('2d');
>   ctx.fillStyle = isTransparent ? '#1C1C1E' : bgColor;
>   ctx.fillRect(0, 0, flat.width, flat.height);
>   ctx.drawImage(canvas, 0, 0);
>   return flat;
> }
> ```
> 渲染时先检测子背景元素颜色、临时去圆角，再导出：
> ```js
> async function renderSlide(el) {
>   const origRadius = el.style.borderRadius;
>   el.style.borderRadius = '0';
>   const bgEl = el.querySelector('.bg-light, .bg-dark');
>   const bg = bgEl ? getComputedStyle(bgEl).backgroundColor : getComputedStyle(el).backgroundColor;
>   const raw = await html2canvas(el, { scale: 2, useCORS: true, backgroundColor: null });
>   el.style.borderRadius = origRadius;
>   return flattenAlpha(raw, bg);
> }
> ```

---

## 三、文章配图（HTML 可下载）

### 尺寸

- 宽度固定 `800px`，高度按内容 `380-500px`
- 导出 2x（`1600px` 宽）

### 设计规范

- **暗底页和浅底页交替出现**
- 暗底：`#1C1C1E` 背景，宣纸白文字
- 浅底：`#F2EDE3` 背景，墨色文字
- 每张图左上角品牌角标，右下角页码 `N/N`
- 每张图顶部有 section-tag 标签（英文大写，letter-spacing: 2px）
- 筝弦金仅用于：强调数字、标签分类名、关键箭头

### 常用配图类型

| 类型 | 适用场景 | 布局 |
|------|---------|------|
| 流程图 | 展示 Pipeline / 工作流 | 横向箭头连接的卡片行 |
| 对比图 | A vs B | 左右双栏，暗/浅对比 |
| 链路图 | 从输入到产出的完整路径 | 横向大卡片 + 箭头 |
| 网格卡片 | 分类展示多个项目 | 3列 grid，墨色小卡片 on 浅底 |
| 星级评分 | 适配度 / 推荐度 | 列表行，左侧星级右侧说明 |

### HTML 结构

```html
<body>
  <div class="toolbar">
    <button onclick="downloadAll()">全部下载 (ZIP)</button>
    <button onclick="downloadOne()">下载当前</button>
  </div>

  <div class="slide-label">配图 N · 放在「xxx」之后</div>
  <div class="slide" style="height:420px;">
    <div class="bg-dark"></div>  <!-- 或 bg-light -->
    <div class="brand light"></div>  <!-- 或 brand dark -->
    <div class="page-num light">1/N</div>
    <div class="content">
      <div class="section-tag on-dark">ENGLISH TAG</div>
      <div class="title-dark" style="font-size:28px;">中文标题</div>
      <!-- 具体内容 -->
    </div>
  </div>

  <!-- html2canvas + JSZip + FileSaver -->
</body>
```

下载脚本用 `html2canvas` 渲染每个 `.slide`，导出前调用 `flattenAlpha()` 去除 alpha 通道，打包为 ZIP。每张图命名 `配图-序号-描述.png`。

### 配图命名和位置标注

每张 `.slide` 上方必须有 `.slide-label` 标注：
```
配图 N · 放在「文章中的哪个小节」之后
```

---

## 四、视觉组件速查（暗底版）

### 品牌角标 SVG

```html
<svg viewBox="0 0 32 32" fill="none">
  <circle cx="13" cy="16" r="10" stroke="rgba(255,255,255,0.5)" stroke-width="2.2" fill="none"/>
  <ellipse cx="13" cy="8.5" rx="7" ry="1.5" stroke="rgba(255,255,255,0.3)" stroke-width="1.2" fill="none"/>
  <ellipse cx="14" cy="17" rx="3.5" ry="2" fill="#C4956A"/>
  <polygon points="10,17 7.5,14.5 7.5,19.5" fill="#C4956A"/>
  <circle cx="16" cy="16.3" r="0.7" fill="#F2EDE3"/>
  <line x1="26" y1="4" x2="26" y2="16" stroke="rgba(255,255,255,0.5)" stroke-width="2" stroke-linecap="round"/>
  <path d="M26 16 Q26 22 22 22" stroke="rgba(255,255,255,0.5)" stroke-width="2" fill="none" stroke-linecap="round"/>
  <circle cx="26" cy="4" r="2" stroke="rgba(255,255,255,0.5)" stroke-width="1.5" fill="none"/>
</svg>
```

浅底版：将 `rgba(255,255,255,...)` 替换为 `rgba(28,28,30,...)`。

### Section Tag

```html
<div style="display:inline-block;font-size:11px;font-weight:700;letter-spacing:2px;padding:4px 12px;border-radius:4px;background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.5);">PIPELINE</div>
```

### 流程卡片

```html
<div style="width:110px;height:80px;border-radius:10px;background:rgba(196,149,106,0.15);display:flex;flex-direction:column;align-items:center;justify-content:center;border:1.5px solid rgba(196,149,106,0.3);">
  <div style="font-size:13px;font-weight:800;color:#F2EDE3;">标题</div>
  <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:4px;">说明文字</div>
</div>
```

箭头：`<div style="color:rgba(255,255,255,0.25);font-size:20px;padding:0 8px;">→</div>`

### 大数字

```html
<div style="font-size:64px;font-weight:900;color:#C4956A;">22</div>
<div style="font-size:22px;font-weight:800;color:#F2EDE3;">个 Skill</div>
```

### 信息行

```html
<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
  <div style="width:6px;height:6px;border-radius:50%;background:#C4956A;flex-shrink:0;"></div>
  <div style="font-size:13px;color:rgba(255,255,255,0.8);">内容文字</div>
</div>
```

---

## 五、色板速查

> 墨筝默认色板。

| 名称 | 色值 | 用途 |
|------|------|------|
| 墨色（主暗色） | `#1C1C1E` | 暗底背景、标题、表头 |
| 筝弦金（重点色） | `#C4956A` | 强调色（仅点睛：数字、箭头、标签名、边框） |
| 宣纸底 | `#F2EDE3` | 浅底背景、暗底上的主文字 |
| 浓墨 | `#2C2A28` | 渐变暗端（`radial-gradient` 终点）、hover 态 |
| 淡墨 | `#7A7876` | 次要文字、辅助信息 |
| 半透白 | `rgba(255,255,255,0.5)` | 暗底上的品牌名 |
| 半透墨 | `rgba(28,28,30,0.4)` | 浅底上的品牌名 |

**比例法则**：墨色 80% : 筝弦金 8% : 宣纸 10% : 其余 2%

### 代码块语法高亮色板

代码块背景用墨色暗底 `#1C1C1E`，文字默认宣纸白 `#F2EDE3`，语法 Token 配色：

| Token | 色值 | 示例 |
|-------|------|------|
| 关键字 | `#C4956A` | `if` `for` `const` `export` |
| 字符串 | `#A8C97F` | `"hello"` `'world'` |
| 注释 | `#7A7876` | `# comment` `// note` |
| 数字 | `#D4A76A` | `42` `3.14` |
| 函数名 | `#8FBCBB` | `fetch()` `setup()` |
| 类型 | `#B48EAD` | `string` `Promise` |
| 操作符 | `#9A8A7B` | `=` `+` `{}` |

内联 `code` 保持浅底 `#f0ece4`，不做语法高亮。

---

## 五B、暖亮风格色板（适用于女性力量 / 温暖可爱 / 轻松有趣类内容）

当文章主题偏向温暖、可爱、女性力量、轻松有趣时，使用暖亮风格替代默认暗底。

### 色板

| 名称 | 色值 | 用途 |
|------|------|------|
| 奶油底 | `#FFF8F0` | 默认暖底背景 |
| 桃花底 | `#FFF0F0` | 交替暖底背景 |
| 薰衣草底 | `#F8F0FF` | 交替暖底背景 |
| 珊瑚粉（主色） | `#FF6B8A` | 强调色、标题、关键数字 |
| 深玫瑰 | `#E8456B` | 重点强调、按钮 |
| 软紫 | `#B8A9E8` | 辅助色、装饰、标签 |
| 暖金 | `#FFB84D` | 高亮、星星、特殊标记 |
| 深紫文字 | `#3D2040` | 主文字 |
| 中紫文字 | `#6B4570` | 次要文字 |
| 淡紫文字 | `#A088A8` | 辅助文字 |

**比例法则**：暖底 70% : 珊瑚粉 10% : 软紫 5% : 暖金 5% : 其余 10%

### 装饰元素（CSS Unicode）

暖亮风格必须包含散点装饰元素，增加可爱感和设计感：

| 元素 | Unicode | 用途 |
|------|---------|------|
| 四角星 | `✦` | 标题旁、卡片角落 |
| 空心星 | `✧` | 较小的装饰点缀 |
| 心形 | `♡` | 女性主题、情感类内容 |
| 花朵 | `✿` | 角落装饰、分隔符 |
| 星星 | `★` | 评分、重点标记 |

装饰元素使用 `position: absolute`，散布在卡片四角和边缘，透明度 0.15-0.35，不遮挡内容。

### 卡片风格

- **圆角**：16-24px（比暗底风格更圆润）
- **阴影**：`0 4px 20px rgba(255,107,138,0.08)`（暖色调阴影）
- **边框**：`1.5px solid rgba(255,107,138,0.15)`（淡粉边框）
- **内卡片**：白色底 `#FFFFFF`，带暖色阴影
- **标签/Tag**：圆角胶囊形，背景 `rgba(255,107,138,0.1)`

### 暖底版品牌角标 SVG

将暗底版的白色替换为深紫色，筝弦金替换为珊瑚粉：
- `rgba(255,255,255,...)` → `rgba(61,32,64,...)`
- `#C4956A` → `#FF6B8A`

---

## 五C、配图数量与内容丰富度标准

### 最低数量要求

| 文章类型 | 最低配图数 | 推荐配图数 |
|---------|----------|----------|
| 深度长文（8000+ 字） | **10 张** | 12-15 张 |
| 教程文章（2000-4000 字） | **6 张** | 8-10 张 |
| 短文/随笔（<2000 字） | **3 张** | 5-6 张 |

### 内容丰富度要求

每张配图必须满足以下至少 2 项：

- [ ] **有实质内容**：不是只有标题 + 一行字，要有表格/列表/卡片/流程等信息载体
- [ ] **有视觉层次**：至少 3 层信息层次（标题 → 子标题 → 内容/数据）
- [ ] **有设计感**：使用卡片、网格、流程线、对比列等布局，而非纯文本列表
- [ ] **有装饰点缀**：散点装饰元素、渐变、图标等增加趣味性
- [ ] **有色彩变化**：相邻配图使用不同底色，避免视觉疲劳

### 布局多样性

一篇文章的 10+ 张配图，布局类型不应重复超过 3 次：

| 布局类型 | 适用场景 |
|---------|---------|
| 三列卡片网格 | 并列概念、分类展示 |
| 左右双栏对比 | Before/After、A vs B |
| 横向流程图 | 管线、工作流、认知路径 |
| 编号列表 | 步骤、要素、阶段 |
| 语录气泡 | 引用、对话、规训话术 |
| 大数字 + 描述 | 数据亮点、统计 |
| 时间线 | 人生线、历史进程 |
| 表格/矩阵 | 多维信息对比 |
| 金句终页 | 文末收束、核心观点 |

---

## 六、CDN 依赖

所有下载功能用这三个库：

```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>
```

---

## 七、Medium 风格变体（推荐：深度长文/技术深度文）

> 当文章偏深度长文/技术分析时，封面和配图可采用 Medium 风格。排版本身已融合 Medium 排版精华，此处仅影响头图/配图的设计风格。
> 核心原则：**少即多** — 一句话主张、一个焦点视觉、一处颜色强调。

### 设计七诫

1. **左对齐，不居中** — 标题贴左边距 60-80px，留右侧 35-45% 给焦点视觉
2. **一个 hero，不堆四件** — 删掉「主标题+副标题+keyword 框+底标签」的四件套，只留「编辑标签 + 主标题 + 一句话」
3. **数字反差** — 标题里的关键数据放到 1.4-1.8 倍主字号，正文文字反而缩小，让对比说话
4. **装饰即主角** — 单个 SVG/插图放右侧，opacity ≥ 0.55；不再用 0.10 的「背景噪音」
5. **一处筝弦金** — 整张封面/配图，筝弦金只许出现在 1 个元素上（首选：标题里的关键数字 / 配图的 section-tag 横线）
6. **字重降一档** — 标题 800（不是 900），副标题 400 italic（Medium 副标题习惯用斜体）
7. **字距收紧** — 大标题 letter-spacing: `-0.022em`；section-tag 反向放宽 `0.18em`

### 封面（900×383）规范

| 字段 | 数值 |
|---|---|
| 内容容器 | `display:flex; align-items:center; padding:0 60px;` 左对齐 |
| 编辑标签 | `font-size:11px; font-weight:700; letter-spacing:0.18em; color:#C4956A;` 上方 1px 金色横线 width: 32px |
| 主标题 | `font-size:64px; font-weight:800; letter-spacing:-0.022em; line-height:1.15; color:#F2EDE3;` 最多 2 行 |
| 标题中关键数字 | `font-size:88px; color:#C4956A;`（仅当 hook 是数字时用） |
| 一句话副标题 | `font-size:18px; font-weight:400; font-style:italic; color:rgba(255,255,255,0.55); margin-top:18px; max-width:520px;` |
| 焦点视觉 | 右侧绝对定位，居中垂直，宽 280-360px，`opacity:0.7-0.85`，不再加渐变遮罩 |
| 品牌角标 | 保留，左上角，缩小到 `22×22`，`brand-text` 改 11px |
| ❌ 删掉 | keyword-row 框、bottom-tags、左/右双装饰 SVG、bg-gradient |

**HTML 骨架：**

```html
<div class="cover" id="cover-main">
  <div class="bg-dark"></div>
  <!-- 焦点视觉：单个 SVG/插图，撑满右侧约 35% -->
  <div class="hero-art">
    <svg width="320" height="260" viewBox="..." style="opacity:0.75">...</svg>
  </div>
  <!-- 品牌角标 left-top -->
  <div class="brand">...</div>
  <!-- 内容：左对齐 -->
  <div class="content">
    <div class="kicker">章节标签·主题</div>
    <h1 class="title">主标题，<span class="hook">数字</span> 后半句</h1>
    <p class="lede">一句话补足主张的 lede，控制在 30 字以内</p>
  </div>
</div>
```

**关键 CSS：**

```css
.cover { width:900px; height:383px; position:relative; overflow:hidden; background:#1C1C1E; }
.hero-art { position:absolute; right:48px; top:50%; transform:translateY(-50%); z-index:1; }
.content { position:absolute; inset:0; display:flex; flex-direction:column; justify-content:center; padding:0 380px 0 70px; z-index:2; }
.kicker {
  font-size:11px; font-weight:700; letter-spacing:0.18em; color:#C4956A;
  text-transform:uppercase; padding-top:10px; position:relative;
}
.kicker::before {
  content:''; position:absolute; top:0; left:0; width:32px; height:1px; background:#C4956A;
}
.title {
  font-size:64px; font-weight:800; letter-spacing:-0.022em; line-height:1.15;
  color:#F2EDE3; margin-top:18px;
}
.title .hook { color:#C4956A; font-size:88px; font-weight:900; letter-spacing:-0.03em; }
.lede {
  font-size:18px; font-weight:400; font-style:italic;
  color:rgba(255,255,255,0.55); margin-top:18px; max-width:520px; line-height:1.5;
}
```

> **次图（200×200）裁剪策略**：因主图左对齐，次图改为「裁主标题左下角 200×200 区块」（含金线 kicker + 标题首两字 + 数字 hook 的一部分），更有识别度。

### 配图（800×420）规范

主要差异：section-tag 改成「金色细横线 + 小写字距」编辑风格，丢弃灰盒。

| 字段 | 暗底 | 浅底 |
|---|---|---|
| section-tag | 上方 1px `#C4956A` 横线 width:28px + 11px 0.18em letter-spacing 文字 `#C4956A` | 同左，颜色不变 |
| 标题 | 32-36px / 800 / `-0.018em` / `#F2EDE3` | 32-36px / 800 / `-0.018em` / `#1C1C1E` |
| 副标题（可选） | 14px italic / 400 / `rgba(255,255,255,0.55)` | 14px italic / 400 / `#7A7876` |
| 装饰大数字 | opacity 0.06（不是 0.15），靠右下，不抢戏 | 同 |
| 卡片间距 | `gap:24px`（比原来宽 8px），呼吸感 | 同 |
| 筝弦金使用 | **每张图只 1 处**：首选 section-tag 横线 | 同 |

**section-tag 模板：**

```html
<div class="section-tag-medium">
  <div class="kicker-line"></div>
  SECTION TAG
</div>
```

```css
.section-tag-medium {
  display:inline-block; font-size:11px; font-weight:700; letter-spacing:0.18em;
  color:#C4956A; text-transform:uppercase; padding-top:10px; position:relative;
}
.section-tag-medium .kicker-line {
  position:absolute; top:0; left:0; width:28px; height:1px; background:#C4956A;
}
```

### 何时用 Medium 风格 vs 默认风格

| 文章类型 | 推荐 |
|---|---|
| 技术深度文 / 长文 | **Medium 风格** |
| 教程 / 工具速记 / 资源列表 | 默认风格（信息密度高，多卡片） |
| 暖亮主题（女性力量等） | 五B 暖亮风格 |
| 游戏 / 测评（带产品截图） | 默认风格 + 截图背景 |

> 决定后写在 manifest.json 的 `cover.style` / `illustrations.style` 字段（值：`mozheng` / `medium` / `warm`），方便后续重新生成对齐。

### Medium 配图常见 bug 与防护（务必遵守）

写 Medium 风格配图时，下列两类错误高频出现，已造成过线上效果问题：

**1. 暗底/浅底文字颜色失效（文字与背景同色）**

错误根源：用 `.on-dark .x-h { color: #F2EDE3 }` 这类选择器，但 `.on-dark` 只挂在 `.brand` / `.ghost-num` 这种局部元素上，根 `.slide` 容器没有 `.on-dark`，正文文字选择不中。

✅ **正确做法**：把 `dark` / `light` 直接打到 `.slide` 根上，所有内文颜色用根类前缀作用域：

```html
<div class="slide dark" style="height:420px;">  <!-- 根容器决定主题 -->
  <div class="bg-dark"></div>
  <div class="brand on-dark">...</div>          <!-- on-dark 仅给品牌/页码用 -->
  <div class="content">
    <h2 class="h-title">...</h2>                <!-- 不再加 on-dark 后缀 -->
    <div class="info-body"><div class="info-h">...</div></div>
  </div>
</div>
```

```css
.slide.dark .info-h { color: #F2EDE3; }
.slide.light .info-h { color: #1C1C1E; }
```

每个 slide 在生成时**必须**带上 `dark` 或 `light`，不能省略。

**2. 流程图模块重叠**

错误根源：`display: grid` 设了 `grid-template-columns: 110px 16px 130px ...`，但子元素 `.flow-card` 又设 `min-width: 130px`，第一列被撑爆压住相邻列。

✅ **正确做法**：流程图统一用 `flex` + `flex-shrink: 0`，让每个卡片按内容宽度自然撑开，不要混用 grid 固定列宽与 flex-card min-width：

```css
.flow-row { display: flex; align-items: center; gap: 4px; flex-wrap: nowrap; }
.flow-row .flow-card { flex-shrink: 0; }       /* 关键：不被压缩 */
.flow-row .arrow { flex-shrink: 0; padding: 0 10px; }
```

**3. 通用自检清单（Medium 配图生成后必查）**

- [ ] 每个 `.slide` 都有 `dark` 或 `light` 根类
- [ ] 浏览器打开后所有文字可读（暗底白字、浅底黑字）
- [ ] 流程图无元素重叠（用 flex，禁用 grid 与 min-width 混搭）
- [ ] section-tag 上方金色横线渲染正常（不被 `overflow:hidden` 切掉）
- [ ] 装饰大数字（ghost-num）不遮挡正文（`pointer-events:none` + 右下角，opacity ≤ 0.06）
- [ ] 整张图筝弦金 `#C4956A` 出现次数 ≤ 2


