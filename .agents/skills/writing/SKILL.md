---
name: writing
description: |
  Writing skill that combines clear writing methodology with AI pattern removal.
  Part 1: 5-step writing process (audience, composition, structure, grammar, proofread).
  Part 2: Detect and remove 30 categories of AI writing patterns (based on Wikipedia's
  "Signs of AI writing" guide). Produces natural, human-sounding text.
---

# Writing Skill

A complete writing guide in two parts: how to write clearly, and how to remove AI fingerprints from the result.

---

## Part 1: Writing Methodology

### Step 1: Consider Audience and Format

Before writing a word, answer two questions:

**Who will read this?** Senior managers, engineers, general public, prospective clients? Your readers define your tone, depth, and vocabulary. Writing for developers means you can use code examples and skip basics. Writing for a general audience means analogies over jargon.

**What format fits?** An informal email, a detailed report, advertising copy, a blog post, a formal letter? The format sets structural expectations. A report has sections and data. A blog post has hooks and personality. Don't write a report when an email will do.

**Practical check:** If you can't describe your reader in one sentence and your format in one word, you're not ready to write.

### Step 2: Pay Attention to Composition and Style

Once you know your audience and format, start composing:

- **Start with your audience.** They may know nothing about your topic. What do they need to know first?
- **Create an outline.** Especially for longer pieces. Outlines break the task into manageable chunks and prevent rambling.
- **Use AIDA for persuasive writing.** Attention (hook them), Interest (keep them reading), Desire (make them want it), Action (tell them what to do next).
- **Try empathy.** If writing a pitch, ask: why should they care? What's in it for them?
- **Identify your main theme.** Pretend you have 15 seconds to explain your position. That sentence is your anchor. Every paragraph should serve it.
- **Use simple language.** Don't use long words to impress. "Use" beats "utilize." "Help" beats "facilitate." Readers trust clarity, not complexity.

### Step 3: Have a Writing Structure in Place

Make your document scannable:

- **Use headings and subheadings.** Break up the text. A page of short paragraphs with section headings gets read; a wall of text gets skipped.
- **Use bullet points and numbered lists.** When listing items or steps, format them as lists, not paragraphs.
- **Use questions as headers.** Questions keep readers engaged and curious. "Why is X faster than Y?" beats "Performance Comparison."
- **Add visual aids.** Tables, charts, and code blocks communicate information faster than prose. Use them.
- **Keep paragraphs short.** 1-3 sentences per paragraph. Dense paragraphs signal "skip me."

### Step 4: Avoid Grammatical Errors

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

### Step 5: Proofread Your Work

Rushing is the enemy of proofreading. Follow these techniques:

1. **Proof headers and subheaders separately.** People skip these assuming they're correct. They often aren't.
2. **Read the document out loud.** This forces you to slow down and catch awkward phrasing.
3. **Use your finger to follow text.** Another way to slow down and catch errors.
4. **Start from the end.** Proofread one sentence at a time, working backward. This separates content from mechanics.
5. **Check formatting consistency.** Are headers styled the same way throughout? Are lists formatted consistently?

---

## Part 2: Remove AI Writing Patterns

Based on Wikipedia's "Signs of AI writing" guide (WikiProject AI Cleanup). When writing or editing text, scan for and eliminate these 30 categories of AI tells.

### Voice Calibration (Optional)

If a writing sample is provided, analyze it first:
- Sentence length patterns (short? long? mixed?)
- Word choice level (casual? academic?)
- Paragraph opening habits
- Punctuation habits (dashes? parentheses? semicolons?)
- Recurring phrases or verbal tics
- Transition style

Match the sample's voice in the output. When no sample is provided, default to natural, varied, opinionated writing.

### Personality and Soul

Avoiding AI patterns is half the job. Sterile, voiceless writing is just as obvious as slop.

**Apply personality when appropriate:** blog posts, essays, opinion pieces, personal writing. For encyclopedic, technical, legal, or reference text, neutral and plain is the correct human voice.

**Signs of soulless writing (even if technically clean):**
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality

**How to add voice:**
- **Have opinions.** "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.
- **Vary your rhythm.** Short punchy sentences. Then longer ones that take their time. Mix it up.
- **Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.

---

### Content Patterns

#### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how things represent or contribute to broader topics.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

#### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

#### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Before:**
> The temple's color palette resonates with the region's natural beauty, symbolizing Texas bluebonnets, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

#### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Before:**
> Nestled within the breathtaking region of Gonder, Alamata stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

#### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Before:**
> Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The river supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

#### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas. Despite these challenges, Korattur continues to thrive.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022.

---

### Language and Grammar Patterns

#### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Before:**
> Additionally, an enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

#### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Before:**
> Gallery 825 serves as LAAA's exhibition space. The gallery features four spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space. The gallery has four rooms totaling 3,000 square feet.

#### 9. Negative Parallelisms and Tailing Negations

**Problem:** "Not only...but..." or "It's not just about..., it's..." overuse. Also clipped fragments like "no guessing" or "no wasted motion" tacked onto sentences.

**Before:**
> It's not just about the beat; it's part of the aggression. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

**Before (tailing negation):**
> The options come from the selected item, no guessing.

**After:**
> The options come from the selected item without forcing the user to guess.

#### 10. Rule of Three Overuse

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

#### 11. Elegant Variation (Synonym Cycling)

**Problem:** AI has repetition-penalty causing excessive synonym substitution (protagonist -> main character -> central figure -> hero).

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.

#### 12. False Ranges

**Problem:** "from X to Y" where X and Y aren't on a meaningful scale.

**Before:**
> Our journey has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

#### 13. Passive Voice and Subjectless Fragments

**Before:**
> No configuration file needed. The results are preserved automatically.

**After:**
> You do not need a configuration file. The system preserves the results automatically.

---

### Style Patterns

#### 14. Em Dashes: Cut Them

The em dash is one of the most reliable AI tells. **The final output must contain zero em dashes (--) or en dashes (--).**

Replace each one with: a period, a comma, a colon, parentheses, or restructure the sentence.

**Before:**
> The term is primarily promoted by Dutch institutions -- not by the people themselves. You don't say "Netherlands, Europe" as an address -- yet this mislabeling continues -- even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

#### 15. Overuse of Boldface

**Before:**
> It blends **OKRs**, **KPIs**, and visual strategy tools such as the **Business Model Canvas** and **Balanced Scorecard**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

#### 16. Inline-Header Vertical Lists

**Before:**
> - **User Experience:** The user experience has been significantly improved.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

#### 17. Title Case in Headings

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships

#### 18. Emojis

**Before:**
> :rocket: **Launch Phase:** The product launches in Q3
> :bulb: **Key Insight:** Users prefer simplicity

**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

#### 19. Curly Quotation Marks

ChatGPT uses curly quotes instead of straight quotes. Use straight quotes consistently.

---

### Communication Patterns

#### 20. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

#### 21. Knowledge-Cutoff Disclaimers and Speculative Gap-Filling

**Words to watch:** as of [date], While specific details are limited..., based on available information, not publicly available, maintains a low profile, likely [grew up/studied/began], it is believed that

**Before:**
> Information about her early life is not publicly available, suggesting she maintains a low profile. She likely grew up in a middle-class household.

**After:**
> Her early life is not documented in the available sources. (Or omit the section.)

#### 22. Sycophantic/Servile Tone

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point!

**After:**
> The economic factors you mentioned are relevant here.

---

### Filler and Hedging

#### 23. Filler Phrases

| Before | After |
|--------|-------|
| In order to achieve this goal | To achieve this |
| Due to the fact that it was raining | Because it was raining |
| At this point in time | Now |
| In the event that you need help | If you need help |
| The system has the ability to process | The system can process |
| It is important to note that the data shows | The data shows |

#### 24. Excessive Hedging

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.

#### 25. Generic Positive Conclusions

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence.

**After:**
> The company plans to open two more locations next year.

#### 26. Hyphenated Word Pair Overuse

Keep attributive-position hyphens (`a high-quality report`). Drop them in predicate position (`the report is high quality`).

#### 27. Persuasive Authority Tropes

**Phrases to watch:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter

**Before:**
> The real question is whether teams can adapt. At its core, what really matters is organizational readiness.

**After:**
> The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.

#### 28. Signposting and Announcements

**Phrases to watch:** Let's dive in, let's explore, let's break this down, here's what you need to know, without further ado

