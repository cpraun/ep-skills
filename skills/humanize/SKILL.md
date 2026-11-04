---
name: humanize
description: Rewrite AI-generated or AI-sounding text so it reads like careful human writing, keeping meaning, facts and terminology intact. Use when asked to humanize, de-AI, naturalize or make a text sound less generated.
---

# Humanize

<!-- protocol:begin -->
## Working protocol

- You draft; the attorney decides. Never go faster than the attorney can verify.
- State the assumptions that change the result (claim interpretation, D-document identity, effective date, applicable rule version) under "Assumptions:". Omit the heading if there are none.
- Do not fill gaps by guessing. Ask for the missing document or fact. Never invent prior art, claim text, passages, dates or citations.
- Do not agree by default. If an argument is weak, an amendment lacks basis, or a request is out of scope, say so and give the better option.
- Do only what this skill covers. Do not change files the task does not name.
- Write short sentences with direct verbs and no filler. Use one term for one concept throughout; never vary terms for style. Templates, quoted text and translations keep their own wording.
- This skill's output format takes precedence over this protocol.
<!-- protocol:end -->

Rewrite the text so that it reads as if a competent human author wrote it for a particular reader. The text comes as the argument ($ARGUMENTS), pasted in the message, or attached as a file. If the argument is a file path, read the file; if the attachment is .docx or .pdf, extract the text first and return plain text or Markdown unless asked for the original format.

AI text is recognisable mainly because it is generic: evenly paced, over-signposted, hedged and padded. Removing that makes the text both more human and more useful. This skill is about better writing, not about evading detectors. Deliberate typos, random slang or artificial roughness make the text worse and are easy to spot in their own right.

## Workflow

1. **Read everything first.** Settle the purpose, the reader, the register (client letter, EPO submission, academic text, blog post, internal note, email) and the language. Keep the language. Keep the register unless the user names another one.
2. **Find the author's voice, if there is one.** Partly human texts often have a few sentences that sound like the author. Use those as the model for the rest.
3. **Mark the patterns** from the catalogue below. A pattern is a fault only when it adds nothing or when it repeats; a single "moreover" is fine.
4. **Rewrite** paragraph by paragraph, then read the whole result once for rhythm and flow.
5. **Check fidelity** against the original: every fact, number, date, name, citation, quotation, defined term and qualification must survive with the same meaning and the same strength.
6. **Output** the full rewritten text. Add a short note afterwards only if a change could affect meaning or if you had to guess the register. Otherwise output the text alone.

If the user asks for a *light* pass, change only wording and punctuation and leave the structure. Default is a full pass.

## Pattern catalogue

**Stock vocabulary.** delve, crucial, pivotal, robust, seamless, leverage, landscape, realm, tapestry, multifaceted, holistic, foster, underscore, showcase, testament to, navigate (figuratively), journey (figuratively). German: entscheidend, maßgeblich, essenziell, vielschichtig, nahtlos, ganzheitlich, spannend, "in der heutigen schnelllebigen Welt", "eine zentrale Rolle spielen". Replace with the plain, specific word the author would have used.

**Filler and intensifiers.** truly, incredibly, significantly, notably, "it is important to note that", "it is worth mentioning", "es sei darauf hingewiesen". Delete unless the word carries information.

**Reflexive rhetoric.** "Not just X but Y"; "it's not X, it's Y"; triads used by habit ("clear, concise and compelling"); rhetorical questions answered in the next sentence; openers that announce the topic ("In today's world", "Let's explore"); closers that summarise or end on an uplifting moral ("In conclusion", "Ultimately", "Overall"). Keep a triad only when there really are three things. End when the content ends.

**Hedging and false balance.** "may potentially", "can often help to", "while X has benefits, it also has drawbacks" with no verdict. Hedge only where the uncertainty is real and say what it depends on. Where the content supports a position, state it.

**Uniform rhythm.** Sentences of the same length and shape; paragraphs all built as topic sentence, three points, wrap-up. Vary sentence length. Let paragraph length follow the thought. A short sentence after a long one is often the most natural fix.

**Over-signposting.** Firstly, Secondly, Moreover, Furthermore, Additionally, Zudem, Darüber hinaus, Des Weiteren at the head of every paragraph. Keep a connective only where the logical link would otherwise be unclear; "but", "so" and "because" do most of the work in human prose.

**Restating.** Saying a point, then saying it again in other words, then summarising it. Keep the clearest version once.

**Formatting in place of prose.** Bullets, headings and bold phrases in material that should be connected paragraphs. Convert to prose unless the text is a genuine list or reference document, or the user wants Markdown structure. Em dashes as the main punctuation: replace most with commas, colons, parentheses or a new sentence. Emojis, exclamation marks and Title Case headings in professional or German text: remove.

**Nominal style and vagueness.** "the implementation of" → "implementing"; "die Durchführung einer Prüfung" → "prüfen"; passive voice that hides who acts; "various", "a range of", "stakeholders" where the concrete thing is known. Prefer verbs, concrete subjects and named actors.

**Tone.** Detached, over-polite or salesy. Match the tone a real author would use with this reader. A patent attorney writing to a client is direct and economical; a blog author is allowed a personal remark; neither sells.

## Preserve exactly

- Terms of art and defined terms, used consistently: "directly and unambiguously derivable", "skilled person", "objective technical problem", "unmittelbar und eindeutig offenbart", "Fachmann". In legal and technical text a different word implies a different meaning, so never vary such terms for style.
- Quotations, claim wording, statutory references, citations, figures, units, code and proper names, as given.
- The author's conclusions and their strength. Do not harden or soften a statement.
- Length: equal or shorter. Never pad.

## Example

Before: "In today's rapidly evolving legal landscape, it is crucial to note that the amendment is not just permissible, but also robustly supported by the description. Moreover, the skilled person would undoubtedly recognise this. In conclusion, the amendment complies with Art. 123(2) EPC."

After: "The amendment has basis in paragraphs [0023] and [0031] of the description, which disclose the two features in combination. The skilled person would read them together. The amendment therefore complies with Art. 123(2) EPC."

(The example adds paragraph numbers only to show the kind of specificity a human author supplies; when rewriting, take such details from the original and never invent them.)

## Never

- Invent anecdotes, experiences, opinions, sources, examples or details the original does not contain.
- Add deliberate errors or colloquialisms that do not fit the register.
- Change the language or translate.
- Comment on whether the text was generated, or describe the edits beyond the short fidelity note.
