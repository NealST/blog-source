# Jev Article Diagrams: Local Style and Assumptions

## Scope

The user explicitly confirmed Mozheng branding for this task only. This directory contains exactly three static, self-contained HTML illustrations. No shared style guide, named profile, project marker, article, aggregation page, preview, or manifest is modified by this task.

Source: `source/_posts/about-jev.md`, as read during this task. Each illustration belongs to a different chapter:

- `03-question-primitives.html`: "它的工作原理与三大核心原语".
- `04-confidence-gate.html`: "概率与置信度：如何设计可靠的业务门禁？".
- `06-fast-slow.html`: "什么时候该用 Jev，什么时候应该避开？".

## Local Tokens

Source: `.agents/skills/content-pipeline/references/brand-colors.md` and the task's explicit confirmation.

| Role | Value | Use |
| --- | --- | --- |
| paper | `#FFFFFF` | Opaque full SVG frame and HTML slide background |
| paper-2 | `#F2EDE3` | Local input, judgment, and decision nodes only |
| ink | `#1C1C1E` | All visible text and primary node outlines |
| accent | `#C4956A` | One focal node per illustration |
| muted / soft | `#7A7876` | Connectors and input outlines, not body text |
| link | `#2C2A28` | Unused link-marker fallback from the brand's strong ink |
| rule | `#1C1C1E` at 0.16 opacity | Local footer separators |

Frames are rectangular, white, and shadow-free. No external fonts, images, scripts, packages, or runtime services are required. CSS selectors and marker IDs are isolated with `jev03`, `jev04`, or `jev06`; accessible-name IDs use the unique file slug as required by the self-check.

## Size and Typography

All three use `doc-inline`, `viewBox="0 0 960 600"`. The title is 28 SVG units. Body labels use the standard 12-unit role and the CJK register-switch rule in a local `scale(2)` group. Their rendered size is 24px at native width, or 20px when the article scales the complete image to 800px. Titles become approximately 23.3px at 800px. The half-scale drawing coordinates preserve a physical 4px grid; corner radii and arrow-marker metrics are intentional exceptions.

Simplified Chinese resolves through the locally available `PingFang SC`, with `Microsoft YaHei` and generic families as cross-platform fallbacks. `Geist` and `Instrument Serif` remain role-family declarations but are not fetched or embedded; this is explicitly an offline local-font rendering, not an exact-font claim for those Latin families. Browser checks confirmed `PingFang SC` availability and no text overflow on this macOS host. Other hosts may substitute fonts.

The screen SVG retains `min-width: 960px` inside a local horizontal scroller. At a 390px mobile viewport the scroller is 374px wide, its content remains 960px, and the document itself does not overflow. Print rules release the minimum width and scrolling. For image export, capture the entire frame at native width, not the clipped mobile scroller.

## Selection and Fidelity

- 03: simplified DATA FLOW, 6 nodes and 5 arrows. State and Questions join one Jev request, then three independent question/answer groups fan out. No answer-to-answer dependencies, benchmark charts, sample probabilities, or fabricated source examples are introduced. The specialized multi-role platform matrix in the type reference is intentionally not used: the task specifies an API fan-in/fan-out, not organizational lanes.
- 04: FLOWCHART, 5 nodes and 4 arrows. Follow the exact ordered article conditions: `< 0.5` sends to human; otherwise `choice == refund AND confidence > 0.9` enters the refund process; all other inputs require confirmation. In particular, confidence exactly 0.9 and non-refund confidence above 0.9 do not enter the refund branch. Footers state private-data backtesting and separate permissions or human review. Starting a refund flow does not itself authorize a transfer.
- 06: ARCHITECTURE, 6 nodes and 6 arrows. Jev only judges; code routes to lightweight generation or slow reasoning/human escalation. Result forwarding, checking, and output share one terminal node. Code owns deterministic permissions and sandbox boundaries for sensitive tools; risk scores are advisory, not enforcement. The feedback loop is omitted to avoid density, and this omission is also stated in the SVG description. No specific latency, vendor, or model performance is implied.

Semantic patterns were read before selection. None of the complete catalog patterns matches these narrowly requested figures: no paired policy traces, deployment/bypass routes, or compensating-layer risk chain is claimed. Native flowchart decision shapes and the architecture's code-owned hard-boundary annotation express the relevant behavior without inventing an unrelated pattern.

## Validation

- Packaged `self_check.py`: passed separately after each first edit and again after the flowchart text-position correction.
- The installed skill and workspace do not contain `verify-geometry.py`; no geometry package was installed. Browser SVG-geometry checks supplement, but do not claim to be, that upstream validator.
- Browser checks for all three: every node's text rectangle is inside its rect/polygon; every visible text lies within the SVG frame; sampled connectors do not pass through non-endpoint nodes or intersect one another; each flowchart arrow-label mask has a 16px physical gap, corresponding to 8 units in the scaled group; minimum effective label size at 800px is 20px.
- The ordered flowchart graph passes 10 boundary cases spanning refund/other and confidence 0.499, 0.5, 0.9, 0.9001, and 1.
- Export is intentionally left to the main content pipeline. No PNG or standalone SVG deliverables are generated here.

## Export Selectors

| Source | Complete opaque frame | SVG-only selector |
| --- | --- | --- |
| `03-question-primitives.html` | `.slide.bg-light[data-num="3"]` | `#jev03-svg` |
| `04-confidence-gate.html` | `.slide.bg-light[data-num="4"]` | `#jev04-svg` |
| `06-fast-slow.html` | `.slide.bg-light[data-num="6"]` | `#jev06-svg` |