# doc-quality Skill Improvements — Handoff

**Source:** Cross-skill consistency review between `~/projects/code-intel` and
`~/projects/doc-quality`. The code-intel skill was used as the reference
implementation — it is more rigorous and was recently refactored. These
recommendations bring doc-quality into alignment.

**Files in scope:**
- `skills/doc-accuracy-audit/SKILL.md` (most changes)
- `skills/doc-quality-audit/SKILL.md` (one change)

**Design decision (item 6):** Flag for discussion before implementing.

---

## 1. Bring Zero-Hallucination inline in doc-accuracy-audit

**File:** `skills/doc-accuracy-audit/SKILL.md`

**Problem:** Step 4 Strict Adherence section defers to CONFIG.md with one pointer
line: "Follow the canonical policy in CONFIG.md#zero-hallucination-policy". If
CONFIG.md is unavailable or misconfigured, the policy silently disappears.
code-intel defines it inline (self-contained, cannot be lost). The CONFIG.md
pointer version also likely lacks the detail the skill actually needs.

**Action:** Add the Zero-Hallucination definition directly in the Strict Adherence
section. Keep the CONFIG.md reference as a supplement, not the sole source.

**Reference text from code-intel Strict Fidelity Rules:**
> Every factual claim — file paths, function names, call directions,
> dependencies, counts — must trace to a tool result from this session. If
> information is unavailable or outside your access, write: "Information not
> found." Do not bridge gaps with inference.

Adapt for doc-accuracy-audit context: "tool result from this session" maps to
grep/rg output, schema inspection results, file reads.

---

## 2. Add comment attribution rule to doc-accuracy-audit

**File:** `skills/doc-accuracy-audit/SKILL.md`

**Problem:** Task 4 (Semantic Logic Check) traces execution paths to verify
documented behavior matches implementation. The skill has no rule requiring
distinction between "a code comment says X" and "the code does X." A comment
saying `// defaults to 30s` is not the same evidence as the code actually
defaulting to 30s. Without this rule, Task 4 verdicts can be overconfident.

**Action:** Add to Strict Adherence section (after Uncertainty Labeling):

> **Comment/annotation attribution:** Claims found in code comments, docstrings,
> or TODO annotations are developer-stated intent, not verified behavior. Label
> them accordingly — e.g. "The author notes in a docstring that..." — not as
> assertions about runtime behavior. Do not cite a comment as Source of Truth;
> trace to actual code.

Also add a check to Verify Before Writing Report (between check 2 Direction
Accuracy and check 3 Enumerated Completeness):

> **Comment attribution:** Scan findings for any "Source of Truth" entry sourced
> from a code comment or docstring rather than actual code. Verify each is
> labeled as developer-stated, not asserted as verified behavior.

---

## 3. Align doc-accuracy-audit search tool default with doc-quality-audit

**File:** `skills/doc-accuracy-audit/SKILL.md`

**Problem:** doc-quality-audit (sibling skill) checks for sg first and uses it
if available. doc-accuracy-audit is rg-first and only adds ast-grep as an
optional enhancement for one Cobra/Go case. Key Reminder #9 explicitly says
"Use rg or grep for source code pattern search." This is an intra-project
inconsistency — two sibling skills with opposite defaults.

