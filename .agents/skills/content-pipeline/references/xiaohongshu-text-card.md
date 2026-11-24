# 小红书文字卡片风格（唯一风格・公众号同源配色）

> 📌 **小红书现在只用这一种风格**。之前的多卡片信息图风格（`xiaohongshu-format.md`）已废弃，仅作为历史存档。
>
> 首选范例：[`xiaohongshu-examples/markdown-faithful-范例.html`](./xiaohongshu-examples/markdown-faithful-范例.html)（v2 Markdown 1:1 还原版式）
> 旧版范例：[`xiaohongshu-examples/文字卡片-范例.html`](./xiaohongshu-examples/文字卡片-范例.html)（仅作回顾）

---

## 二、配色（与公众号 preview.html 完全同源）

直接复用 `md2wechat_formatter.py` 产物 `content/[slug]/preview.html` 里的色板，保证小红书 / 公众号视觉统一。

| 名称 | 色值 | 用途 |
|------|------|------|
| 宣纸底 | `#F2EDE3` | 主背景色（卡片可用 `#F6F1E7 → #F2EDE3 → #ECE4D2` 渐变做层次） |
| 墨色 | `#1C1C1E` | 用户名、深色关键词、金句标题（`.ink` / `.q`） |
| 正文灰 | `#333` | 普通段落正文 |
| 弱文字灰 | `#888` | 日期、品牌字、页码、CTA label |
| 筝弦金 | `#C4956A` | **序号底、头像描边、品牌角标、h2 左竖线、CTA、END 分隔** |
| 金色高亮 | `rgba(196,149,106,0.08-0.18)` | 装饰光晕、CTA 背景 |
| 分隔线 | `rgba(28,28,30,0.08)` | Footer 顶部分隔 |

**比例法则**：宣纸 75% · 灰文字 18% · 筝弦金 5% · 墨色 2%。**禁用朱红等其它强调色**，确保与公众号无缝衔接。

**内容页背景色强制要求**：所有内容页（第 2 张 ~ 倒数第 2 张）必须使用宣纸底 `#F2EDE3`（`.bg-paper` 渐变），**禁止使用纯白 `#FFFFFF`**。纯白在小红书 app 的深色边框下显得「飘」，宣纸底更有质感且与公众号视觉统一。

**字体**：

```css
font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
             "Noto Sans SC", "Microsoft YaHei", sans-serif;
```

全局使用系统无衬线字体。**例外**：h1 文章主标题使用 `"Songti SC", "Source Han Serif SC", serif` 衬线字体（配合上下黑色细线装饰），与 markdown-faithful 范例一致。

---

## 三、尺寸

- 单卡显示：`540 × 720 px`（3:4 小红书标准）
- 导出：`1080 × 1440 px`（2x，复用主模板的 `renderSlide` + `flattenAlpha`，fallback 色改为 `#F2EDE3`）
- 卡片内 padding：`32px 40px 24px`（与 markdown-faithful 范例一致）
- 段落字号：`18px / line-height 1.6`（与 markdown-faithful 范例一致）

### 原文图片尺寸例外

`540 × 720` 只适用于生成的文字卡、封面和封底。原文 Markdown 图片不进入该画布：

- 每张原图本身就是一张独立轮播素材；
- 保持原图宽高比，不裁切、不补黑边、不补宣纸底、不加圆角或阴影；
- 预览容器使用 `height:auto`，导出时使用图片的 `naturalWidth × naturalHeight` 创建 PNG 画布；
- 禁止用 `object-fit: contain` 把横图塞进 3:4 卡片。

---

## 四、Header 设计（每张文字卡都有）

```
[头像 44×44 圆形]   墨筝                         关注我
                    MM/DD              持续更新 AI 实战
```

左侧作者信息保持原结构，右侧关注提示必须靠右对齐。关注提示是文字卡、封面和封底的固定品牌组件；原文图片独占页不得添加。

```html
<header class="post-header">
  <div class="avatar-wrap">...</div>
  <div class="meta">
    <div class="name">墨筝</div>
    <div class="date">MM/DD</div>
  </div>
  <div class="follow-prompt">
    <div class="follow-title">关注我</div>
    <div class="follow-subtitle">持续更新 AI 实战</div>
  </div>
</header>
```

