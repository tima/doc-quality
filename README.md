# Documentation Quality Skills

A suite of four skills for CLI documentation auditing with zero-hallucination verification and auto-framework detection.

## The Problem

CLI documentation drifts from code: users hit undocumented flags, missing commands, or flags that behave differently than documented. This suite prevents that by comparing docs against actual code and catching quality issues.

## What This Does
- Compares your documentation against actual CLI code (never hallucinates)
- Auto-detects your CLI framework (argparse, Cobra, Bash, Click)
- Audits for ghost items (documented but missing) and quality issues
- Prevents tone shifts, clarity problems, and consistency gaps
- Applies fixes interactively

## Skills

- **[doc-accuracy-audit](skills/doc-accuracy-audit/SKILL.md)** — Cross-references CLI documentation against source code. Finds ghost items (documented but missing), hidden items (exist but undocumented), and detail mismatches. Zero-hallucination verification prevents uncited claims. **v1: CLI tools only. Terraform/OpenAPI deferred to v2.**

- **[doc-quality-audit](skills/doc-quality-audit/SKILL.md)** — Evaluates docs for tone, style, clarity, and plain language compliance. Reports issues with severity ratings and suggestions.

- **[doc-quality-revise](skills/doc-quality-revise/SKILL.md)** — Applies corrections from audit reports: auto-revises simple issues, guides interactive review for complex changes.

- **[doc-quality-check](skills/doc-quality-check/SKILL.md)** — Orchestrates the full pipeline in one command: accuracy audit → quality audit → apply revisions.

## Pipeline

```
/doc-accuracy-audit → accuracy-audit-report.md
/doc-quality-audit  → quality-audit-report.md
/doc-quality-revise → revised docs
/doc-quality-check  → runs all three in sequence
```

## What's Supported (v1)

**CLI Tools:** argparse (Python), Cobra (Go), Click (Python), Bash function dispatch
**Accuracy Audit:** Auto-detects framework, finds ghost items, hidden items, detail mismatches with zero-hallucination verification
**Quality Audit:** Works on any documentation (tone, clarity, consistency, completeness, audience, examples)

**Deferred to v2:** Terraform providers, OpenAPI/Swagger specs. See [V1-SCOPE.md](docs/V1-SCOPE.md) for details.

## Installation

**Option 1: Local development (recommended for testing)**
```bash
git clone <repo-url> ~/projects/doc-quality
# Symlink each skill
ln -sf ~/projects/doc-quality/skills/doc-accuracy-audit ~/.claude/skills/doc-accuracy-audit
ln -sf ~/projects/doc-quality/skills/doc-quality-audit ~/.claude/skills/doc-quality-audit
ln -sf ~/projects/doc-quality/skills/doc-quality-revise ~/.claude/skills/doc-quality-revise
ln -sf ~/projects/doc-quality/skills/doc-quality-check ~/.claude/skills/doc-quality-check
```

**Option 2: Published registry (when available)**
```bash
# Replace REGISTRY_PATH with actual registry location
npx skills add REGISTRY_PATH/doc-quality -g
```

### Uninstall

```bash
npx skills remove doc-accuracy-audit           # project scope
npx skills remove doc-accuracy-audit --global  # user scope
# (repeat for each skill)
```

## License

MIT — see [LICENSE](LICENSE).
