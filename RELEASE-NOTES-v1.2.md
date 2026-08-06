# doc-quality v1.2 Release Notes

**Release Date:** 2026-08-06  
**Status:** PRODUCTION READY

---

## Overview

doc-quality v1.2 provides comprehensive documentation accuracy and quality auditing for multiple code project types. Includes polyglot project detection fix, verification passes to prevent hallucination, and production validation on real-world projects.

---

## New in v1.2

### Polyglot Project Detection (Phase 3)

**Problem:** Multi-language projects misclassified based on secondary language markers (e.g., abbenay detected as Python library because of Python files, ignoring TypeScript primary type).

**Solution:** Root manifest priority tier system ensures primary language is detected correctly:

```
1. package.json at root (substantive: main/bin/dependencies) → TypeScript/JavaScript
2. go.mod → Go
3. Cargo.toml → Rust
4. setup.py/pyproject.toml → Python
5. CLI framework signatures (fallback)
6. Python library structure (fallback)
```

**Impact:** abbenay now correctly detected as `typescript-library` (was `python-library` in v1.1).

**Validation:** 5 real repositories tested, 100% correct detection, 0 regressions.

---

## Features (All Versions)

### Code Structure Auto-Detection

Automatically detects project type and framework without manual selection:

**Supported Types:**
- **CLI Tools** — Cobra (Go), argparse/Click (Python), Bash function dispatch
- **Python Libraries** — Classes, functions, public API (__all__ exports)
- **VS Code Extensions** — Commands, settings, contributions

**Detection Output:** `{type, framework, confidence, patterns}`

### Accuracy Auditing (doc-accuracy-audit)

Cross-reference documentation against source code to find:
- Ghost items (documented but not in code)
- Hidden items (in code but not documented)
- Mismatches (different values between docs and code)

**Verification Pass (6 checks):** Prevents uncited ghost claims, direction inversion, count mismatches, entity type confusion.

### Quality Auditing (doc-quality-audit)

Assess documentation across 10 quality dimensions:
- Tone/voice consistency
- Clarity/readability
- Structure/flow
- Consistency
- Completeness
- Audience appropriateness
- Examples quality
- Visual formatting
- SEO/accessibility
- Plain language compliance

**Verification Pass (3 checks):** Prevents paraphrased quotes, uncalibrated confidence, count mismatches.

---

## Known Limitations

### Semantic Type Detection
grep patterns cannot distinguish class vs function definitions. Documentation claiming a class when code implements a function (or vice versa) requires manual review.

**Mitigation:** Audit reports type mismatches for user review. AST-based detection planned for future release.

### Private vs Public Symbols
Patterns find all symbol definitions (public + private). Library audit cannot filter private symbols without `__all__` or naming conventions.

**Mitigation:** Check `__all__` exports or ignore symbols starting with `_` (underscore).

---

## Release Contents

### Skills
- `skills/doc-accuracy-audit/` — Full skill with 6-check verification pass
- `skills/doc-quality-audit/` — Full skill with 3-check verification pass
- Pattern detection libraries and test validation

### Documentation
- `docs/ARCHITECTURE.md` — Design reference for multi-type detection
- `docs/PHASE-1-2-VALIDATION.md` — End-to-end validation on real projects
- `docs/PHASE-1-3-QUALITY-AUDIT.md` — Quality audit on production docs
- `docs/PHASE-1A-2A-VERIFICATION-PASSES.md` — Verification pass procedures and validation
- `docs/VERIFICATION-PASSES-TEST-RESULTS.md` — Test results confirming passes prevent hallucination
- `docs/V1-SCOPE.md` — v1 scope and project type coverage
- `docs/PHASE-1-3-QUALITY-AUDIT-ABBENAY-CORRECTED.md` — Real-world audit correction example

### Configuration
- `CONFIG.md` — Zero-hallucination policy and style guide configuration

---

## Git History

```
v1.0 (baseline)    — CLI-only detection and auditing
v1.1               — Multi-type support (CLI, library, extension)
v1.1.1             — Verification passes added, tested, validated
v1.2               — Polyglot detection fix, real-world validation
```

**Total commits:** 24 logical commits with detailed messages
**Total lines:** 3000+ added across skills, docs, validation

---

## Validation

### Accuracy-Audit Verification Pass
✓ Traceability: Every finding cites grep/rg/sg result  
✓ Direction accuracy: Code is source of truth (right side)  
✓ Enumerated completeness: Summary counts match findings  
✓ Exclusivity gate: "Missing" claims require 0-result searches  
✓ Verdict consistency: No duplicate verdicts  
✓ Entity type naming: Commands/flags/resources labeled correctly  

### Quality-Audit Verification Pass
✓ Quote traceability: Current Text matches source verbatim  
✓ Confidence calibration: High Confidence requires rule citation  
✓ Count consistency: Summary matches findings tally  

### Real-World Testing
✓ 5 repositories tested (ansible-creator, django-ansible-base, vscode-ansible, abbenay, kubectl)  
✓ 100% correct detection, 0 regressions  
✓ Polyglot project (abbenay) correctly identified  
✓ Verification passes catch and correct false findings  

---

## Upgrade from v1.1

No breaking changes. v1.1 users can upgrade to v1.2 without modifying existing audits.

**Key Improvement:** Polyglot projects now detected correctly. Re-run audits on TypeScript/Python hybrid projects to get correct type classification.

---

## Quick Start

### Audit CLI Documentation
```
/doc-accuracy-audit path/to/docs --type cli --source /path/to/code
```

### Audit Library Documentation
```
/doc-accuracy-audit path/to/docs --type python-library --source /path/to/code
```

### Quality Check Documentation
```
/doc-quality-audit path/to/docs --dimensions clarity,completeness
```

---

## Support

Report issues or feedback at: [project repository]

---

## Metrics

| Metric | v1.0 | v1.1 | v1.2 |
|--------|------|------|------|
| Project types supported | 1 (CLI) | 3 | 3 |
| Verification passes | 0 | 2 | 2 |
| Test coverage | Basic | Comprehensive | Comprehensive |
| Polyglot support | No | Partial (buggy) | Yes (fixed) |
| Production ready | Yes | Yes | Yes |

---

**Release prepared:** 2026-08-06  
**Tag:** v1.2  
**Status:** Ready for production deployment
