# Design

## Mood
Deep tech benchmark — two open-weight contenders squaring off. Dashboard-serious with 墨筝 warmth on the hero moments. Reads like a live scoreboard, not a slide deck.

## Colors
- Background: `#0B1222` (deep navy-black, tech shift from 墨色 #1C1C1E)
- Foreground: `#F0EBE3` (warm white, from 宣纸底 #F2EDE3)
- Accent 1 (winner / GLM): `#E0A458` (video-grade 筝弦金, warmth on winner side)
- Accent 2 (challenger / Kimi): `#5B9CF6` (cool blue for contrast)
- Accent 3 (data / value): `#2EC4B6` (teal — positive metrics, matches highlights)
- Muted: `#162033` (panel backgrounds, cards)
- Border: `#2A3A52` (structural lines, dividers)
- Warning red: `#FF6B7A` (only for "gap"/"miss" annotations)

## Typography
- Headlines: Montserrat, 800 weight
- Body: Montserrat, 400 weight
- Data/Code: JetBrains Mono, 500/700 weight

## Constraints
- All text in Chinese except model names (GLM, Kimi), code identifiers (SHA-256, bcrypt), and numeric data
- Monospace for all numbers, scores, and code identifiers
- Gold for GLM signals, blue for Kimi signals — never swap
- No pie charts, no gradient text
- Portrait 1080×1920 with 340px 340×64 top safe area for 小红书 / 视频号
