# Sweety Handdraw Video 集成

> 将 `sweety-handdraw-video` 作为 content-pipeline Path C 的独立视频后端。它与 HyperFrames 并列，不嵌入 HyperFrames，也不只抽取描线脚本。

## 实现原理

完整链路分为两层：

1. **Agent 创作层**：读取文章，确定受众、口播路线、开场、画风、分镜、绘制计划、部位顺序和插画提示词；生成并实际检查插画，记录简报、提示词、图片哈希和视觉证据。
2. **确定性渲染层**：Python 使用 Pillow、NumPy、SciPy 和 FFmpeg，将已确认的 `job.json` 编译为时间线。旁白时间戳是主时钟；引擎从插画提取线稿、按语义部位逐笔描线和填色，汉字按笔顺书写，手部跟随笔尖，最后烧录唯一字幕层并编码 MP4。

关键点：它不是“传入 Markdown 自动返回视频”的黑盒 CLI。CLI 只执行已确定的素材、时间线和质量门禁，不能替 Agent 写分镜、生成图片或完成主观审片。

## 后端路由

| 需求 | 后端 | 原因 |
|------|------|------|
| 数据对比、产品演示、UI、代码、快速动效摘要 | `hyperframes`（默认） | HTML 动效与界面组合效率高 |
| 故事、观点、机制讲解、寓言、希望“边画边讲” | `handdraw` | 旁白驱动，插画逐笔形成 |
| 用户明确说“手绘视频 / 白板动画 / 边画边讲” | `handdraw` | 明确意图优先 |
| 用户只说“做视频”且两者都适合 | 先说明默认使用 `hyperframes`，必要时用原生选项询问 | 不同时生成两套昂贵产物 |

不得把 handdraw 的逐笔引擎嵌进 HyperFrames 时间线。两套后端的主时钟、素材门禁和验证模型不同，组合会丢失上游的旁白哈希、绘制预算与 finalize 约束。

## 安装与版本

上游以 MIT 许可发布。使用固定版本的完整 skill 安装包，保留其 `LICENSE`、`THIRD_PARTY_NOTICES.md` 和内置依赖许可。不要把仓库工作副本或单个脚本复制到 content-pipeline。

建议安装：

```bash
npx skills add threerocks/sweety-handdraw-video --skill sweety-handdraw-video --agent claude-code --global --copy --yes
```

当前验证版本为 `1.4.1`。运行前读取安装目录的 `VERSION`；升级时先在一个短任务上回归，不自动跟随仓库主分支。

首次由用户明确同意后执行环境安装：

```bash
bash <HANDDRAW_SKILL_DIR>/scripts/setup.sh
```

content-pipeline 只能自动运行只读检查：

```bash
bash <HANDDRAW_SKILL_DIR>/scripts/setup.sh --check
```

不得静默下载 VoxCPM2（约 3.2GB）、购买服务或切换云端 TTS。只有用户明确选择时才运行 `setup.sh --voxcpm`。

## 任务目录契约

每篇文章使用独立任务目录：

```text
content/[slug]/video/handdraw/
├── job.json
├── design.json
├── storyboard.json
├── review.json
├── design/
│   ├── art-direction.json
│   ├── drawing-plan.json
│   ├── drawing-review.json
│   ├── briefs/
│   └── prompts/
├── inputs/
│   ├── cover.png
│   ├── illustrations/
│   └── narration/
│       ├── master.wav
│       └── alignment.json
├── work/                    # build/render 中间产物
└── outputs/
    ├── film.mp4
    ├── cover.png
    ├── captions.srt
    ├── script.txt
    ├── verification.json
    └── verification.txt
```

任务数据留在文章产物目录；skill 安装目录只读。不要与 `content/[slug]/video/hyperframes/` 共用 `work`、音频或输出文件名。

## Content Pipeline 执行流程

### 1. 环境门禁

1. 定位已安装的完整 `sweety-handdraw-video` skill，读取 `VERSION`。
2. 运行 `setup.sh --check`。
3. 确认可用的生图能力。宿主没有生图工具且用户未提供插画时停止，禁止降级为纯文字视频。
4. 确认一条真实配音路径：本地 VoxCPM2、兼容 VoiceStudio、用户配置密钥的云端 TTS，或用户提供的完整旁白与时间戳。

`doctor` 需要已有最小 `job.json`，不能拿它替代 setup 检查。`doctor.ready` 表示当前任务素材可合成；`capabilities.generate_narration` 才表示能生成新旁白。

### 2. 文章改编