```css
.follow-prompt { margin-left: auto; text-align: right; line-height: 1.35; }
.follow-title { color: #C4956A; font-size: 14px; font-weight: 700; }
.follow-subtitle { color: #888; font-size: 11px; margin-top: 2px; letter-spacing: .5px; }
.cover-slide .follow-title,
.end-slide .follow-title { color: #D8B28C; }
.cover-slide .follow-subtitle,
.end-slide .follow-subtitle { color: rgba(242,237,227,.55); }
```

**对齐硬规则**：`.follow-prompt` 必须同时设置 `margin-left:auto` 与 `text-align:right`，两行文案右边缘对齐，不得紧贴昵称或居中。

### 头像处理（重点 ⚠️）

头像图片放在仓库根目录的共享位置：

```
content/_shared/avatar.jpg
```

在范例 HTML（位于 `.agents/skills/content-pipeline/references/xiaohongshu-examples/`）中引用路径要 **回退 5 级**：

```html
<img class="avatar" src="../../../../../content/_shared/avatar.jpg" alt="墨筝"
     onerror="this.style.display='none'">
```

**如果在 `content/[slug]/` 目录下生成正式发布的 HTML**，路径只需 **回退 2 级**：

```html
<img class="avatar" src="../_shared/avatar.jpg" alt="墨筝" onerror="this.style.display='none'">
```

**回退方案**：用 `.avatar-wrap` 双层结构，外层是金色渐变 + "墨" 字 fallback，`<img>` 加载失败时隐藏，自动露出回退层。再也不会出现"图崩了卡片就崩了"的情况。

```html
<div class="avatar-wrap">
  <span class="avatar-fallback">墨</span>
  <img class="avatar" src="..." onerror="this.style.display='none'">
</div>
```

```css
.avatar-wrap {
  position: relative; width: 44px; height: 44px;
  border-radius: 50%; overflow: hidden;
  border: 1.5px solid #C4956A;
  background: linear-gradient(135deg, #C4956A 0%, #8a6240 100%);
  box-shadow: 0 2px 10px rgba(28,28,30,0.18);
}
.avatar-wrap .avatar {
  position: absolute; inset: 0; z-index: 1;
  width: 100%; height: 100%; object-fit: cover; display: block;
}
.avatar-wrap .avatar-fallback {
  position: absolute; inset: 0; display: flex;
  align-items: center; justify-content: center;
  color: #F2EDE3; font-size: 22px; font-weight: 700;
  font-family: "Songti SC", serif; z-index: 0;
}
```

**验收要求**：头像加载成功时只能看到头像照片，不能看到“墨”字。`.avatar-fallback` 必须绝对定位在底层，`.avatar` 必须绝对定位并完整覆盖容器；两者不能作为普通 flex 子项并排。

### 日期自动注入

```html
<script>
  const d = new Date();
  const mm = String(d.getMonth()+1).padStart(2,'0');
  const dd = String(d.getDate()).padStart(2,'0');
  document.querySelectorAll('.date').forEach(el => el.textContent = `${mm}/${dd}`);
</script>
```

---

## 五、Body 设计

```html
<section class="post-body">
  <p>开场段。一句话钩住，<strong>加粗关键概念</strong>用深色突出。</p>
  <p>展开段。<span class="ink">想压深色的关键词用 .ink</span>。</p>

  <div class="num-item">
    <span class="num">1</span>
    <p><strong>核心观点。</strong>展开说明。</p>
  </div>
</section>
```

### ⚠️ 金色使用禁区（高频错误，必须逐项检查）

> **筝弦金 `#C4956A` 只允许用在以下 6 处**：h2 左竖线、序号圆底 `.num`、头像描边、顶栏关注标题 `.follow-title`、footer 品牌字 `.gz`、封底 `.hl` 高亮（最多 1 处）。
>
> **以下元素禁止使用 `#C4956A`，违反即为 BUG**：
> - `strong` → 必须 `color: #1C1C1E; font-weight: 700`
> - `.h3` → 必须 `color: #2C2A28`（不是金色！）
> - `.bullet`（列表圆点）→ 必须 `color: #999`
> - `code`（内联代码）→ 必须 `color: #1C1C1E`

