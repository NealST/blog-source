#!/usr/bin/env python3
"""
Insert <!-- IMAGE:文件名.png --> placeholders into preview.html.

Reads illustration anchors from illustrations.html's .slide-label elements,
then inserts placeholders into preview.html at the matching section boundaries.

Supports two label formats (can be mixed in the same illustrations.html):

  Brand (info-graphic rendered via html2canvas as `配图-N.png`):
      <div class="slide-label">配图 N · 放在「锚点文字」之后</div>
      → emits  <!-- IMAGE:配图-N.png -->

  Xiaohei (AI-generated PNG already on disk in xiaohei-illustrations/):
      <div class="slide-label">小黑 NN · 放在「锚点文字」之后 · 文件:01-eternal-day-one.png</div>
      → emits  <!-- IMAGE:01-eternal-day-one.png -->

Order of insertion follows the visual order of labels in illustrations.html
(i.e. the order placeholders appear within a section).

Usage:
    python3 insert_image_placeholders.py <preview.html> <illustrations.html>
"""

import re
import sys


# Returns list of (placeholder_filename, anchor) preserving document order so that
# multiple images attached to the same section land in the same order they appear
# in illustrations.html.
def parse_slide_labels(illustrations_path: str) -> list[tuple[str, str]]:
    """Extract (filename, anchor) pairs from .slide-label elements."""
    with open(illustrations_path, 'r', encoding='utf-8') as f:
        html = f.read()

    items: list[tuple[str, str]] = []
    pattern = re.compile(
        r'class="slide-label"[^>]*>([^<]+)</div>',
        re.UNICODE,
    )

    for m in pattern.finditer(html):
        label = m.group(1).strip()

        # Xiaohei form: 小黑 NN · 放在「锚点」之后 · 文件:filename.png
        mx = re.match(
            r'小黑\s*\d+\s*·\s*放在「([^」]+)」之后\s*·\s*文件\s*[:：]\s*(\S+\.png)',
            label,
        )
        if mx:
            anchor = mx.group(1)
            fname = mx.group(2)
            items.append((fname, anchor))
            continue

        # Brand form: 配图 N · 放在「锚点」之后
        mb = re.match(r'配图\s*(\d+)\s*·\s*放在「([^」]+)」', label)
        if mb:
            num = int(mb.group(1))
            anchor = mb.group(2)
            items.append((f'配图-{num}.png', anchor))
            continue

    return items


def insert_placeholders(preview_path: str, items: list[tuple[str, str]]) -> int:
    """Insert <!-- IMAGE:<filename> --> into preview.html at section boundaries.

    Each item is (filename, anchor). When multiple items share the same anchor,
    they are inserted in the order they appeared in the source list.
    """
    with open(preview_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # insertions: line_index → ordered list of placeholder strings
    insertions: dict[int, list[str]] = {}

    def normalize_dashes(s: str) -> str:
        return s.replace('—', '-').replace('–', '-').replace('--', '-')

    for fname, anchor in items:
        anchor_norm = normalize_dashes(anchor)
        heading_lines = []
        for i, line in enumerate(lines):
            if ('<h2' in line or '<h3' in line) and anchor_norm in normalize_dashes(line):
                heading_lines.append(i)

        if not heading_lines:
            print(f"⚠ Could not find anchor for {fname}: {anchor}")
            continue

        for heading_line in heading_lines:
            # Find end of section: next h2 or h3
            section_end = None
            for j in range(heading_line + 1, len(lines)):
                if re.search(r'<h[23]\s', lines[j]):
                    section_end = j
                    break
    
            if section_end is None:
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
            insertions[section_end].append(f'<!-- IMAGE:{fname} -->\n')
            print(f"✓ {fname} → insert before line {section_end + 1} (anchor: {anchor})")

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

    items = parse_slide_labels(illustrations_path)
    if not items:
        print("No slide labels found in illustrations.html")
        sys.exit(1)

    print(f"Found {len(items)} illustration anchors")
    insert_placeholders(preview_path, items)


if __name__ == '__main__':
    main()
