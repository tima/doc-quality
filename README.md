# doc-quality

Comprehensive documentation accuracy and quality auditing for code projects.

**Latest Release:** v1.2 (2026-08-06) — [Release Notes](RELEASE-NOTES-v1.2.md)

## The Problem

Documentation drifts from code: users hit undocumented features, missing commands, or behavior that doesn't match docs. Code structure changes outpace doc updates. Quality issues (unclear writing, inconsistent terminology) go undetected. This suite prevents that by automatically comparing docs against code and assessing documentation quality.

## What This Does

**Accuracy Auditing**
- Compares documentation against actual code (never hallucinates)
- Auto-detects project type and framework (CLI, library, extension)
- Finds ghost items (documented but missing in code)
- Finds hidden items (exist in code but undocumented)
- Catches detail mismatches (flags/params with different defaults)

**Quality Auditing**
- Assesses tone, clarity, structure, consistency, completeness
- Checks audience appropriateness, examples quality, plain language
- Reports issues with severity, citations, and fix suggestions

**Verification Passes**
- 6-check accuracy pass prevents uncited claims, direction inversion
- 3-check quality pass prevents paraphrased quotes, miscalibrated confidence
- Zero-hallucination guarantee: every finding cites evidence

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

## What's Supported (v1.2)

**Code Project Types:**
- CLI tools: Cobra (Go), argparse/Click (Python), Bash function dispatch
- Python libraries: classes, functions, public API (__all__ exports)
- VS Code extensions: commands, settings, activation events

**Polyglot Detection:**
- Root manifest priority ensures correct primary type detection
- Handles multi-language projects correctly (e.g., TypeScript with Python build scripts)

**Quality Dimensions:**
- All documentation types: libraries, extensions, CLIs, guides, API documentation
- 10 dimensions: tone, clarity, structure, consistency, completeness, audience, examples, formatting, SEO, plain language

**Tool Compatibility:**
- Works with any AI tool supporting agent skills
- Tool-agnostic (no vendor lock-in)

**Deferred to v2:**
- Terraform providers, OpenAPI/Swagger specs
- See [docs/reference/V1-SCOPE.md](docs/reference/V1-SCOPE.md) for detailed scope

**Future exploration:**
- Ansible playbooks, roles, execution environments, collections
- See [docs/EXPLORATION-ANSIBLE-AUDITING.md](docs/EXPLORATION-ANSIBLE-AUDITING.md) for research and patterns

## Installation

### System Requirements

**Required:**
- `rg` (ripgrep) — Fast regex search for source code
  - macOS: `brew install ripgrep`
  - CentOS/RHEL: `yum install ripgrep`
  - See https://github.com/BurntSummaryxyz/ripgrep#installation

- `python3` — For project type detection and Python library auditing

**Optional:**
- `sg` (ast-grep) — Structural code search, planned for v1.2 (Terraform/OpenAPI support)
  - See https://ast-grep.github.io/guide/quick-start.html

### Via npx skills (Recommended)

```bash
# All skills, user scope (available in all sessions)
npx skills add tima/doc-quality -g

# All skills, project scope (this project only)
npx skills add tima/doc-quality

# Specific skills only
npx skills add tima/doc-quality --skill doc-accuracy-audit -g
npx skills add tima/doc-quality --skill doc-quality-audit -g
npx skills add tima/doc-quality --skill doc-quality-revise -g
npx skills add tima/doc-quality --skill doc-quality-check -g
```

### Local Development

```bash
git clone https://github.com/tima/doc-quality.git ~/projects/doc-quality
ln -sf ~/projects/doc-quality/skills/doc-accuracy-audit ~/.claude/skills/doc-accuracy-audit
ln -sf ~/projects/doc-quality/skills/doc-quality-audit ~/.claude/skills/doc-quality-audit
ln -sf ~/projects/doc-quality/skills/doc-quality-revise ~/.claude/skills/doc-quality-revise
ln -sf ~/projects/doc-quality/skills/doc-quality-check ~/.claude/skills/doc-quality-check
```

### Uninstall

**Registry installed:**
```bash
npx skills remove doc-accuracy-audit --global
npx skills remove doc-quality-audit --global
npx skills remove doc-quality-revise --global
npx skills remove doc-quality-check --global
```

**Locally symlinked:**
```bash
rm ~/.claude/skills/doc-accuracy-audit
rm ~/.claude/skills/doc-quality-audit
rm ~/.claude/skills/doc-quality-revise
rm ~/.claude/skills/doc-quality-check
```

See [INSTALL.md](INSTALL.md) for detailed installation, updating, and troubleshooting.

## License

MIT — see [LICENSE](LICENSE).
