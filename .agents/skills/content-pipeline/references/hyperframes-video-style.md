# 墨筝 HyperFrames 视频风格

这是 `content-pipeline` 生成 HyperFrames 视频时的默认品牌预设。它适合技术分析、产品对比、架构解释和选型建议，目标是形成“技术编辑部 + 电影感信息图”的稳定视觉语言。

## 视觉定位

- 气质：克制、精确、沉稳，有编辑判断力，不做泛科技炫光
- 画面：大字号、结构线、分层图解、非对称构图
- 节奏：信息进入清晰，停留时间充足，转场利落但不躁动
- 默认画幅：1080×1920 竖版
- 平台安全区：顶部至少 180px；正文容器使用 `padding:340px 64px 80px`

## 固定色板

生成 `design.md` 和 composition 时默认使用以下颜色，不另造近似色：

| 角色 | 色值 |
|------|------|
| 背景 | `#1C1C1E` |
| 前景 | `#F2EDE3` |
| 筝弦金 | `#C4956A` |
| 浅金 | `#D8B28C` |
| 次级文字 | `#B8B0A4` |
| 面板 | `#272528` |
| 规则线 | `#4A4540` |

背景使用墨色实底，可叠加局部暖金径向光和低对比网格。禁止整屏线性渐变、青紫霓虹和渐变文字。

## 字体

字体资产的 single source of truth：

```text
content/_shared/fonts/zcool-xiaowei.ttf
content/_shared/fonts/noto-sans-sc.ttf
```

每次创建视频项目时复制到 `content/[slug]/video/hyperframes/fonts/`。`IBM Plex Mono` 由 HyperFrames 自动解析。

```css
@font-face {
  font-family: "ZCOOL XiaoWei";
  src: url("fonts/zcool-xiaowei.ttf") format("truetype");
  font-style: normal;
  font-weight: 400;
  font-display: swap;
}
@font-face {
  font-family: "Noto Sans SC";
  src: url("fonts/noto-sans-sc.ttf") format("truetype");
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
}
```

| 内容 | 字体 | 字号 | 字重 |
|------|------|------|------|
| 中文展示标题 | `ZCOOL XiaoWei` | 76–112px | 400 |
| 中文正文 | `Noto Sans SC` | 32–42px | 300–700 |
| 技术标签/英文 | `IBM Plex Mono` | 20–30px | 500–700 |

展示标题保持 `line-height:1.0–1.1`、`letter-spacing:-0.03em–-0.05em`。不要对 `letter-spacing` 做 GSAP 动画；只使用 transform 和 opacity。

## 画面组件

### 背景层

- 80×80px 低对比网格
- 轻微颗粒纹理，opacity 约 `0.10–0.14`
- 260px 左右的超大幽灵词，使用筝弦金 8%–12% 透明度
- 局部暖金径向光，不超过画面三分之一

### 信息面板

- 背景 `#272528`
- 边框 `2–3px solid #4A4540`
- 重点面板边框改用 `#C4956A`
- 圆角 8–16px，禁止胶囊形
- 不使用通用投影卡片；仅允许局部暖金辉光

### 构图

- 标题、图解和卡片采用非对称排列
- 用规则线、箭头、编号和注册标记组织阅读顺序
- 避免等宽等高的通用卡片矩阵；根据内容层级改变尺寸和偏移
- 技术图解优先使用层级、路径、边界和状态关系，不堆装饰图标

## 动效

- 每个场景所有主要元素都要有入口动画
- 入口混合使用方向滑入、比例盖章、线条绘制和透明度显现
- 同一场景至少使用 3 种 easing，避免机械一致
- 环境动效只做慢速网格漂移、局部呼吸和关系线脉冲
- 场景之间使用 0.8 秒左右的筝弦金遮罩转场；禁止跳切
- 除最终场景外不做退出动画，转场负责覆盖上一场景
- 最终场景可在最后 0.8–1 秒轻微淡出
- 禁止动画 `letterSpacing`、布局尺寸和其他会触发布局重排的属性

时间轴必须 paused、同步构建、有限循环，并注册到 `window.__timelines`。

## 品牌元素

- 常驻水印：`公众号：墨筝`
- 水印位置：`top:228px; left:60px`
- 水印透明度约 0.7，后接一条 180px 筝弦金细线
- BGM：`content/_shared/bgm.mp3`，`data-volume="0.3"`
- 尾屏 CTA：`完整对比与选型细节，请关注公众号「墨筝」`

水印需要 `class="clip"` 供 Studio 识别，但不得继承场景全屏背景：

```css
.clip { position: absolute; }
section.clip { inset: 0; overflow: hidden; background: #1C1C1E; }
```

## `design.md` 最小模板

```markdown
# [Topic] — Video Design

## Format
- Canvas: 1080 × 1920
- Mood: technical editorial, calm authority, precise rather than futuristic
- Density: cinematic infographic; large type, structural rules, layered diagrams

## Palette
- Background: `#1C1C1E`
- Foreground: `#F2EDE3`
- Accent: `#C4956A`
- Accent light: `#D8B28C`
- Secondary text: `#B8B0A4`
- Panel: `#272528`
- Rule: `#4A4540`

## Typography
- Display: `"ZCOOL XiaoWei", serif`, weight 400
- Body: `"Noto Sans SC", sans-serif`, weight 300–700
- Technical labels: `"IBM Plex Mono", monospace`, weight 500–700
- Headlines: 76–112px
- Body: 32–42px
- Labels: 22–26px

## Shape and Depth
- Corners: 8–16px, never pill-shaped
- Borders: 2–3px
- Flat panels with localized warm glow
- Subtle grid, grain, oversized ghost terms, registration marks

## Avoid
- Cyan or purple neon
- Gradient text
- Generic equal-sized card grids
- Centered web-page layouts
- Tiny UI text
- Excessive glow
- Emojis
```

## 验收

1. `npx hyperframes lint`
2. `npx hyperframes check --samples 15`
3. 先渲染 `draft.mp4`，从每个场景中段提取关键帧，实际检查 1080×1920 全画布
4. 确认无文字裁切、越界、遮挡和空场景
5. 确认转场覆盖完整，水印和 CTA 可见
6. 最终使用 `npx hyperframes render --output output.mp4 --quality high`
7. 用 `ffprobe` 核对时长、1080×1920、视频轨和 AAC 音轨

若当前 HyperFrames 版本的 `check`/`inspect` 自身报错，但 lint 和渲染可用，不得跳过视觉验收；改用 draft render + 关键帧检查。
