# Design

## Mood
Dark editorial — technical depth, contemplative authority. The feeling of reading a well-crafted engineering teardown that respects the reader's intelligence.

## Colors
- Background: `#1C1C1E` (墨色)
- Foreground: `#F2EDE3` (宣纸白)
- Accent (Gold): `#D4A76A` (筝弦金 — video-level, elevated from brand #C4956A)
- Panel: `#2C2A28` (浓墨, card backgrounds)
- Muted: `#7A7876` (淡墨, secondary text)
- Code Green: `#A8C97F` (苔绿)
- Code Blue: `#8FBCBB` (青瓷)
- Panel border: `rgba(212,167,106,0.18)` (subtle gold rim)

## Typography
- Display / Numbers: DM Sans, 800 weight
- Body Chinese: -apple-system, PingFang SC, Microsoft YaHei, sans-serif
- Code / Mono: JetBrains Mono, 500 weight

## Layout
- Format: Vertical 1080×1920
- Top platform safety zone: 180px
- Watermark position: top 228px, left 60px ("公众号：墨筝")
- Scene content padding: 340px top, 64px sides, 80px bottom

## Constraints
- All text in Chinese except technical identifiers (e.g. @vscode/prompt-tsx, temperature, BudgetExceededError)
- Gold (#D4A76A) sparingly — max 1-2 gold elements per scene
- No pure white; use #F2EDE3 for all foreground text
- No full-screen linear gradients (H.264 banding risk) — localized radial glows only
- Video duration: ~60 seconds, 8 scenes
