# Part 3: Self-Check Process

After writing, run this checklist before delivering:

## Writing Quality Check

| Check | Method |
|-------|--------|
| Main theme | 用一句话概括全文。如果概括不出来，或者有段落和这句话无关，说明主线不清晰或有跑题段落。 |
| Opening hook | 读开头前三句。是否提供了数据、悬念或具体场景？如果以"随着X的发展""在当今Y的背景下"开头，需要重写。 |
| Paragraph length | **筛查步骤：** 逐段数句子（以句号、问号、感叹号为断句标志）。超过 3 句的段落标记出来，检查能否在逻辑层次切换处（从描述到评价、从现象到原因、从一个对象到另一个对象）用空行断开。连续两段纯文字没有被列表/表格/代码块打断的，检查是否需要插入视觉辅助。 |
| Sentence overload | **筛查步骤：** 找出包含三个以上逗号分句的长句。如果一句话承载了三层及以上独立信息（如"盲区是X，如果你Y，那么Z互补，而且Z还W"），在层次切换处用句号断开。 |
| Content redundancy | **筛查步骤：** 对每个独立小节，问"这一节的核心信息是否已在前文出现过？"。如果一节的主要内容可以从前文拼出来（只多了一两个修饰词），要么合并到前文，要么补充实质性新信息让它值得独立存在。特别检查"方法论/设置"类小节是否与开头段重复。 |
| Simple language | 搜索以下词并替换："utilize"→"use"，"facilitate"→"help"，"leverage"→"use"。中文同理："进行讨论"→"讨论"，"实现了对X的Y"→"Y了X"。 |
| Active voice | 找出被动句（"被X所Y""由X来完成"），检查能否改为主动语态。"这个工具将编译时间缩短到 3 秒"优于"编译时间被显著缩短了"。 |
| Evidence over adjectives | 搜索"显著""大幅""明显"等程度副词。每个命中项检查能否替换为具体数据。"10 倍提速"优于"显著提升了性能"。 |
| Transitions | **筛查步骤：** 读每段的第一句，检查它是否和上一段有逻辑衔接（因果、转折、递进、时间）。特别检查章节边界：两个 ## 标题之间的最后一段和下一节的第一段之间是否有未衔接的跳跃。 |
| Ending | 结尾不能是全文摘要。检查是否以"总之""综上""In conclusion"开头。好的结尾：回扣开头、指向下一步、或抛出更大的问题。检查结尾的核心论点是否与开头的钩子形成呼应。 |

