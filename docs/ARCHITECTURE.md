# Architecture: Multi-Type Code Structure Auditing

## Overview

doc-accuracy-audit now supports auditing three types of code projects:
1. **CLI Tools** (argparse, Cobra, Click, Bash)
2. **Python Libraries** (classes, functions, public API)
3. **VS Code Extensions** (commands, settings, contributions)

Each type has a dedicated pattern set for finding ghost items (documented but missing), hidden items (exist but undocumented), and detail mismatches.

---

## Code Structure Detection

### Detection Flow

```
code path
  ↓
detect_project_type()
  ├─→ Check for package.json + "contributes" → vscode-extension
  ├─→ Check for CLI framework markers → cli
  ├─→ Check for Python package markers → python-library
  └─→ Default → cli
```

**Key insight:** CLI framework detection runs BEFORE Python library checks. This ensures projects with both pyproject.toml and ArgumentParser (like ansible-creator) are correctly identified as CLI tools.

### Type Identification Heuristics

| Type | Detected By | Confidence |
|------|-------------|-----------|
| **vscode-extension** | package.json with "contributes" or "activationEvents" | high |
| **cli** | ArgumentParser, @click, AddCommand, or cmd_* patterns | high/medium |
| **python-library** | setup.py, pyproject.toml, or __init__.py (if no CLI markers) | high/medium |

---

## Pattern Sets by Type

### CLI Tools (detect-cli-framework.py)

**Cobra/Go:**
```bash
Commands:    grep -r 'AddCommand(' --include='*.go'
Flags:       grep -r '.Flags()' --include='*.go'
```

**argparse (Python):**
```bash
Parsers:     grep -r 'ArgumentParser' --include='*.py'
Arguments:   grep -r 'add_argument(' --include='*.py'
```

**Click (Python):**
```bash
Commands:    grep -r '@click\.(command|group)' --include='*.py'
Options:     grep -r '@click\.(option|argument)' --include='*.py'
```

**Bash:**
```bash
Commands:    grep -r '^cmd_' --include='*.sh'
Dispatch:    grep -r 'case' --include='*.sh' | grep ' in'
```

### Python Libraries

**Classes:**
```bash
grep -r '^class ' --include='*.py'
```

**Functions (top-level, non-private):**
```bash
grep -r '^def [^_]' --include='*.py' | grep -v '    def'
```

**Public API (explicit exports):**
```bash
grep -r '__all__' --include='*.py'
```

### VS Code Extensions

**Commands (in package.json):**
```bash
grep '"commands"' package.json
```

**Command registrations (in TypeScript):**
```bash
grep -r 'registerCommand' --include='*.ts'
```

**Settings:**
```bash
grep '"configuration"' package.json
```

**Activation:**
```bash
grep '"activationEvents"' package.json
```

---

## Audit Tasks by Type

### CLI Tools

1. **Inventory:** Command tree (commands, subcommands) vs docs
2. **Details:** Flags, arguments, defaults, types, constraints
3. **Alignment:** Upstream vs downstream docs
4. **Validation:** Trace command through code, verify behavior

### Python Libraries

1. **Inventory:** Classes, functions, public API (__all__) vs docs
2. **Details:** Method signatures, return types, exceptions
3. **Alignment:** Package docs vs API docs, class docs vs implementation
4. **Validation:** Verify class instantiation examples, function calls

### VS Code Extensions

1. **Inventory:** Registered commands vs docs
2. **Details:** Command parameters, settings schema, activation events
3. **Alignment:** package.json + TypeScript consistency
4. **Validation:** Verify command registration, setting defaults, activation

---

## Zero-Hallucination Verification

All findings go through a verification pass before report output:

### Traceability Check
Every finding must cite search evidence:
- CLI: Search command + match count (e.g., `grep -r 'AddCommand' — 78 matches`)
- Library: grep command + match count (e.g., `grep -r '^class ' — 655 matches`)
- Extension: Search in package.json or TypeScript (e.g., `registerCommand — 60 matches`)

### Direction Accuracy
"Docs say X, Source says Y" is always stated with source as right-hand side (source of truth).

### Exclusivity Gate
Claims of "missing" or "absent" must cite 0-result searches with command + scope (e.g., `searched: grep 'flag-name' src/ — 0 matches across 47 Python files`).

