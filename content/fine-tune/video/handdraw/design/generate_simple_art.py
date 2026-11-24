from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "inputs" / "illustrations"
SCALE = 3
WIDTH, HEIGHT = 1024, 1536
PAPER = "#F2EDE3"
INK = "#162844"
GOLD = "#E8B84A"
BLUE = "#6F8EAE"
RED = "#D9583B"
LINE = 7 * SCALE


def point(x, y):
    return round(x * SCALE), round(y * SCALE)


def box(left, top, right, bottom):
    return (*point(left, top), *point(right, bottom))


def canvas():
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), PAPER)
    return image, ImageDraw.Draw(image)


def save(image, name):
    image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).save(OUTPUT / name)


def house(draw, left, top, right, bottom, fill=GOLD):
    middle = (left + right) / 2
    roof = top + (bottom - top) * 0.28
    draw.polygon(
        [
            point(left, roof),
            point(middle, top),
            point(right, roof),
            point(right - 25, roof),
            point(right - 25, bottom),
            point(left + 25, bottom),
            point(left + 25, roof),
        ],
        fill=fill,
        outline=INK,
        width=LINE,
    )


def arrow(draw, points, fill=INK):
    draw.polygon(
        [point(x, y) for x, y in points],
        fill=fill,
        outline=INK,
        width=LINE,
    )


def opening():
    image, draw = canvas()
    house(draw, 170, 205, 854, 890)
    draw.polygon(
        [point(420, 820), point(604, 820), point(632, 1020), point(392, 1020)],
        fill=PAPER,
    )
    draw.line(
        [point(470, 875), point(540, 920), point(490, 965)],
        fill=RED,
        width=24 * SCALE,
        joint="curve",
    )
    draw.polygon(
        [
            point(140, 1045),
            point(345, 1015),
            point(365, 1095),
            point(290, 1110),
            point(330, 1315),
            point(260, 1350),
            point(220, 1125),
            point(155, 1140),
        ],
        fill=INK,
    )
    draw.rounded_rectangle(
        box(665, 1080, 850, 1305),
        radius=12 * SCALE,
        fill=GOLD,
        outline=INK,
        width=LINE,
    )
    save(image, "01-library-problem.png")


def three_tools():
    image, draw = canvas()
    house(draw, 320, 260, 740, 920)
    draw.rounded_rectangle(
        box(90, 500, 245, 690), radius=12 * SCALE, fill=GOLD, outline=INK, width=LINE
    )
    draw.rounded_rectangle(
        box(160, 800, 390, 975), radius=10 * SCALE, fill=BLUE, outline=INK, width=LINE
    )
    draw.ellipse(box(185, 945, 245, 1005), fill=INK)
    draw.ellipse(box(310, 945, 370, 1005), fill=INK)
    draw.line([point(750, 520), point(900, 830)], fill=INK, width=28 * SCALE)
    draw.ellipse(box(710, 455, 795, 540), outline=INK, width=18 * SCALE)
    save(image, "02-three-tools.png")


def full_finetune():
    image, draw = canvas()
    house(draw, 60, 245, 545, 980, fill=BLUE)
    for left in (570, 710, 850):
        house(draw, left, 560, left + 125, 920, fill=GOLD)
    draw.polygon(
        [point(210, 1050), point(390, 1085), point(360, 1195), point(180, 1160)],
        fill=RED,
        outline=INK,
        width=LINE,
    )
    save(image, "03-full-finetune.png")


def peft():
    image, draw = canvas()
    draw.rounded_rectangle(
        box(115, 245, 910, 1030), radius=22 * SCALE, fill=BLUE, outline=INK, width=LINE
    )
    for x in (275, 512, 750):
        draw.arc(box(x - 62, 420, x + 62, 600), 180, 360, fill=INK, width=14 * SCALE)
        draw.rounded_rectangle(
            box(x - 72, 530, x + 72, 720),
            radius=12 * SCALE,
            fill=INK,
        )
        draw.ellipse(box(x - 22, 760, x + 22, 804), fill=GOLD, outline=INK, width=LINE)
    save(image, "04-peft-locks.png")


def lora():
    image, draw = canvas()
    house(draw, 140, 210, 700, 900, fill=BLUE)
    draw.rounded_rectangle(
        box(680, 430, 770, 820), radius=12 * SCALE, fill=GOLD, outline=INK, width=LINE
    )
    draw.rounded_rectangle(
        box(785, 540, 945, 820), radius=12 * SCALE, fill=GOLD, outline=INK, width=LINE
    )
    for left in (135, 390, 645):
        draw.rounded_rectangle(
            box(left, 1050, left + 190, 1225),
            radius=14 * SCALE,
            fill=GOLD,
            outline=INK,
            width=LINE,
        )
    save(image, "05-lora-cards.png")