## AI Pattern Audit

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
| Data fabrication | For every number, cost, date, or statistic in the output: can you point to the exact source sentence? If not, mark as derived or remove. Never fill gaps with plausible guesses. |
| Stiff handoff | **筛查步骤：** ① 检查每个段落的最后一句，是否以模糊指代（"那个搭档""这个方案"）收尾而把具体名称推到下一段开头；② 检查相邻段落的首尾衔接，如果段落 A 结尾是悬念、段落 B 开头才揭晓，合并为一句。 |
| Calqued metaphors | **筛查步骤：** ① 逐句对照英文原文，找出中文表达能逐词回译为英文习语/隐喻/固定搭配的位置（"径直走过了"←"walked right past"，"安全网"←"safety net"）；② 搜索中文里不常见的 动词+方位词 组合（走过、落回、指给），这类结构往往是英文 phrasal verb 的直译；③ 检查名词搭配是否在中文语境中成立（"买保险"成立，"买安全网"不成立）。 |
| Calqued syntax | **筛查步骤：** ① 全文搜索"是...的"句式，逐个判断能否换成动词谓语；② 搜索破折号"——"后跟长定语从句的结构；③ 搜索"而"连接的对称镜像分句，拆成独立分句；④ 搜索"解释了'""指出'"等动词+引号组合，间接转述去掉引号；⑤ 找出"动词+超过6字定语+宾语"结构，用将/把字句前置宾语或拆分；⑥ 对每句做回译测试：能逐词还原英文原句结构就是句法硬译。**不要凭语感跳过。** |
| Calqued rhetoric | **筛查步骤：** ① 搜索重型句式关键词（要么、无论、不是...而是、既...又），检查同一结构是否在同段或相邻段连续出现 2 次以上；② 对照英文原文，如果原文用了平行结构（anaphora、either/or triplet），检查中文是否照搬了相同的重复模式；③ 同一句式连用超过 1 次时，至少将其中一处替换为中文原生变体（反问、直接否定、条件句等）；④ 检查段落末尾是否有不超过四个字的独立短句（无动词的名词短语），如果去掉它上文仍然完整，是英文 dramatic kicker 的直搬，需融入前句并补充谓语和语境。 |
| Sentence-for-sentence | **筛查步骤：** ① 逐段对比中英文句子数量，1:1 对应的段落重点检查是否可以压缩；② 识别英文中的"铺垫段"（用多个例子论证同一个论点），检查中文是否有更简洁的惯用表达能一句说透；③ 问自己"删掉这段，下文读者还能不能跟上？"，如果能，说明这段是可压缩的冗余。 |
| Register check | For tech blogs: scan for colloquial/slangy verbs (丢给、甩了、整了、搞了). Replace with neutral action verbs (交给、给出、完成、处理). Professional tone with opinions, not casual chat. |
| Idiom register | **筛查步骤：** ① 标记文中所有四字成语和熟语；② 判断每个成语的源域（军事、体育、文学、法律）是否匹配技术写作语境；③ 判断情感预设（负面揭露、夸张赞叹）和表达意图是否一致；④ 不匹配的替换为语域中性的表述，优先使用文章自身已建立的术语（"命中""检出"）。 |
| Flat enumeration dump | **筛查步骤：** 找出句中三个以上顿号分隔项的位置，检查：① 读者是否需要记住每个名称？② 信息是否已在附近表格中呈现？如果不需要/已呈现，改为按类别归纳 + 总数概括。 |
| Vague pronoun in comparison | **筛查步骤：** 搜索"其中一个""另一个""有一个"等模糊指代词，检查上文是否在做多对象对比、后半句是否突出某对象的差异化特征。如果是，替换为具体名称。 |
| Mechanical negation chains | **筛查步骤：** 搜索连续出现的"没有""也没""完全没""未能"等否定词，如果相邻两句以上使用结构相同的否定句式，需变换：补因果、换否定形式、或改为对比句。 |
| Compressed technical explanation | **筛查步骤：** ① 搜索超过 15 字的括号注释，检查是否应提取为独立句子；② 找出"这是X不是Y"类判断句，确认读者在此之前已理解X和Y；③ 找出无上下文的技术行为描述，补上前置背景。 |
| Abstract mismatch claim | **筛查步骤：** 搜索"对不上""不匹配""不符""低于预期"等抽象判断，检查句中是否给出了具体的两端数据和方向。如果读者需要脑补"哪里对不上"，用量化对比替换。 |
| Self-contradicting absolute | **筛查步骤：** ① 搜索同段的绝对否定词（"没有""完全""从未"），对照前文是否有部分肯定，矛盾时改为程度化表述；② 搜索"钉在""锁在""挂在"等动词+方位词，检查是否为英文 phrasal verb 直译。 |
| Anaphoric stacking | **筛查步骤：** ① 找出连续三句以上使用相同动词的排比结构，合并为概括 + 一个反差点；② 搜索文学色彩四字词（"耿耿于怀""视而不见"），换为克制的技术表达；③ 检查段落末尾讽刺 kicker，如果纯陈述事实效果更强，去掉修辞。 |
| Instructional tone leak | **筛查步骤：** 搜索"还需要你""你需要""请用/请拿"等指令性结构，检查所在段落是分析/评述还是教程/指南。如果是分析文章，改为陈述不确定性（"准不准还得验""尚未核实"），不要给读者发操作指令。 |
| Skeletal recommendation | **筛查步骤：** ① 找出以"选/用/推荐"开头的祈使句，检查前面是否有场景描述；② 找出逗号连接三个以上无主语短语的句子（"它X，Y，也Z"），展开为各自完整的分句；③ 检查推荐理由中的动词是否具体——如果全是"推理""覆盖""验证"这类抽象词，还原为具体动作描述。 |
| Formulaic causation | **筛查步骤：** 搜索"这足以""这应该让你""这足够""这意味着你需要"等因果跳板。如果去掉跳板后结论仍然清晰，删掉跳板，让事实和结论用破折号或逗号自然衔接。 |
| Back-to-back label-colon | **筛查步骤：** 检查结论/总结段落中冒号（：）数量。同段出现两个及以上"标签：内容"结构时，第一个标签删除或移到句尾做附注，第二个替换为短转折词（≤5字）。 |
| Fragmented headers | **筛查步骤：** 对每个标题，读其后的第一句话。如果该句只是用同义词复述标题或副标题（"最大惊喜"→"最出人意料"，"覆盖最广"→"审得最广也最细"），删掉它，让段落直接从数据或细节开始。 |
| Ratio arithmetic | **筛查步骤：** 搜索"不到""不足""超过""至少""多于""少于"等不等式关键词，对每个命中项用计算器验证方向。$0.08 ÷ $0.72 = 11.1% > 10%，所以"不到十分之一"是错的。重点检查圆整分数（十分之一、三分之一）。 |
| Soulless writing | Read it aloud. Does it sound like a person talking, or a press release? Add opinion, uncertainty, or specific detail where the tone feels flat. |

## Final Proofread

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

