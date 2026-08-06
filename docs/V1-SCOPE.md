# v1 Scope: CLI Tools Only

## What v1 Covers

**Supported project types:**
- CLI tools with documentation

**Supported CLI frameworks (auto-detected):**
- Python: argparse, Click
- Go: Cobra
- Bash: function-based command dispatch

**Accuracy audit checks:**
- Command tree: documented commands vs code (ghost, hidden, verified)
- Flags/arguments: documented flags vs code (ghost, hidden, mismatches in defaults, types, constraints)
- Upstream vs downstream docs alignment (optional)
- Semantic logic validation (documented behavior vs code implementation)

**Quality audit checks:**
- Tone/voice consistency
- Clarity/readability (plain language compliance)
- Structure/flow
- Consistency (terminology, formatting)
- Completeness
- Audience appropriateness
- Example quality

## What v1 Does NOT Cover

**Deferred to v2:**
- Terraform provider schemas
- OpenAPI/Swagger specifications
- Configuration file schemas (pyproject.toml, ansible.cfg, etc.)
- TypeScript CLI frameworks (Commander.js)
- Extension/VSCode plugin documentation
- API documentation (GraphQL, REST without OpenAPI)

## Why CLI Tools First?

1. **Clear source of truth:** Code is the definitive source; docs are secondary
2. **Deterministic patterns:** Command registration and flag definition are structural and consistent
3. **Auto-detection works:** Framework detection is reliable (tested on 3 real repos)
4. **High value:** Many open-source projects use argparse/Cobra/Bash
5. **Verification is straightforward:** Grep/rg patterns are reliable; no complex spec parsing needed

## Example Use Cases (v1)

### ✓ Works: Kubernetes CLI (kubectl)
- Source: https://github.com/kubernetes/kubernetes (Cobra/Go)
- Docs: https://kubernetes.io/docs/reference/kubectl/
- Audit: Commands registered via `AddCommand()`, flags via `Flags().StringVar()`, etc.

### ✓ Works: Ansible Creator
- Source: ~/projects/ansible-creator (argparse/Python)
- Docs: docs/ directory with command documentation
- Audit: Parsers via `ArgumentParser()`, args via `add_argument()`, etc.

### ✓ Works: dotpkg
- Source: ~/projects/dotpkg (Bash function dispatch)
- Docs: README with command descriptions
- Audit: Commands via `cmd_*()` functions, options via `case` statements

### ✗ Does NOT work: AWS Provider
- Source: terraform-provider-aws (Go schemas)
- Docs: Terraform Registry
- Audit: Would require v2 schema parsing (deferred)

### ✗ Does NOT work: OpenAPI Pet Store
- Source: OpenAPI 3.0 YAML spec
- Docs: Auto-generated API docs
- Audit: Would require v2 spec parsing (deferred)

## Using the Skills

### Accuracy Audit (CLI tools only)

```bash
/doc-accuracy-audit <docs-path> --source <code-path>
```

Skill auto-detects CLI framework and runs appropriate patterns.

Example:
```bash
/doc-accuracy-audit docs/ --source ~/projects/ansible-creator
# Auto-detects: argparse
# Finds: 47 ArgumentParsers, 51 add_argument calls
# Compares to docs, reports ghost/hidden/mismatch findings
```

### Quality Audit (works on ANY docs)

```bash
/doc-quality-audit <docs-path>
```

No source code needed. Audits style, tone, clarity, completeness, etc.

Example:
```bash
/doc-quality-audit docs/
# Checks: tone shifts, long sentences, unclear phrasing, etc.
# Works on any markdown/rst/txt documentation
```

### Quality Check (accuracy + quality for CLI tools)

```bash
/doc-quality-check docs/ --source ~/path/to/code
```

Runs both audits in sequence, then offers revisions.

## Testing v1 Features

All features tested on real repositories:

| Feature | Test Repo | Result |
|---------|-----------|--------|
| argparse detection | ansible-creator | ✓ 47 files, high confidence |
| Cobra detection | kubectl | ✓ 78 files, high confidence |
| Bash detection | dotpkg | ✓ 8 cmd_* functions, medium confidence |
| Pattern execution | All three | ✓ Finds expected constructs |
| Verification passes | All three | ✓ Prevents hallucination |
| Quality audit | Any docs | ✓ Checks tone, clarity, consistency |

## Migration to v2

When v2 adds Terraform and OpenAPI support:

1. No changes to CLI audit behavior (backward compatible)
2. New auto-detection for Terraform providers and OpenAPI specs
3. New pattern sets and verification logic for schemas
4. Existing CLI skills remain unchanged

v1 users can upgrade without re-running existing audits.
