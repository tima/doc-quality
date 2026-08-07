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

- **[doc-accuracy-audit](skills/doc-accuracy-audit/SKILL.md)** — Cross-references CLI documentation against source code. Finds ghost items (documented but missing), hidden items (exist but undocumented), and detail mismatches. Zero-hallucination verification prevents uncited claims. **v1: CLI tools only. Schema-based auditing (IaC, APIs) deferred to v2.**

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
- Schema-based auditing: IaC (infrastructure-as-code), APIs, configuration specs
- See [docs/reference/V1-SCOPE.md](docs/reference/V1-SCOPE.md) for detailed scope

**Future exploration:**
- Ansible playbooks, roles, execution environments, collections
- See [docs/EXPLORATION-ANSIBLE-AUDITING.md](docs/EXPLORATION-ANSIBLE-AUDITING.md) for research and patterns

## Installation

Skills work with any tool supporting agent skills. ripgrep and ast-grep are optional dependencies that improve search quality (see [INSTALL.md](INSTALL.md) for system requirements).

**Quick start:**
```bash
npx skills add tima/doc-quality -g
```

For detailed installation, updating, local development, and troubleshooting, see [INSTALL.md](INSTALL.md).

## License

MIT — see [LICENSE](LICENSE).