```css
/* ===== Body 核心样式（必须原样复制） ===== */
.post-body p { font-size: 18px; line-height: 1.6; color: #333; margin-bottom: 8px; }
.post-body strong { color: #1C1C1E; font-weight: 700; }   /* ❌ 禁止金色 */
.cover .post-body strong { color: #F2EDE3; }              /* 深色封面必须显式覆盖 */
.post-body .ink { color: #1C1C1E; font-weight: 700; }

/* h3 子标题：深色，不用金色 */
.post-body .h3 {
  font-size: 19px; font-weight: 700; color: #2C2A28;       /* ❌ 禁止 #C4956A */
  margin-bottom: 10px; margin-top: 4px; letter-spacing: 0.5px;
}

/* 列表项 */
.list-item { display: flex; gap: 8px; margin-bottom: 7px; font-size: 18px; line-height: 1.6; }
.list-item .bullet { color: #999; font-weight: bold; flex-shrink: 0; } /* ❌ 禁止金色 */
.list-item.sub { margin-left: 18px; font-size: 16px; }

/* 内联代码 */
code {
  background: #E8E0D1; color: #1C1C1E;                     /* ❌ 禁止 #b8621b 等非品牌色 */
  padding: 1px 5px; border-radius: 4px;
  font-family: "SF Mono", Menlo, monospace; font-size: 0.92em;
  white-space: nowrap;
}
code.cmd-block {
  display: block; white-space: pre-wrap; word-break: break-word;
  padding: 8px 12px; margin-top: 6px; line-height: 1.55;
}

/* 序号圆（仅此处可用金色底） */
.num-item { display: flex; gap: 14px; margin-bottom: 22px; align-items: flex-start; }
.num-item .num {
  flex: 0 0 32px; height: 32px; border-radius: 50%;
  background: #C4956A; color: #F2EDE3;
  font-size: 15px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 6px rgba(196,149,106,0.3);
}
```

### 深浅主题文字覆盖规则

正文页的墨色文字规则不能直接套到深色封面或深色封底。凡容器切换为 `#1C1C1E` 等深色背景，容器内所有承载内容的文字变体（至少包括 `p`、`strong`、`.ink`、标题、链接和代码注释）都必须由主题选择器显式指定浅色，不能依赖继承或通用正文选择器。深色封面的加粗文字固定使用：

```css
.cover .post-body strong { color: #F2EDE3; }
```

主题覆盖选择器必须与实际 HTML 容器 class 一致，并放在通用正文规则之后。生成后需在浏览器中读取最终 computed style 验证，不能只搜索 CSS 源码。

---

## 五B、代码块样式

技术类文章中的代码块使用暗底样式（与公众号代码块一致）：

```html
<div class="code-block">
  <div class="code-lang">python</div>
  <pre><code>def hello():
    print("world")</code></pre>
</div>
```

```css
.code-block {
  background: #1C1C1E; border-radius: 8px; overflow: hidden;
  margin-bottom: 10px;
}
.code-block .code-lang {
  background: #2C2A28; color: #C4956A;
  font-family: 'SF Mono', Menlo, monospace;
  font-size: 11px; font-weight: 600; padding: 4px 14px;
  letter-spacing: 1px; text-transform: uppercase;
  border-bottom: 1px solid #3D3632;
}
.code-block pre {
  padding: 12px 16px; margin: 0;
}
.code-block code {
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 14px; line-height: 1.5; color: #F2EDE3;
  white-space: pre-wrap; word-break: break-word;
}
```

**规则**：代码块超过 8 行时截断，末尾注释 `// 完整代码见公众号原文「墨筝」`。

---

## 六、Footer

每张卡片 footer 都包含两部分：

```html
<footer class="post-footer">
  <div class="brand-wrap">
    <svg ... fill="#C4956A">品牌角标</svg>
    <span class="brand">微信搜索公众号<span class="gz">「墨筝」</span>查看更多精彩内容</span>
  </div>
  <span class="page">1 / 3</span>
</footer>
```

