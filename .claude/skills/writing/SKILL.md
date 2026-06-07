---
name: writing
description: |
  Writing skill: guides both drafting and quality-checking.
  Phase 1: Writing methodology — structure raw material into well-organized prose, or audit existing text for structural issues.
  Phase 2: AI pattern removal — write clean of AI fingerprints, or scan existing text against 51 pattern categories.
  Phase 3: Self-check — final checklist covering writing quality, AI patterns, and mechanical proofreading.
---

# Writing Skill

A writing guide that works in two modes: **drafting** (turning raw material into polished prose) and **quality-checking** (auditing existing text for issues). All three phases apply in both modes.

## Execution Discipline

**All three phases must execute in order. No phase may be skipped.**

Phase 1 establishes structure and composition. In drafting mode, it organizes raw material into the best possible outline and prose structure. In quality-check mode, it audits existing text for structural problems. Either way, structural issues must be resolved before Phase 2, because AI pattern work on broken structure is wasted effort.

Phase 2 guides word-level and sentence-level craft: voice, register, and 51 categories of AI writing patterns. In drafting mode, it ensures clean writing from the start. In quality-check mode, it scans for and fixes violations.

Phase 3 is a final checklist pass plus mechanical proofreading.

When reporting results, explicitly list findings from each phase under its own heading. If a phase produces zero findings, state that explicitly rather than omitting the phase.

---

## Phase 1: Writing Methodology

**Read:** `references/writing-methodology.md`

**Purpose:** Organize content into clear, well-structured prose — or audit existing prose for structural problems.

**When drafting from raw material:**
1. Identify audience and format
2. Extract the main theme (one sentence that anchors every paragraph)
3. Build an outline: decide section order, what goes where, what to cut
4. Write with short paragraphs (1-3 sentences), clear transitions, and a hook opening
5. Ensure the ending echoes the opening or points forward, never summarizes

**When quality-checking existing text:**
- Main theme can be stated in one sentence; every paragraph serves it
- Opening hook uses data, suspense, or a concrete scene (not "随着X的发展")
- Paragraphs are 1-3 sentences; longer ones are split at logic boundaries
- No sentence carries 3+ independent information layers in comma-spliced clauses
- No section repeats information already covered elsewhere
- Simple language: no "utilize"/"facilitate"; Chinese: no "进行" padding
- Active voice preferred over passive
- Adjectives backed by data ("10x faster" not "significantly faster")
- Every paragraph transition has logical connective (causal, contrastive, temporal)
- Ending is not a summary

**Output:** In drafting mode, produce structured prose. In quality-check mode, list issues with locations and fixes. Resolve structural issues before proceeding to Phase 2.

---

## Phase 2: AI Pattern Audit

**Read:** `references/ai-patterns.md`

**Purpose:** Write clean of AI fingerprints, or detect and remove them from existing text. Covers 51 pattern categories.

**Voice calibration:** If a writing sample is provided, analyze sentence length, word choice, paragraph openings, punctuation habits, and transition style. Match that voice. If no sample, default to natural, varied, opinionated writing within the appropriate register.

**Core actions (both modes):**
- Apply all 51 pattern categories — avoid these patterns when drafting, scan for them when quality-checking
- Pay special attention to patterns that are hard to self-detect: calqued metaphors (#35), calqued syntax (#36), calqued rhetoric (#37), sentence-for-sentence translation (#38), register check (#39), idiom register (#40)
- Check the Detection Guidance section for false-positive awareness

**Register reminder for tech blogs:** Professional tone with opinions. Avoid slangy verbs (丢给、甩了、整了) but also avoid sterile corporate prose. Neutral action verbs (交给、给出、完成) let facts carry the tone.

**Output:** In drafting mode, the text should already be clean. In quality-check mode, list each pattern violation with category number, location, and fix. Resolve before proceeding to Phase 3.

---

## Phase 3: Self-Check

**Read:** `references/self-check.md`

**Purpose:** Final verification that nothing was missed, plus mechanical proofreading.

**Core actions:**
1. Run the **Writing Quality Check** table (10 items): main theme, opening hook, paragraph length, sentence overload, content redundancy, simple language, active voice, evidence over adjectives, transitions, ending
2. Run the **AI Pattern Audit** table (30+ items): em dashes, AI vocabulary, significance inflation, rule of three, boldface, filler phrases, collaborative artifacts, delayed reveal, source point omission, data fabrication, and all Chinese-specific checks
3. Run **Final Proofread**: proof headers separately, read aloud, read backward for mechanics, verify formatting consistency

**Output:** Report pass/fail for each checklist item. Fix any remaining issues.
