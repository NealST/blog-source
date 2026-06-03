import re

with open("/Users/nealkaffrey/projects/blog-source/dramas/the-fake-ai-leap/storyboard.md", "r") as f:
    content = f.read()

shot15_orig = """### Shot 15 (02:11 - 02:18) 终末：幽暗深渊中的诡异微笑
**🕘 总时长**: 7s 
**📍 布景**: 极其昏暗局促的桌底角落 (坐标方案 B 隐藏区域)
**👔 服装**: 林工
**🎬 动作与表情**: Accompanied by a crisp "Ding" of an HR termination notice from Kevin's phone above (voiceover), the real Lin under the desk is slumped into a lifeless heap like a ragdoll. But as the voice announcing Kevin's termination falls, the corners of that mouth, under eyes that had long rolled back vacant and hollow, uncontrollably curl upward frantically. He wears an incredibly eerie and peaceful smile filled with the sweet thrill of revenge.
**⏱️ 时序**: `00:00.0-00:05.0` 在凄然气氛中拉出极致诡异的反差微笑；`00:05.0-00:07.0` 缓慢沉没。
**🎙️ 台词**: 
  - (Pure silence, accompanied by a crisp off-screen "Ding——" of an email notification)
  - [中文字幕]: (无声，邮件提示音“叮——”)
**🎥 运镜**: 贴地低视角极其缓慢地推镜头，像是在凝视一个亡灵的深渊。
**🔄 转场**: 黑场淡出 (Fade to Black)。

---

*(留白：深空低频环境音效垫底，中央缓缓打出冷白色强对比字幕，停留 4s)*
**"AI finally replaced humans as desired"**
**(1.5s 后打出后半句话)**
**"— Starting with those who only write PPTs."**
*(中文字幕)*: 
**"AI 终于如愿替代了人类"**
**"——从只会写 PPT 的开始。"**

*(剧终)*"""

shot15_new = """### Shot 15 (02:11 - 02:18) 终末：绝杀留白
**🕘 总时长**: 7s 
**📍 布景**: 纯黑背景
**👔 服装**: 无
**🎬 动作与表情**: Pure black screen. A crisp "Ding" of an HR termination email from Kevin's phone breaks the silence, followed by the appearance of the stark white title cards.
**⏱️ 时序**: `00:00.0-00:01.5` 黑场与清脆的“叮——”声；`00:01.5-00:04.5` 第一句字幕缓缓浮现并定格；`00:04.5-00:07.0` 第二句字幕如利刃般打出，余音回荡并淡出。
**🎙️ 台词**: 
  - (Pure silence, accompanied by a crisp background "Ding——" of an email notification)
  - [画面内字]: **"AI finally replaced humans as desired"** ... **"— Starting with those who only write PPTs."**
  - [中文字幕] 纯黑场内缓缓打出冷白字幕：
    **"AI 终于如愿替代了人类"**
    **"——从只会写 PPT 的开始。"**
**🎥 运镜**: 无画面，深空低频环境音效垫底，配合冷白色高对比度字幕。
**🔄 转场**: 随着字体缓慢淡出 (Fade out)，全剧终。"""

content = content.replace(shot15_orig, shot15_new)

with open("/Users/nealkaffrey/projects/blog-source/dramas/the-fake-ai-leap/storyboard.md", "w") as f:
    f.write(content)
