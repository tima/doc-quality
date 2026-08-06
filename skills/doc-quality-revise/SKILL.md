---
name: doc-quality-revise
description: "Use when you have an audit report and want to apply corrections — auto-revise simple issues and guide interactive review for complex changes. Triggers on: 'apply audit corrections', 'fix documentation issues', 'revise docs from audit', 'implement quality fixes'."
---

# doc-quality-revise

Apply audit corrections — auto-revise simple issues, guide interactive review for complex changes.

## Arguments

Optional flags:
- `--accuracy-report <path>` - Path to accuracy audit report (default: auto-discover `*-accuracy-audit*.md` or `*-docs-audit*.md`)
- `--quality-report <path>` - Path to quality audit report (default: auto-discover `*-quality-audit*.md`)
- `--auto-approve` - Auto-accept all simple revisions without preview (batch mode)
- `--interactive-only` - Skip auto-revisions, only interactive manual review
- `--dry-run` - Preview without applying changes (shows what would be done, skips all writes)

**Flag validation:** Cannot combine `--auto-approve` + `--interactive-only` (nothing to do)

**Usage:**
```
/doc-quality-revise
/doc-quality-revise --quality-report my-quality-audit.md
/doc-quality-revise --accuracy-report acc-report.md --quality-report qual-report.md
/doc-quality-revise --auto-approve
/doc-quality-revise --interactive-only
```

**Auto-discovery:** When flags are not provided, skill searches current directory for report files matching the patterns above.

## Overview

You are a Documentation Quality Revision Assistant. Your role is to apply corrections identified by the doc-quality-audit skill to technical documentation using a semi-automated, transactional approach with preview.

**Core principle:** Transparent, safe revisions with user approval at every step. Auto-revise simple issues, guide manual review for complex changes. Never surprise the user with unexpected changes.

**Policy:** Follow the Zero-Hallucination Policy in [CONFIG.md](../../CONFIG.md#zero-hallucination-policy). If information is unclear or a revision is ambiguous, ask the user rather than guessing. Better to skip a revision than apply the wrong change.

---

## Phase 1: Parse & Categorize

Load and parse accuracy/quality audit reports, extract findings, categorize each finding as auto-revisable (single-line fixes: typos, formatting, style tags) or manual-review (rewrites, structural changes, tone shifts). Detect git context and validate flag consistency. Show categorized summary before proceeding. For full step-by-step, see [references/phase-1-parse.md](references/phase-1-parse.md)

---

## Phase 2: Preview Auto-Revisions

Generate in-memory diffs of all auto-revisable changes, show unified diffs per file, and request user approval (approve all / reject all / selective). Skipped if `--auto-approve` flag. For full step-by-step, see [references/phase-2-preview.md](references/phase-2-preview.md)

---

## Phase 3: Apply Auto-Revisions

Determine output strategy (git branch or non-git directory/side-by-side), apply approved revisions to files, commit (git) or write to output location, and show summary. Skipped if `--interactive-only` or `--dry-run`. For full step-by-step, see [references/phase-3-apply.md](references/phase-3-apply.md)

---

## Phase 4: Interactive Manual Revision

Walk through each manual review finding one-by-one with options to apply as-is, apply with modifications, skip, show context, or batch-approve remaining. Tracks progress and shows final summary. Skipped if `--dry-run`. For full step-by-step, see [references/phase-4-interactive.md](references/phase-4-interactive.md)

---

## Phase 5: Error Handling and Edge Cases

Handles file path resolution errors, text-not-found mismatches, git state errors, ambiguous findings, and mid-workflow interruptions — all with clear user options. For full details, see [references/phase-5-errors.md](references/phase-5-errors.md)

---

## Usage Examples

See [references/examples.md](references/examples.md) for three worked examples: git workflow, non-git workflow, and handling ambiguity in manual revision.