**Before:**
> Let's dive into how caching works in Next.js. Here's what you need to know.

**After:**
> Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.

#### 29. Fragmented Headers

A heading followed by a one-line paragraph that restates the heading before the real content begins.

**Before:**
> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.

**After:**
> ## Performance
>
> When users hit a slow page, they leave.

#### 30. Diff-Anchored Writing

Unless the document is version-scoped (changelogs, release notes), it should read coherently without knowing what changed.

**Before:**
> This function was added to replace the previous approach of iterating through all items, which caused O(n2) performance.

**After:**
> This function uses a hash map for O(1) lookups, avoiding the O(n2) cost of naive iteration.

#### 31. Delayed Reveal (Abstract-then-Name)

**Problem:** First sentence introduces something abstractly ("最好的发现" / "the best finding"), next sentence reveals what it is ("那个发现是 X" / "That finding is X"). This creates artificial suspense that reads like a formulaic setup-punchline cadence. Human writers name the thing directly when they first bring it up.

**Words to watch:** 那个X是Y, That X is Y, The answer/reason/finding is, What makes this special is

**Before:**
> 它交出了全场最好的单项发现。
>
> 那个发现是余额模型。这是全场最难的 Bug，因为它分布在三个文件中。

**After:**
> 它在余额模型这个全场最难的 Bug 上，给出了比所有前沿模型都完整的诊断。
>
> 这个 Bug 难在它分布在三个文件中。

**English example:**

**Before:**
> There was one thing that set Grok apart from the rest. That thing was its handling of the balance model.

**After:**
> Grok's handling of the balance model set it apart from the rest.

**Fix:** Merge the abstract reference and the concrete name into one sentence. If the thing is interesting, name it immediately; the details that follow are the real payoff, not the name itself.

#### 32. Source Material Key Point Omission

**Problem:** When writing from source material (notes, English drafts, research), the AI drops points from TL;DR sections, executive summaries, or numbered takeaways — especially the last 1-2 items. The result reads complete on its own, so neither writer nor reader notices a gap until they compare against the source. This happens most with negative findings (failures, caveats) and "universal" statements (all models failed, nobody solved X).

**How it manifests:**
- Source TL;DR has 5 bullets, output covers 3
- Failure/disappointment points get silently pruned (positivity bias)
- "All X did Y" universal claims dropped in favor of per-item analysis
- Final twist or caveat omitted because the piece already feels concluded

**Fix:** Before writing, extract every discrete claim from the source's summary/TL;DR/abstract into a numbered checklist. After drafting, tick each one off against the output. Any unchecked item must be added — typically to the opening paragraph or the conclusion, wherever the density of key claims lives.

**Audit question:** "Does my opening paragraph (or summary section) contain every major finding from the source material's TL;DR, including negative results and universal statements?"

---

### Detection Guidance

#### What NOT to flag (false positives)

These are not reliable AI indicators on their own:

- Perfect grammar and consistent style (professionals and editors exist)
- Mixed casual and formal registers (common in tech writers)
- Formal or academic vocabulary (AI overuses specific fancy words, not all fancy words)
- Common transition words in isolation (one "however" is not a tell)
- Curly quotes alone (macOS/Word auto-curl by default)
- Em dashes alone (many journalists use them; only a tell when paired with other patterns)
- Unsourced claims (most of the web is unsourced)

**Look for clusters of tells, not isolated ones.** A single em dash means nothing. Em dashes plus rule-of-three plus "vibrant tapestry" plus a "Conclusion" section is a confession.

#### Signs of human writing (preserve these)

- Specific, unusual, hard-to-fabricate detail ("the lawyer who used to work upstairs from my dentist")
- Mixed feelings and unresolved tension ("I think this is mostly good, but it bothers me")
- Dated, era-bound references (slang and memes that map to a specific year)
- Variety in sentence length (real writing alternates short and long)
- Genuine asides and self-corrections ("I keep wanting to say 'almost' here, but it really was certain")

---

## Part 3: Self-Check Process

After writing, run this checklist before delivering:

### Writing Quality Check

