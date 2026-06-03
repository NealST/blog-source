import re

skill_path = "/Users/nealkaffrey/projects/blog-source/.agents/skills/ai-short-drama/SKILL.md"

with open(skill_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """> ⚠️ **单镜头物理限制与拆镜红线**
> 目前主流 AI 视频生成工具（Kling, Runway Gen-3, Sora 等）稳定出片上限通常为 4~8 秒，超过此限度人物的一致性与画面的稳定性断崖式下跌。
> **强制规则**：
> - 单个 Shot 时长**绝不可超过 10 秒**（推荐 4~8 秒）。
> - 当遇到人物长篇台词或复杂动作时，必须通过以下手法进行“拆镜（Split Shots）”：
>   - **正反打 (Shot Reverse Shot)**：镜头切向对话另一方的反应。
>   - **特写切入 (Cut-in)**：如“震惊时近景推成脸部大特写”、“拍桌子时手部震动特写”。
>   - **动作匹配 (Match on Action)**：换角度接续同一连续动作。
>   - **J-Cut / L-Cut（声音引导）**：声音先于画面切入下一镜。
> - 在计算每个镜头的总时长 (`🕘 总时长`) 时，必须根据台词语速或动作物理耗时逆推，超出 10s 直接打碎成 a/b 两个 shot。"""

new_text = """> ⚠️ **单镜头物理限制与拆镜红线**
> 目前主流 AI 视频生成工具（Kling, Runway Gen-3, Sora 等）的最大物理生成时长上限为 15 秒，但超过 8~10 秒后人物一致性与画面的稳定性会有较大崩溃风险。
> **强制规则**：
> - 单个 Shot 时长**物理绝对不可超过 15 秒**（强烈推荐保持在 4~8 秒的最佳稳定区间）。
> - 当遇到人物长篇台词或复杂动作时，必须通过以下手法进行“拆镜（Split Shots）”：
>   - **正反打 (Shot Reverse Shot)**：镜头切向对话另一方的反应。
>   - **特写切入 (Cut-in)**：如“震惊时近景推成脸部大特写”、“拍桌子时手部震动特写”。
>   - **动作匹配 (Match on Action)**：换角度接续同一连续动作。
>   - **J-Cut / L-Cut（声音引导）**：声音先于画面切入下一镜。
> - 在计算每个镜头的总时长 (`🕘 总时长`) 时，必须根据台词语速或动作物理耗时逆推，超出 15s **必须**强制打碎成 a/b 两个 shot（超过 10s 也**强烈建议**打碎）。"""

content = content.replace(old_text, new_text)

with open(skill_path, "w", encoding="utf-8") as f:
    f.write(content)
