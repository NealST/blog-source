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
| 筝弦金 | `#C4956A` | **强调 strong、序号底、头像描边、品牌角标、CTA、END 分隔** |
| 金色高亮 | `rgba(196,149,106,0.08-0.18)` | 装饰光晕、CTA 背景 |
| 分隔线 | `rgba(28,28,30,0.08)` | Footer 顶部分隔 |

**比例法则**：宣纸 75% · 灰文字 18% · 筝弦金 5% · 墨色 2%。**禁用朱红等其它强调色**，确保与公众号无缝衔接。

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

---

## 四、Header 设计（每张卡都有）

```
[头像 44×44 圆形, 筝弦金 1.5px 描边]   墨筝
                                       MM/DD     ← 灰 #888 13px
```

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
.avatar-wrap .avatar { width:100%; height:100%; object-fit: cover; position: relative; z-index: 1; }
.avatar-wrap .avatar-fallback {
  position: absolute; inset: 0; display: flex;
  align-items: center; justify-content: center;
  color: #F2EDE3; font-size: 22px; font-weight: 700;
  font-family: "Songti SC", serif; z-index: 0;
}
```

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
  <p>开场段。一句话钩住，<strong>金色 strong</strong> 用于关键概念。</p>
  <p>展开段。<span class="ink">想压深色的关键词用 .ink</span>。</p>

  <div class="num-item">
    <span class="num">1</span>
    <p><strong>核心观点。</strong>展开说明。</p>
  </div>
</section>
```

```css
.post-body p { font-size: 18px; line-height: 1.6; color: #333; margin-bottom: 8px; }
.post-body strong { color: #C4956A; font-weight: 600; }
.post-body .ink { color: #1C1C1E; font-weight: 700; }

.num-item { display: flex; gap: 14px; margin-bottom: 22px; align-items: flex-start; }
.num-item .num {
  flex: 0 0 32px; height: 32px; border-radius: 50%;
  background: #C4956A; color: #F2EDE3;
  font-size: 15px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 6px rgba(196,149,106,0.3);
}
```

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
