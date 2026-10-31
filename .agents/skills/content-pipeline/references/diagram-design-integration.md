# diagram-design 正文配图集成

本参考只负责 content-pipeline 与 diagram-design 之间的衔接。图型、连线、复杂度、可访问性与导出规范以 `../../diagram-design/SKILL.md` 及其对应 references 为准，不在这里复制整套规则。

## 1. 职责与选型

- TopView：公众号头图，突出单一主体或视觉隐喻，流程不变。
- xiaohei-illustrations：观点、隐喻、情绪、认知锚点，仍为正文默认风格。
- diagram-design：读者需要看清组件关系、执行顺序、状态转移或数据比较时，生成品牌结构图。
- 普通清单、属性对照、单句概念：优先文字或表格，不为覆盖章节而强行画图。

每个章节最多一张图。先检查原文已有图片，再决定是否补图；新图不能只是重复已有图片的语义。图中结论、节点、关系、数值与单位须能追溯至正文或明确来源，不把推测画成事实。

常见路由如下；实际绘制前必须读取 diagram-design 的对应图型参考：

| 核心信息 | 图型 |
| --- | --- |
| 组件与连接 | Architecture |
| 改造前后的拓扑变化 | Architecture delta |
| 判断分支与条件 | Flowchart |
| 调用顺序与参与方 | Sequence |
| 状态、转移与触发条件 | State machine |
| 跨角色职责交接 | Swimlane / Process（选主导图型） |
| 实体关系、数据结构 | ER / data model |
| 层级或依赖 | Tree / Dependency graph（按关系选择） |
| 数量对比、趋势、二维数值 | Bar / Line / Heatmap（按数据选择） |

行为、安全边界或风险传播承载核心含义时，先读取 `../../diagram-design/references/semantic-patterns.md`，选一个语义模式，再选布局图型。静态图为默认，不因支持动画就添加动画。

## 2. 品牌与首次设置

生成前按 `../../diagram-design/references/profiles.md` 解析项目 `.diagram-design` marker 与有效 profile。已有明确选择时使用该 profile；缺失或无效时按该技能的恢复流程处理，不静默换肤。

没有有效 profile 且仍为出厂样式时，按 onboarding 的“已安装 skill”或“本地设计系统”路径，将 content-pipeline 品牌规范作为来源，向用户展示映射后确认。用户要求直接生图不等于授权覆盖 profile 或修改全局风格。此时不应静默输出出厂橙色皮肤，也不应跳过首次设置门槛。

默认建议映射（用户明确指定其他品牌时遵从其选择）：

| 语义角色 | content-pipeline 建议 |
| --- | --- |
| `paper` | `#FFFFFF`，正文配图整页纯白 |
| `paper-2` | `#F2EDE3`，仅用于局部容器，不作为整图底色 |
| `ink` | `#1C1C1E`，主文字与主要线条 |
| `accent` | `#C4956A`，筝弦金，仅用于少量焦点 |
| 其他角色与字体 | 从 `brand-colors.md` 和有效 style guide 中解析，核对对比度，不凭空补色 |

品牌色以 `brand-colors.md` 为来源；参考 `cover-template.md` 的配图约束，但不沿用封面装饰布局。中文字体按 diagram-design 的非拉丁标签规范配置，确认实际字体已加载并说明回退。浅底整图不得使用宣纸色；深底仅在用户明确指定或已有视觉方案要求时使用。

保存命名 profile、写项目 marker 或切换共享工作副本时，严格遵守 profiles 的授权流程。不要为了本次文章改写 diagram-design 的通用 SKILL.md；新增图型不需要改本管线。

## 3. 规划与单图生成

shot list 中每张结构图记录：

- 稳定编号与文件名：`N`、`NN-topic.html`。
- 正文锚点、图的主题、信息来源、与已有图片的差异。
- 主图型、语义模式（如有）、尺寸预设、受复杂度预算限制而合并或移出的内容。
- 品牌 profile 或确认后的风格来源。

默认采用 diagram-design 的 `doc-inline` 尺寸预设，按其 output-spec 设置 viewBox 和字号；横向关系较多可用 `doc-wide`。以发布后的正文实际宽度检查中文可读性，不直接把复杂大图缩小到正文宽度。超预算时先简化；若必须拆成总览与细节，重新规划位置，不违反每章一图的规则。

按 diagram-design 的模板输出自包含 HTML，保存至 `content/[slug]/diagrams/NN-topic.html`。绘制前简短说明图型、尺寸和删减项；已明确指定时按该技能的确认规则执行。

## 4. 接入现有渲染链

本管线的配图任务明确包含 PNG 导出；因此按 diagram-design 的 `references/export.md` 读取导出要求，最终仍沿用管线的文件名与占位符。

1. 单图通过 diagram-design 的检查后，将内联 SVG 与所需 CSS 汇入 `content/[slug]/illustrations.html`。保留 `diagrams/` 中的原始 HTML 便于编辑。
2. 用既有 `.slide[data-num="N"]` 包裹图，不用 iframe、外链 SVG 或整页截图。样式限制在该 slide 内，避免单图的 `body`、`h1` 或全局 `svg` 规则污染其他图。
3. SVG 的所有 ID、marker、clipPath、渐变及其引用使用该图独有的前缀；同步更新 `aria-labelledby`。保留 `<title>`、`<desc>` 和 `role="img"`。
4. 如需可见标题，将其放在 SVG 内或稳定的导出框内；`slide-label` 只表示插入位置，不进入 PNG。导出框使用不透明背景、直角外边缘，不能截断 SVG、中文标签或图例。浏览器预览可横向滚动，截图区域必须完整包含图。
5. 使用 `scripts/render_pngs.py content/[slug]` 导出 `配图-N.png`。小黑仍为 `.xiaohei-row`，该脚本会跳过它。
6. 使用 `scripts/insert_image_placeholders.py` 的现有流程插入 `<!-- IMAGE:配图-N.png -->`。manifest 的 `wechat.images` 按正文顺序包含品牌 PNG 与小黑 PNG，不放单图 HTML 或 SVG。

汇总页沿用以下接口：

```html
<div class="slide-label">配图 N · 放在「锚点文字」之后</div>
<div class="slide bg-light" data-num="N">
  <!-- 内联该图已验证的 SVG，ID 与样式须独立 -->
</div>
```

不要以 `cover-template.md` 的旧信息卡模板替代 diagram-design 的布局，也不要改变既有占位符脚本的标签格式。

## 5. 验证与交付

- 单图先运行 diagram-design 随包提供的 `scripts/self_check.py`，并执行其 taste gate；几何检查脚本可用时按该技能运行，不假设完整仓库工具都在已安装包中。
- 在浏览器检查单图与汇总页：字体就绪、中文不溢出、连接线不重叠、标签不压线、图例完整，且各图的 marker 与样式互不干扰。
- 导出后检查 PNG：内容非空、尺寸符合计划、没有黑角/底边、文字在正文显示宽度下可读。不能仅凭 HTML 校验通过就判定图片完成。
- 核对 PNG、preview 占位符与 manifest 路径一一对应，并保持图的顺序一致。
- 小红书转换沿用原图独立轮播素材规则，不把结构图强塞进文字卡，不额外添加页眉、页脚或装饰框。视频若复用该图，沿用 Path C 资源流程，不让 diagram-design 自动生成视频。

Python 校验与渲染命令使用项目选定的 Python 环境；环境缺失时先配置。不得为补齐图型或通过检查而编造正文中不存在的关系与数据。