- 从 `source/_posts/[slug].md` 读取全文。
- 保留文章中的事实、数字、来源、适用条件和作者观点。
- Path C 仍是导流型讲解，不要求逐字搬运全文；但用户要求“按原文”时不得擅自改写。
- 写完整口播后按不超过约 100 字的语义段生成旁白；由真实音频生成 `alignment.json`，禁止手写时间戳。
- `design.json` 写明开场、叙事路线和 `presentation.mode`；品牌要求写入画风简报，不覆盖上游的绘制约束。

墨筝默认映射：宣纸背景 `#F2EDE3`、墨线 `#1C1C1E`、筝弦金 `#C4956A` 仅作少量强调；`hand.pen_text` 默认空，`watermark.text` 可设为 `公众号：墨筝`，不加背景音乐，除非用户明确要求。

### 3. 分镜与素材

1. 根据真实旁白时长生成 `storyboard.json`，运行：

   ```bash
   python <HANDDRAW_SKILL_DIR>/scripts/storyboard_lint.py JOB --budget
   ```

2. 写 `design/drawing-plan.json`。每张插画生成前遵循上游美术指导，先保存 brief 和完整 prompt，再绑定证据。
3. 先完成一个代表场景，实际看图并检查主体、构图、可辨认性和部位可分性；通过后再扩展其余素材。
4. 清理图片元数据，填写 `art-direction.json` 与 drawing review，运行缩略图、线稿和部位检查。
5. 编写 `job.json`，所有插画 action 关联 storyboard visual 与 drawing plan id。

不得直接复用文章正文配图冒充“可逐笔绘制素材”。只有线条、部位、构图和证据门禁都通过时才能复用；否则按视频预算重做插画。

### 4. 构建与代表段

使用 skill 自带 venv 的 Python，按顺序执行：

```bash
python <HANDDRAW_SKILL_DIR>/scripts/handdraw_video.py doctor JOB
python <HANDDRAW_SKILL_DIR>/scripts/handdraw_video.py build JOB
python <HANDDRAW_SKILL_DIR>/scripts/handdraw_video.py verify JOB --assets-only
python <HANDDRAW_SKILL_DIR>/scripts/handdraw_video.py render JOB --preview --duration 15
```

实际查看代表段，至少覆盖封面衔接、字幕、完整插画描线和填色。失败时只修对应层，再重新 build 和预览；不能通过放宽门禁或加速笔画掩盖问题。

### 5. 整片与验收

```bash
python <HANDDRAW_SKILL_DIR>/scripts/handdraw_video.py render JOB
python <HANDDRAW_SKILL_DIR>/scripts/handdraw_video.py verify JOB
```

查看全部页面、关键绘制阶段和最终抽帧；可以播放时从头到尾播放并实际听音。将观察证据写入 `review.json` 后运行：

```bash
python <HANDDRAW_SKILL_DIR>/scripts/handdraw_video.py finalize JOB
```

工程 `verify` 不等于观感通过。没有实际听音时必须把 `listening` 写为 `not_done` 并在交付中说明。发布时声明“AI 生成”；MP4 内置 AIGC 元数据不能替代平台显式声明。

## Manifest

保持旧的 `outputs.video.path` 兼容，同时增加可辨识后端与验证产物：

```json
{
  "outputs": {
    "video": {
      "backend": "handdraw",
      "path": "content/[slug]/video/handdraw/outputs/film.mp4",
      "cover": "content/[slug]/video/handdraw/outputs/cover.png",
      "captions": "content/[slug]/video/handdraw/outputs/captions.srt",
      "script": "content/[slug]/video/handdraw/outputs/script.txt",
      "verification": "content/[slug]/video/handdraw/outputs/verification.json",
      "job": "content/[slug]/video/handdraw/job.json",
      "format": "1080x1920",
      "aigc": true
    }
  }
}
```

HyperFrames 新任务同样增加 `"backend": "hyperframes"`，旧 manifest 无该字段时按路径中的 `index.html` / `output.mp4` 视为 HyperFrames 兼容格式。

## 失败与降级

| 失败 | 处理 |
|------|------|
| render venv 缺失 | 报告 `setup.sh` 命令，征得用户同意后安装 |
| 无生图能力 | 停止，等待用户提供插画或接入生图工具 |
| 无配音后端 | 接受用户提供的完整旁白与 alignment；否则停止 |
| 画面超过绘制预算 | 简化插画或调整分镜，不压缩旁白、不超速绘制 |
| 工程 verify 通过但未审片/听音 | 不声称完成；记录 open checks |
| 用户拒绝成片 | 执行 `reject` 并返工，不复用旧 finalize 结果 |

不自动回退到 HyperFrames。后端变化会改变用户要求的视觉语言，必须明确告知并获得同意。
