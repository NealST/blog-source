#!/usr/bin/env python3
"""One-off rewrite of content/agent-experience/illustrations.html.

Keeps brand slides 1, 4, 7 (renumbered as 配图 1 / 4 / 7) and replaces
slides 2, 3, 5, 6, 8 with inline previews of xiaohei PNGs sitting in
content/agent-experience/xiaohei-illustrations/.

The slide-label format for the xiaohei rows uses the dual-style form
understood by scripts/insert_image_placeholders.py:

    小黑 NN · 放在「锚点」之后 · 文件:NN-name.png
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "content/agent-experience/illustrations.html"

# 1-indexed line ranges (inclusive) of each slide block: from comment line to closing </div>
# Verified via grep_search + read_file inspection.
BRAND_KEEP = {1: (103, 172), 4: (267, 325), 7: (435, 499)}
REPLACE = [
    # (slide_num_original, anchor_text, xiaohei_filename, kicker, title, sub)
    (
        2,
        "什么是 Agent 体验",
        "02-feedback-loop-machine.png",
        "CORE LOOP",
        "核心问题：构建反馈循环",
        "重点不是更聪明的提示词，而是闭合的‘跑—验—跑’回路",
    ),
    (
        3,
        "原则一：上下文即 onboarding",
        "01-eternal-day-one.png",
        "PRINCIPLE 01 · ETERNAL DAY 1",
        "对 agent 来说，每次任务都是 Day 1",
        "没有累积、没有记忆，onboarding 在每次任务开头重做一遍",
    ),
    (
        5,
        "原则三：交付前必须验证",
        "04-review-scale.png",
        "PRINCIPLE 03 · EVIDENCE",
        "交付时附证据，不甩锅给审查者",
        "测试日志、截图、录屏一起递上柜台，再盖一个 PASS",
    ),
    (
        6,
        "原则四：安全必须是系统性的",
        "03-crack-in-the-road.png",
        "PRINCIPLE 04 · SYSTEMIC SAFETY",
        "DX 让危险困难；AX 让危险不可能",
        "护栏要罩在系统层，不能靠每个人都看得见‘rm -rf’",
    ),
    (
        8,
        "原则七：agent 是跨职能协作的粘合剂",
        "05-stitch-and-create.png",
        "FINAL · GLUE VS CREATE",
        "Agent 做胶水，人做创造",
        "agent 缝合模块、清理输出；人留出空间做判断、品味、架构、策略",
    ),
]


def xiaohei_block(num: int, anchor: str, fname: str, kicker: str, title: str, sub: str) -> str:
    """Build the replacement HTML for one xiaohei slide row."""
    # The slide-label feeds insert_image_placeholders.py.
    return f"""<!-- ===== 配图 {num} · 小黑 · {fname} ===== -->
<div class="slide-label">小黑 {num:02d} · 放在「{anchor}」之后 · 文件:{fname}</div>
<div class="slide xiaohei-row" data-xiaohei="{fname}" style="background:#FFFFFF;padding:0;border:1px solid rgba(28,28,30,0.08);border-radius:8px;overflow:hidden;">
  <div style="padding:14px 22px 6px;display:flex;align-items:center;justify-content:space-between;">
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;color:#C4956A;text-transform:uppercase;">{kicker}</div>
      <div style="font-size:18px;font-weight:800;color:#1C1C1E;margin-top:4px;letter-spacing:-0.01em;">{title}</div>
      <div style="font-size:12px;color:#7A7876;margin-top:3px;font-style:italic;">{sub}</div>
    </div>
    <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;color:rgba(28,28,30,0.35);">小黑手绘 · AI 直出</div>
  </div>
  <img src="xiaohei-illustrations/{fname}" alt="{title}" style="display:block;width:100%;height:auto;" />
</div>

