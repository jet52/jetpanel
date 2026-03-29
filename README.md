# jetpanel v1.0.0

Multi-perspective legal analysis panel for close questions of statutory or constitutional interpretation. A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill.

## What It Does

Deploys a panel of five (optionally six) subagents, each representing a distinct jurisprudential methodology, to analyze the same interpretive question in parallel:

| Panelist | Methodology | Model |
|----------|-------------|-------|
| MANNING | Statutory Formalist / Textualist | John F. Manning |
| BARNETT-SOLUM-THOMAS | Originalist | Barnett + Solum + Thomas (blended) |
| VERMEULE | Natural Law / Conservative Consequentialist | Adrian Vermeule |
| STRAUSS | Common Law Constitutionalist | David Strauss |
| POSNER-BREYER | Pragmatist / Consequentialist | Posner + Breyer (blended) |
| PAULSEN | Constitutional Supremacist / Formalist | Michael Stokes Paulsen (bullpen -- constitutional cases only) |

Subagents do not see each other's analyses. Disagreement is the point. The orchestrator synthesizes convergence and divergence across methodologies.

## Installation

```bash
python3 install.py
```

This copies the skill to `~/.claude/skills/jetpanel/`.

## Usage

### Standalone -- Direct Question

Provide a specific legal question plus relevant authority:

> `/jetpanel` -- Is N.D.C.C. section 14-09-06.2(1)(j) a "best interests" factor or an independent ground for modification? The parties dispute whether the statute's plain text limits judicial discretion. Here are the competing readings and the key cases...

### Standalone -- Bench Memo Input

Point the panel at an existing bench memo:

> `/jetpanel` -- Analyze the close interpretive questions in 20250319_memo.md

The panel reads the memo, identifies close interpretive questions from the issue sections, and runs panel analysis on each.

### Integrated with jetmemo

When both jetpanel and [jetmemo](https://github.com/jtufte/jetmemo-skill) are installed, jetmemo can optionally invoke the panel during bench memo generation. This happens automatically when:

1. `recommend_mode` is enabled (user says "with recommendation")
2. The legal framing identifies a close interpretive question

The panel produces a condensed analysis section that is inserted into the bench memo after the relevant issue's analysis.

## Output

### Standalone

Full panel analysis document (`{question}_panel.md`) with:
- Each panelist's complete analysis labeled by methodology
- Key authorities cited by each panelist, tagged by source (provided, local, or external with URLs)
- Synthesis mapping convergence, divergence, domain weighting, and backward-reasoning flags

### Integration (bench memo)

Condensed section inserted into the memo showing the panel split, each school's position in 1-3 sentences, and the strongest arguments each way.

## Local Authority

The skill works best with a local `~/refs/` directory containing:

| Path | Content |
|------|---------|
| `~/refs/nd/opin/markdown/` | ND Supreme Court opinions (markdown) |
| `~/refs/nd/code/` | North Dakota Century Code |
| `~/refs/nd/regs/` | North Dakota Administrative Code |
| `~/refs/nd/rule/` | North Dakota Court Rules |
| `~/refs/nd/cnst/` | North Dakota Constitution |

Without `~/refs/`, the skill falls back to web lookups for authority.

## Token Budget

~85-170K tokens per panel run, depending on the complexity of the question and amount of authority. Runs in subagent contexts, so standalone usage does not compete with other skills for the main context window.

## Requirements

- Claude Code
- `~/refs/` directory (optional, improves authority lookup)

## License

MIT
