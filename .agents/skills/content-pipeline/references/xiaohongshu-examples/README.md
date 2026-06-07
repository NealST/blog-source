# 小红书范例

> 小红书现在 **只用一种风格：文字卡片**（公众号同源配色）。生成前必读对应规范。

---

## 📝 文字卡片 · 唯一风格

**首选范例：** [`markdown-faithful-范例.html`](./markdown-faithful-范例.html)（v2 Markdown 1:1 还原版式，含 h1/h2/h3 区分 + 图片独占卡片 + 下载工具栏）
**旧版范例：** [`文字卡片-范例.html`](./文字卡片-范例.html)（仅作回顾，新出稿一律用 v2）
**规范：** [`../xiaohongshu-text-card.md`](../xiaohongshu-text-card.md)

公众号同源配色：宣纸底 `#F2EDE3` + 墨色文字 `#1C1C1E` + 筝弦金 `#C4956A` + PingFang SC 无衬线。3:4 卡片，540×720 显示 / 1080×1440 导出。

### 质量标准

✅ **每张卡 Header**：圆形头像（金色描边） + "墨筝" + 当前日期 `MM/DD`（脚本自动注入）
✅ **段落 + 编号项交替**：18px / line-height 1.6，`<strong>` 金色，`.ink` 墨色压重
✅ **每张卡 Footer**：分隔线下左侧 `[图标] 微信搜索公众号「墨筝」查看更多精彩内容`，右侧页码 `n / N`
✅ **封底卡**：金句 + dash + 副标题 + END mark
✅ **头像回退**：`.avatar-wrap` 双层结构，`<img onerror>` 失败自动露出金色 + "墨"字 fallback，永远不会塌
✅ **导出脚本**：复用 `renderSlide` + `flattenAlpha`，宣纸底 fallback 色 `#F2EDE3`

---

## 头像资源

放置路径：

```
content/_shared/avatar.jpg
```

要求：正方形 ≥ 256×256。换头像直接覆盖此文件，所有引用同步生效。