def qlora():
    image, draw = canvas()
    draw.rounded_rectangle(
        box(65, 280, 515, 1030), radius=18 * SCALE, fill=BLUE, outline=INK, width=LINE
    )
    for y in (465, 650, 835):
        draw.line([point(80, y), point(500, y)], fill=INK, width=10 * SCALE)
    arrow(
        draw,
        [(540, 600), (665, 600), (665, 545), (760, 665), (665, 785), (665, 730), (540, 730)],
    )
    draw.rounded_rectangle(
        box(760, 390, 960, 930), radius=18 * SCALE, fill=GOLD, outline=INK, width=LINE
    )
    draw.line([point(775, 660), point(945, 660)], fill=INK, width=10 * SCALE)
    draw.rounded_rectangle(
        box(795, 690, 990, 855), radius=10 * SCALE, fill=BLUE, outline=INK, width=LINE
    )
    draw.arc(box(845, 850, 985, 1020), 300, 80, fill=INK, width=14 * SCALE)
    save(image, "06-qlora-compress.png")


def direction():
    image, draw = canvas()
    draw.ellipse(box(135, 230, 890, 985), outline=INK, width=LINE)
    for start, end in (
        ((512, 250), (512, 315)),
        ((512, 900), (512, 965)),
        ((155, 610), (220, 610)),
        ((805, 610), (870, 610)),
    ):
        draw.line([point(*start), point(*end)], fill=INK, width=16 * SCALE)
    arrow(draw, [(495, 650), (495, 410), (455, 450), (512, 345), (570, 450), (530, 410), (530, 650)])
    arrow(draw, [(520, 650), (690, 650), (690, 610), (775, 665), (690, 720), (690, 680), (520, 680)], GOLD)
    arrow(draw, [(515, 650), (725, 420), (680, 405), (805, 315), (765, 455), (748, 410), (545, 675)], RED)
    save(image, "07-direction-coupling.png")


def dora():
    image, draw = canvas()
    draw.rounded_rectangle(
        box(90, 330, 935, 1010), radius=35 * SCALE, outline=INK, width=LINE
    )
    for x in (310, 715):
        draw.ellipse(box(x - 105, 650, x + 105, 860), fill=GOLD, outline=INK, width=LINE)
        draw.line([point(x, 755), point(x + 45, 705)], fill=INK, width=16 * SCALE)
    arrow(draw, [(420, 500), (690, 500), (690, 445), (805, 560), (690, 675), (690, 620), (420, 620)], GOLD)
    draw.line([point(310, 650), point(455, 545)], fill=BLUE, width=12 * SCALE)
    draw.line([point(715, 650), point(715, 560)], fill=BLUE, width=12 * SCALE)
    save(image, "08-dora-controls.png")


def qdora():
    image, draw = canvas()
    draw.rounded_rectangle(
        box(100, 360, 555, 1030), radius=24 * SCALE, fill=BLUE, outline=INK, width=LINE
    )
    draw.ellipse(box(175, 520, 305, 650), fill=GOLD, outline=INK, width=LINE)
    draw.ellipse(box(350, 520, 480, 650), fill=GOLD, outline=INK, width=LINE)
    draw.rounded_rectangle(
        box(600, 500, 765, 930), radius=14 * SCALE, fill=GOLD, outline=INK, width=LINE
    )
    draw.polygon(
        [point(785, 480), point(955, 520), point(930, 920), point(760, 880)],
        fill=PAPER,
        outline=INK,
        width=LINE,
    )
    draw.line([point(810, 680), point(900, 760)], fill=RED, width=18 * SCALE)
    save(image, "09-qdora-combine.png")


def choice():
    image, draw = canvas()
    house(draw, 250, 120, 775, 650, fill=BLUE)
    draw.line([point(512, 520), point(512, 1010)], fill=INK, width=20 * SCALE)
    arrow(draw, [(500, 600), (350, 520), (350, 485), (255, 545), (350, 605), (350, 570), (500, 650)], GOLD)
    arrow(draw, [(525, 600), (675, 520), (675, 485), (770, 545), (675, 605), (675, 570), (525, 650)], BLUE)
    arrow(draw, [(500, 690), (360, 690), (360, 655), (270, 715), (360, 775), (360, 740), (500, 740)], RED)
    arrow(draw, [(525, 690), (665, 690), (665, 655), (755, 715), (665, 775), (665, 740), (525, 740)], GOLD)
    draw.rounded_rectangle(
        box(90, 1110, 285, 1300), radius=12 * SCALE, fill=GOLD, outline=INK, width=LINE
    )
    draw.rounded_rectangle(
        box(400, 1100, 625, 1280), radius=12 * SCALE, fill=BLUE, outline=INK, width=LINE
    )
    draw.ellipse(box(425, 1250, 480, 1305), fill=INK)
    draw.ellipse(box(545, 1250, 600, 1305), fill=INK)
    draw.line([point(760, 1110), point(900, 1300)], fill=INK, width=28 * SCALE)
    draw.ellipse(box(710, 1050, 795, 1135), outline=INK, width=18 * SCALE)
    save(image, "10-choice-roadmap.png")


for generate in (opening, three_tools, full_finetune, peft, lora, qlora, direction, dora, qdora, choice):
    generate()