```css
.post-footer { padding-top: 14px; border-top: 1px solid rgba(28,28,30,0.08); 
               display: flex; justify-content: space-between; align-items: center; }
.post-footer .brand-wrap { display: flex; align-items: center; gap: 8px; }
.post-footer .brand-svg { opacity: 0.7; }
.post-footer .brand { font-size: 11px; color: #888; letter-spacing: 1.5px; }
.post-footer .brand .gz { color: #C4956A; font-weight: 700; padding: 0 2px; }
.post-footer .page { font-size: 12px; color: #888; }
```

品牌角标 SVG：复用旧 `xiaohongshu-format.md` 中的角标，stroke `rgba(28,28,30,0.5)`，主色 fill `#C4956A`。

---

## 六B、封面滑动引导（仅第 1 张）

封面卡底部增加滑动引导提示，位于 footer 上方：

```html
<div class="swipe-hint">
  <span class="swipe-arrow">←</span> 左滑查看更多
</div>
```

```css
.swipe-hint {
  text-align: center; font-size: 12px; letter-spacing: 1px;
  margin-top: auto; padding-bottom: 8px;
}
/* 深底封面 */
.swipe-hint.dark { color: rgba(242,237,227,0.5); }
/* 浅底封面 */
.swipe-hint.light { color: rgba(28,28,30,0.3); }
```

**静态箭头**（PNG 导出友好，替代 CSS animation）：

```html
<div class="swipe-hint dark">
  <span class="swipe-arrows">‹ ‹ ‹</span> 左滑查看更多
</div>
```

```css
.swipe-arrows {
  display: inline-block;
  letter-spacing: 3px; font-weight: 300; opacity: 0.7;
  background: linear-gradient(90deg, currentColor 0%, transparent 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

渐隐箭头序列在静态截图中也能传达"向左滑动"的视觉暗示。如果目标仅为浏览器预览（不导出 PNG），仍可保留 `@keyframes swipe-nudge` 动画。

**规则**：仅第 1 张封面卡有，内容页和封底不需要。

---

## 七、封底卡

最后一张结构：**金句 + END mark + 统一 footer**。不再使用大 CTA 盒子，微信推广由 footer 的提示行统一承担。

```html
<div class="quote-card">
  <div>
    <div class="q">金句一句话，<span class="hl">关键字金色</span>。</div>
    <div class="dash"></div>
    <div class="sub">— 副标题灰色字 —</div>
  </div>
</div>

<div class="end-mark" style="margin-top: auto;">— END —</div>
<!-- footer 同上 -->
```

`.end-mark` 直接复用公众号文末的"— END —"样式（`#C4956A` letter-spacing 3px opacity 0.6）。

---

## 八、多卡片分页规则

1. 每张卡只放 720px 高度内能自然容纳的内容（一般 3-5 段或 2-3 个编号项）。
2. Header 在每张卡片都重复。
3. 页码 `n / N` 右下角持续显示。
4. 不在中间硬切句子，整段移到下一张。
5. 最后一张作为封底。

---

## 九、与默认墨色风格的关系

| 维度 | 默认（墨色暗底信息图） | 文字卡片（本规范） |
|------|---------|---------|
| 调性 | 科技 / 产品 / 教程 | 个人 / 分享 / 观感 |
| 底色 | 墨色 `#1C1C1E` | 宣纸 `#F2EDE3` |
| 文字 | 宣纸白 `#F2EDE3` | 正文灰 `#333` / 墨色 `#1C1C1E` |
| 强调色 | 筝弦金 `#C4956A` | 筝弦金 `#C4956A`（一致） |
| 字体 | PingFang SC | PingFang SC（一致） |
| 与公众号 preview.html | 互补（深色） | **完全同源**（直接搬色板） |

文字卡片相当于把公众号文章的视觉直接搬到了小红书 3:4 画布上，**用户从小红书图跳到公众号不会有违和感**。

---

## 十、头像资源放置

```bash
mkdir -p content/_shared
# 把头像图片保存为：
# content/_shared/avatar.jpg
```

**要求**：
- 正方形 ≥ 256×256
- JPG 或 PNG（统一命名 `.jpg`）
- 换头像直接覆盖这个文件，所有引用同步生效

**为什么头像不显示？** 99% 是这两个原因之一：
1. `content/_shared/avatar.jpg` 不存在 → 按上面命令保存
2. HTML 在不同目录层级里，相对路径 `..` 数错了 → 按本文第四节的两种场景对照路径