"""


def main():
    text = SRC.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Collect line indices to drop (slides being replaced) and where to insert their xiaohei block.
    drop_ranges = []  # list[(start_idx, end_idx_exclusive)]
    insertions = {}   # start_idx -> xiaohei html block

    for num, anchor, fname, kicker, title, sub in REPLACE:
        start_line = None
        for i, line in enumerate(lines, start=1):
            if line.startswith(f"<!-- ===== 配图 {num} ·"):
                start_line = i
                break
        assert start_line is not None, f"could not find slide {num}"

        # End of slide div: scan forward for the first line that is exactly "</div>\n"
        # that closes the outermost slide div. We look for the pattern: blank line
        # followed by the next slide comment OR </body>.
        end_line = None
        for j in range(start_line, len(lines) + 1):
            ln = lines[j - 1] if j - 1 < len(lines) else ""
            # the slide ends at "</div>\n" immediately followed by a blank line and another slide marker
            if ln.rstrip() == "</div>" and j < len(lines):
                # Look ahead for either next slide or the script block
                k = j
                while k < len(lines) and lines[k].strip() == "":
                    k += 1
                if k < len(lines) and (
                    lines[k].lstrip().startswith("<!-- ===== 配图")
                    or "<script" in lines[k]
                ):
                    end_line = j
                    break

        assert end_line is not None, f"could not find end of slide {num}"
        drop_ranges.append((start_line - 1, end_line))  # 0-indexed half-open
        insertions[start_line - 1] = xiaohei_block(num, anchor, fname, kicker, title, sub)

    # Rebuild
    out = []
    i = 0
    while i < len(lines):
        # Check if a replacement starts at this index
        replaced = False
        for (s, e), in zip([(s, e) for (s, e) in drop_ranges], ):
            pass
        # Simpler: dict-based
        for s, e in drop_ranges:
            if i == s:
                out.append(insertions[s])
                i = e
                replaced = True
                break
        if not replaced:
            out.append(lines[i])
            i += 1

    new_text = "".join(out)

    # Update download script: skip xiaohei-row, use data-num for brand filename
    new_text = new_text.replace(
        "async function downloadAll() {\n"
        "  const zip = new JSZip();\n"
        "  const slides = document.querySelectorAll('.slide');\n"
        "  for (let i = 0; i < slides.length; i++) {\n"
        "    const canvas = await renderSlide(slides[i]);\n"
        "    const blob = await new Promise(res => canvas.toBlob(res, 'image/png'));\n"
        "    zip.file(`配图-${String(i+1).padStart(2,'0')}.png`, blob);\n"
        "  }\n"
        "  const content = await zip.generateAsync({ type: 'blob' });\n"
        "  saveAs(content, '配图-Agent体验.zip');\n"
        "}\n"
        "async function downloadOne(idx) {\n"
        "  const slides = document.querySelectorAll('.slide');\n"
        "  const i = idx ?? 0;\n"
        "  if (!slides[i]) return;\n"
        "  const canvas = await renderSlide(slides[i]);\n"
        "  canvas.toBlob(blob => saveAs(blob, `配图-${String(i+1).padStart(2,'0')}.png`), 'image/png');\n"
        "}",
        "function brandSlideNum(slide, idx) {\n"
        "  const n = slide.getAttribute('data-num');\n"
        "  return n || String(idx + 1).padStart(2, '0');\n"
        "}\n"
        "async function downloadAll() {\n"
        "  const zip = new JSZip();\n"
        "  // Only render brand slides; xiaohei slides are already PNGs on disk.\n"
        "  const slides = document.querySelectorAll('.slide:not(.xiaohei-row)');\n"
        "  for (let i = 0; i < slides.length; i++) {\n"
        "    const canvas = await renderSlide(slides[i]);\n"
        "    const blob = await new Promise(res => canvas.toBlob(res, 'image/png'));\n"
        "    const name = brandSlideNum(slides[i], i);\n"
        "    zip.file(`配图-${name}.png`, blob);\n"
        "  }\n"
        "  const content = await zip.generateAsync({ type: 'blob' });\n"
        "  saveAs(content, '配图-品牌-Agent体验.zip');\n"
        "}\n"
        "async function downloadOne(idx) {\n"
        "  const slides = document.querySelectorAll('.slide:not(.xiaohei-row)');\n"
        "  const i = idx ?? 0;\n"
        "  if (!slides[i]) return;\n"
        "  const canvas = await renderSlide(slides[i]);\n"
        "  const name = brandSlideNum(slides[i], i);\n"
        "  canvas.toBlob(blob => saveAs(blob, `配图-${name}.png`), 'image/png');\n"
        "}",
    )

    # Add data-num to the 3 kept brand slides so filenames are stable (配图-1 / 4 / 7).
    # Inject right after `<div class="slide dark"` or `<div class="slide light"` for slides we keep.
    # Each brand slide currently has a unique min-height comment near it; we use slide-label as anchor.
    for keep_num in (1, 4, 7):
        label_re = re.compile(
            r'(<div class="slide-label">配图 ' + str(keep_num) + r' · 放在[^<]*</div>\s*\n<div class="slide )(dark|light)("[^>]*)>'
        )
        new_text, n = label_re.subn(rf'\1\2\3 data-num="{keep_num}">', new_text, count=1)
        assert n == 1, f"failed to tag brand slide {keep_num}"

    SRC.write_text(new_text, encoding="utf-8")
    print(f"wrote {SRC}")


if __name__ == "__main__":
    main()
