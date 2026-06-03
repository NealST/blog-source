import re

with open("/Users/nealkaffrey/projects/blog-source/dramas/the-fake-ai-leap/storyboard.md", "r") as f:
    content = f.read()

# Fix shot 8 (16s)
shot8_orig = """### Shot 08 (00:50 - 01:06) 冲突升级：无用的救主兜底
**🕘 总时长**: 16s (情绪逐渐失控的密集长台词)
**📍 布景**: 冰冷且充满压迫感的晋升答辩室 (坐标方案 C)
**👔 服装**: 林工 + Kevin (作为评委坐着)
**🎬 动作与表情**: Lin stands in front of the projection giving a report. Kevin interrupts him with a disgusted and highly impatient face. Lin is pushed to the limit, directly slamming both hands heavily on the conference table, his bloodshot eyes bulging, roaring out the truth.
**⏱️ 时序**: `00:00.0-00:06.0` 林工尝试陈述功劳；`00:06.0-00:11.0` Kevin 傲慢打断；`00:11.0-00:15.5` 林工拍桌爆怒；`00:15.5-00:16.0` 桌子震动余韵。
**🎙️ 台词**: 
  - 林工: "This year, I refactored the legacy shit-mountain codebase, and manually intercepted over 30,000 fatal hallucinations from AI 001, avoiding..." (Pace: Normal slightly tense)
  - Kevin: "Lin, your presentation lacks 'Large Model Thinking'. Fixing legacy code offers no AI leverage. Manual interception is pure primitive farming." (Pace: Fastish / Sharp interruption, disgust)
  - 林工: "But without my manual interception, last month's payment demo would have bankrupted the company!" (Pace: Very fast / Slamming table roaring, the most real venting line)
  - [中文字幕]
    林工: 这一年，我重构了历史遗留的屎山代码，并且人工拦截了 AI 员工 001 号产生的三万多次致命幻觉报错，避免了……
    Kevin: 林工，你的汇报缺乏‘大模型思维’。修历史代码，没有 AI 杠杆率；人工拦截，那就是典型的刀耕火种。
    林工: 可是如果没我兜底拦截，上个月接支付的 Demo 早让公司破产了！
**🎥 运镜**: 中景交代林工在投影前，迅速推近到 Kevin 鄙夷的半身，紧接着用摇镜带出林工拍桌怒吼的爆发场面。
**🔄 转场**: 视线匹配 (Eyeline Match)直切 Kevin 的最终宣判。"""

shot8_new = """### Shot 08a (00:50 - 01:00) 冲突升级：无用的救主兜底（汇报与打断）
**🕘 总时长**: 10s
**📍 布景**: 冰冷且充满压迫感的晋升答辩室 (坐标方案 C)
**👔 服装**: 林工 + Kevin (作为评委坐着)
**🎬 动作与表情**: Lin stands in front of the projection giving a report. Kevin interrupts him with a disgusted and highly impatient face, waving his hand dismissively.
**⏱️ 时序**: `00:00.0-00:05.5` 林工尝试陈述功劳；`00:05.5-00:10.0` Kevin 傲慢打断。
**🎙️ 台词**: 
  - 林工: "This year, I refactored the legacy shit-mountain codebase, and manually intercepted over 30,000 fatal hallucinations from AI 001, avoiding..."
  - Kevin: "Lin, your presentation lacks 'Large Model Thinking'. Fixing legacy code offers no AI leverage. Manual interception is pure primitive farming."
  - [中文字幕]
    林工: 这一年，我重构了历史遗留的屎山代码，并且人工拦截了 AI 员工 001 号产生的三万多次致命幻觉报错，避免了……
    Kevin: 林工，你的汇报缺乏‘大模型思维’。修历史代码，没有 AI 杠杆率；人工拦截，那就是典型的刀耕火种。
**🎥 运镜**: 中景交代林工在投影前，迅速推近到 Kevin 鄙夷的半身特写。
**🔄 转场**: 声音引导切镜头 (J-Cut) 切向林工的爆发。

### Shot 08b (01:00 - 01:06) 冲突升级：桌面的震怒
**🕘 总时长**: 6s
**📍 布景**: 晋升答辩室会议桌前
**👔 服装**: 林工
**🎬 动作与表情**: Lin is pushed to the limit, directly slamming both hands heavily on the conference table, his bloodshot eyes bulging, roaring out the truth.
**⏱️ 时序**: `00:00.0-00:04.5` 林工拍桌爆怒；`00:04.5-00:06.0` 桌子震动伴随粗重喘息。
**🎙️ 台词**: 
  - 林工: "But without my manual interception, last month's payment demo would have bankrupted the company!"
  - [中文字幕]
    林工: 可是如果没我兜底拦截，上个月接支付的 Demo 早让公司破产了！
**🎥 运镜**: 从桌面猛烈震动起幅，摇镜快速抬升怼脸特写 (Whip pan up to tight close-up)。
**🔄 转场**: 视线匹配 (Eyeline Match) 直切 Kevin 的最终宣判。"""

content = content.replace(shot8_orig, shot8_new)