| Check | Method |
|-------|--------|
| Main theme | Can you summarize the entire piece in one sentence? Does every paragraph serve that sentence? |
| Opening hook | Do the first 3 sentences give the reader a reason to continue? Data, surprise, or concrete scene work. "As X develops..." does not. |
| Paragraph length | Any paragraph over 3 sentences? Any two consecutive paragraphs without a list/table/code block? Split or restructure. |
| Simple language | Replace "utilize" with "use", "facilitate" with "help", "leverage" with "use". Readers trust clarity. |
| Active voice | "This tool cuts compile time to 3s" beats "Compile time was significantly reduced." |
| Evidence over adjectives | "10x faster" beats "significantly improved performance." |
| Transitions | Each paragraph opening connects to the previous one (cause, contrast, progression, time). No unexplained jumps. |
| Ending | Not a summary. A callback to the opening, a next step, or a bigger question. Never start with "In conclusion" / "To summarize." |

### AI Pattern Audit

| Check | Method |
|-------|--------|
| Em/en dashes | Search for `--` and `--`. Any hit means the draft isn't done. |
| AI vocabulary | Scan for: delve, crucial, pivotal, landscape, tapestry, vibrant, testament, underscore, foster, showcase, interplay, intricate. Replace or cut. |
| Significance inflation | Any sentence containing "marking a", "setting the stage", "represents a shift", "key turning point"? Cut the ceremony, state the fact. |
| Rule of three | Did you accidentally group things in threes? Break the pattern. |
| Boldface | Is bold used mechanically on every list item header? Remove most of it. |
| Filler phrases | "In order to", "it is important to note that", "due to the fact that" -> simplify. |
| Collaborative artifacts | "I hope this helps", "Let me know", "Great question!" -> delete. |
| Delayed reveal | "它交出了最好的X。那个X是Y。" -> merge into one sentence that names Y directly. |
| Source point omission | Compare output's opening/summary against source TL;DR checklist. Every discrete claim (especially negatives and universals) must appear. |
| Soulless writing | Read it aloud. Does it sound like a person talking, or a press release? Add opinion, uncertainty, or specific detail where the tone feels flat. |

### Final Proofread

1. Proof headers separately from body text
2. Read the entire piece out loud
3. Read backward, one sentence at a time, checking mechanics only
4. Verify formatting consistency (header styles, list formats, punctuation)

---

## Full Example

**Before (AI-sounding):**
> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale.
>
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts, from solo developers to cross-functional teams. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.
>
> - **Speed:** Code generation is significantly faster, reducing friction and empowering developers.
> - **Quality:** Output quality has been enhanced through improved training.
> - **Adoption:** Usage continues to grow, reflecting broader industry trends.
>
> While specific details are limited, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies, the ecosystem continues to thrive.
>
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey toward excellence. Let me know if you'd like me to expand on any section!

**Draft rewrite:**
> AI coding assistants speed up some tasks. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools are good at boilerplate: config files, test scaffolding, repetitive refactors. They are bad at knowing when they are wrong. I have mass-accepted suggestions that compiled, passed lint, and still did the wrong thing because I stopped paying attention.
>
> The productivity claims are hard to verify. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not correctness, and correctness is not value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
>
> None of this means the tools are useless. It means they are tools. They do not replace judgment, and they do not eliminate the need for tests.

**Audit ("What makes the draft still sound AI-generated?"):**
- The rhythm is still a bit too tidy (clean contrasts, evenly paced paragraphs)
- The closer leans a touch slogan-y
- Named studies can read like plausible-but-made-up placeholders unless real and sourced

**Final rewrite:**
> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> People I talk to tend to land in two camps. Some use it like autocomplete for chores and review every line. Others disable it after it keeps suggesting patterns they don't want. Both feel reasonable.
>
> The productivity metrics are slippery. GitHub can say Copilot users "accept 30% of suggestions," but acceptance isn't correctness, and correctness isn't value. If you don't have tests, you're basically guessing.

**Changes made:** Stripped chatbot framing, significance inflation, promotional and -ing padding, rule-of-three, synonym cycling, false ranges, copula avoidance, em dashes, emojis, boldface, curly quotes, formulaic "challenges" section, hedging disclaimers, filler, persuasive framing, and the generic upbeat conclusion. Rebuilt the voice with varied rhythm and concrete detail.

---

## Reference

Part 2 of this skill is based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.
