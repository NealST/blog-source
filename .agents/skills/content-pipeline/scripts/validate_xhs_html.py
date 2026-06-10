#!/usr/bin/env python3
"""
validate_xhs_html.py — 小红书 HTML 质量检查

用法：
  python3 validate_xhs_html.py path/to/小红书版.html
  python3 validate_xhs_html.py content/slug/*小红书版.html

退出码：0 = 通过，1 = 有违规，2 = 用法错误
"""

import re
import sys

# ── A. CSS 颜色合规 ──

CSS_RULES = [
    {
        "name": "strong 使用金色",
        "pattern": re.compile(
            r'\.post-body\s+strong[^{]*\{[^}]*color\s*:\s*#C4956A',
            re.IGNORECASE,
        ),
        "fix": "strong { color: #1C1C1E; font-weight: 700; }",
    },
    {
        "name": ".h3 使用金色",
        "pattern": re.compile(
            r'\.post-body\s+\.h3[^{]*\{[^}]*color\s*:\s*#C4956A',
            re.IGNORECASE,
        ),
        "fix": ".h3 { color: #2C2A28; }",
    },
    {
        "name": ".bullet 使用金色",
        "pattern": re.compile(
            r'\.bullet[^{]*\{[^}]*color\s*:\s*#C4956A',
            re.IGNORECASE,
        ),
        "fix": ".bullet { color: #999; }",
    },
    {
        "name": "code 使用非品牌色 #b8621b",
        "pattern": re.compile(
            r'(?<!\.)code\s*\{[^}]*color\s*:\s*#b8621b',
            re.IGNORECASE,
        ),
        "fix": "code { color: #1C1C1E; }",
    },
]

INLINE_RULES = [
    {
        "name": "strong 内联金色",
        "pattern": re.compile(
            r'<strong[^>]*style="[^"]*color\s*:\s*#C4956A[^"]*"',
            re.IGNORECASE,
        ),
        "fix": "strong style 中 color 应为 #1C1C1E",
    },
    {
        "name": "strong font-weight 非 700",
        "pattern": re.compile(
            r'<strong[^>]*style="[^"]*font-weight\s*:\s*(?!700)\d+',
            re.IGNORECASE,
        ),
        "fix": "strong style 中 font-weight 应为 700",
    },
]


# ── B. 结构完整性 ──

def check_swipe_hint(content: str) -> list[str]:
    """第 1 张封面卡必须有滑动引导。"""
    errors = []
    slides = re.findall(r'<div\s+class="slide"[^>]*id="slide-1"[\s\S]*?(?=<div\s+class="slide"|$)', content)
    if not slides:
        slides = re.findall(r'<div\s+class="slide"[\s\S]*?(?=<div\s+class="slide"|$)', content)
    if slides:
        first_slide = slides[0]
        if 'swipe-hint' not in first_slide and '左滑' not in first_slide:
            errors.append('  [结构] 第 1 张封面缺少滑动引导 → 添加 <div class="swipe-hint">← 左滑查看更多</div>')
    return errors


def check_white_background(content: str) -> list[str]:
    """内容页禁止使用纯白 #FFFFFF 背景。"""
    errors = []
    slides = re.findall(r'<div\s+class="slide"[^>]*>([\s\S]*?)(?=<div\s+class="slide"|$)', content)
    for i, slide_html in enumerate(slides):
        slide_num = i + 1
        if slide_num == 1 or slide_num == len(slides):
            continue
        if re.search(r'class="bg-light"', slide_html):
            errors.append(f'  [背景] 第 {slide_num} 张使用了废弃的 .bg-light（纯白），应改为 .bg-paper（宣纸底 #F2EDE3）')
        if re.search(r'background\s*:\s*#(?:fff(?:fff)?|FFF(?:FFF)?)\b', slide_html) and 'bg-paper' not in slide_html:
            errors.append(f'  [背景] 第 {slide_num} 张使用了纯白背景 #FFFFFF，应使用宣纸底 #F2EDE3')
    return errors


def check_page_numbers(content: str) -> list[str]:
    """页码 n/N 中的 N 必须等于实际 slide 数。"""
    errors = []
    slide_count = len(re.findall(r'<div\s+class="slide"', content))
    if slide_count == 0:
        return errors
    page_totals = re.findall(r'class="page">[^<]*?(\d+)\s*/\s*(\d+)', content)
    for current, total in page_totals:
        if int(total) != slide_count:
            errors.append(f'  [页码] 页码显示 {current}/{total}，但实际有 {slide_count} 张卡片')
            break
    return errors


def check_bg_paper_format(content: str) -> list[str]:
    """确认使用新版 .bg-paper 格式而非废弃的 .slide-title 格式。"""
    errors = []
    if re.search(r'class="slide-title"', content) and not re.search(r'class="bg-paper"', content):
        errors.append('  [格式] 使用了废弃的 .slide-title 格式，应迁移到 .bg-paper + .post-header/.post-body/.post-footer')
    return errors


def check_header_footer(content: str) -> list[str]:
    """每张内容卡都应有 header 和 footer。"""
    errors = []
    slides = re.findall(r'<div\s+class="slide"[^>]*>([\s\S]*?)(?=<div\s+class="slide"|$)', content)
    for i, slide_html in enumerate(slides):
        slide_num = i + 1
        is_img_only = 'img-only' in slide_html
        if is_img_only:
            continue
        if 'post-header' not in slide_html:
            errors.append(f'  [结构] 第 {slide_num} 张缺少 .post-header')
        if 'post-footer' not in slide_html:
            errors.append(f'  [结构] 第 {slide_num} 张缺少 .post-footer')
    if len(errors) > 6:
        errors = errors[:3] + [f'  [结构] ... 还有 {len(errors) - 3} 处缺失']
    return errors


# ── Main ──

def validate(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # A. CSS 颜色合规
    for rule in CSS_RULES:
        if rule["pattern"].search(content):
            errors.append(f"  [CSS] {rule['name']} → 应改为 {rule['fix']}")

    for rule in INLINE_RULES:
        matches = rule["pattern"].findall(content)
        if matches:
            errors.append(f"  [inline] {rule['name']}（{len(matches)} 处）→ {rule['fix']}")

    # B. 结构完整性
    errors.extend(check_swipe_hint(content))
    errors.extend(check_white_background(content))
    errors.extend(check_page_numbers(content))
    errors.extend(check_bg_paper_format(content))
    errors.extend(check_header_footer(content))

    return errors


def main():
    if len(sys.argv) < 2:
        print("用法: python3 validate_xhs_html.py <html文件路径>...", file=sys.stderr)
        sys.exit(2)

    has_errors = False
    for path in sys.argv[1:]:
        errors = validate(path)
        if errors:
            has_errors = True
            print(f"✗ {path}")
            for e in errors:
                print(e)
        else:
            print(f"✓ {path}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