# Fix shot 9 (19s)
shot9_orig = """### Shot 09 (01:06 - 01:25) 冲突升级：宣读 35 岁的极刑
**🕘 总时长**: 19s (高密度冰冷文本宣告)
**📍 布景**: 压迫感的答辩室，高管席 (坐标方案 C)
**👔 服装**: Kevin
**🎬 动作与表情**: Kevin remains entirely unswayed by Lin's fury. Instead, he sneers and slowly raises the tablet in his hand. He looks at Lin with the cold eyes of someone looking at weeds, dragging out his tone, reading word by word the AI's ultimate verdict on the 35-year-old employee.
**⏱️ 时序**: `00:00.0-00:03.0` 前奏与冷笑举平板；`00:03.0-00:18.0` 以摧毁人心的语速念出长长的一大段死刑；`00:18.0-00:19.0` 宣判后的极致静默与压迫死寂。
**🎙️ 台词**: 
  - Kevin: "The company values the Large Model vision! Besides..." (Pace: Slow)
  - Kevin: "I just casually had the AI audit your efficiency data. The model is highly accurate: you are 35 years old, still writing low-level code without reaching P8. Extremely low compute-conversion-rate. You're a textbook 'overage, low-potential employee.' The AI's recommendation is direct social distribution. You should be glad I haven't fired you. Your promotion is denied." (Pace: Normal-slow / Reading word by word, extreme coldness and harshness, lacking any human touch)
  - [中文字幕]
    Kevin: 公司看重的是大模型愿景！另外……
    Kevin: 我刚刚随手让 AI 盘点了下你的人效数据。模型计算得很精确：你今年 35 岁，还在写底层代码没升到 P8，算力转化率极低，属于标准的‘大龄低潜员工’。AI 的建议是直接把你向社会输送，我没开掉你就不错了。你的晋升，免谈。
**🎥 运镜**: 中近景（Medium Close-up）对准 Kevin，镜头从下往上极其微弱地移动 (Slow low-angle tilt up)，让那个平板上的光照在老板脸上，宛如宣判的死神。
**🔄 转场**: 画面直接拉入长达 1 秒的纯黑 (Fade to Black 1s) —— 沉入深夜里绝望的无底深渊。"""

shot9_new = """### Shot 09a (01:06 - 01:15) 冲突升级：冰冷的数据审判
**🕘 总时长**: 9s 
**📍 布景**: 压迫感的答辩室，高管席 (坐标方案 C)
**👔 服装**: Kevin
**🎬 动作与表情**: Kevin remains entirely unswayed by Lin's fury. Instead, he sneers and slowly raises the tablet in his hand. He drags out his tone to read the AI's analysis.
**⏱️ 时序**: `00:00.0-00:03.0` 前奏与冷笑举平板；`00:03.0-00:09.0` 极度傲慢地低头读平板。
**🎙️ 台词**: 
  - Kevin: "The company values the Large Model vision! Besides... I just casually had the AI audit your efficiency data."
  - [中文字幕]
    Kevin: 公司看重的是大模型愿景！另外……我刚刚随手让 AI 盘点了下你的人效数据。
**🎥 运镜**: 中近景（Medium Close-up）对准 Kevin，慢落幅 (Slow tilt down) 聚焦到发光的平板。
**🔄 转场**: 动作匹配切入 (Match on Action) 切向平板反射。

### Shot 09b (01:15 - 01:25) 冲突升级：宣读 35 岁的极刑
**🕘 总时长**: 10s 
**📍 布景**: 压迫感的答辩室，由于光线反射显得更冰冷
**👔 服装**: Kevin
**🎬 动作与表情**: Kevin looks up at Lin with the cold eyes of someone looking at weeds, reading word by word the ultimate verdict on the 35-year-old employee. Every word is a nail in the coffin.
**⏱️ 时序**: `00:00.0-00:09.0` 以摧毁人心的语速念出长长的一大段死刑；`00:09.0-00:10.0` 宣判后的极致静默与压迫死寂。
**🎙️ 台词**: 
  - Kevin: "The model is highly accurate: you are 35 years old, still writing low-level code without reaching P8. Extremely low compute-conversion-rate. You're a textbook 'overage, low-potential employee.' The AI says: direct social distribution. Your promotion is denied."
  - [中文字幕]
    Kevin: 模型计算得很精确：你今年 35 岁，还在写底层代码没升到 P8，算力转化率极低，属于标准的‘大龄低潜员工’。AI 的建议是直接向社会输送。你的晋升，免谈。
**🎥 运镜**: 极具压迫感的大特写 (Extreme Close-up)，镜头从下往上极其微弱地移动 (Slow low-angle tilt up)，平板上的冷光照在老板脸上，宛如宣判的死神。
**🔄 转场**: 画面直接拉入长达 1 秒的纯黑 (Fade to Black 1s) —— 沉入深夜里绝望的无底深渊。"""

content = content.replace(shot9_orig, shot9_new)

with open("/Users/nealkaffrey/projects/blog-source/dramas/the-fake-ai-leap/storyboard.md", "w") as f:
    f.write(content)