---

## File Structure

```
skills/doc-accuracy-audit/
├── SKILL.md                          # Skill definition (updated for 3 types)
├── lib/
│   ├── detect-cli-framework.py       # Multi-type detector
│   ├── test-patterns.sh              # Pattern validation script
│   └── run-cli-audit.sh              # Orchestration script
├── evals/
│   └── evals.json                    # Test cases for verification
└── test-scenarios.md                 # Manual validation checklist

docs/
├── V1-SCOPE.md                       # v1 coverage (3 types)
├── PATTERN-DISCOVERY.md              # Pattern reference
└── ARCHITECTURE.md                   # This file
```

---

## Implementation Details

### detect-cli-framework.py

**Main entry point:** `detect_code_structure(code_path)`

Returns JSON with:
```json
{
  "type": "cli|python-library|vscode-extension",
  "framework": "argparse|cobra-go|click|bash-dispatch|python-library|vscode-extension",
  "confidence": "high|medium|low",
  "patterns": { ... },
  "message": "Human-readable result"
}
```

**Key functions:**
- `detect_project_type()`: Determines type (CLI first, then library, then extension)
- `detect_cli_framework()`: Identifies CLI framework via grep markers
- `detect_python_library()`: Counts classes/functions, checks __all__
- `detect_typescript_extension()`: Checks package.json + TypeScript source
- `get_patterns_for_type()`: Returns audit patterns for the detected type

### test-patterns.sh

Validates that detected patterns find expected constructs.

**Usage:**
```bash
bash test-patterns.sh <repo-path>
# Output: Pass/fail for each pattern on the repo
```

---

## Testing

### Validated on Real Projects

| Project | Type | Detection | Patterns |
|---------|------|-----------|----------|
| ansible-creator | CLI (argparse) | ✓ high confidence | ✓ 47 parsers, 51 arguments |
| django-ansible-base | Library | ✓ high confidence | ✓ 655 classes, 1867 functions |
| vscode-ansible | Extension | ✓ high confidence | ✓ 60 commands, contributes found |
| dotpkg | CLI (bash) | ✓ medium confidence | ✓ 8 cmd_* functions |
| kubectl | CLI (cobra) | ✓ high confidence | ✓ 78 AddCommand matches |

### Test Scenarios

See `test-scenarios.md` for:
- Test 1-6: CLI framework auditing + verification passes
- Test 7: Python library auditing (django-ansible-base)
- Test 8: VS Code extension auditing (vscode-ansible)

---

## Migration Path to v2

When v2 adds Terraform and OpenAPI support:

1. New detection logic for Terraform schema patterns + OpenAPI spec parsing
2. New pattern sets for Terraform resources/attributes and API endpoints/parameters
3. Backward compatibility: CLI, library, extension audits unchanged
4. All skills remain CLI/library/extension compatible in v2

---

## Edge Cases & Limitations

### Ambiguous Projects
- **Small Python projects with setup.py:** Correctly detected as CLI if ArgumentParser found
- **Monorepos with multiple types:** Detection runs on specified path; user can point to CLI subfolder, library root, or extension directory

### Pattern Reliability
- Grep-based patterns are reliable for syntactic matching (class/function names, decorators, registrations)
- More complex semantic verification (method signatures, parameter defaults) requires additional manual inspection
- Examples: Click decorators, Cobra command nesting, TypeScript imports

### Documentation Mismatch
- Public API detection (__all__ for libraries, contributes for extensions) may not capture all exported symbols
- Private/internal functions/commands are correctly filtered by patterns (start with _ or aren't registered)
- Users can supplement with manual code review for undocumented internal API

---

## Future Enhancements

### v1.x
- Add TypeScript/JavaScript CLI (Commander.js, yargs)
- Improve library detection for compiled languages (Go, Rust)
- Add configuration schema auditing (pyproject.toml, setup.cfg, ansible.cfg)

### v2
- Terraform provider schema parsing
- OpenAPI/Swagger spec parsing
- GraphQL schema parsing
- Protocol buffer schema parsing

### v3+
- Machine learning for semantic correctness (behavior matching)
- Cross-reference external API docs (imported libraries)
- Automated example generation and validation
