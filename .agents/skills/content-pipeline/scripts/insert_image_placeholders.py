#!/usr/bin/env python3
"""
Insert <!-- IMAGE:配图-N.png --> placeholders into preview.html.

Reads illustration anchors from illustrations.html's .slide-label elements,
then inserts placeholders into preview.html at the matching section boundaries.

Usage:
    python3 insert_image_placeholders.py <preview.html> <illustrations.html>
"""

import re
import sys


def parse_slide_labels(illustrations_path: str) -> dict[int, str]:
    """Extract anchors from .slide-label elements in illustrations.html.

    Expected format: 配图 N · 放在「锚点文字」之后
    Returns: {1: "锚点文字", 2: "锚点文字", ...}
    """
    with open(illustrations_path, 'r', encoding='utf-8') as f:
        html = f.read()

    anchors = {}
    for m in re.finditer(
        r'class="slide-label"[^>]*>配图\s*(\d+)\s*·\s*放在「([^」]+)」',
        html,
    ):
        num = int(m.group(1))
        anchor = m.group(2)
        anchors[num] = anchor

    return anchors


def insert_placeholders(preview_path: str, anchors: dict[int, str]) -> int:
    """Insert <!-- IMAGE:配图-N.png --> into preview.html at section boundaries."""
    with open(preview_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    insertions: dict[int, list[str]] = {}

    for img_num, anchor in anchors.items():
        heading_line = None
        # Normalize dashes for matching (-- vs – vs —)
        def normalize_dashes(s: str) -> str:
            return s.replace('—', '-').replace('–', '-').replace('--', '-')

        anchor_norm = normalize_dashes(anchor)
        for i, line in enumerate(lines):
            if ('<h2' in line or '<h3' in line) and anchor_norm in normalize_dashes(line):
                heading_line = i
                break

        if heading_line is None:
            print(f"⚠ Could not find anchor for 配图 {img_num}: {anchor}")
            continue

        # Find end of section: next h2 or h3
        section_end = None
        for j in range(heading_line + 1, len(lines)):
            if re.search(r'<h[23]\s', lines[j]):
                section_end = j
                break

        if section_end is None:
            # Last section — insert before END marker or </section>, not </body>
            for j in range(len(lines) - 1, heading_line, -1):
                if '— END —' in lines[j] or '-- END --' in lines[j]:
                    section_end = j
                    break
            if section_end is None:
                for j in range(len(lines) - 1, heading_line, -1):
                    if '</section>' in lines[j]:
                        section_end = j
                        break
            if section_end is None:
                for j in range(len(lines) - 1, heading_line, -1):
                    if '</body>' in lines[j]:
                        section_end = j
                        break
            if section_end is None:
                section_end = len(lines) - 1

        insertions.setdefault(section_end, [])
        insertions[section_end].append(f'<!-- IMAGE:配图-{img_num}.png -->\n')
        print(f"✓ 配图 {img_num} → insert before line {section_end + 1}")

    # Rebuild
    new_lines = []
    for i, line in enumerate(lines):
        if i in insertions:
            for placeholder in insertions[i]:
                new_lines.append(placeholder)
        new_lines.append(line)

    with open(preview_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    total = sum(len(v) for v in insertions.values())
    print(f"\nInserted {total} placeholders into {preview_path}")
    return total


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <preview.html> <illustrations.html>")
        sys.exit(1)

    preview_path = sys.argv[1]
    illustrations_path = sys.argv[2]

    anchors = parse_slide_labels(illustrations_path)
    if not anchors:
        print("No slide labels found in illustrations.html")
        sys.exit(1)

    print(f"Found {len(anchors)} illustration anchors")
    insert_placeholders(preview_path, anchors)


if __name__ == '__main__':
    main()
