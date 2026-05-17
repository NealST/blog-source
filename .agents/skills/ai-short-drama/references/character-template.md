# 角色卡模板 (Character Card Template)

> 复制此模板到 `dramas/[slug]/characters.md`，每个角色一张卡。

---

## 全局风格底词 (Style Anchor) — 所有角色共用

```
3D stylized animation caricature, reminiscent of Pixar and Spider-Verse,
exaggerated features, hyper-detailed textures, vibrant colors,
cinematic lighting, octane render, 8k resolution.
```

> ⚠️ 每条提示词都要带这段底词，保证整部剧画风统一。

---

## 角色 N：[角色代号]（影射 [现实原型，仅文档可见]）

### 规避版权要点
- ❌ 不写真实姓名 / 球队名 / 真实赛事 LOGO
- ✅ 用"特征 + 配色 + 标志道具"暗示身份
- ✅ 五官夸张化（不像真人，但球迷一眼认出）

### 特征锚点 (Identity Anchors)

| 维度 | 描述 |
|------|------|
| 体型 | [身高 / 肌肉 / 比例的夸张化描述] |
| 肤色 | [皮肤色调] |
| 标志特征 | [最具辨识度的一处，如"浓密络腮胡"、"修长四肢 + 小脑袋"] |
| 标准服装 | [日常穿搭 + 配色暗示队伍] |
| 标志道具 | [手机 / 书 / 牙套 / 头带 等] |
| 微表情默认 | [常态情绪：自恋 / 蔫坏 / 阳光 / 高冷] |

### 基准图生成提示词 (Base Portrait Prompt)

```
[Style Anchor 底词],
a [体型] [肤色] male character with [标志特征],
wearing [标准服装 with 配色],
holding [标志道具],
[默认表情], standing pose, neutral background, full body portrait.
```

### 垫图用法 (Image-to-Video Workflow)

1. 用上述 prompt 生成 4-6 张候选基准图
2. 选定一张作为「角色锚定图」存入 `assets/character-[代号].png`
3. 所有视频镜头使用 **Image-to-Video** 模式，垫入此基准图
4. 视频 prompt 中**仍需复述**：服装、道具、表情，不依赖图片自动继承

### 梗资产清单 (Meme Inventory)

- **视觉梗**：[每次出场都能让观众会心一笑的固定动作 / 道具]
- **语言梗**：[标志性口头禅 / 引用]
- **人设梗**：[性格反差点]

---

## 角色关系图

```
角色A ←(矛盾点)→ 角色B
   ↘             ↙
     角色C (调和 / 火上浇油)
```

[用一段话描述本剧核心人物关系与冲突源头]