**Note:** doc-accuracy-audit uses text-scan patterns (.AddCommand(, @click.,
ArgumentParser) that don't require AST. Full sg adoption is v1.2 scope per the
Limitations section. The goal here is alignment with doc-quality-audit's
availability-check pattern, not forcing sg for all searches.

**Action:**
1. Add an sg availability check in Step 1 (after gathering context), matching
   doc-quality-audit's pattern:
   ```bash
   command -v sg >/dev/null 2>&1 && echo "sg available" || echo "sg not found"
   ```
   - If not found: note it (same friendly message doc-quality-audit uses)
   - If found: proceed silently

2. Update Key Reminder #9 to reflect the two-tier model: "Use sg when available
   for structural searches (see framework sections for supported patterns); fall
   back to rg/grep when sg cannot express the pattern or sg is not installed."

3. For existing sg examples (Cobra/Go Task 1 and Task 2): keep them, but frame
   them as "if sg available" consistently (they already do this, verify wording).

---

## 4. Add version/spec keyword validity check to doc-accuracy-audit

**File:** `skills/doc-accuracy-audit/SKILL.md`

**Problem:** doc-accuracy-audit explicitly audits OpenAPI specs and Terraform
schemas, yet has no rule requiring verification that a keyword or feature is
valid for the declared spec version. A finding could confidently report a schema
mismatch without checking whether the keyword is even valid for the declared
draft/version — producing wrong causal explanations.

This was a documented failure mode in code-intel testing: an agent reported
`unevaluatedProperties` as effective in a draft-07 schema (it is draft-2019-09+
only, silently ignored by conforming validators).

**Action:** Add to Strict Adherence section (after Uncertainty Labeling):

> **Version/spec keyword validity:** Before asserting that a schema keyword,
> API parameter, or library method is effective or enforced, verify it is
> supported by the declared version or spec in use. Check the version declaration
> first (`$schema`, OpenAPI `openapi:` field, framework version in manifest).
> If a keyword or parameter is present but unsupported by the declared version,
> state it explicitly: "This keyword is not valid in [declared version] and will
> be silently ignored — its presence does not enforce the intended constraint."
> Do not infer behavior from presence alone.

Key draft/version boundaries to note:
- JSON Schema draft-07: `additionalProperties`, `if/then/else`, `contains`, `const`
- JSON Schema draft-2019-09+: `unevaluatedProperties`, `unevaluatedItems`
- JSON Schema draft-2020-12+: `prefixItems`
- OpenAPI 3.0 vs 3.1: nullable handling differs; 3.1 adopts JSON Schema draft-2020-12

---

## 5. Add spot-check threshold to doc-quality-audit

**File:** `skills/doc-quality-audit/SKILL.md`

**Problem:** doc-quality-audit's Verify Before Delivering Report has 3 checks
but no scope-based threshold — it runs the same 3 checks regardless of whether
the audit covers 2 files or 200. doc-accuracy-audit uses an explicit `>50 items`
threshold. code-intel uses `>20 files / >10 grep result sets`.

**Action:** Add a scope gate to doc-quality-audit's Verify section (before
check 1 Quote Traceability):

> **Execution mode:** If auditing ≤30 files, run all 3 checks on all findings.
> If >30 files, run checks 1 and 3 on High Confidence findings only (spot-check
> mode). Always run check 2 (Confidence Calibration) in full — it is fast and
> high-leverage.

Threshold of 30 is a suggested starting point; adjust based on observed
performance.

---

## 6. Permission gate for doc-accuracy-audit (design decision)

**File:** `skills/doc-accuracy-audit/SKILL.md`

**Problem:** code-intel Step 4 presents a user-facing permission gate — it lists
the commands it plans to run and asks A/B/C approval before executing anything.
doc-accuracy-audit runs its framework detection silently and proceeds to grep/rg
without any equivalent approval step.

**Question for the team:** Is an explicit permission gate appropriate for
doc-accuracy-audit? Arguments:

- **Add it:** Consistent with code-intel interaction model. Gives users visibility
  into what's being searched and control over scope.
- **Skip it:** doc-accuracy-audit already has an extensive Step 1 (context
  gathering) and Step 2 (scope confirmation) that serves a similar purpose. A
  third gate before execution may feel redundant.

**No action required until decision is made.** Note here for discussion.

---

## Summary

| # | File | Effort | Type |
|---|------|--------|------|
| 1 | doc-accuracy-audit | Low | Add inline definition |
| 2 | doc-accuracy-audit | Low | Add rule + verify check |
| 3 | doc-accuracy-audit | Low | Add availability check, update Key Reminder #9 |
| 4 | doc-accuracy-audit | Low | Add rule to Strict Adherence |
| 5 | doc-quality-audit | Low | Add scope gate to Verify section |
| 6 | doc-accuracy-audit | — | Design decision, discuss first |
