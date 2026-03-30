---
name: jetpanel
version: 1.0.0
description: 'Multi-perspective legal analysis panel for close questions of statutory or constitutional interpretation. Deploys subagents representing distinct jurisprudential methodologies (textualist, originalist, natural law, living constitutionalist, pragmatist) to analyze the same question in parallel, then synthesizes convergence and divergence. Use when the user provides a legal interpretive question or a bench memo with close questions. Triggers: interpretive panel, panel analysis, jetpanel, jet panel, run the panel, multi-perspective analysis, run panel analysis.'
---

# Interpretive Panel

Deploy a panel of jurisprudential subagents to analyze close questions of statutory or constitutional interpretation from competing methodological perspectives. Each subagent analyzes independently; the orchestrator synthesizes convergence and divergence.

## Fixed Paths

| Resource       | Path                                                   |
| -------------- | ------------------------------------------------------ |
| This skill     | `~/.claude/skills/jetpanel/`                           |
| Panel roster   | `~/.claude/skills/jetpanel/references/panel-roster.md` |
| Local authority| `~/refs/`                                              |

**Read access to `~/refs/` is pre-authorized.** All agents (including subagents) may read files from this directory without additional permission. Do not modify or delete existing files. Read `~/refs/CLAUDE.md` for directory structure, naming conventions, and path resolution patterns.

---

## Phase 1: Question Framing (Orchestrator, Sequential)

### Step 0: Read the Panel Roster

Read `~/.claude/skills/jetpanel/references/panel-roster.md` into context. This is the authoritative specification for each panelist's commitments, analytical instructions, and watch items.

### Step 1: Identify Input Mode

Two input modes are supported:

**Mode A — Direct Question:**
The user provides a specific legal question plus relevant authority (statutory text, constitutional provision, precedent, legislative history, etc.). Proceed to Step 2.

**Mode B — Bench Memo Input:**
The user provides a bench memo file (`.md` or `.docx`) or points to one in the working directory. Read the memo and identify close interpretive questions from the issue sections. Look for:

- Competing textual readings of a statute or constitutional provision
- Disputed statutory meaning where the parties invoke different canons or interpretive methods
- Constitutional questions where the text, history, and precedent point in different directions
- Issues where the memo's analysis identifies strong arguments on both sides without clear resolution
- Canons of construction that cut against each other

Extract each close question as a separate panel question. If no close interpretive questions are found, tell the user and ask whether they want to designate a question for panel analysis.

### Step 2: Assemble the Authority Packet

For each question, assemble:

1. **The provision text** — the statute, constitutional clause, rule, or regulation at issue. If a local copy exists in `~/refs/`, read it. Otherwise, use WebFetch on the relevant URL.

2. **Relevant precedent** — cases cited by both sides on this question. If `citations.json` exists in the working directory (from a prior jetmemo run), use it for pre-resolved local paths and URLs. Otherwise, identify the key cases from the user's input and look them up:
   - Local files first (see `~/refs/CLAUDE.md` for path conventions), then ndcourts.gov, CourtListener, or Justia

3. **The competing interpretive positions** — what reading does each side advance, and what interpretive method does each rely on?

4. **Legislative history or historical evidence** (if available) — committee reports, constitutional convention records, founding-era sources. Note what is available and what is not.

5. **Applicable canons** — identify canons of construction that both sides invoke or that may apply.

### Step 3: Determine Panel Composition

**Starting panel (always deployed):**
- MANNING (Statutory Formalist / Textualist)
- BARNETT-SOLUM-THOMAS (Originalist)
- VERMEULE (Common Good Constitutionalist / Natural Law)
- STRAUSS (Common Law Constitutionalist)
- POSNER-BREYER (Pragmatist / Purposivist)

**Bullpen evaluation:** If the question is constitutional, evaluate PAULSEN's activation criteria (from the roster). Deploy PAULSEN if one or more criteria are met:
- The question involves whether judicial precedent binds non-judicial actors
- The question involves departmentalism
- The question involves a foundational constitutional error the Court has declined to revisit
- The question involves the scope or legitimacy of judicial supremacy
- Starting panel convergence may rest on a shared assumption about judicial authority

If no activation criteria are met, do not deploy PAULSEN. Log the decision.

---

## Phase 2: Panel Analysis (Subagents, Parallel)

Launch all active panelists **simultaneously** using the Agent tool. Each subagent receives:

- The framed question
- The authority packet (provision text, precedent, competing positions, canons)
- That panelist's section from `panel-roster.md` (core commitments, analytical instructions, watch items)
- Output format instructions (below)
- Instruction: label your methodology explicitly throughout the analysis

