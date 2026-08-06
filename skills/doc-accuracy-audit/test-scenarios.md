# Test Scenarios: doc-accuracy-audit Skill

Validation test cases for CLI tools, Python libraries, and VS Code extensions. Run these to confirm skill works end-to-end across all supported project types.

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

---

## Test 7: Python Library (django-ansible-base)

**Repo:** django-ansible-base  
**Path:** ~/projects/django-ansible-base  
**Doc path:** docs/ directory with API reference  
**Type:** Python library (655 classes, 1867 functions)  
**Expected outcome:** Detect python-library, find classes and functions, compare to docs

**Manual setup:**
```bash
# Verify detection
python3 skills/doc-accuracy-audit/lib/detect-cli-framework.py ~/projects/django-ansible-base
# Should output: "type": "python-library", "confidence": "high"

# Run test patterns
bash skills/doc-accuracy-audit/lib/test-patterns.sh ~/projects/django-ansible-base
# Should find: 655 class definitions, 1867 function definitions, 38 __all__ declarations
```

**Expected findings:**
- Classes documented in API reference exist in code ✓
- Methods listed for a class match class definition ✓
- Symbols in __all__ exports are documented ✓
- Undocumented public functions (helper library) reported as hidden

**Test assertion:**
- Skill detects python-library automatically
- Skill finds class/function definitions using grep patterns
- Verification pass confirms all findings cite grep evidence
- Report distinguishes between classes and functions

---

## Test 8: VS Code Extension (vscode-ansible)

**Repo:** vscode-ansible  
**Path:** ~/projects/vscode-ansible  
**Doc path:** README.md + docs/commands.md  
**Type:** VS Code extension (60 registered commands)  
**Expected outcome:** Detect vscode-extension, find commands/settings, compare to docs

**Manual setup:**
```bash
# Verify detection
python3 skills/doc-accuracy-audit/lib/detect-cli-framework.py ~/projects/vscode-ansible
# Should output: "type": "vscode-extension", "confidence": "high"

# Run test patterns
bash skills/doc-accuracy-audit/lib/test-patterns.sh ~/projects/vscode-ansible
# Should find: contributes declaration, activationEvents, 60 registerCommand calls
```

**Expected findings:**
- Commands in package.json "contributes.commands" exist in code ✓
- Command IDs match between docs and package.json ✓
- Settings in contributes.configuration documented ✓
- Undocumented activation events reported as hidden

**Test assertion:**
- Skill detects vscode-extension automatically
- Skill finds contributions in package.json
- Skill finds registerCommand calls in TypeScript
- Verification pass cites grep results for each command

---

## Phase 3 Checklist

### CLI Tests
- [ ] Test 1 (argparse): Manual run on ansible-creator passes
- [ ] Test 2 (bash-dispatch): Manual run on dotpkg passes
- [ ] Test 3 (cobra-go): Manual run on kubectl passes

### Library & Extension Tests (NEW)
- [ ] Test 7 (python-library): Manual run on django-ansible-base passes
- [ ] Test 8 (vscode-extension): Manual run on vscode-ansible passes

### Verification Tests
- [ ] Test 4 (verification traceability): Fake finding removed
- [ ] Test 5 (verification direction): Direction correct
- [ ] Test 6 (exclusivity gate): Zero-match searches cited

### Final Checks
- [ ] All evals pass structural validation (json -c on evals.json)
- [ ] Skill calls detect-cli-framework.py automatically (no manual selection)
- [ ] Detection works for CLI, library, and extension types
- [ ] Report includes type detection result + patterns used
- [ ] Quality-audit works on any project type (no code dependency)
