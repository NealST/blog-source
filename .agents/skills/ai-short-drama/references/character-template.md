# 角色卡 + 生图提示词模板 (Character & Image-Prompt Template)

> 复制此模板到 `dramas/[slug]/characters.md`，每个角色一张卡。
> 本文件最终交付物 = **可直接复制到 GPT Image / Nano Banana 的提示词**。

---

## 全局画风底词 (Style Anchor) — 所有角色共用

> ⚠️ 内容应与 `art-direction.md` 中确定的画风方案完全一致。每条提示词都要带这段底词，保证全剧画风统一。

```
[填写最终敲定的画风底词，例如：
3D stylized animation caricature, reminiscent of Pixar and Spider-Verse,
exaggerated features, hyper-detailed textures, vibrant colors,
cinematic lighting, octane render, 8k resolution.]
```

---

## 推荐生图工具

| 工具 | 入口 | 优点 |
|------|------|------|
| **GPT Image** | ChatGPT 内置图像生成 | 提示词理解力强，支持自然语言迭代 |
| **Nano Banana** | Google Gemini 2.5 Flash Image | 一致性极强，适合多视角同角色生成 |

**操作流程**：
1. 复制下方每个角色的"基准图生成提示词"到工具中
2. 每个角色生成 4-6 张候选
3. 挑选最佳一张保存为 `assets/character-[代号].png`
4. 后续视频镜头一律用 **Image-to-Video** 模式垫这张图

---

## 角色 N：[角色代号]

### 规避版权要点
- ❌ 不写真实姓名 / 品牌 / 真实作品 LOGO
- ✅ 用"特征 + 配色 + 标志道具"塑造唯一辨识度
- ✅ 五官夸张化（动画化但可辨认）

### 特征锚点 (Identity Anchors)

| 维度 | 描述 |
|------|------|
| 体型 | [身高 / 体格 / 比例的夸张化描述] |
| 年龄段 | [儿童 / 青年 / 中年 / 老年] |
| 肤色 | [皮肤色调] |
| 标志特征 | [最具辨识度的一处，如"浓密络腮胡"、"修长四肢 + 小脑袋"、"独眼带眼罩"] |
| 标准服装 | [日常穿搭 + 明确配色] |
| 标志道具 | [贯穿全剧的标志物：手机 / 书 / 滑板 / 眼镜 / 笔记本 ……] |
| 微表情默认 | [常态情绪：自恋 / 蔫坏 / 阳光 / 高冷 / 疲惫] |
| 配色暗示 | [主色 + 辅色，用于强化身份] |

### 基准图生成提示词 (Base Portrait Prompt)

> 直接复制下方代码块到 **GPT Image** 或 **Nano Banana**。

```
[全局画风底词],
a [体型] [年龄] [性别] character with [标志特征],
[五官夸张化描述],
wearing [标准服装 with 配色],
holding / accompanied by [标志道具],
[默认表情], standing pose, full body portrait,
neutral background, studio lighting, character sheet style,
high detail, consistent character design, 8k.
```

### 多视角生成提示词（可选）

> 选定主基准图后，如需补充侧面 / 背面 / 表情包，复用同一描述，只改 `pose` / `angle` / `expression`。

```
[全局画风底词],
same character as before, [体型/特征/服装 全部复述],
[three-quarter view / side profile / back view / close-up of face],
[新表情或新动作],
neutral background, consistent character design.
```

### 垫图用法 (Image-to-Video Workflow)

1. 选定基准图存入 `assets/character-[代号].png`
2. 所有视频镜头使用 **Image-to-Video** 模式垫入此图
3. 视频 prompt 中**仍需复述**：服装、道具、表情，不依赖图片自动继承

### 梗资产清单 (Meme Inventory)

- **视觉梗**：[每次出场都能让观众会心一笑的固定动作 / 道具]
- **语言梗**：[标志性口头禅 / 引用]
- **人设梗**：[性格反差点 / 反预期行为]

---

## 角色关系图

```
角色A ←(矛盾点)→ 角色B
   ↘             ↙
     角色C (调和 / 火上浇油)
```

[用一段话描述本剧核心人物关系与冲突源头]
