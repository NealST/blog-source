# Part 3: Final Verification

Phase 3 is a lightweight residue check, not a re-run of Phase 1 or Phase 2. Its job is to catch issues that the earlier phases *introduced* or *missed at the seams*, then do a mechanical proofread.

## Residue Check

Phase 1 and Phase 2 edits can create new problems:

| What to check | How |
|---------------|-----|
| Broken transitions | Re-read the first sentence of each paragraph. Does it still connect to the previous paragraph, or did a Phase 1/2 edit break the bridge? |
| Orphaned references | Search for "上文""前面""如前所述" — do they still point to content that exists? Phase 1 may have moved or cut the referenced section. |
| Inconsistent terminology | If Phase 2 changed a term (e.g., "全军覆没" → "几乎没有命中"), check that the new term is used consistently throughout, not just at the edit site. |
| New redundancies | Merging paragraphs (Phase 1) or expanding compressed sentences (Phase 2, #43) can create repetition with nearby content. Read the ±2 paragraphs around each major edit. |
| Created comma-splice | Phase 2 sentence merges (#31, #34) can produce new run-on sentences. Check that merged sentences don't carry 3+ information layers. |

## Title-Body Coherence

Phase 1 and 2 edits may have shifted the article's angle. Re-check:
- Does the title still match the final content?
- Does the opening paragraph still set up what the article actually delivers?
- Does the ending still echo the opening or point forward?

If the angle shifted, update the title — don't force the body back to match an outdated title.

## Mechanical Proofread

1. **Proof headers separately from body text.** Read only the headers in sequence — do they tell a coherent story? Are they styled consistently?
2. **Read backward, one sentence at a time.** This separates content from mechanics and catches typos your brain auto-corrects when reading forward.
3. **Verify formatting consistency:** header levels, list formats, punctuation style (Chinese vs. English), code block language tags.
4. **Check numbers and names:** every number, proper noun, and version number against the source material. Phase 2 data fabrication checks (#33) catch invented numbers; this step catches transcription errors in real ones.

---

## Reference: Full Skill Execution Example

This example shows all three phases working together on a single piece.

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

**Phase 1 findings:** No main theme. Opening is ceremony, not hook. "Challenges" section is a template. Ending is generic summary. No data, no specifics. Structure is outline-shaped, not argument-shaped.

**Phase 2 findings:** Collaborative artifacts (#20: "Great question!", "I hope this helps!", "Let me know"). Significance inflation (#1: "pivotal moment", "enduring testament"). AI vocabulary (#7: "landscape", "tapestry"-class words). Rule of three (#10: two instances). Boldface (#15: mechanical list headers). Filler (#23: "at its core"). Negative parallelism (#9: "not just...it's about"). Vague attribution (#5: "Industry observers"). Hedging (#24: "could potentially possibly"). Generic conclusion (#25).

**Draft rewrite:**
> AI coding assistants speed up some tasks. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools are good at boilerplate: config files, test scaffolding, repetitive refactors. They are bad at knowing when they are wrong. I have mass-accepted suggestions that compiled, passed lint, and still did the wrong thing because I stopped paying attention.
>
> The productivity claims are hard to verify. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not correctness, and correctness is not value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
>
> None of this means the tools are useless. It means they are tools. They do not replace judgment, and they do not eliminate the need for tests.

**Phase 2 re-check:** Rhythm is still a bit too tidy. The closer leans a touch slogan-y. Named studies should be verified against real sources.

**Final rewrite:**
> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> People I talk to tend to land in two camps. Some use it like autocomplete for chores and review every line. Others disable it after it keeps suggesting patterns they don't want. Both feel reasonable.
>
> The productivity metrics are slippery. GitHub can say Copilot users "accept 30% of suggestions," but acceptance isn't correctness, and correctness isn't value. If you don't have tests, you're basically guessing.

**Phase 3 check:** No broken transitions. No orphaned references. Terminology consistent. Headers: none needed for this length. Numbers: "30%" is attributed to GitHub (verifiable). Clean.

**Changes across all phases:** Stripped chatbot framing, significance inflation, promotional and -ing padding, rule-of-three, synonym cycling, false ranges, copula avoidance, em dashes, emojis, boldface, curly quotes, formulaic "challenges" section, hedging disclaimers, filler, persuasive framing, and the generic upbeat conclusion. Rebuilt the voice with varied rhythm and concrete detail.
