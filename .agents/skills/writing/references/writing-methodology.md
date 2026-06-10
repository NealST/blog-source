# Part 1: Writing Methodology

### Step 1: Consider Audience and Format

Before writing a word, answer two questions:

**Who will read this?** Senior managers, engineers, general public, prospective clients? Your readers define your tone, depth, and vocabulary. Writing for developers means you can use code examples and skip basics. Writing for a general audience means analogies over jargon.

**What format fits?** An informal email, a detailed report, advertising copy, a blog post, a formal letter? The format sets structural expectations. A report has sections and data. A blog post has hooks and personality. Don't write a report when an email will do.

**Practical check:** If you can't describe your reader in one sentence and your format in one word, you're not ready to write.

### Step 2: Write the Title First

Write the title before the body. A title forces you to commit to one angle — if you can't write a compelling title, your piece doesn't have a clear enough thesis.

**Tech blog title patterns that work:**
- **Data-first:** "我用 5 个前沿模型审了同一份代码，最便宜的赢了" — leads with the surprising finding
- **How/why question:** "为什么你的 Code Review 流程需要两个模型" — frames the article as answering a question
- **Direct claim:** "单模型审查是筛子，不是判决书" — states the thesis upfront
- **Tool/method + outcome:** "用 Claude Code 的 Memory 功能管理写作风格" — names the tool and what it achieves

**Title anti-patterns:**
- Vague umbrella: "关于 AI Code Review 的一些思考" — says nothing specific
- Clickbait without substance: "震惊！这个模型竟然..." — erodes trust
- Too long: anything over 25 Chinese characters or 12 English words loses scannability
- Too technical: "基于 AST 差分的多模型代码审查管线优化" — reads like a paper title, not a blog post

**Practical check:** Show the title to someone unfamiliar with the topic. If they can't tell what they'll learn from reading the article, rewrite it.

### Step 3: Choose a Structure Template

Different article types have proven structures. Pick one before outlining:

**Comparison/benchmark:**
1. Hook with the most surprising result
2. Methodology (brief — readers want results, not setup)
3. Per-item analysis (strongest to weakest, or by category)
4. Cross-cutting insights (patterns that emerge across items)
5. Recommendation with specific scenarios

**Tutorial/how-to:**
1. Problem statement (what the reader can't do yet)
2. Solution overview (one sentence)
3. Step-by-step walkthrough
4. Gotchas and edge cases
5. What to try next

**Opinion/analysis:**
1. Thesis (stated directly, not buried)
2. Strongest evidence
3. Counter-evidence or limitations (shows intellectual honesty)
4. Refined thesis (evolved from the opening, not just restated)

**Incident/postmortem:**
1. What happened (timeline, impact)
2. Why it happened (root cause chain)
3. What we did (fix, not just "we fixed it")
4. What we changed (process/systemic improvements)

Don't force a piece into a template that doesn't fit — but if you're staring at a blank outline, a template gives you a starting skeleton.

### Step 4: Control Scope

Before writing, decide boundaries:

**Signs your scope is too wide:**
- The outline has more than 5 top-level sections
- You need more than 3000 words (Chinese) or 2000 words (English) to cover everything
- Two sections could each be standalone articles
- You keep adding "I should also mention X" while outlining

**When to split into a series:**
- The topic has natural parts (setup → usage → advanced) that serve different readers
- Each part can stand alone — a reader who lands on Part 2 via search shouldn't be lost
- You have enough material for 1500+ words per part

**When to keep it as one post:**
- The argument builds cumulatively — Part 2 only makes sense after Part 1
- The total length stays under 3000 words
- Splitting would create parts too thin to be interesting on their own

**Scope control technique:** Write one sentence per section in your outline. If you can't — if the section needs a paragraph just to describe what it covers — that section is too big and should be split or narrowed.

### Step 5: Pay Attention to Composition and Style

Once you know your audience and format, start composing:

- **Start with your audience.** They may know nothing about your topic. What do they need to know first?
- **Create an outline.** Especially for longer pieces. Outlines break the task into manageable chunks and prevent rambling.
- **Use AIDA for persuasive writing.** Attention (hook them), Interest (keep them reading), Desire (make them want it), Action (tell them what to do next).
- **Try empathy.** If writing a pitch, ask: why should they care? What's in it for them?
- **Identify your main theme.** Pretend you have 15 seconds to explain your position. That sentence is your anchor. Every paragraph should serve it.
- **Use simple language.** Don't use long words to impress. "Use" beats "utilize." "Help" beats "facilitate." Readers trust clarity, not complexity.

### Step 6: Have a Writing Structure in Place

Make your document scannable:

- **Use headings and subheadings.** Break up the text. A page of short paragraphs with section headings gets read; a wall of text gets skipped.
- **Use bullet points and numbered lists.** When listing items or steps, format them as lists, not paragraphs.
- **Use questions as headers.** Questions keep readers engaged and curious. "Why is X faster than Y?" beats "Performance Comparison."
- **Add visual aids.** Tables, charts, and code blocks communicate information faster than prose. Use them.
- **Keep paragraphs short.** 1-3 sentences per paragraph. Dense paragraphs signal "skip me."

#### Integrating Code Examples

Code blocks are powerful but break reading flow. Use them deliberately:

**When to use inline code** (`backticks`):
- Function names, variable names, CLI commands mentioned in passing
- Short expressions that are part of a sentence: "调用 `deleteTransaction` 时不会回退余额"

**When to use code blocks:**
- Anything over one line
- Code the reader needs to understand structurally (not just the name of)
- Before/after comparisons

**Code block hygiene:**
- Keep blocks under 15 lines — if longer, show only the relevant portion and say where the rest is
- Add context before the block: what the reader should notice ("注意第 3 行的 `balance +=`")
- Add interpretation after the block: what it means for the argument
- Never drop a code block between two paragraphs with no prose connecting them

**Common mistake:** Using a code block to "prove" a claim when a prose description would be clearer. Code blocks are for when the exact syntax matters — if only the behavior matters, describe it in words.

### Step 7: Avoid Grammatical Errors

Common mistakes that spell checkers miss:

| Error | Rule | Example |
|-------|------|---------|
| affect/effect | affect = verb (to influence), effect = noun (the result) | "The change will affect revenue." / "The effect was immediate." |
| then/than | then = sequence in time, than = comparison | "First X, then Y." / "X is faster than Y." |
| your/you're | your = possessive, you're = you are | "Your file." / "You're the new manager." |
| its/it's | its = possessive, it's = it is | "Its motor." / "It's often heavy." |
| possessive vs. plural | company's = possession, companies = plural | "The company's trucks." / "The companies suffered." |

**Chinese-specific checks (when writing in Chinese):**
- 的/地/得 usage: 的 modifies nouns, 地 modifies verbs, 得 indicates degree
- 做/作 distinction
- Avoid "进行" padding ("进行讨论" -> "讨论")
- Use Chinese punctuation in prose, English punctuation in code
