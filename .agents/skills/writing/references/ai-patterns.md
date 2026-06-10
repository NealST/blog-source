# Part 2: Remove AI Writing Patterns

Based on Wikipedia's "Signs of AI writing" guide (WikiProject AI Cleanup). When writing or editing text, scan for and eliminate these 51 categories of AI tells.

These patterns are not limited to translation or adaptation from English sources. LLMs produce them in all Chinese writing because their internal representations favor English-like structures, metaphors, and rhetorical patterns. A model writing Chinese "from scratch" will calque English syntax (#36), stack mechanical negation chains (#42), and dump flat enumerations (#40) just as readily as one working from an English draft. Every pattern below applies to all writing.

## Voice Calibration (Optional)

If a writing sample is provided, analyze it first:
- Sentence length patterns (short? long? mixed?)
- Word choice level (casual? academic?)
- Paragraph opening habits
- Punctuation habits (dashes? parentheses? semicolons?)
- Recurring phrases or verbal tics
- Transition style

Match the sample's voice in the output. When no sample is provided, default to natural, varied, opinionated writing — but for tech blogs, stay within a professional register (see "Tech blog register constraint" below).

## Personality and Soul

Avoiding AI patterns is half the job. Sterile, voiceless writing is just as obvious as slop.

**Apply personality when appropriate:** blog posts, essays, opinion pieces, personal writing. For encyclopedic, technical, legal, or reference text, neutral and plain is the correct human voice.

**Tech blog register constraint:** Tech blogs sit between casual and formal. Keep them direct, readable, and opinionated — but never slangy. Avoid colloquial verbs that carry attitude beyond the content (e.g., "丢给" implies carelessness, "甩了一句" implies disdain). Use neutral action verbs ("交给", "只给了一句指令") that let the facts carry the tone. The goal is a professional writer who has opinions, not a friend chatting over drinks. When in doubt, choose the more restrained option — readers trust authority over casualness in technical content.

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

**Chinese variant — subtitle synonym restatement:**

When a heading includes a subtitle summary (e.g., "### X：覆盖最广，推理最细"), the AI often opens the body by paraphrasing that subtitle ("X 审得最广也最细。"). The restatement adds no information — delete it and start directly with data or detail.

**Before:**
> ### Claude Opus 4.8：覆盖最广，推理最细
>
> Opus 审得最广也最细。它命中了两个 React Bug、全部三个日期 Bug、以及三个余额 Bug 中的两个。

**After:**
> ### Claude Opus 4.8：覆盖最广，推理最细
>
> Opus 命中了两个 React Bug、全部三个日期 Bug、以及三个余额 Bug 中的两个。

**Why it's a problem:**
- "覆盖最广，推理最细"和"审得最广也最细"是同义词替换，读者获得的新信息为零
- 标题已经承载了概括功能，正文的第一句应该提供标题无法传递的具体数据
- 同义复述还会造成相关词汇重复：如果第一段的开头和文章其他部分使用了同一个词（如"出人意料"/"最大惊喜"），重复会更显眼

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

#### 33. Data Fabrication (Plausible but Unsourced Numbers)

**Problem:** When source material provides partial data (some numbers stated, others implied or absent), the AI fills gaps with plausible-looking values rather than acknowledging the gap. This is especially dangerous with costs, percentages, dates, and statistics — readers trust specific numbers and won't verify them against the source. The fabricated values often "feel right" because the AI infers them from context, making them harder to catch than outright hallucinations.

**How it manifests:**
- Source gives a ratio ("9x cheaper") and one anchor ($0.08); AI calculates the other value and presents it as stated fact
- Source omits data for some items in a comparison; AI invents numbers to complete the table
- Source uses vague language ("about half"); AI converts to a specific percentage (48%)
- Derived values presented without marking them as derived
- Tables with mixed real and fabricated data in the same column

**Fix:** Before including any number, cost, date, percentage, or statistic in the output, verify it falls into one of three categories:

1. **Directly stated** in the source — use as-is
2. **Derivable** from stated values — mark explicitly as derived (e.g., "按原文比例推算约为...")
3. **Not available** — say so, or omit the data point entirely

Never fill an empty cell with a plausible guess. A table with blank cells or a paragraph that says "原文未披露" is more trustworthy than one with fabricated precision.

**Audit question:** "For every number in my output, can I point to the exact sentence in the source that states it, or have I clearly marked it as derived/unavailable?"

#### 34. Stiff Handoff Transitions (Generic Pointer → Named Reveal)

**Problem:** Paragraph A ends with a generic recommendation or abstract pointer ("find a model that's strong at X"), then Paragraph B opens by naming the specific thing ("That partner is Y"). This two-step setup creates a formulaic, rigid cadence — especially across a paragraph break. Human writers merge the pointer and the name into one sentence, letting the details that follow be the real payoff.

**Words to watch:** 那个X是Y, That [noun] is Y, The answer is, The tool for this is, The solution is

**Before (Chinese):**
> 它的盲区是日期计算，如果你的代码依赖时区和周期性调度，配一个日期方面强的模型。
>
> 那个搭档是 Sonnet 4.6。它和 Grok 的检出率相同但路径互补。

**After (Chinese):**
> 它的盲区是日期计算——如果你的代码依赖时区和周期性调度，得找个日期方面强的搭档。Sonnet 4.6 刚好补上这块，它和 Grok 的检出率相同但路径互补。

**English example:**

**Before:**
> Its blind spot is date math. If your code leans on timezones, pair it with something that owns that.
>
> That partner is Sonnet 4.6. It matched Grok's score through the opposite strengths.

**After:**
> Its blind spot is date math, so if your code leans on timezones, pair it with Sonnet 4.6. It matched Grok's score through the opposite strengths.

**Fix:** Merge the generic pointer and the concrete name into one sentence. Don't use a paragraph break to create artificial suspense about a recommendation. The name itself isn't the payoff — the details that follow are.

**Difference from Delayed Reveal (#31):** Delayed Reveal abstracts *within* a passage ("它交出了最好的X → 那个X是Y"). This pattern splits a *recommendation* across a paragraph boundary, creating a stiff "setup paragraph → payoff paragraph" handoff. Both share the same root cause (naming things indirectly), but this variant is specific to cross-paragraph transitions and advisory/recommendation writing.

#### 35. Calqued Metaphors (Literal Translation of Source-Language Idioms)

**Problem:** LLMs naturally produce Chinese text with English-shaped metaphors and idiomatic expressions — whether or not an English source exists. This happens because the model's internal representations favor English patterns, so even "original" Chinese writing comes out with calqued idioms. The result reads like translation software, not a person writing in Chinese. The same applies in reverse (Chinese idioms calqued into English).

**How it manifests:**
- English metaphors transplanted verbatim: "buys the widest net" → "买得到最宽的安全网"
- Idiomatic verb-object pairings that don't exist in Chinese: "paint a picture" → "画一幅画面"
- English personification carried over: "the data tells us" → "数据告诉我们" (acceptable in some contexts but often a calque)
- Phrasal structures that mirror English syntax: "what X brings to the table" → "X带到桌上的东西"

**Before (Chinese, calqued from "Opus still buys the widest net"):**
> Opus 仍然买得到最宽的安全网。当审查是代码上线前的最后一道闸，多花的钱是便宜的保险。

**After (natural Chinese):**
> Opus 的覆盖面仍然最广，当审查是代码上线前的最后一道闸，多花的钱买的是保险。

**Fix:** When writing Chinese from English source material, translate the *meaning*, not the *expression*. If a sentence reads like you could reverse-translate it back to English word-for-word, it's probably a calque. Ask: "Would a Chinese writer who never saw the English draft phrase it this way?" If not, rewrite using the concept the metaphor conveys, not the metaphor itself.

**Example 2 — 技术动词和术语的直译 calque：**

技术文章中尤其容易出现一类 calque：英文的技术动词、phrasal verb、半术语被逐词翻译成中文，单个词都认识，但组合起来不是中文技术写作的自然表达。

| English | Calqued Chinese | Natural Chinese | 问题类型 |
|---------|----------------|-----------------|---------|
| state mutates | 状态发生变异 | 状态被修改 / 修改状态 | "变异"是生物学用词，代码语境用"修改" |
| a single finding | 一条 finding | 一次分析 / 一条结论 | 英文术语直搬 |
| linked to the same root cause | 关联到同一个根因 | 追溯到同一个根因 | "关联到"是"linked to"的直译，中文用"追溯" |
| resulting drift | 由此产生的漂移 | 数值偏移 | "漂移"是"drift"的直译，中文技术语境用"偏移" |
| went further than any other model | 比任何其他模型都走得更远 | 进一步 | phrasal verb "go further" 的逐词翻译 |
| go with event sourcing | 走事件溯源 | 采用事件溯源 | "走"是"go with"的直译 |
| derive balances | 派生余额 | 推导余额 | "派生"是"derive"的直译，中文用"推导" |

**Before:**
> 只有状态在多个地方发生变异时才会出问题。Grok 在一条 finding 中把它拆干净了...它把三个错误关联到同一个根因，标记了由此产生的重复计算和漂移，然后比任何其他模型都走得更远，给出了修复方案：用不可变账本派生余额，或者走事件溯源让 base balance 永远不被直接修改。

**After:**
> 只有多处同时修改状态才会暴露。Grok 在一次分析中完整拆解了它...它把三个错误追溯到同一个根因，指出了重复计算和数值偏移的问题，进一步给出了修复思路：用不可变账本推导余额，或采用事件溯源确保 base balance 不被直接修改。

**与 Example 1 的区别：**
- Example 1 是隐喻/惯用语的 calque（"买得到最宽的安全网"←"buys the widest net"），修复方式是换一个中文自然表达来传达同样的概念
- Example 2 是技术动词和术语的 calque（"发生变异"←"mutates"，"派生"←"derive"），修复方式是找到中文技术写作中对应的常用动词

**筛查方法：** 技术文章中遇到以下信号时重点检查：① 中文里不常见的"动词+到"组合（关联到、映射到、链接到）；② 直接使用英文术语原词（finding、drift）或其音译/硬译；③ 用"走/跑/开"等口语动词搭配技术概念（走事件溯源、跑流水线、开一个PR）——这类搭配通常是英文 phrasal verb 的痕迹。

**Scope:** This pattern appears in all LLM-generated Chinese text, not just translations. The examples use English→Chinese pairs because they make the calque structure visible, but the same patterns appear when the LLM writes Chinese without any English source. The principle also applies symmetrically to other language pairs.

#### 36. Calqued Sentence Structure (英文句法套中文)

**Problem:** Different from #35 (calqued metaphors, which operates at the word/phrase level). This pattern is about the AI keeping English *sentence structure* when writing Chinese: noun predicates where Chinese uses verb predicates, participial appositives crammed into 破折号+长定语, relative clause nesting that follows English "a X that Y" order. Individual words may all be correct Chinese, but the sentence reads like Google Translate because its skeleton is English.

**Common structural calques:**

| English structure | Calqued Chinese | Natural Chinese |
|-------------------|----------------|-----------------|
| X was the Y (noun predicate) | X 是最大的Y | X 最让人Y (verb predicate) |
| ...missing/doing Z (participial appositive) | ——一个...的Z，它... | ...的Z它直接... (tighter clause) |
| a bug so obvious that... (result clause) | 一个其他四个模型全部抓到的Bug | 其他四个模型都抓到的Bug (drop "一个", reduce formality) |
| X, which is Y (non-restrictive relative) | X，它是Y的 | X是Y的 (merge into one clause) |
| flagged X rather than Y | 标记的问题是X，而不是Y | 标记的是X，没有识别出Y（拆成两个独立陈述） |

**Before:**
> Gemini 3.1 Pro 是最大的失望——一个其他四个模型全部抓到的 Bug，它径直走过了。

**After:**
> Gemini 3.1 Pro 最让人失望，其他四个模型都抓到的 Bug 它直接没看见。

**Changes made:**
- "是最大的失望" (noun predicate, calqued from "was the letdown") → "最让人失望" (verb predicate, natural Chinese)
- 破折号 + "一个...的Bug，它..." (English participial appositive structure) → 逗号 + tighter clause with subject flowing directly
- Dropped "一个" which was mimicking English "a bug"

**Fix:** After drafting from English source material, read each sentence and ask: "Is this sentence's *skeleton* Chinese or English?" If you can mentally slot English words back in and recover the original sentence structure, it's a calque. Restructure using Chinese-native patterns: verb predicates over noun predicates, shorter clauses over nested relatives, topic-comment over subject-verb-object when it fits.

**筛查纪律：** 不要凭语感判断"读着通顺就没问题"——"Grok 是这次测试的主角"读着通顺，但骨架仍然是英文的 "X was the Y"。必须对每一句执行以下机械检查：
1. **搜索"是...的"：** 全文搜索所有"X 是...的 Y"句式，逐个判断是否为英文名词谓语的直译，能否改为动词谓语
2. **搜索破折号"——"：** 检查是否后跟英文式的长定语从句或同位语结构
3. **搜索"而"对比连词：** 检查"而"两侧是否为结构对称的镜像分句（"X从A开始而Y从B开始"），如果是，拆成两个独立分句
4. **搜索引号间接转述：** 检查"解释了'""指出'""认为'"等"动词+引号"组合，间接转述不应加引号，改为正常叙述
5. **检查长定语隔断动宾：** 找出"动词+长定语+宾语"结构（定语超过 6 个字），如果读者需要回溯才能把动词和宾语对上，用"将/把"字句前置宾语，或拆成两个分句
6. **回译测试：** 尝试把中文逐词替换为英文，如果能还原出自然的英文句子，说明骨架是英文的

**Example 2 — choppy sentence boundaries + jargon calque:**

English source:
> None of them will make the code throw. The test suite passes. The catch is that you have to understand how a budget app *should* do math before you can see that it's doing it wrong.

**Before:**
> 这些 Bug 表面上看代码能跑。测试套件是通过的。难点在于你得理解一个预算应用"应该"怎么算，才能发现它算错了。

**After:**
> 这些 Bug 不会让代码报错，测试也照样能过。关键是你得懂一个预算应用该怎么算钱，才看得出它是否算错。

**Changes made:**
- 三句断为两句：英文三个短句各占一句是英文节奏，中文用逗号连成两句更流畅
- "测试套件" (calqued jargon from "test suite") → "测试"（中文语境不需要"套件"）
- "是通过的" (calqued "是...的" structure from "passes") → "照样能过"（口语化，更自然）
- "难点在于" (formal transition calqued from "The catch is that") → "关键是"（更轻便）
- "理解一个预算应用'应该'怎么算" → "懂一个预算应用该怎么算钱"（"懂"比"理解"更口语，"算钱"比"算"更具体）

**Example 3 — "而"对比连词硬接 + 引号间接转述：**

技术解释段落中容易同时出现两种句法硬译：① 用"而"把英文 "X but Y" 的对比结构塞进一个中文分句；② 用引号包裹间接转述，镜像英文 "explained that 'X does Y'" 的引用方式。

English source:
> Since JavaScript months are zero-indexed but the app's month strings aren't, recurring transactions land a month late. Opus caught the off-by-one and explained that a May selection schedules into June.

**Before:**
> 但 JavaScript 月份从零开始而应用的月份字符串从一开始。Opus 抓住了这个偏移，解释了"选五月会排到六月"。

**After:**
> 但 JavaScript 的月份参数从 0 开始计数，应用传入的却是从 1 开始的值。Opus 识别出了这个差一问题，指出用户选五月实际会被排到六月。

**Changes made:**
- "从零开始而...从一开始"：英文 "zero-indexed but...aren't" 的 but 对比结构用"而"硬接，两个"从X开始"挤在一句里节奏拗口 → 拆成两个独立分句，用"却"做转折，各自完整
- "应用的月份字符串"："the app's month strings" 的逐词直译 → "应用传入的值"，中文技术写作不需要强调"字符串"这个类型
- "解释了'选五月会排到六月'"：英文 "explained that 'a May selection schedules into June'" 的引号间接转述在中文里不自然 → "指出用户选五月实际会被排到六月"，用正常的间接叙述，去掉引号

**筛查方法：**
- **"而"对比连词：** 搜索全文的"而"，检查是否连接了两个结构对称的分句（"X从A开始而Y从B开始""X支持Z而Y不支持"）。如果"而"两侧的结构几乎镜像，大概率是英文 "X but Y" 的直译，应拆成两个独立分句
- **引号间接转述：** 搜索"解释了'""指出'""认为'""说明'"等"动词+了/过+引号"组合。中文的间接转述不加引号，直接用"指出X会导致Y"的形式。引号仅用于直接引语（原话照搬）或特殊术语标注

**Difference from #35:**
- **#35 Calqued Metaphors:** foreign *expressions* translated literally ("buys the widest net" → "买得到最宽的安全网")
- **#36 Calqued Syntax:** correct Chinese words in a foreign *sentence structure* ("是最大的失望——一个...的Bug，它..."), or English sentence boundaries preserved where Chinese would merge ("X。Y是Z的。" → "X，Y也Z。")

**Example 4 — 长定语隔断动宾：**

英文 "doesn't reverse the amount already added to base balance" 的语序是动词(reverse)+宾语(amount)+后置定语(already added...)。中文直译时定语前置，变成"不回退[已经加到 base balance 上的]金额"，动词(回退)和宾语(金额)之间插入了一个长定语，读者需要读完整个定语才能找到宾语，被迫回溯理解句意。

English source:
> Opus reasoned cleanly about adds and imports but never noticed that deleteTransaction leaves the account balance untouched. One function short of the full picture.

**Before:**
> 它漏掉的那个余额 Bug：`deleteTransaction` 不回退已经加到 base balance 上的金额。Opus 分析了增加和导入的逻辑，但没有检查删除路径。差一个函数，差一步完整。

**After:**
> Opus 在余额类中漏了一个：`deleteTransaction` 在删除交易时，不会将已计入 base balance 的金额回退。它分析了新增和导入的逻辑，唯独没有覆盖删除，离完整诊断只差一步。

**Changes made:**
- "不回退已经加到 base balance 上的金额"：动词"回退"与宾语"金额"之间隔了 11 个字的定语 → 用"将"字句前置宾语，变成"不会将...的金额回退"，读者先看到对象再看到动作，无需回溯
- "没有检查删除路径"："删除路径"是 "deletion path" 的直译，中文技术写作中不说"路径" → "没有覆盖删除"，用文章自身已建立的术语
- "差一个函数，差一步完整"：重复"差"字的文学对仗，在技术分析中显得刻意（另见 #39 语域错配） → "离完整诊断只差一步"，一句话说清，不追求修辞效果

**筛查方法：** 找出所有"动词+超过 6 个字的定语+宾语"结构，检查读者是否需要读完定语后回头才能理解动词的作用对象。如果需要，用"将/把"字句前置宾语，或将定语拆成独立分句。

**Example 5 — 多操作逗号链（代码分析场景）：**

英文技术写作常用 "X does A, Y does B, and Z does C" 的逗号链一口气串联多个代码操作。中文直译后变成一条超长复句，读者必须同时记住所有操作才能理解末尾的总结。代码分析中尤其常见，因为 Bug 描述往往涉及多个函数的联动。

English source:
> addTransaction mutates the base balance, deleteTransaction never reverses that delta, and getAccountBalances then recomputes a projected balance as balance + sum(transactions) on top of the already-mutated number.

**Before:**
> `addTransaction` 直接修改 base balance，`deleteTransaction` 从不撤销这个改动，而 `getAccountBalances` 又用 `balance + sum(transactions)` 重新计算投影余额，等于在已经改过的数字上又加了一遍。

**After:**
> `addTransaction` 每次新增交易都会直接修改 base balance。`deleteTransaction` 删除交易时却不会把这笔改动撤销。而 `getAccountBalances` 在计算投影余额时，用的是 `balance + sum(transactions)`，相当于在已经改过的数字上又加了一遍。

**Changes made:**
- 一条逗号链拆成三个独立短句，每句只描述一个函数的行为，读者逐句消化，不用同时追踪三层逻辑
- 给每个函数补上动作语境（"每次新增交易""删除交易时""在计算投影余额时"），读者不看代码也知道每个函数在什么场景下被触发
- "而"从句内连接词降级为句首过渡词，承接前两句铺垫引出第三个操作的叠加问题
- "等于"改为"相当于"，更准确——这是类比说明，不是等价判断

**筛查方法：** 搜索包含三个及以上代码标记（反引号对）的句子。如果一句话中出现三个以上 `funcName` 或 `varName`，且用逗号或"而""并""同时"串联，大概率是英文逗号链的直译。拆成独立短句，每句只讲一个操作，用句号断开。

#### 37. Calqued Rhetorical Patterns (英文修辞手法直搬)

**Problem:** Different from #35 (word/phrase level) and #36 (sentence structure level). This pattern operates at the *discourse* level: an English rhetorical device — parallel construction, anaphora, either/or triplets — is mechanically transplanted into Chinese without adapting the device itself. The issue isn't that the Chinese words are wrong, or that any single sentence's structure is English-shaped. It's that the *multi-sentence pattern* was designed for English rhythm and doesn't produce the same effect in Chinese.

**Why it happens:** English "either X or Y" is light — two syllables for the frame, and the construction flows. Chinese "要么X，要么Y" is heavier — four characters of framing per clause, more formal register. Repeating it three times in English builds momentum; repeating it three times in Chinese creates a plodding, mechanical cadence. The same applies to other devices: English anaphora ("We will... We will... We will...") has different weight than Chinese "我们将...我们将...我们将...".

**Before (three "either...or" sentences calqued as three "要么...要么"):**
> 一笔存款要么加到你的目标进度里，要么没有。删掉一笔交易，余额要么正确回退，要么永远错下去。月末预测算了一次房租还是两次，答案不存在"看你怎么理解"。

**After (varied structures, same point):**
> 一笔存款进去，目标进度加了还是没加，一看就知道。删掉一笔交易，余额要么正确回退，要么永远错下去。月末预测算了一次房租还是两次，没有"看你怎么理解"的余地。

**Changes made:**
- First sentence: "要么加了，要么没有" → "加了还是没加，一看就知道"（用中文更自然的"V了还是没V"反问 + 短结论，替代 either/or 模板）
- Second sentence: 保留一次"要么...要么"，单独用没问题
- Third sentence: "答案不存在'X'" → "没有'X'的余地"（更自然的否定方式）
- 三句不再是同一个模板的三次复制，而是三种不同说法表达同一个意思：结果是确定的

**Fix:** When the English source uses a repeated rhetorical device, don't translate the device — translate the *effect*. The effect of three "either...or" sentences is: "every example has a binary, unambiguous answer." Find Chinese-native ways to achieve that effect: vary the sentence structures (反问, 要么...要么, 直接否定), keep at most one instance of any heavy construction, and let rhythm variation do the work that English parallelism does.

**Example 2 — Dramatic Kicker（超短句独立收尾）：**

英文常用一个超短句独立收尾制造节奏冲击，例如 "Eight cents." "Done." "One line."。这在英文中是成立的修辞手法——极短的句子在一段长分析后形成强烈反差。但直接搬到中文里，一个光秃秃的名词短语（"八分钱。"）既缺少谓语，也缺少上下文衔接，读者不知道你在强调什么。

**Before:**
> ...除此之外，它标记的问题全部准确。八分钱。

**After:**
> ...失分仅限于日期这一个类别，其余检出全部准确——整个分析只花了八分钱。

**Changes made:**
- "八分钱。"孤立成句 → 用破折号接入前句，"整个分析只花了八分钱"既保留强调效果，又提供了完整的语境（什么只花了八分钱）
- 中文的强调不靠句子短，靠的是信息落差：先铺"全部准确"的正面结论，再用破折号引出出人意料的低价格

**筛查方法：** 检查段落末尾是否有不超过四个字的独立短句。如果这个短句是名词短语（没有动词），且去掉它上文仍然完整，大概率是英文 dramatic kicker 的直搬。将其融入前一句，用破折号或逗号衔接，补充必要的谓语和语境。

**Difference from #35 and #36:**
- **#35 Calqued Metaphors:** one foreign *expression* translated literally
- **#36 Calqued Syntax:** one sentence with a foreign *skeleton*
- **#37 Calqued Rhetoric:** a *multi-sentence pattern* transplanted without adapting the device to the target language's rhythm

#### 38. Sentence-for-Sentence Translation Trap (逐句对译)

**Problem:** LLMs produce Chinese prose that mirrors English paragraph structure: the same number of examples, the same level of explicitness, the same framing paragraphs. This happens both when working from English source material and when generating "original" Chinese text — the model's internal reasoning follows English-like structure, then surfaces in Chinese with that structure intact. A Chinese writer making the same argument might use one idiom where the LLM used three examples, or cut an entire framing paragraph because the point is already obvious from context.

**Key insight:** The issue isn't just word choice or syntax — it's structural. When a Chinese text uses the same number of examples, the same paragraph organization, and the same level of explicitness as an English text would, the writing sounds machine-generated even if no English source exists. The fix is sometimes radical compression: extract the core point, find the most natural Chinese way to say it, and drop everything the LLM used to *build toward* that point.

**Before (three English examples mechanically translated, plus a framing paragraph):**

English source:
> A contribution either adds to your goal or it doesn't. A deleted transaction either reverses its effect on your balance or it leaves the balance wrong forever. A forecast counts your rent once or it counts it twice. There's no design-judgment gray area for a weak review to hide behind.
>
> So this was less a test of whether a model can spot a missing semicolon and more a test of whether it can track state that mutates in three different places and stay consistent about it.

Mechanical translation:
> 往储蓄目标存一笔钱，进度涨了没涨，一看就知道。删掉一笔交易，余额要么正确回退，要么永远错下去。月末预测算了一次房租还是两次，没有"看你怎么理解"的余地。
>
> 这测的不是能不能找到少了个分号，而是一个状态在三个地方都会变，模型能不能跟住，前后还对得上。

**After (one Chinese idiom replaces three examples + framing paragraph):**
> 钱的计算对于准确性要求极高，对就是对，错就是错，没有任何可转圜的余地。

**Why the compressed version is better:**
- "对就是对，错就是错" 是地道的中文表达，六个字说清了英文三句 either/or 的全部含义
- "没有任何可转圜的余地" 用的是中文现成的说法，比 "没有灰色地带"（calqued from "no gray area"）更自然
- 三个具体例子（存款、删除交易、月末预测）在紧接着的 Bug 分类表里已经全部覆盖，上面再铺一遍是冗余的
- 删掉 "这测的不是找分号" 那段也不损失信息，因为 Bug 表本身就说明了测试的难度层级

**Fix:** 翻译完一段后问自己："这些句子在原文里是为了证明什么？" 找到那个核心论点，然后看中文里有没有一句话就能说透的表达。如果有，用它替换整段，把原文的具体例子留给后文更合适的位置。不是每一句英文都需要在中文里有一个对应句。

**Difference from #37:**
- **#37 Calqued Rhetoric:** the English rhetorical *device* is transplanted (three either/or → three 要么...要么). Fix: vary the structures.
- **#38 Sentence-for-Sentence Trap:** the English *structure* (number of examples, paragraph organization) is preserved wholesale. Fix: compress to the core point using Chinese-native idiom, let downstream content carry the specifics.

#### 39. Register-Mismatched Idioms (语域错配的成语/熟语)

**Problem:** Different from #35 (foreign idioms calqued into Chinese). This pattern uses *native* Chinese idioms whose source domain (military, sports, literary drama) or connotation (negative, humorous) clashes with the neutral-professional register of tech writing. The AI reaches for vivid idioms to avoid sounding flat, but overshoots into dramatic territory. Each idiom is grammatically correct and semantically close — the problem is purely register.

**Common categories:**

| 语域 | 错配示例 | 问题 | 替换 |
|------|---------|------|------|
| 军事 | 全军覆没、溃不成军、兵败如山倒 | 描述数据表现用歼灭级隐喻，力度远超语境 | 几乎没有命中、表现不佳 |
| 体育赛事 | 全场零检出、完胜、碾压、吊打 | 赛事解说语气，不适合技术分析 | 五个模型均未检出、明显优于 |
| 负面揭露 | 暴露无遗、原形毕露 | 暗示有意隐瞒被揭穿，用于中性呈现时语义错位 | 一目了然、清晰可见 |
| 文学夸张 | 可歌可泣、惊天动地、叹为观止 | 文学抒情语气，技术文章中显得不严肃 | 用具体数据或事实说明 |
| 文学对仗 | 差一个X，差一步Y；少一分X，多一分Y | 重复字的对仗结构追求修辞效果，技术文章中显得刻意 | 合并为一句直接陈述（"离完整诊断只差一步"） |

**Before:**
> 各模型的性格在这张表里暴露无遗。Opus 和 Sonnet 包揽了日期 Bug，其他模型几乎全军覆没。预测类 Bug 全场零检出。

**After:**
> 各模型的强项和盲区在这张表里一目了然。Opus 和 Sonnet 包揽了全部日期 Bug，其他模型在这一类别上几乎没有命中。预测类 Bug 五个模型均未检出。

**Why the originals are wrong:**
- "暴露无遗"：语义预设是"本来藏着，现在被揭穿"，但表格只是在呈现数据，没有揭露任何隐瞒
- "全军覆没"：全歼级军事隐喻，用来说"3 个日期 Bug 只命中了 0-1 个"力度严重过载
- "全场零检出"："全场"是体育解说的时间框架词（上半场/全场），技术文章中没有"场次"的概念

**Fix:** 对每个成语/熟语问两个问题：① 它的源域（军事、体育、文学、法律...）和当前语境是否匹配？② 它的情感预设（负面揭露、褒义赞叹、中性陈述）和你要表达的意思是否一致？如果任一不匹配，换成同义但语域中性的表述。技术文章中，用文章自身已建立的术语体系（"命中""检出"）比借用外部隐喻更精确。

**Difference from other patterns:**
- **#35 Calqued Metaphors:** foreign idiom translated into Chinese ("buys the widest net" → "买得到最宽的安全网")
- **#39 Register-Mismatched Idioms:** native Chinese idiom used in the wrong register ("全军覆没" in a data table description)
- Both result in unnatural writing, but for opposite reasons: #35 imports expressions that don't exist in Chinese; #39 uses expressions that exist but belong to a different domain

#### 40. Flat Enumeration Dump (顿号清单堆砌)

**Problem:** When the source material lists multiple items (bugs found, features supported, tools used), the AI mechanically translates each item name and strings them together with 顿号（、）, producing a long flat list that reads like a database query result rather than prose. Human writers group items by category, summarize with a count, or pick representative examples — they don't dump raw lists into running text.

**How it manifests:**
- 6+ proper nouns or technical terms connected by 顿号 in a single sentence
- Items from different categories mixed into one flat list without grouping
- The list exists to show *breadth* but forces readers to parse each item individually
- Redundancy: items already visible in a nearby table are re-enumerated in prose

**Before:**
> 除此之外，Grok 还命中了两个 React Bug、目标反转、过时搜索缓存、CSV 解析、子字符串月份匹配和 JSON 崩溃，而且它在 CSV 那条上不只是指出 `split(',')` 有问题，还给出了正确的修复方案。

**After:**
> 余额之外，Grok 对 React 模式、数据解析、数值计算三个类别也都有覆盖，总计另外命中了六个 Bug。其中 CSV 那条值得单独说：它不只是指出 `split(',')` 有问题，还给出了正确的修复方案。

**Changes made:**
- 六个具体 Bug 名称 → 归纳为三个类别 + 总数，读者已有分类表做参照，正文不需要重复每个名字
- 长句拆成两句：第一句说覆盖面，第二句聚焦值得展开的单项细节
- "除此之外...而且"的长链式连接 → 两个独立短句，各自承载一个信息点

**Fix:** 当列表的目的是展示覆盖面（"它找到了很多"）而不是精确引用（"具体是这几个"），用以下策略替代逐项枚举：
1. **按类别归纳：** "对 X、Y、Z 三个类别都有覆盖"
2. **总数概括：** "总计命中了 N 个"
3. **代表性举例：** "包括 A 和 B 等"
4. **指向已有表格：** 如果上文已有详细表格，正文只需点出结论性数字

只有在每个具体名称都对论证有用时（例如逐项对比两个模型的差异），才逐一列出。如果列表可以替换为"N 个 Bug"而不损失论点，说明逐项枚举是冗余的。

**筛查方法：** 找出句中包含三个以上顿号分隔项的位置。问两个问题：① 读者需要记住每个具体名称才能理解后文吗？② 这些信息是否已经在附近的表格中呈现过？如果任一答案为否/是，改为归纳式表述。

---

#### 41. Vague Pronoun in Comparison (比较句中的模糊指代)

**Problem:** When comparing multiple items and then making a claim about one of them, the AI uses vague references like "其中一个" (one of them), "the other one", "another model" instead of naming the subject directly. In English this sometimes works because the sentence structure makes the referent guessable. In Chinese, "其中一个" forces the reader to pause and figure out which one is being discussed — especially when the comparison involves cost or performance, and the whole point is to highlight *which specific item* stands out.

**How it manifests:**
- "A 和 B 都做到了X，其中一个只花了Y" — reader doesn't know if A or B is cheap
- "两个模型解出了这道题，另一个的表现更稳定" — which one?
- "Three models caught this bug, and one of them did it for pennies" — in a comparison context, name it

**Before:**
> 只有 Grok 和 GPT-5.5 完整拆解了余额矛盾，其中一个只花了八分钱。

**After:**
> 只有 Grok 和 GPT-5.5 完整拆解了余额矛盾，而 Grok 做到这件事只花了八分钱。

**Why the original is wrong:**
- 读者需要回忆前文或查表才能判断"其中一个"是 Grok 还是 GPT-5.5
- 这句话的重点恰恰是"谁更便宜"，用模糊指代把关键信息藏起来了
- 英文 "and one of them costs eight cents" 在上下文中可以靠价格信息反推（读者知道 Grok 便宜），但中文读者未必有这个前置知识

**Fix:** 在比较句中，如果后半句的目的是突出某个对象的特征（价格、速度、准确率），直接点名。"其中一个"只适合用在指代对象不重要的场景（"其中一个已经停止维护了"——具体是哪个不影响论点）。当指代对象本身就是信息的重点时，必须点名。

**筛查方法：** 搜索"其中一个""另一个""有一个"等模糊指代词，检查：① 上文是否在做两个或多个对象的对比；② 后半句的信息是否旨在突出某个对象的差异化特征。如果两者都是，替换为具体名称。

#### 42. Mechanical Negation Chains (连续否定句式堆叠)

**Problem:** When describing something's weaknesses or misses, the AI produces a sequence of structurally identical negation sentences: "没有识别出X。Y也完全没有发现。失分仅限于Z。" Each sentence is a standalone negative statement with the same rhythm (subject + 没有/不 + verb + object). This reads like a checklist of failures being ticked off, not a human explaining what went wrong. Human writers vary the negation structure, add causal connectors, and use contrast to keep the flow natural.

**How it manifests:**
- Two or more consecutive sentences using "没有V" / "也没有V" / "完全没有V"
- Parallel negative structures with no variation in how the negation is framed
- Missing logical connectors between negations (why did it miss? what did it focus on instead?)
- A summarizing sentence ("失分仅限于X") that reads like a report conclusion rather than flowing prose

**Before:**
> 它注意到了 `getUpcomingRecurring`，但标记的是伪造 `-next` ID 泄漏到下游，没有识别出零索引月份偏移。`monthKey` 的时区漂移也完全没有发现。失分仅限于日期这一个类别。

**After:**
> 它看到了 `getUpcomingRecurring` 有问题，但关注点落在了伪造的 `-next` ID 会泄漏到下游，真正的零索引月份偏移反而没有认出来。`monthKey` 的时区漂移则完全不在它的雷达上。不过丢分也就限于日期这一个类别。

**Changes made:**
- "但标记的是...没有识别出" → "但关注点落在了...真正的X反而没有认出来"：补充了因果（它不是没看，是判断偏了），用"反而"做转折比裸"没有"更有层次
- "也完全没有发现" → "则完全不在它的雷达上"：换一种否定方式，避免连续两句"没有X"的重复句式
- "失分仅限于" → "不过丢分也就限于"：用"不过"做语气转折，让结论句和前面的负面描述之间有情绪过渡，而不是生硬地总结

**Fix:** 当连续描述两个以上的缺陷或遗漏时，使用以下策略打破否定句式的重复：
1. **补因果：** 不只说"没有发现X"，还说明它把注意力放在了哪里（"关注点落在了Y，X反而没有认出来"）
2. **换否定形式：** "没有发现" → "不在雷达上" / "完全略过" / "从头到尾没有触及"，避免连续使用同一个"没有+动词"结构
3. **加转折词：** 在总结句前用"不过""但""话说回来"等过渡词，让负面描述到结论之间有情绪转换
4. **用对比代替纯否定：** "它抓到了A但漏掉了B"比"它没有发现B"更有信息量

**筛查方法：** 搜索连续出现的"没有""也没""完全没""未能"等否定词。如果相邻两句以上使用结构相同的否定句式（主语+没有+动词+宾语），需要变换其中至少一句的表达方式：补因果、换否定形式、或改为对比句。

---

#### 43. Compressed Technical Explanation (技术细节压缩过度)

**Problem:** When the source material explains a technical cause-and-effect chain, the AI compresses it into one dense sentence (often with parenthetical asides), assuming the reader can unpack the logic themselves. The result reads like a commit message or code comment rather than prose meant for a human reading linearly. Key issues: ① jargon-heavy noun phrases that need unpacking appear without context ("静默返回 600 个月上限"); ② the causal chain (symptom → root cause → consequence) is crammed into one sentence or a parenthetical instead of being laid out step by step; ③ evaluative conclusions ("这是症状不是原因") appear before the reader understands what's being evaluated.

**How it manifests:**
- Parenthetical asides containing the actual explanation: "这是X不是Y（因为A传入B，但C期望D，导致E）"
- Technical behavior described without context: "静默返回 600 个月上限" — reader doesn't know what "600 个月" means in this context
- Conclusion before explanation: "这是症状不是原因" appears before the reader understands what the symptom or cause is
- Multiple causal steps compressed into one clause with 、and 导致

**Before:**
> Sonnet 标记了 `estimateDebtPayoffMonths` 在还款低于月利息时静默返回 600 个月上限。这是症状不是原因（UI 传入的是百分比值 19.99，但函数期望的是小数 0.1999，月利息直接膨胀到任何还款都压不下去），但 Sonnet 至少触及了症状，虽然没有追到根因。比其他四个都近一步。

**After:**
> Sonnet 发现 `estimateDebtPayoffMonths` 有一条兜底逻辑：当月还款额不够覆盖利息时，函数直接返回 600 个月（即上限值），不做任何提示。Sonnet 认为这是个问题并标记了出来。但它只看到了表象——真正的根因是 UI 把 APR 以百分比形式（19.99）传入，而函数期望的是小数（0.1999），导致月利息被放大了一百倍，几乎任何还款额都会触发这条兜底。Sonnet 没有追到这一层，不过已经比其他四个模型都近了一步。

**Changes made:**
- "静默返回 600 个月上限"拆开：先说有兜底逻辑，再说触发条件和具体行为，读者不用猜"600 个月"是什么
- 括号里的因果链提取为独立句子，按"表象 → 根因 → 后果"顺序铺开
- "这是症状不是原因"换成"它只看到了表象——真正的根因是"，先让读者理解完表象再引入根因
- "虽然没有追到根因。比其他四个都近一步"合并为一句完整的评价

**Fix:** 技术因果链的写作原则是"一步一句"：
1. **先给上下文：** 描述技术行为前，先用一句话说明这段代码的职责或场景（"有一条兜底逻辑"）
2. **再说具体行为：** 触发条件是什么、做了什么、结果是什么，各占一个分句
3. **因果链拆开：** 如果存在"表象→根因→后果"的多层关系，每层独立成句，不要塞进括号
4. **评价放在最后：** "这是症状不是原因"类的判断句必须出现在读者已经理解了症状和原因之后，不能先下结论再补充解释

**筛查方法：** ① 搜索包含技术术语的长括号注释（超过 15 字的括号内容），检查是否应该提取为独立句子；② 找出"这是X不是Y"类判断句，检查上文是否已经让读者理解了X和Y分别指什么；③ 找出描述代码行为的句子，检查读者是否需要先知道某个前置背景才能理解该行为——如果需要，补上一句上下文。

#### 44. Abstract Mismatch Claim (抽象失配判断)

**Problem:** When expressing that something disappoints expectations, the AI uses an abstract "mismatch" statement ("和X对不上""与预期不符") without specifying the two concrete endpoints being compared. The reader has to infer: what was expected? what was the actual result? in which direction is it bad? Human writers make the gap concrete — they name the price AND the result, letting the reader feel the contrast directly.

**How it manifests:**
- "和价格对不上" — reader doesn't know if the price is too high or the result too low, or what the comparison anchor is
- "与其定位不匹配" — what positioning? what result contradicts it?
- "性价比不高" — compared to what? by how much?
- "表现低于预期" — whose expectation? what was expected?

**Before:**
> Gemini 的结果我反复看了好几遍，因为和价格对不上。

**After:**
> Gemini 的结果我反复看了好几遍，花了 Grok 四倍多的钱，检出率却只有它的零头。

**Why the original is wrong:**
- "对不上"需要两个对等的参照物，但"结果"和"价格"不在同一维度上，读者要自己补全"花了多少→得到多少→所以不合理"的推理链
- 抽象判断传递的是作者的情绪（失望），不是让读者自己形成判断的事实
- 用具体数字对比（四倍价格 vs 零头检出率），读者直接感受落差，不需要脑补

**Fix:** 当要表达"A 不配 B"或"A 和 B 对不上"时，把抽象判断替换为具体的两端对比：
1. **量化双方：** 给出具体的数字或比例（"四倍的钱""零头的检出率"）
2. **指明方向：** 让读者知道是"贵但差"还是"便宜但好"
3. **提供参照物：** 不要孤立评价，要和另一个具体对象比（"花了 Grok 四倍多的钱"比"价格不低"有信息量）

**筛查方法：** 搜索"对不上""不匹配""不符""不高""低于预期"等抽象失配表达，检查：① 句中是否同时出现了具体的两端数据？② 读者能否不看上下文就理解"哪里对不上"？如果缺少具体数据或方向不明，用量化对比替换。

#### 45. Self-Contradicting Absolute + Logical Incoherence (绝对化表述与上下文矛盾)

**Problem:** Two related issues that often co-occur: ① The AI uses absolute negation ("没有去看""完全没有") when the context has already established a partial positive ("只抓到两个"), creating a logical contradiction. ② Technical descriptions are calqued from English in ways that don't parse naturally in Chinese ("把所有依赖钉在 latest" ← "pinning everything to latest"). The reader notices the contradiction and the awkward phrasing together, making the paragraph feel unpolished.

**How it manifests:**
- Paragraph says "它抓到了X" then later says "没有去看Y"，where Y includes things similar to X — readers ask "so did it look or not?"
- Absolute negation ("没有去看""完全忽略") when the reality is partial ("looked but didn't go deep enough")
- English technical idioms calqued: "钉在 latest" (pin to latest), "锁定在 main" (lock to main), "指向 HEAD" (point to HEAD) where Chinese would phrase differently

**Before:**
> 它只抓到两个植入 Bug：useEffect 依赖数组和 CSV 转义。输出也是五个模型里最短的，而且把一部分篇幅花在了非植入发现上（表单默认日期的时区问题、package.json 把所有依赖钉在 latest），没有去看摆在明面上的植入 Bug。

**After:**
> 它只抓到两个植入 Bug：useEffect 依赖数组和 CSV 转义。输出也是五个模型里最短的，而且有限的篇幅里还分了一部分给非植入问题（表单默认日期的时区、依赖版本全写 `latest` 没有锁定），真正该深挖的植入 Bug 反而只触及了表层。

**Changes made:**
- "package.json 把所有依赖钉在 latest" → "依赖版本全写 `latest` 没有锁定"：用中文技术写作的自然表述替代英文 "pinning to latest" 的直译
- "没有去看摆在明面上的植入 Bug" → "真正该深挖的植入 Bug 反而只触及了表层"：不再和前面"抓到两个"矛盾，语义从"完全没看"修正为"精力分配失当、没有深入"

**Fix:** 两个问题分别处理：

**逻辑一致性：**
1. 写完一段后回读，检查"绝对否定"是否和同段的"部分肯定"矛盾
2. 如果实际情况是"做了一点但不够"，用程度化表述（"只触及表层""没有深入""覆盖不足"）替代绝对否定（"没有去看""完全忽略"）
3. 对比前后文的主语行为：如果前句说"它抓到了X"，后句不能说"它没看"，只能说"没有再深入"或"剩下的没有覆盖"

**技术术语本地化：**
1. 遇到英文技术动词（pin, lock, point, wire up, hook into）不要逐词翻译，找中文技术社区的常见说法
2. "钉在/锁在/挂在"这类动词+方位词组合如果在中文技术文章中不常见，换用描述性表达（"全写 latest 没有锁定版本"）

**筛查方法：** ① 搜索同一段落中的绝对否定词（"没有""完全""从未"），对照前文是否有部分肯定的描述，存在矛盾时改为程度化表述；② 搜索"钉在""锁在""挂在""指向"等动词+方位词组合，检查是否为英文 phrasal verb 的直译。

---

#### 46. Anaphoric Stacking for Emphasis (排比堆砌制造强调)

**Problem:** The AI transplants English rhetorical emphasis patterns — especially the "X did it. Y did it. Z did it. But W didn't." anaphoric stack — directly into Chinese. In English, short repeated sentences with the same structure build dramatic tension ("Grok caught it. Opus caught it. Sonnet caught it."). In Chinese, this reads like一条一条在念名单, mechanical rather than dramatic. Combined with a sarcastic kicker ("名字里带 Pro 的模型视而不见"), the whole paragraph feels like translated copywriting rather than technical analysis.

**How it manifests:**
- Three or more short sentences with identical structure (subject + 同一个动词) stacked for emphasis
- A sarcastic/ironic "punchline" sentence at the end that relies on the stack for its punch
- Register mismatch: literary/emotional expressions ("耿耿于怀""视而不见") in technical evaluation context
- The point could be stated in one sentence but is stretched across five for dramatic effect

**Before:**
> 让我耿耿于怀的是储蓄目标那个 Bug。handler 标着"Add contribution"然后做了减法，每次存钱进度都往后退。Grok 抓到了，Opus 抓到了，Sonnet 和 GPT-5.5 抓到了。一个八分钱的 Grok 运行抓到了。名字里带 Pro 的模型对一个反转核心功能的 Bug 视而不见。

**After:**
> 最让我想不通的是储蓄目标那个 Bug。逻辑很简单：handler 名字叫"Add contribution"，里面却在做减法，用户每存一笔钱进度反而倒退。这个 Bug 其他四个模型全部抓到了，八分钱的 Grok 也抓到了，唯独 Gemini 没有反应。

**Changes made:**
- "让我耿耿于怀" → "最让我想不通"：语域从文学抒情调整为技术博客的专业口语
- "handler 标着...然后做了减法" → 先用"逻辑很简单"给读者预期，再具体说明，降低认知负荷
- 四句排比堆砌（"Grok 抓到了。Opus 抓到了。..."）→ 一句概括"其他四个模型全部抓到了"，再单独提 Grok 价格做反差
- "名字里带 Pro 的模型对...视而不见" → "唯独 Gemini 没有反应"：去掉讽刺修辞，让事实本身说话

**Fix:**
1. **概括代替逐一列举：** 当多个主体做了同一件事，用"全部/都/其他N个"一句概括，不要逐个点名重复同一个动词
2. **保留一个反差点：** 如果要突出某个对比（八分钱的 Grok 也能做到），单独提它就够了，不需要先铺垫所有其他模型
3. **让事实制造讽刺：** "唯独 Gemini 没有反应"比"名字里带 Pro 的模型视而不见"更有力——前者是读者自己得出的结论，后者是作者在替读者下判断
4. **给技术细节加引导：** 描述 Bug 具体表现前，加一句"逻辑很简单"或"问题很直观"，让读者知道接下来的内容不需要费力理解

**筛查方法：** ① 找出连续三句以上使用相同动词（"抓到了""发现了""命中了"）的排比结构，合并为一句概括 + 一个反差点；② 搜索文学/情感色彩的四字词（"耿耿于怀""视而不见""不可思议"），检查是否可以换为更克制的技术评测表达；③ 检查段落末尾的"讽刺 kicker"，如果去掉讽刺、只陈述事实后效果更强，就去掉。

#### 47. Skeletal Recommendation (骨感推荐句)

**Problem:** When writing a conclusion or recommendation, the AI produces a telegraphic sentence: imperative verb + product name, followed by comma-separated bare phrases as justification ("它找到最多，跨文件推理，也是唯一X的"). This mirrors English bullet-point summary style ("Pick Opus. It found the most, reasons across files, and is the only one to verify test data.") which works in English because the language tolerates subject-less fragments. In Chinese, this reads like a product spec sheet or slide deck bullet point — not prose a reader would naturally follow.

**How it manifests:**
- Imperative opening with no scene-setting: "选X" / "用Y" as a standalone sentence
- Comma-separated bare phrases as justification without complete sentence structure: "它找到最多，跨文件推理，也是唯一..."
- Calqued noun phrases as conditions: "正确性敏感的变更" (← "correctness-sensitive changes")
- The recommendation lacks context (when? why? compared to what?) that would make it actionable

**Before:**
> 如果要在正确性敏感的变更上做最后一道把关，选 Opus 4.8。它找到最多，跨文件推理，也是唯一主动去验证测试数据的。

**After:**
> 如果你的变更对正确性要求高、上线前需要一道最严格的审查，Opus 4.8 是当前最稳的选择。覆盖面最广，能跨文件追踪状态联动，而且是五个模型里唯一会自己打开测试文件验算数字的。

**Changes made:**
- "正确性敏感的变更"（calqued noun phrase）→ "你的变更对正确性要求高"：改为动词谓语句，给出具体场景（"上线前"）
- "选 Opus 4.8"光秃秃的祈使句 → "Opus 4.8 是当前最稳的选择"：补上判断语气，不是在命令读者
- "它找到最多，跨文件推理"两个断裂短语 → 展开为完整分句，补上具体内容（"能跨文件追踪状态联动"）
- "唯一主动去验证测试数据的" → "唯一会自己打开测试文件验算数字的"：用具体动作（打开文件、验算）替代抽象概括（验证数据），读者能想象这个画面

**Fix:** 推荐/结论段落的写作原则：
1. **场景先行：** 不要直接说"选X"，先用一句话描述适用场景（"如果你的变更对正确性要求高"），让读者判断是否适用于自己
2. **判断而非命令：** "X是当前最稳的选择"比"选X"更有说服力——前者是你的评估，后者是未经论证的指令
3. **展开理由为完整分句：** 每条理由应该是读者不看上文也能理解的独立陈述，不是逗号分隔的关键词碎片
4. **用具体动作替代抽象概括：** "会自己打开测试文件验算数字"比"主动验证测试数据"有画面感，读者能想象模型在做什么

**筛查方法：** ① 找出以"选/用/推荐"开头的祈使句，检查前面是否有场景描述；② 找出逗号连接三个以上无主语短语的句子（"它X，Y，也Z"），展开为各自完整的分句；③ 检查推荐理由中的动词是否具体——如果全是"推理""覆盖""验证"这类抽象词，尝试还原为具体的动作描述。

#### 48. Instructional Tone Leak (说明书语气入侵)

**Problem:** 分析性文章中突然插入一句操作指令式的表达（"还需要你拿自己的X来Y一下"），读起来像用户手册或产品文档，打断了正在进行的评述节奏。英文技术写作常用祈使句做轻量级提醒（"Verify it against your own data before trusting it"），直译成中文后"还需要你+动词+具体操作对象"会产生说明书感，因为中文祈使句在非教程语境中比英文更突兀。

**How it manifests:**
- "你需要/还需要你+拿/用/打开+具体对象+动词一下"结构出现在分析段落中间
- 本意是"这个结论需要验证"，但写成了"你要执行以下操作来验证"
- 操作对象被过度具体化（"拿自己的样本数据核实"），而语境只需要表达"不确定"
- 与前后的叙述/评价语气形成断裂

**Before:**
> 它报告说期望值差了整整 200，所以 npm run test 会失败。这不是我们植入的 Bug，具体数字还需要你拿自己的样本数据核实一下，但这种"自己去验证数字"的本能，通常只有亲自 review 的人类才有。

**After:**
> 它报告说期望值差了整整 200，所以 npm run test 会失败。这不是我们植入的 Bug，具体数字准不准还得你自己验，但这种主动验算的本能，通常只有亲自 review 的人类才有。

**Changes made:**
- "具体数字还需要你拿自己的样本数据核实一下" → "具体数字准不准还得你自己验"：从指令式（"需要你+操作"）变为陈述式（"准不准+还得+验"），语气从说明书回到评述
- 去掉了过度具体的操作对象（"拿自己的样本数据"）——读者不需要被告知验证的具体步骤，他们只需要知道"这个数字不保证准确"
- "这种'自己去验证数字'的本能" → "这种主动验算的本能"：前半句已经用了"验"，引号内再重复"验证数字"是冗余

**Fix:** 当你想在分析段落中表达"某个结论有待验证"时，区分两种写法：
1. **陈述不确定性（适合分析文章）：** "准不准还得验""具体数字尚未核实""这个结论还需要确认"——主语是事实本身，读者自行判断是否去验
2. **给出操作指令（适合教程/文档）：** "你需要拿X来验证Y""请用自己的数据核实一下"——主语是读者，明确告诉他做什么

分析性文章中用第 2 种会产生语域断裂。除非文章本身就是教程，否则用第 1 种。

**筛查方法：** 搜索"还需要你""你需要""请用/请拿"等指令性结构，检查所在段落是分析/评述还是教程/指南。如果是前者，改为陈述不确定性的方式，让读者自己决定是否去验证。

#### 49. Formulaic Causation Template (套路化因果句式)

**Problem:** 用"这足以让你+动词"或"这应该让你+动词"把一个事实和读者应有的反应机械连接起来。这是 "X should change how much you Y" / "this is enough to make you Z" 的直译模板。问题不在于因果关系本身，而在于这个句式把因果包装成一个从事实到读者心理反应的"充分条件"，读起来像逻辑推导而非自然评述。人类写作中，评价和事实融合在一起，不会先摆事实再用"这足以"做推论跳板。

**How it manifests:**
- "这足以让你重新X一下Y" / "这应该让你对X产生Y"
- "这足够说明/证明..."
- 事实陈述 + "这足以/这应该/这意味着你需要" + 读者应有的反应
- 英文源头通常是 "X should change how much you trust Y" / "this is enough to make you reconsider"

**Before:**
> 一个八分钱的模型都能抓到的功能反转 Bug 它没看见，这足以让你重新掂量一下单模型审查到底靠不靠谱。

**After:**
> 八分钱的模型都能抓到的功能反转 Bug 它直接略过——单模型审查能信几分，到这里得打个问号。

**Changes made:**
- "这足以让你重新掂量一下X到底Y" → "X能信几分，到这里得打个问号"：去掉"这足以让你"的推论跳板，把结论直接说出来
- "它没看见" → "它直接略过"：更有动作感，暗示不是看漏了而是没有深入
- 用破折号连接事实和评价，让两者融为一体，而不是"事实。因此你应该..."的两步结构

**Why the template feels mechanical:**
- 它假设读者不会自己判断，需要作者明确指出"到什么程度足以让你改变看法"
- 它把主观评价伪装成逻辑推导（"这足以"暗示充分条件），但实际上"够不够"完全取决于读者自己的标准
- 人类作者会把评价融进事实描述中（"它直接略过"本身已经在表达态度），不需要额外加一句"所以你应该..."

**Fix:** 当你想表达"某个事实应该改变读者对X的看法"时：
1. **把评价融进事实描述：** 用动词选择（"直接略过"vs"没看见"）和修饰词（"连...都"）在描述事实时就传递态度
2. **直接陈述结论：** "单模型审查能信几分，到这里得打个问号"——这是作者的判断，不是逻辑推导
3. **避免"这足以/这应该"跳板：** 如果去掉"这足以让你"后句子仍然成立，说明这个跳板本来就是多余的

**筛查方法：** 搜索"这足以""这应该让你""这足够""这意味着你需要"等因果跳板结构。检查：① 去掉这个跳板后，结论是否仍然清晰？如果是，直接删掉跳板，让事实和结论用破折号或逗号自然衔接；② 读者是否真的需要被告知"到什么程度足以改变看法"？如果事实本身已经足够震撼（"八分钱的模型都能抓到"），不需要再加一层"这足以让你..."。

#### 50. Back-to-Back Label-Colon Structure (标签冒号结构背靠背)

**Problem:** 结论或总结段落中，连续使用"标签：内容"的结构（"X是：...。Y是：..."），读起来像提纲或 PPT 要点而非文章收尾。英文中 "The conclusion is: ... The twist is: ..." 因为冒号轻量（一个标点）而尚可接受，但中文的"X是："结构更重——它先宣告一个类别标签，再填充内容，读者要经历两次"预告→交付"的认知循环，节奏显得机械。

**How it manifests:**
- 同一段落中出现两个及以上"名词/短语+是/为：+内容"结构
- 常见于结论段："核心结论是：...。新发现是：...。启示是：..."
- 每个"标签："都在预告接下来的内容，但正文不是演讲，不需要为每个论点打标题卡
- 源头通常是英文 "The X is: ... The Y is: ..." 或 "What changed is: ... What stayed is: ..."

**Before:**
> 核心结论没有变：单个模型是筛子不是判决书，最佳策略仍然是两个互补模型，或者一个前沿模型加一个仔细的人工过审。这次测试新增的发现是："前沿"和"在最难的 Bug 上表现最好"不是同一件事。那些需要真正领域理解的 Bug，目前为止还是得依靠人类。

**After:**
> 单个模型是筛子不是判决书，两个互补模型或前沿模型加人工过审，仍然是最稳的策略——这和上次的结论一样。不同的是："前沿"和"在最难的 Bug 上最强"不是一回事。需要真正领域理解的 Bug，目前为止还是得靠人。

**Changes made:**
- "核心结论没有变：" 标签删除，直接以结论本身开头，用"——这和上次的结论一样"在句尾轻轻收住旧知
- "这次测试新增的发现是：" → "不同的是："——从 7 字标签缩减为 4 字转折词，重量大幅降低
- 两处"标签：内容"的重复节奏被打破：第一个结论融入正文流，第二个用短转折词引入
- "依靠人类" → "靠人"：结尾更利落

**Why back-to-back labels feel mechanical:**
- 每个"标签："都在暗示"我要告诉你一个归类好的要点了"——一次可以，连续两次读者会觉得在看幻灯片
- 标签把内容预先框定了性质（"这是结论""这是发现"），剥夺了读者自行感受论点分量的机会
- 正文的力量在于内容本身的说服力，不在于你给它贴了什么标签

**Fix:**
1. **第一个结论直接说：** 不要用"核心结论是："开头——如果内容本身就是结论，读者能认出来，不需要标签
2. **用句尾附注代替句首标签：** "——这和上次一样""——这没变"放在结论之后，比"核心结论没有变："放在结论之前更轻
3. **转折词代替第二个标签：** "不同的是""但这次""变的地方在于"——短转折词（≤5字）比完整标签句（"这次测试新增的发现是"）更不打断流
4. **同段最多一个冒号引导：** 如果已经用了一次"X：内容"结构，第二个论点必须换别的方式引入

**筛查方法：** 检查结论/总结段落中冒号（：）的数量。如果同一段出现两个及以上"标签：内容"结构（"X是/为/在于：...。Y是/为/在于：..."），将第一个标签删除或移到句尾做附注，第二个替换为短转折词。

#### 51. Ratio Arithmetic Error (比值不等式方向错误)

**Problem:** When comparing two numbers using inequality language ("不到X的十分之一""超过Y的三倍"), the AI picks a round fraction (1/10, 3x, half) for rhetorical impact without verifying the arithmetic. "不到十分之一" is a strict inequality claim (< 10%), not a rough estimate. If the actual ratio is 1/9 (11.1%, which is MORE than 10%), the inequality is reversed and the statement is factually wrong.

**How it manifests:**
- "不到X的十分之一" when the actual ratio is 1/9 (11.1% > 10%)
- "超过三倍" when the actual multiplier is 2.8x
- Round fractions chosen for rhetorical punch (1/10 sounds more impressive than 1/9) without checking direction
- The direction error is invisible in casual reading because the intended message ("it's much cheaper") is correct even when the specific claim is wrong

**Before:**
> 以不到 Opus 十分之一的价格追平了 Sonnet

($0.08 ÷ $0.72 = 11.1%，大于 10%，"不到十分之一"方向错误)

**After:**
> 以约 Opus 十分之一的价格追平了 Sonnet

("约"替代"不到"，11.1% ≈ 10% 作为近似值成立)

**Fix:** 使用不等式措辞（不到、超过、至少、不足）时，必须验证不等式方向：
1. **算出实际比值：** $0.08 ÷ $0.72 = 0.111
2. **检查不等式方向：** 0.111 > 0.1，所以"不到十分之一"（< 0.1）是错的
3. **选择正确措辞：** 用"约"替代"不到"，或选一个方向正确的分数（"不到八分之一"，因为 0.111 < 0.125 = 1/8）

**筛查方法：** 搜索"不到""不足""超过""至少""多于""少于"等不等式关键词，对每个命中项用计算器验证方向。重点检查分母为整十整百的圆整分数（十分之一、百分之一、三分之一），因为这些最容易被选中用于修辞效果而非精确表达。

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

## Reference

This part is based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.