**Do not run subagents sequentially.** Parallel execution prevents anchoring on the first analysis produced. No subagent sees another's analysis.

### Subagent Prompt Template

> **[PANELIST NAME] — [Methodology] Analysis**
>
> You are analyzing a legal interpretive question from the perspective of [methodology]. Your role is defined below. Analyze exclusively from this perspective. Do not defer to other methodologies or seek consensus.
>
> **Your Commitments and Instructions:**
> [Insert panelist's Core Commitments and Analytical Instructions from panel-roster.md]
>
> **Watch Items:**
> [Insert panelist's Watch section from panel-roster.md]
>
> ---
>
> **Question Presented:**
> [The framed interpretive question]
>
> **Provision at Issue:**
> [Statutory text, constitutional clause, or rule]
>
> **Competing Positions:**
> - Position A: [First reading with interpretive basis]
> - Position B: [Second reading with interpretive basis]
>
> **Relevant Authority:**
> [Precedent, legislative history, historical evidence, canons — with file paths or URLs for lookup]
>
> **Read access to `~/refs/` is pre-authorized.** You may read files from this directory without additional permission. Do not modify or delete existing files.
>
> ---
>
> **Instructions:**
>
> 1. Read the provision text and any authority you need from the paths or URLs provided.
> 2. Analyze the question exclusively from your assigned perspective.
> 3. Apply your analytical instructions rigorously. Do not introduce methods from other perspectives.
> 4. If your methodology produces a result that is uncomfortable, state it directly. Do not soften.
> 5. Flag any watch items that arise in your analysis.
>
> **Return your analysis in this format:**
>
> ```
> ## [PANELIST NAME] — [Methodology Label]
>
> ### Position
> [1-2 sentence bottom line: which reading do you adopt and why]
>
> ### Analysis
> [Full analysis per your analytical instructions. Label your methodology
> explicitly. Cite specific authority with pinpoint references. Apply
> relevant canons and identify them by name.]
>
> ### Key Authorities
> [List each citation relied upon with pinpoint references and what it
> establishes. For each, indicate the source:
>   - (provided) — from the authority packet
>   - (local) — found in ~/refs/ beyond what was provided
>   - (external) — retrieved via web research
> For (external) sources, include the URL where the material was found.]
>
> ### Flags
> [Any watch items triggered — backward reasoning, manufactured confidence,
> indeterminacy avoidance, etc. If none, state "None."]
> ```

---

## Phase 3: Synthesis (Orchestrator, Sequential)

### Step 4: Collect Results

Wait for all subagents to return. Use `TaskOutput` with `block: true` for each. If a subagent exceeds 5 minutes, treat it as failed and note the gap in the synthesis.

### Step 5: Synthesize

Working from the collected analyses, produce the synthesis:

1. **Convergence Map**
   - Which panelists agree on the **result** (same reading)?
   - Which agree on the **reasoning** (same interpretive basis for the same result)?
   - Full-panel convergence is rare and significant — note it prominently if it occurs.

2. **Divergence Map**
   - Where do panelists split on the result?
   - Trace each disagreement to the specific methodological commitment that drives it.
   - Identify whether the divergence is about **meaning** (what the text says) or **method** (how to determine what it says).

3. **Domain Weighting**
   - Note which panelists are in their strongest domain for this question:
     - MANNING: statutory text and structural canons
     - BARNETT-SOLUM-THOMAS: constitutional text and founding-era history
     - VERMEULE: administrative law, institutional authority, tradition
     - STRAUSS: precedent-heavy areas with doctrinal evolution
     - POSNER-BREYER: regulatory questions, consequentialist tradeoffs
   - Weight these panelists' analyses more heavily in the synthesis narrative.

4. **Formalist Floor / Pragmatist Ceiling**
   - MANNING + BARNETT-SOLUM-THOMAS convergence = strong formalist floor
   - STRAUSS + POSNER-BREYER convergence = strong pragmatist ceiling
   - Map the question between these poles. Where do the formalists and pragmatists agree? Where do they diverge?

5. **Backward-Reasoning Flags**
   - Review each panelist's self-reported flags.
   - Independently evaluate: is any panelist working from a preferred result backward to a methodological justification? Most common with:
     - BARNETT-SOLUM-THOMAS (liberty valence)
     - VERMEULE (authority valence)
     - POSNER-BREYER (consequentialist rationalization)

6. **PAULSEN Diagnostic** (if activated)
   - Does PAULSEN's analysis identify a foundational institutional problem that the starting panel assumed away?
   - Is his resolution judicially available, or is it diagnostic only?
   - Note separately from the main synthesis.

### Step 6: Write Output

**Determine output mode:**

- **Standalone mode** (default): User invoked `/jetpanel` directly. Write the full panel analysis.
- **Integration mode**: The skill was invoked by jetmemo or the user requests a condensed section for a bench memo. Write the condensed format.

#### Standalone Output Format

Write to `{question_slug}_panel.md` in the working directory. If analyzing multiple questions from a bench memo, write one file per question or a single file with sections for each.

```markdown
# INTERPRETIVE PANEL ANALYSIS

**Question Presented:** {The close interpretive question}

**Provision at Issue:** {Citation to the statute, clause, or rule}

**Panel Composition:** {List active panelists; note if PAULSEN was activated and why}

---

## Panel Analyses

{Insert each subagent's full analysis in roster order: MANNING, BARNETT-SOLUM-THOMAS, VERMEULE, STRAUSS, POSNER-BREYER, then PAULSEN if activated}

---

## Synthesis

### Convergence
{Which panelists agree on result and/or reasoning}

### Divergence
{Where they split and what methodological commitment drives it}

### Domain Weighting
{Which panelists are in their strongest domain; how that affects the weight of their analyses}

### Formalist Floor / Pragmatist Ceiling
{MANNING + BARNETT-SOLUM-THOMAS position vs. STRAUSS + POSNER-BREYER position; where the question falls between these poles}

### Backward-Reasoning Flags
{Any panelist working from result to method}

### PAULSEN Diagnostic
{If activated: institutional problem identified, judicial availability of resolution}
{If not activated: "PAULSEN not activated — no activation criteria met."}

### Bottom Line
{1-3 sentences: what this panel analysis reveals about the interpretive question — where the strongest arguments lie, what methodological commitments drive the outcome, and what a court applying any reasonable methodology should grapple with}
```

#### Integration Output Format (for bench memos)

When called from jetmemo or when the user requests a condensed version:

```markdown
### Interpretive Panel: {Issue heading}

**Question:** {The close interpretive question}

**Panel Result:** {X-Y split or consensus, with methodology labels}

**Formalist Position (MANNING, BARNETT-SOLUM-THOMAS):** {1-3 sentences — the textual/originalist reading and its basis}

**Living Constitution / Pragmatist Position (STRAUSS, POSNER-BREYER):** {1-3 sentences — the precedent-based or consequentialist reading}

**Natural Law Position (VERMEULE):** {1-3 sentences — the common-good reading}

**Key Divergence:** {What methodological commitment produces the split}

**Strongest Arguments Each Way:**
- For {reading A}: {best argument with citation}
- For {reading B}: {best argument with citation}
```

This section slots into the bench memo after the issue's Analysis paragraph and before the next issue heading.

---

## Token Efficiency

| Content                | Strategy                               |
| ---------------------- | -------------------------------------- |
| Panel roster           | Orchestrator reads once; extracts relevant section per subagent |
| Provision text         | Local `~/refs/` files preferred; web fallback |
| Precedent              | Use `citations.json` if available; local files then web |
| Subagent prompts       | Each gets only its own methodology section, not the full roster |
| Synthesis              | Orchestrator collects structured outputs; no raw document re-reading |

**Estimated token budget:**
- Each subagent: ~10-20K input, ~3-5K output
- 5-6 subagents total: ~50-120K input, ~15-30K output
- Synthesis: ~20-30K input, ~5-10K output
- **Total: ~85-170K tokens per panel run**

## Fallback Handling

- If a subagent fails or times out: note the gap in the synthesis and proceed with the remaining panelists. A 4-panelist synthesis is still valuable.
- If authority lookup fails (no local file, web fetch fails): the subagent should note "authority not verified" and analyze based on the provision text and competing positions alone.
- If the question is not an interpretive question (e.g., purely procedural, factual sufficiency): tell the user the panel is designed for interpretive questions and ask whether they want to proceed anyway.

## Important Rules

- **Subagents do not see each other's analyses.** This is enforced by parallel execution. Do not summarize one panelist's view for another.
- **Disagreement is the point.** Do not seek consensus in the synthesis. Map the disagreement and trace it to methodological commitments.
- **Label methodology explicitly.** Every analytical claim in every subagent output must be traceable to a specific methodological commitment.
- **Do not fabricate authority.** Subagents may cite cases and sources provided in the authority packet, found in `~/refs/`, or retrieved via web research (WebFetch/WebSearch). If a subagent retrieves authority beyond the provided packet, it must tag the source as described in the Key Authorities format and include the URL. If a subagent's methodology calls for historical evidence that is not available and cannot be found, it should say so honestly.
- **Watch items are mandatory.** Each subagent must report on watch items even if none are triggered.
- **The synthesis is not a vote.** Do not count panelists as if this were a poll. Trace the reasoning.
