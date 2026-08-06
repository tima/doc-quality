# v1 Scope: CLI Tools, Libraries, and Extensions

## What v1 Covers

**Supported project types (auto-detected):**

1. **CLI Tools**
   - Python: argparse, Click
   - Go: Cobra
   - Bash: function-based command dispatch

2. **Python Libraries**
   - Classes, functions, public API exports (__all__)
   - setup.py, pyproject.toml, or __init__.py based detection

3. **VS Code Extensions**
   - Registered commands (registerCommand)
   - Settings/configuration points
   - Activation events (package.json)

**Accuracy audit checks (framework-specific):**

| Type | Checks |
|------|--------|
| CLI | Command tree, flags/arguments, defaults, types, semantic behavior |
| Library | Classes/functions vs docs, method signatures, return types, exceptions, public API |
| Extension | Registered commands, settings, schemas, activation logic |

**Quality audit checks (all types):**
- Tone/voice consistency
- Clarity/readability (plain language compliance)
- Structure/flow
- Consistency (terminology, formatting)
- Completeness
- Audience appropriateness
- Example quality

## What v1 Does NOT Cover

**Deferred to v2:**
- Schema-based auditing: Infrastructure-as-code (IaC) providers, APIs (OpenAPI/Swagger/GraphQL), configuration specs
- TypeScript CLI frameworks (Commander.js)
- Additional CLI frameworks beyond v1 scope

**Future exploration:**
- Ansible playbooks, roles, execution environments, collections — See [../EXPLORATION-ANSIBLE-AUDITING.md](../EXPLORATION-ANSIBLE-AUDITING.md) for research on feasibility and patterns

## Why These Three in v1?

1. **Clear source of truth:** Code is definitive; docs are secondary (unlike specs/schemas)
2. **Deterministic patterns:** Registration and exports are structural and consistent
3. **Auto-detection works:** Type detection tested on 3 real projects (django-ansible-base, vscode-ansible, abbenay)
4. **High value:** Covers libraries, CLI tools, and extensions — major open-source categories
5. **Verification is straightforward:** Grep/rg patterns reliable; no complex spec parsing needed

## Example Use Cases (v1)

### CLI Tools

#### ✓ Works: Kubernetes CLI (kubectl)
- Source: https://github.com/kubernetes/kubernetes (Cobra/Go)
- Docs: https://kubernetes.io/docs/reference/kubectl/
- Audit: Commands via `AddCommand()`, flags via `Flags().StringVar()`, etc.

#### ✓ Works: Ansible Creator
- Source: ~/projects/ansible-creator (argparse/Python)
- Docs: docs/ directory with command documentation
- Audit: Parsers via `ArgumentParser()`, args via `add_argument()`, etc.

#### ✓ Works: dotpkg
- Source: ~/projects/dotpkg (Bash function dispatch)
- Docs: README with command descriptions
- Audit: Commands via `cmd_*()` functions, options via `case` statements

### Python Libraries

#### ✓ Works: django-ansible-base
- Source: ~/projects/django-ansible-base (655 classes, 1867 functions)
- Docs: docs/ directory with API reference
- Audit: Classes, functions, __all__ exports vs documentation

#### ✓ Works (small): abbenay
- Source: ~/projects/abbenay (13 classes, 3 functions)
- Docs: docs/ and README with class documentation
- Audit: Library structure detection, public API verification

### VS Code Extensions

#### ✓ Works: vscode-ansible
- Source: ~/projects/vscode-ansible (339 TypeScript files, 60 commands)
- Docs: README, wiki with command reference
- Audit: Registered commands via `registerCommand()`, settings in package.json

### Not Yet Supported (v2)

### ✗ Does NOT work: Schema-based Auditing (v2)
- Examples: IaC providers, API specs, configuration schemas
- Issue: Requires schema parsing + semantic validation (deferred to v2)

## Using the Skills

### Accuracy Audit (CLI, Library, Extension)

```bash
/doc-accuracy-audit <docs-path> --source <code-path>
```

Skill auto-detects project type and runs appropriate patterns.

**CLI example:**
```bash
/doc-accuracy-audit docs/ --source ~/projects/ansible-creator
# Auto-detects: argparse CLI
# Finds: 47 ArgumentParsers, 51 add_argument calls
# Reports ghost/hidden/mismatch findings
```

**Library example:**
```bash
/doc-accuracy-audit docs/ --source ~/projects/django-ansible-base
# Auto-detects: Python library (655 classes, 1867 functions)
# Finds: documented classes vs code, method signatures
# Reports missing/undocumented classes and functions
```

**Extension example:**
```bash
/doc-accuracy-audit docs/ --source ~/projects/vscode-ansible
# Auto-detects: VS Code extension (60 registered commands)
# Finds: documented commands, settings, activation events
# Reports mismatches between package.json and docs
```

### Quality Audit (works on ANY docs)

```bash
/doc-quality-audit <docs-path>
```

No source code needed. Audits style, tone, clarity, completeness, etc. Works on CLI, library, extension, or any other documentation.

Example:
```bash
/doc-quality-audit docs/
# Checks: tone shifts, long sentences, unclear phrasing, consistency
# Works on any markdown/rst/txt documentation for any project type
```

### Quality Check (accuracy + quality for all types)

```bash
/doc-quality-check docs/ --source ~/path/to/code
```

Runs both audits in sequence, then offers revisions. Works for CLI, library, or extension docs.

## Testing v1 Features

All features tested on real repositories:

| Feature | Test Repo | Result |
|---------|-----------|--------|
| argparse detection | ansible-creator | ✓ 47 files, high confidence |
| Cobra detection | kubectl | ✓ 78 files, high confidence |
| Bash detection | dotpkg | ✓ 8 cmd_* functions, medium confidence |
| Python library detection | django-ansible-base | ✓ 655 classes, 1867 functions, high confidence |
| VS Code extension detection | vscode-ansible | ✓ 339 TypeScript files, 60 commands, high confidence |
| Pattern execution (CLI) | All three CLI repos | ✓ Finds expected constructs |
| Pattern execution (Library) | django-ansible-base, abbenay | ✓ Class/function enumeration works |
| Pattern execution (Extension) | vscode-ansible | ✓ Command and setting detection works |
| Verification passes | All repos | ✓ Prevents hallucination |
| Quality audit | Any docs | ✓ Checks tone, clarity, consistency |

## Migration to v2

When v2 adds schema-based auditing (IaC, APIs, etc.):

1. No changes to CLI audit behavior (backward compatible)
2. New auto-detection for schema-based project types
3. New pattern sets and verification logic for schemas
4. Existing CLI skills remain unchanged

v1 users can upgrade without re-running existing audits.
