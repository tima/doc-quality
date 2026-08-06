# Test Scenarios: doc-accuracy-audit Skill

Validation test cases for each CLI framework. Run these to confirm skill works end-to-end.

---

## Test 1: argparse (Python)

**Repo:** ansible-creator  
**Path:** ~/projects/ansible-creator  
**Doc path:** ~/projects/ansible-creator/docs/installing.md  
**Framework:** Python argparse (47 files)  
**Expected outcome:** Detect argparse, find argument definitions, compare to docs

**Manual setup:**
```bash
# Verify detection
python3 skills/doc-accuracy-audit/lib/detect-cli-framework.py ~/projects/ansible-creator
# Should output: "framework": "argparse", "confidence": "high"

# Run test patterns
bash skills/doc-accuracy-audit/lib/test-patterns.sh ~/projects/ansible-creator
# Should find: 47 ArgumentParsers, 51 add_argument calls, 5 subparsers
```

**Expected findings:**
- `--force` flag: documented in docs/installing.md, defined in arg_parser.py ✓ VERIFIED
- `--no-ansi` flag: documented, in arg_parser.py ✓ VERIFIED
- `init collection` command: documented, defined in _init_collection() ✓ VERIFIED

**Test assertion:**
- Skill detects argparse automatically (no manual framework selection)
- Skill finds command tree and flags using rg/grep patterns
- Verification pass confirms all findings cite grep evidence
- Report shows correct verdicts (Verified, not Ghost/Hidden)

---

## Test 2: bash-dispatch (Bash)

**Repo:** dotpkg  
**Path:** ~/projects/dotpkg  
**Doc path:** README.md (infer from code comments, no formal docs)  
**Framework:** Bash function dispatch (cmd_* functions)  
**Expected outcome:** Detect bash-dispatch, find command functions, verify against code comments

**Manual setup:**
```bash
# Verify detection
python3 skills/doc-accuracy-audit/lib/detect-cli-framework.py ~/projects/dotpkg
# Should output: "framework": "bash-dispatch", "confidence": "medium"

# Run test patterns
bash skills/doc-accuracy-audit/lib/test-patterns.sh ~/projects/dotpkg
# Should find: 4 cmd_ functions, 16 case statements
```

**Expected findings (from dotpkg script):**
- `cmd_init`: defined in dotpkg ✓ VERIFIED
- `cmd_add`: defined in dotpkg ✓ VERIFIED
- `cmd_sync`: defined in dotpkg ✓ VERIFIED
- `cmd_status`: defined in dotpkg ✓ VERIFIED
- `cmd_list`: defined in dotpkg ✓ VERIFIED
- `cmd_update`: defined in dotpkg ✓ VERIFIED
- `cmd_create`: defined in dotpkg ✓ VERIFIED
- `cmd_adopt`: defined in dotpkg ✓ VERIFIED

**Test assertion:**
- Skill detects bash-dispatch automatically
- Skill finds all 8 cmd_* functions
- No ghost commands (all commands exist in code)
- Verification pass confirms function names via grep

---

## Test 3: Cobra (Go)

**Repo:** kubectl (staging copy)  
**Path:** /tmp/kubectl-src/staging/src/k8s.io/kubectl/pkg/cmd  
**Doc path:** https://kubernetes.io/docs/reference/kubectl/kubectl/ (or local copy)  
**Framework:** Go Cobra (78 files with AddCommand)  
**Expected outcome:** Detect cobra-go, find command registrations, verify against official docs

**Manual setup:**
```bash
# Verify detection
python3 skills/doc-accuracy-audit/lib/detect-cli-framework.py /tmp/kubectl-src/staging/src/k8s.io/kubectl/pkg/cmd
# Should output: "framework": "cobra-go", "confidence": "high"

# Run test patterns
bash skills/doc-accuracy-audit/lib/test-patterns.sh /tmp/kubectl-src/staging/src/k8s.io/kubectl/pkg/cmd
# Should find: 78 AddCommand calls, 834 Flags() references
```

**Expected findings (sample):**
- `kubectl init` command: defined in cmd.go (AddCommand), documented ✓ VERIFIED
- `kubectl apply` command: documented, in apply.go ✓ VERIFIED
- `--verbose` flag: documented, defined via Flags().BoolVar() ✓ VERIFIED

**Test assertion:**
- Skill detects cobra-go automatically
- Skill finds all AddCommand registrations
- Skill finds flag definitions via Flags() patterns
- Verification pass cites rg results for each finding

---

## Test 4: Verification Pass (Traceability)

**Purpose:** Confirm verification pass catches hallucinations

**Scenario:** Create a fake finding without evidence
```
**GHOST ITEM (High Confidence):** --fake-flag documented but not in code
(No citation. Where was it searched? How many matches?)
```

**Expected behavior:**
1. Verification pass detects: no search result cited
2. Finding is REMOVED or downgraded to Low Confidence with "Needs manual verification"
3. Report output shows zero ghost items for --fake-flag

**Test assertion:**
- Verification pass prevents uncited claims
- All findings in final report cite evidence
- Example citation format: `(searched: rg '\\.AddCommand\\(' . — 78 matches)`

---

## Test 5: Verification Pass (Direction Accuracy)

**Purpose:** Confirm "Docs say X, Code says Y" is correct direction

**Scenario:** Flag --config documented as "optional", but code shows `Required: true`

**Expected behavior:**
1. Finding states:
   - **Doc Claim:** Optional flag
   - **Source of Truth:** Required: true (from arg_parser.py)
2. Verdict: Mismatch (with correct direction)

**Test assertion:**
- Finding correctly identifies code as source of truth (right side)
- No inverted verdicts
- Doc claim vs code evidence are on correct sides

---

## Test 6: Exclusivity Gate

**Purpose:** Confirm "missing" claims require 0-result search evidence

**Scenario:** Auditor claims "--profile flag not found in code"

**Expected behavior (before verification pass):**
- Finding: "Hidden item: --profile flag not in source"
- NO citation

**Expected behavior (after verification pass):**
- Finding is REMOVED, or
- Finding is updated to include: `(searched: rg 'profile' src/ — 0 matches across 45 Python files)`

**Test assertion:**
- Exclusivity gate blocks bare "not found" claims
- Claims require search command + result count in citations

---

## Phase 3 Checklist

- [ ] Test 1 (argparse): Manual run on ansible-creator passes
- [ ] Test 2 (bash-dispatch): Manual run on dotpkg passes
- [ ] Test 3 (cobra-go): Manual run on kubectl passes
- [ ] Test 4 (verification traceability): Fake finding removed
- [ ] Test 5 (verification direction): Direction correct
- [ ] Test 6 (exclusivity gate): Zero-match searches cited
- [ ] All evals pass structural validation (json -c on evals.json)
- [ ] Skill calls detect-cli-framework.py automatically (no manual selection)
- [ ] Report includes framework detection result + patterns used
