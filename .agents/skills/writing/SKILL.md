---
name: writing
description: |
  Writing skill: guides both drafting and quality-checking.
  Phase 1: Writing methodology — structure, composition, title craft, and scope control.
  Phase 2: AI pattern removal — write clean of AI fingerprints, or scan existing text against 51 pattern categories.
  Phase 3: Final verification — lightweight residue check and mechanical proofreading.
---

# Writing Skill

A writing guide that works in two modes: **drafting** (turning raw material into polished prose) and **quality-checking** (auditing existing text for issues). All three phases apply in both modes.

## Execution Modes

Choose a mode based on scope:

- **full** (default): All three phases in order. Use for new articles or comprehensive quality checks.
- **quick**: Phase 2 only, focused on the highest-frequency patterns. Use for spot-checking a paragraph or short piece.
- **structure**: Phase 1 only. Use when the content exists but the organization needs work.

When no mode is specified, run **full**.

## Execution Discipline

**In full mode, all three phases execute in order. No phase may be skipped.**

Phase 1 establishes structure, composition, and title. In drafting mode, it organizes raw material into the best possible outline and prose structure. In quality-check mode, it audits existing text for structural problems. Structural issues must be resolved before Phase 2, because pattern-level work on broken structure is wasted effort.

Phase 2 guides word-level and sentence-level craft: voice, register, and 51 categories of patterns that make writing sound machine-generated. These patterns apply to all writing — they reflect how LLMs naturally construct prose, regardless of whether an English source exists.

Phase 3 is a lightweight residue check: verify that Phase 1 and Phase 2 fixes didn't introduce new issues, then do a mechanical proofread. Phase 3 does NOT re-run Phase 1 or Phase 2 checks.

When reporting results, explicitly list findings from each phase under its own heading. If a phase produces zero findings, state that explicitly rather than omitting the phase.

---

## Phase 1: Writing Methodology

`references/writing-methodology.md`

**Purpose:** Organize content into clear, well-structured prose — or audit existing prose for structural problems. This includes title craft, scope control, genre-appropriate structure, and code example integration.

**When drafting from raw material:**
1. Write the title first — it forces you to commit to a single angle
2. Identify audience and format
3. Extract the main theme (one sentence that anchors every paragraph)
4. Choose a structural template that fits the genre (comparison, tutorial, opinion, postmortem)
5. Build an outline: decide section order, what goes where, what to cut
6. Decide scope: one post or a series? (see Scope Control in reference)
7. Write with short paragraphs (1-3 sentences), clear transitions, and a hook opening
8. Integrate code examples deliberately — context before, interpretation after
9. Ensure the ending echoes the opening or points forward, never summarizes

**When quality-checking existing text:**
- Title passes the "would I click this?" test and contains the article's single angle
- Main theme can be stated in one sentence; every paragraph serves it
- Structure matches a recognizable genre template, not a shapeless info-dump
- Opening hook uses data, suspense, or a concrete scene (not "随着X的发展")
- Paragraphs are 1-3 sentences; longer ones are split at logic boundaries
- No sentence carries 3+ independent information layers in comma-spliced clauses
- No section repeats information already covered elsewhere
- Simple language: no "utilize"/"facilitate"; Chinese: no "进行" padding
- Active voice preferred over passive
- Adjectives backed by data ("10x faster" not "significantly faster")
- Every paragraph transition has logical connective (causal, contrastive, temporal)
- Code blocks have context before and interpretation after; no orphaned code blocks
- Ending is not a summary
- Scope is controlled: no section that could be its own article

**Output:** In drafting mode, produce structured prose with a title. In quality-check mode, list issues with locations and fixes. Resolve structural issues before proceeding to Phase 2.

---

## Phase 2: AI Pattern Audit

`references/ai-patterns.md`

**Purpose:** Write clean of patterns that make prose sound machine-generated, or detect and remove them from existing text. Covers 51 pattern categories.

These patterns are not translation artifacts — they reflect how LLMs naturally construct Chinese prose. An LLM writing Chinese from scratch will produce calqued syntax (#36), mechanical negation chains (#42), and skeletal recommendations (#47) just as readily as one working from English source material. Every pattern in this phase applies to all writing.

**Voice calibration:** If a writing sample is provided, analyze sentence length, word choice, paragraph openings, punctuation habits, and transition style. Match that voice. If no sample, default to natural, varied, opinionated writing within the appropriate register.

**Core actions (both modes):**
- Apply all 51 pattern categories — avoid these patterns when drafting, scan for them when quality-checking
- Pay special attention to patterns that are hard to self-detect: calqued metaphors (#35), calqued syntax (#36), calqued rhetoric (#37), register check (#39), idiom register (#40)
- Check the Detection Guidance section for false-positive awareness

**Quick mode subset:** When running in quick mode, focus on these high-frequency patterns: #14 (em dashes), #7 (AI vocabulary), #1 (significance inflation), #10 (rule of three), #29 (fragmented headers), #35 (calqued metaphors), #36 (calqued syntax), #20 (collaborative artifacts), #31 (delayed reveal), #39 (register-mismatched idioms).

**Register reminder for tech blogs:** Professional tone with opinions. Avoid slangy verbs (丢给、甩了、整了) but also avoid sterile corporate prose. Neutral action verbs (交给、给出、完成) let facts carry the tone.

**Output:** In drafting mode, the text should already be clean. In quality-check mode, list each pattern violation with category number, location, and fix. Resolve before proceeding to Phase 3.

---

## Phase 3: Final Verification

`references/self-check.md`

**Purpose:** Lightweight residue check — verify that Phase 1 and Phase 2 fixes didn't introduce new issues, then do a mechanical proofread. This phase does NOT re-run Phase 1 or Phase 2 checks.

**Core actions:**
1. **Residue scan:** Read the text end-to-end looking for issues introduced *by* Phase 1/2 edits — broken transitions, orphaned references, inconsistent terminology, new redundancies from paragraph merges/splits
2. **Title-body coherence:** Does the title still match the final content? Phase 1/2 edits may have shifted the angle
3. **Mechanical proofread:** Proof headers separately, read backward for typos, verify formatting consistency, check all numbers and proper nouns against source material

**Output:** Report any residue issues found and fix them. If clean, state "Phase 3: no residue issues found."

---

## Handoff

After Phase 3, if the piece is ready for publishing, invoke the **content-pipeline** skill for formatting (WeChat, Xiaohongshu) and distribution.
