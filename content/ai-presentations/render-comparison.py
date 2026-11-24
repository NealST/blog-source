from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1686, 924
MARGIN_X, TOP, BOTTOM = 32, 22, 28
TABLE_W = WIDTH - MARGIN_X * 2
TABLE_H = HEIGHT - TOP - BOTTOM
COL_WIDTHS = [340, 641, 641]
HEADER_H = 80
ROW_H = (TABLE_H - HEADER_H) // 7

FONT_PATH = str(Path(__file__).parents[1] / "_shared" / "fonts" / "noto-sans-sc.ttf")
FONT_HEADER = ImageFont.truetype(FONT_PATH, 36)
FONT_LABEL = ImageFont.truetype(FONT_PATH, 28)
FONT_BODY = ImageFont.truetype(FONT_PATH, 28)
FONT_MUTED = ImageFont.truetype(FONT_PATH, 25)

INK = "#1C1C1E"
MUTED = "#656360"
PAPER = "#FFFFFF"
PAPER_2 = "#F2EDE3"
LABEL_BG = "#FAF8F4"
GOLD = "#C4956A"
PURPLE = "#7562A8"

ROWS = [
    ("使用方式", "在 PowerPoint 和 Google Slides 内运行", "独立 Web 应用，并提供移动端应用"),
    ("最适合", "团队在 PowerPoint 或 Slides 中共同编辑的工作演示", "快速制作视觉演示，通过演示或链接分享"),
    ("免费方案", "7 天试用，含 1,000 积分\n需绑定信用卡", "免费方案\n无需信用卡"),
    ("起始价格", "15 美元/月\n年付 10 美元/月", "X 美元/月\n年付 X 美元/月"),
    ("主要优势", "原生、完全可编辑，并兼容现有模板", "不到一分钟即可生成美观初稿"),
    ("主要不足", "默认设计较朴素；上传和图片生成需要 Pro 版", "导出 PowerPoint 后需要清理；布局控制有限"),
    ("品牌定制", "团队版及以上", "Pro 版及以上"),
]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines():
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and draw.textlength(candidate, font=font) > max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        lines.append(current)
    return lines


def draw_cell_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    color: str,
    centered: bool = False,
) -> None:
    x1, y1, x2, y2 = box
    lines = wrap_text(draw, text, font, x2 - x1 - 36)
    line_height = font.size + 9
    total_height = line_height * len(lines) - 9
    y = y1 + (y2 - y1 - total_height) / 2
    for line in lines:
        line_color = MUTED if line.startswith(("需绑定", "无需信用卡", "年付")) else color
        if centered:
            width = draw.textlength(line, font=font)
            x = x1 + (x2 - x1 - width) / 2
        else:
            x = x1 + 18
        draw.text((x, y), line, font=font if line_color == color else FONT_MUTED, fill=line_color)
        y += line_height


image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, int(WIDTH * 0.34), 8), fill=GOLD)
draw.rectangle((int(WIDTH * 0.34), 0, int(WIDTH * 0.66), 8), fill=INK)
draw.rectangle((int(WIDTH * 0.66), 0, WIDTH, 8), fill=PURPLE)

x_positions = [MARGIN_X]
for width in COL_WIDTHS:
    x_positions.append(x_positions[-1] + width)

draw.rectangle((MARGIN_X, TOP, MARGIN_X + TABLE_W, TOP + TABLE_H), outline=INK, width=2)
draw.rectangle((x_positions[1], TOP, x_positions[2], TOP + HEADER_H), fill=PAPER_2)
draw.rectangle((x_positions[2], TOP, x_positions[3], TOP + HEADER_H), fill=PAPER_2)
draw.rectangle((x_positions[1], TOP, x_positions[2], TOP + 6), fill=GOLD)
draw.rectangle((x_positions[2], TOP, x_positions[3], TOP + 6), fill=PURPLE)

for x in x_positions[1:-1]:
    draw.line((x, TOP, x, TOP + TABLE_H), fill=INK, width=2)

header_bottom = TOP + HEADER_H
draw.line((MARGIN_X, header_bottom, MARGIN_X + TABLE_W, header_bottom), fill=INK, width=2)
draw_cell_text(draw, (x_positions[1], TOP, x_positions[2], header_bottom), "Plus AI", FONT_HEADER, INK, True)
draw_cell_text(draw, (x_positions[2], TOP, x_positions[3], header_bottom), "Gamma", FONT_HEADER, INK, True)

for index, (label, plus, gamma) in enumerate(ROWS):
    y1 = header_bottom + index * ROW_H
    y2 = TOP + TABLE_H if index == len(ROWS) - 1 else y1 + ROW_H
    draw.rectangle((MARGIN_X, y1, x_positions[1], y2), fill=LABEL_BG)
    if index:
        draw.line((MARGIN_X, y1, MARGIN_X + TABLE_W, y1), fill=INK, width=2)
    draw_cell_text(draw, (MARGIN_X, y1, x_positions[1], y2), label, FONT_LABEL, INK)
    draw_cell_text(draw, (x_positions[1], y1, x_positions[2], y2), plus, FONT_BODY, INK)
    draw_cell_text(draw, (x_positions[2], y1, x_positions[3], y2), gamma, FONT_BODY, INK)

output = Path(__file__).parent / "localized-images" / "01-plusai-gamma-comparison-cn.png"
image.save(output)
