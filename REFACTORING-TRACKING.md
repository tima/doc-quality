# Refactoring Tracking: Writing-for-Agents Review

**Review date:** 2026-08-06  
**Framework:** mattpocock-skills:writing-for-agents

---

## Completed (HIGH Priority)

✓ **v2 scope isolation** — Removed Terraform/OpenAPI from Arguments, Step 1 context questions, type options  
✓ **Zero-Hallucination consolidation** — Single canonical in CONFIG.md, all skills reference  
✓ **Confidence Levels canonicalization** — Added to CONFIG.md, removed duplication from doc-quality-audit  
✓ **Severity Classification canonicalization** — Added to CONFIG.md, referenced from doc-quality-audit  
✓ **Phase summaries expansion** — doc-quality-revise Phase 1 expanded with auto-revisable/manual-review distinction  
✓ **v2 examples removal** — Terraform/OpenAPI examples moved out, CLI examples retained with forward reference  

**Impact:** ~80 lines removed from operational sections, single sources of truth established, v1 scope clarified.

---

## Backlog (MEDIUM Priority)

### M1: Auto-Revisable Criteria Definition
**File:** skills/doc-quality-revise/SKILL.md  
**Issue:** "Auto-revisable vs manual-review" mentioned but criteria is fuzzy. Users don't know which findings will be auto-handled.  
**Recommendation:** Inline explicit definition in Step 1 or Overview:
- Auto-revisable: single-line fixes (typo correction, formatting, style tag addition)
- Manual-review: rewrites >1 sentence, tone shifts, structural changes, context rework

**Related:** Phase 1 summary now hints at this distinction; formalize it.

---

### M2: Explicit Completion Criteria for All Steps
**Files:** All SKILL.md files  
**Issue:** Completion criteria are vague ("audit complete", "provide feedback") or missing. Invites premature completion.  
**Example from doc-accuracy-audit:**
- Step 4: "Execute the Audit" has no explicit close signal. Add: "All 4 tasks (or selected scope) complete when each task's findings are collected into findings list. Proceed to Step 5."
- Step 1: "Fallback Strategies" buried. Add to completion: "Do not proceed to Step 4 until all context Qs answered + user confirms scope."

**Recommendation:** Each step should end with: "Complete when: [checkable, exhaustive condition]"

---

### M3: Flag Interaction Clarity
**File:** skills/doc-quality-check/SKILL.md  
**Issue:** `--parallel` flag behavior not upfront. Users don't know it only applies when both accuracy + quality enabled.  
**Current:** Hidden in Step 3 "Run Pipeline Phases"  
**Recommendation:** Add to Arguments section:
- `--parallel` - Run accuracy + quality audits concurrently (if both enabled; note: parallelization skipped if `--skip-accuracy` or `--skip-quality` flags present)

Also clarify in Step 1 validation: "After flag parsing, determine which phases to run. If both audits enabled AND `--parallel`: set parallel=true. Else: serial execution."

---

### M4: Framework Detection Patterns Extraction
**File:** skills/doc-accuracy-audit/SKILL.md (lines 195-346)  
**Issue:** ~150 lines of framework-specific patterns inline in Step 4. Makes skill file bloated; patterns are reference, not procedural steps.  
**Current:** 6 frameworks (cobra-go, argparse, click, bash-dispatch, python-library, vscode-extension) with full task descriptions per framework  
**Recommendation:** Create `skills/doc-accuracy-audit/references/detection-patterns.md` with all 6 frameworks. Step 4 says: "See [detection-patterns.md](references/detection-patterns.md) for patterns matching [framework]."

---

## Backlog (LOW Priority)

### L1: Limitations Consolidation
**File:** skills/doc-accuracy-audit/SKILL.md (lines 739-771)  
**Issue:** "Limitations (v1.1)" section describes polyglot detection, semantic type detection, private vs public symbols. These are known constraints, not operational guidance.  
**Recommendation:** Move to CONFIG.md#known-issues or create docs/LIMITATIONS.md. Keep in skill only if users need to see it before running the skill.

---

### L2: Step Numbering Standardization
**Issue:** Some skills use "Step 1", some use "Phase 1", some mix "Step 1.1" + "Substep". Inconsistency across skills.  
**Recommendation:** Standardize on one convention (e.g., "Step N: [Name]", substeps as "Step N.[letter]: [Name]" or "Substep N.1: [Name]").

---

### L3: Leading Word Cleanup (Lower Impact)
**Identified in review but low yield:**
- "project type" appears 14x across skill. Context-specific, acceptable repetition.
- "source of truth" appears 22x. Meaningful repetition in procedural steps; collapsing would hurt clarity.
- "Framework auto-detection" vs "Detection" — mixed usage. Minor token save if collapsed; low priority.

**Recommendation:** Skip unless undertaking full token-optimization pass.

---

## Review Metrics

| Category | Count | Status |
|----------|-------|--------|
| HIGH (completed) | 6 | ✓ Done |
| MEDIUM (backlog) | 4 | — Review |
| LOW (backlog) | 3 | — Deferred |
| **Total** | **13** | — |

---

## Next Steps

1. **Before next review:** Implement M1-M3 when editing those skills for other reasons
2. **v1.2 milestone:** M4 (patterns extraction) useful when Terraform support lands; defer with clear TODO
3. **v2+ work:** L1-L3 can be batched into a broader refactor pass

**Rationale for deferral:** M2-M4 and L1-L3 require distributed changes across multiple files or would be disrupted by upcoming v2 work. M1 is quick; implement when touching doc-quality-revise next.

