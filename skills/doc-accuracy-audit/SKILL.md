---
name: doc-accuracy-audit
description: "Use when you need to cross-reference documentation against a source of truth — CLI source code, Python library source, VS Code extension source, Terraform provider schemas, or OpenAPI specs. Triggers on: 'audit docs against source', 'verify docs match code', 'find ghost commands', 'find undocumented classes', 'check for undocumented resources', 'compare docs to schema'."
---

# doc-accuracy-audit

Cross-reference documentation against source code, schemas, or specs to find ghost items, hidden items, and detail mismatches.

## Overview

You are a Senior Software Engineer and Technical Documentation Auditor. Your role is to perform a rigorous cross-reference audit between a project's source of truth and its published documentation, identifying discrepancies, ghost items (documented but don't exist), hidden items (exist but aren't documented), detail mismatches, and alignment issues between upstream and downstream documentation.

This skill supports multiple code project types in v1:

- **CLI Tools** (v1) -- Audit source code against CLI documentation
  - Supported frameworks: argparse (Python), Cobra (Go), Click (Python), Bash function dispatch
  - Checks: Commands, flags, arguments, defaults, subcommands
  - Auto-detects framework; no manual framework selection needed

- **Python Libraries** (v1) -- Audit source code against library documentation
  - Detects: Classes, functions, public API (__all__ exports)
  - Checks: Class definitions, method signatures, public functions, exported symbols
  - Auto-detects structure from setup.py, pyproject.toml, class/function counts

- **VS Code Extensions** (v1) -- Audit source code against extension documentation
  - Detects: Commands, settings, activation events, contributions
  - Checks: Registered commands (registerCommand), settings in package.json, contribution points
  - Auto-detects from package.json and TypeScript source

**Deferred to v2 (not yet implemented):**
- Terraform Providers -- Planned for future release
- OpenAPI/Swagger APIs -- Planned for future release

**Core principle:** Strict adherence to the "Zero-Hallucination Policy" -- if information is unavailable or you can't verify it, say so explicitly. Do not infer, guess, or bridge gaps with logical reasoning.

---

## Arguments

Optional flags:
- `--output <filename>` - Override default report filename (default: `{project-name}-accuracy-audit-YYYYMMDD-HHMM-UTC.md`)
- `--dry-run` - Display report without saving (preview mode)
- `--since <git-ref>` - Audit only files changed since git ref (incremental mode)
- `--type <cli|python-library|vscode-extension>` - Project type (skip type detection prompt). Terraform/OpenAPI support deferred to v2.
- `--source <path-or-url>` - Source of truth: code repo (skip source prompt)
- `--upstream <path-or-url>` - Upstream docs location (skip upstream prompt)
- `--downstream <path-or-url>` - Downstream/enterprise docs (skip downstream prompt)

**Usage:**
```
/doc-accuracy-audit path/to/docs
/doc-accuracy-audit path/to/docs --output custom-report.md
/doc-accuracy-audit path/to/docs --dry-run
/doc-accuracy-audit path/to/docs --since HEAD~3
/doc-accuracy-audit docs/cli/ --type cli --source https://github.com/org/repo
```

---

## Step 1: Gather Context

**Config file check:** Follow config loading procedure in [CONFIG.md](../../CONFIG.md#loading-doc-qualityyml). This skill uses fields: style_guide, incremental.*, output.path

Stop and ask the user for the following information. Do NOT proceed to the audit until you have this. **Skip any question already answered by inline flags** (--type, --source, --upstream, --downstream).

### Identify the Project Type

First, determine which type of project you are auditing (v1 support):

- **CLI Tool** -- A command-line tool with commands, subcommands, flags, and arguments
- **Python Library** -- A Python package with classes, functions, and public API exports
- **VS Code Extension** -- A TypeScript extension with commands, settings, and contributions

If `--type` flag provided, use that value. Otherwise, if the project type is not clear from the user's request, ask: "What type of project is this -- a CLI tool, a Python library, or a VS Code extension?"

**Note:** Terraform and OpenAPI auditing are deferred to v2. Users requesting those should see: "Terraform and OpenAPI auditing are planned for v1.2. For now, this skill supports CLI tools, Python libraries, and VS Code extensions."

### Context Questions by Type

**All project types:**

1. **Project Name** -- What are you auditing? (e.g., Podman, django-ansible-base, vscode-ansible, terraform-provider-aws, Acme API)
2. **Documentation** -- Link to official docs, or local path (can be same as source if docs are in the repo)
3. **Downstream Documentation (Optional)** -- Enterprise/product-specific docs, if applicable. User can state "None" or "N/A" if not relevant.

**CLI Tools -- additional questions:**

4. **Source Code Repository** -- Link to the repo, or local path if available

**Python Libraries -- additional questions:**

4. **Source Code Repository** -- Link to the repo, or local path if available
5. **Entry Points** -- If multiple setup.py/pyproject.toml files, which is the primary one to audit?

**VS Code Extensions -- additional questions:**

4. **Source Code Repository** -- Link to the repo, or local path if available
5. **TypeScript Source Path** -- Where is the main extension code? (e.g., src/, extension/), or auto-detect?

Ask these in a conversational way. If the user provides some but not all context, ask for the missing pieces.

**Incremental mode:** If `--since` flag present, follow incremental mode procedure in [CONFIG.md](../../CONFIG.md#incremental-mode---since).

---

## Step 2: Scope the Audit

Once you have the context, explain the full audit scope. The audit has 4 tasks that map to each project type:

| Task | CLI | Python Library | VS Code Extension | Terraform (v2) | API (v2) |
|------|-----|------------------|-------------------|-----------|----------|
| 1. Inventory | Command tree vs docs | Classes/functions vs docs | Commands/settings vs docs | Resource registry vs docs | Endpoint list vs docs |
| 2. Detail Audit | Flags, defaults, aliases | Method signatures, return types | Command params, settings schema | Schema attributes, types | Parameters, responses, auth |
| 3. Multi-Source Alignment | Upstream vs downstream docs | Package docs vs API docs | Marketplace vs docs site | Registry vs enterprise docs | Spec vs docs site |
| 4. Example Validation | Trace command through code | Validate class instantiation | Validate command registration | Validate HCL against schema | Validate examples against spec |

Present the 4 tasks using the labels appropriate to the project type.

**If incremental mode:** Show "Incremental audit will check only X changed files against source of truth"

Then ask: "Do you want the full audit, or would you like to focus on specific areas?"

If the project is large (100+ commands, resources, or endpoints), offer to start with primary items and skip edge cases.

---

## Step 3: Clarify Ambiguities

Before you start analyzing:

- If the prompt is too vague (e.g., "all CLIs in the repo", "all providers", "all APIs"), ask for clarification on which specific tool, provider, or API to audit.
- If terminology is ambiguous (e.g., "flag" vs "option", "attribute" vs "argument", "parameter" vs "field"), confirm definitions with the user.
- If the repo is huge or the docs are scattered, ask the user to prioritize (e.g., "focus on the `deploy` subcommand family", "focus on the `aws_instance` resource family", "focus on the `/users` endpoint family").

---

## Step 4: Execute the Audit

Perform the requested tasks.

**If incremental mode active:** Only audit files in `changed_files` list (see [CONFIG.md](../../CONFIG.md#incremental-mode---since)).

### Code Structure Auto-Detection

**For CLI, Python Library, and VS Code Extension project types** (skip for Terraform and API audits):

Automatically detect the project type and framework/structure in use. This eliminates manual guessing and selects the right patterns for code analysis.

**Detection process (silent, no user interaction):**

```bash
# Detect project type and framework from code path
python3 skills/doc-accuracy-audit/lib/detect-cli-framework.py <code-path>
```

Returns JSON with:
- `type`: Project type (cli, python-library, vscode-extension)
- `framework`: Detected framework name (cobra-go, argparse, click, bash-dispatch, python-library, vscode-extension)
- `confidence`: high/medium/low based on file count
- `patterns`: Search patterns to use for this type/framework
- `message`: Human-readable result

**If detection succeeds:** Use patterns from the appropriate section below (CLI, Python Library, or VS Code Extension).  
**If detection fails or unknown:** Ask user to clarify type; offer manual pattern selection.

### Source Search Tool

**For CLI, Python Library, and VS Code Extension project types** (skip for Terraform and API audits):

Search for source code patterns using text-based tools. `rg` (ripgrep) is preferred if available; `grep` is the fallback.

Check tool availability:

```bash
command -v rg >/dev/null 2>&1 && echo "rg available" || echo "Using grep"
```

**Recommended approach:**
1. Use `rg` patterns from the detected framework section below.
2. If `rg` not available, substitute `grep -n` patterns (shown in each section).

**Terraform and API audits:** Skip this check. Terraform schemas and API specs use specialized tools (grep/jq/yq) described in their respective audit sections.

#### Detected: cobra-go (Go CLI using Cobra)

**Task 1: Command Tree Comparison**

Commands are registered via `AddCommand()`:
```bash
rg '\.AddCommand\(' --type go
grep -n "AddCommand(" *.go  # if rg unavailable
```

**Task 2: Flag and Argument Audit**

Flags defined via `Flags().StringVar()`, `Flags().BoolVar()`, etc.:
```bash
rg '\.Flags\(\)\.(StringVar|BoolVar|IntVar)' --type go
rg '\.PersistentFlags\(\)\.' --type go
grep -n "\.Flags()" *.go  # if rg unavailable
```

**Tasks 3-4:** Follow standard CLI audit procedure (upstream vs downstream, semantic logic check).

---

#### Detected: argparse (Python CLI using argparse)

**Task 1: Command Tree Comparison**

Commands are registered via subparsers:
```bash
rg 'ArgumentParser\(' --type py
rg '\.add_subparsers\(' --type py
grep -n "ArgumentParser\|add_subparsers" *.py  # if rg unavailable
```

**Task 2: Flag and Argument Audit**

Arguments defined via `add_argument()`:
```bash
rg '\.add_argument\(' --type py
grep -n "add_argument" *.py  # if rg unavailable
```

**Tasks 3-4:** Follow standard CLI audit procedure.

---

#### Detected: click (Python CLI using Click)

**Task 1-2: Commands and Options**

Click uses decorators for commands and options:
```bash
rg '@click\.(command|group)\(' --type py
rg '@click\.(option|argument)\(' --type py
grep -n "@click\." *.py  # if rg unavailable
```

**Tasks 3-4:** Follow standard CLI audit procedure.

---

#### Detected: bash-dispatch (Bash CLI with function dispatch)

**Task 1: Command Tree Comparison**

Commands are defined as `cmd_*()` functions:
```bash
rg '^cmd_[a-z_]+\(' --include='*.sh' .
find . -type f ! -name '*.sh' -exec grep -l '^cmd_' {} \;  # includes executable bash scripts
grep -n "^cmd_" *.sh  # if rg unavailable
```

**Task 2: Flag and Argument Audit**

Flags parsed via case statements:
```bash
rg 'case\s+"\$1"\s+in' --type sh
grep -n "case.*\$1.*in" *.sh  # if rg unavailable
```

**Tasks 3-4:** Follow standard CLI audit procedure.

---

#### Detected: python-library (Python Library or Package)

**Task 1: Class and Function Inventory**

Classes and top-level functions are the public API:
```bash
rg '^class ' --type py | head -30  # or: grep -n "^class " *.py
rg '^def [^_]' --type py | head -30  # top-level functions (non-private)
```

Check for `__all__` declaration (explicit public API):
```bash
rg '__all__' --type py
grep -n "__all__" *.py
```

**Task 2: Signature and Export Audit**

For each class in docs, verify:
- Class exists in code with matching name
- Methods listed in docs are present in source
- Public functions (not starting with `_`) listed in docs exist

For each exported symbol (in `__all__` or docs), verify:
```bash
rg 'class ClassName' --type py
rg 'def function_name' --type py
```

**Tasks 3-4:** Follow standard audit procedure for library docs: check parameter descriptions, return types, exceptions match code.

---

#### Detected: vscode-extension (VS Code Extension)

**Task 1: Command and Setting Inventory**

Commands are registered in `package.json` and in source code:
```bash
grep '"commands"' package.json  # in contributes section
rg 'registerCommand' --type ts
```

Settings/configuration points:
```bash
grep '"configuration"' package.json
rg 'workspace\.getConfiguration' --type ts
```

**Task 2: Command and Setting Details**

For each command in docs, verify:
- Command ID exists in package.json `contributes.commands`
- Command registered via `registerCommand()` in source
- Title, description, category match declarations

For each setting in docs, verify:
- Setting ID exists in package.json `contributes.configuration`
- Default value documented matches schema default
- Type (string, boolean, number, etc.) matches docs

```bash
rg 'registerCommand\([\'"]' --type ts  # extract command IDs
grep -A2 '"id":' package.json | grep -E '(title|description|category)'
```

**Tasks 3-4:** Follow standard audit procedure for extension docs: check examples for registered commands, validate setting schemas.

---

Follow these **Strict Adherence Rules** religiously:

### Zero-Hallucination Policy

Follow the canonical policy in [CONFIG.md](../../CONFIG.md#zero-hallucination-policy).

For doc-accuracy-audit, tool results include: grep/rg search output, file reads (docs and source), schema inspection (for Terraform/API v2), Python AST parsing (library detection), and JSON/YAML parsing (config inspection). Every finding must cite at least one of these sources or be removed before report output.

### Contradiction Flagging

- If you find conflicting data (docs say X, source of truth says Y, examples show Z), do NOT try to reconcile.
- Present both sides and label: **"Conflicting Evidence: [source A says X, source B says Y]"**

### Uncertainty Labeling

- If a detail is based on a non-definitive source, prefix with: **"Unverified report suggests..."**
- Example: "Unverified report suggests the `timeout` parameter defaults to 30s, but this was not found in the source of truth."

### Ambiguity Stops

- If you encounter genuine ambiguity you can't resolve, stop and ask for clarification rather than guessing.

### Confidence Levels

Annotate all findings with confidence level based on verification method:

- **High Confidence** - Direct source verification, unambiguous evidence (e.g., flag in docs not found in code after thorough grep)
- **Medium Confidence** - Indirect evidence, minor ambiguity (e.g., default value differs between docs and code comments but code itself unclear)
- **Low Confidence** - Uncertain, requires manual review (e.g., could not parse argument definition, documentation ambiguous)

**Format:** `**FINDING TYPE (Confidence Level):** description`

**Examples:**
- `**GHOST ITEM (High Confidence):** --debug flag documented but not in source`
- `**POSSIBLE MISMATCH (Medium Confidence):** Default value differs (docs: 5, code: 10)`
- `**NEEDS REVIEW (Low Confidence):** Could not parse argument definition`

### Audit Execution by Project Type

Follow the subsection that matches the identified project type.

#### CLI Tools

**Task 1 -- Command Tree Comparison:**
Show progress: "Auditing commands... [Task 1/4]"
Read source code for command registration patterns (Cobra, argparse, Click, or framework-specific). List all registered commands and subcommands. Compare against the documented command list. Flag ghost commands (documented but not in code) and hidden commands (in code but not documented).

**For Cobra (Go) CLIs, if ast-grep available:**
```bash
ast-grep scan --inline-rules "id: addcmd
language: go
rule: {kind: call_expression, regex: AddCommand}" .
```
**Fallback (if ast-grep not available):**
```bash
rg '\.AddCommand\(' --type go
rg 'cobra\.Command{' --type go
```

**Task 2 -- Flag and Argument Audit:**
Show progress: "Auditing flags... [Task 2/4]"
For each command in scope, extract flags and arguments from source code: names, aliases, types, default values, constraints, required/optional status. Compare against documented flags. Flag naming mismatches, missing defaults, incorrect types, and undocumented constraints.

**For Cobra (Go) CLIs, if ast-grep available:**
```bash
ast-grep scan --inline-rules "id: flags
language: go
rule: {kind: call_expression, regex: '(StringVar|BoolVar|IntVar|StringP|BoolVarP|IntVarP)'}" .
```
**Fallback (if ast-grep not available):**
```bash
rg '\.Flags\(\)\.' --type go
rg '\.PersistentFlags\(\)\.' --type go
```

**Task 3 -- Upstream vs Downstream Alignment:**
Show progress: "Checking alignment... [Task 3/4]"
Compare claims between upstream (official/community) docs and downstream (enterprise/product) docs. Flag any downstream additions, removals, or contradictions not supported by the code. If no downstream docs, skip this task and note it.

**Task 4 -- Semantic Logic Check:**
Show progress: "Verifying behavior... [Task 4/4]"
Pick the most representative command (or let the user choose). Trace its execution path in the source code. Verify that the documented behavior (input handling, output format, error behavior, side effects) matches the implementation.

**Important:** Distinguish between actual code behavior and developer-stated intent (docstrings/comments). If a default value is documented:
- If found in **code** (e.g., `timeout := 30`): **Source of Truth:** code, behavior is verified.
- If found only in **docstring/comment** (e.g., `// defaults to 30s`): label as **Developer-Stated Intent (Not Verified):** [file:line]. Do NOT treat as verified behavior; note that the actual default requires manual code inspection.

---

**Terraform Providers and API Documentation** are deferred to v2. Placeholders removed to avoid confusion about v1 scope.

---

### Fallback Strategies

If you cannot access documentation or the source of truth:

1. State explicitly: "Cannot access [resource]. Information not found."
2. Ask user to provide: "Please provide the content of [file/URL] or paste the relevant section."
3. Offer manual commands: "Run these commands and share the output: [commands]"
4. Do NOT proceed with guesses or assumptions.

---

## Step 5: Format the Report

### Verify Before Writing Report

**[Silent — no output to user. Run before writing any section.]**

Before writing the audit report, perform these 6 verification checks. These prevent hallucination (claims without evidence).

**Execution mode:** If auditing ≤50 items, run all 6 checks. If >50 items, run checks 1, 3, 4 on High Confidence findings only (spot-check mode).

#### 1. Traceability

Every ghost/hidden/mismatch finding must cite a tool result — a grep match, rg output, file path, schema field, or 0-result search count. A finding with no cited evidence must be removed or downgraded to Low Confidence with "Needs manual verification."

Example citations:
- `(searched: rg '\.AddCommand\(' src/ — 0 matches)` 
- `(inspected: acme/resource_certificate.go line 142 — no Default field)`
- `(found: 47 matches for rg 'ArgumentParser' src/ )`

#### 2. Direction Accuracy

Re-read evidence for every "Docs say X, source says Y" claim. Direction inversion is common. The source of truth (code/spec) is always the right-hand side of "Source of Truth:". Flip any inverted claims.

Example: If docs claim "required" and code shows `Required: false`:
- **Wrong:** Doc Claim: Required | Source of Truth: Required field (inverted reading)
- **Correct:** Doc Claim: Required | Source of Truth: Optional (Required: false in schema)

Check every finding with "mismatch" or "differs" in its description.

#### 3. Enumerated Completeness

Tally findings by category (ghost, hidden, mismatch). Cross-check that summary counts match the section item counts exactly. Correct any discrepancy before writing the report.

Example:
```
Section Body: Lists 3 ghost items, 2 hidden items, 1 mismatch
Summary says: 3 ghost, 2 hidden, 1 mismatch ✓
(If summary says 4 ghost, correct it before output)
```

#### 4. Exclusivity Gate

Any finding claiming "missing", "absent", "not found", "only", "not in", or "not documented" must cite the search command and its result count inline. A 0-result search IS evidence (not a failure); gate only to prevent "missing" claims without proof.

Required format: `(searched: COMMAND — RESULT_COUNT matches)`

Example citations:
- `(searched: rg "flag-name" src/ — 0 matches across 45 Go files)`
- `(searched: sg --lang go -p '$PATTERN' . — 0 matches)`
- `(searched: grep -r "ResourceName" terraform/ — 0 lines)`

A finding stating "the --profile flag is not documented" MUST show: `(searched: rg '\..*profile' src/ — 0 matches)` or equivalent.

#### 5. Verdict Consistency

Scan the report for any item appearing under more than one verdict (e.g., same flag listed as both Ghost and Hidden). Remove duplicates; assign the verdict supported by the strongest evidence.

Example: If `--debug` appears as both Ghost and Hidden, keep only the one with clearer evidence and remove the duplicate.

#### 6. Named Entity Type

Commands are commands, flags are flags, resources are resources, attributes are attributes, endpoints are endpoints. Check that entity type labels in findings match what was actually found in the source.

Example:
- If a search found `def advisory_lock()`, it's a function, not a class. Don't label it "class AdvisoryLock."
- If a search found `registerCommand('acme.deploy')`, it's a command, not a setting. Label accordingly.

### File naming

- If `--output` flag is provided, use that filename exactly
- Otherwise, use default timestamped pattern: `{project-name}-accuracy-audit-YYYYMMDD-HHMM-UTC.md`
- **Before saving:** 
  - If `--dry-run` flag: Display report to screen, show "DRY RUN: Would save to {filename}", skip file write. END HERE.
  - Otherwise: Save to timestamped filename. If file already exists (unlikely with timestamps), append `-2` suffix automatically without prompting.

### Report structure

Use Markdown headers for each task. Format mismatch findings as:

```
**Doc Claim:** [what the docs say]
**Source of Truth:** [what the code/schema/spec actually defines]
**Verdict:** [Verified / Ghost / Hidden / Mismatch]
**File Path:** [relevant file and line number or spec path, if available]
```

For items that are 100% accurate, simply list as "Verified."

### Summary section

End with **Summary & Recommendations** outlining:
- Total items audited, items with issues
- High-priority fixes for maintainers
- Specific docs to update, implementations to clarify, etc.

### Metadata footer

After the summary, add a metadata footer with generation details:

```
---

**Report Generated By:** [AI Provider] | [Model Name] | [Timestamp]
```

Example:
```
---

**Report Generated By:** Anthropic | Claude Sonnet 4.5 | Jun-05-2026 14:30 GMT
```

The timestamp should use the format: `MMM-DD-YYYY HH:MM GMT` (e.g., "Oct-30-2021 23:59 GMT")

---

## Edge Cases & Flexibility

### Large/Complex Projects
If the project is massive (100+ commands, resources, or endpoints), ask the user which subsystem, subcommand family, resource family, or endpoint group to audit first. You can always expand the scope later.

### Partial Audits
If the user only cares about one task (e.g., "just check if documented flags actually exist", "only verify schema attributes", "just validate the examples"), perform only that task and skip the others.

### No Downstream Docs
If the user says "no downstream docs," skip Task 3 (Multi-Source Alignment) and note this in the report.

### Local vs. Remote
If the user provides local file paths instead of URLs, read those files directly. If they provide URLs and you can't access them, state "Information not found" and ask the user to provide the content or local paths.

### Schema Access Methods (Terraform)
- If you can run terraform CLI: prefer `terraform providers schema -json` for definitive schema
- If you can only read Go code: inspect Schema maps in resource files
- If you have both: cross-verify CLI output against Go implementation

### Spec Format Variations (API)
- OpenAPI 3.x and Swagger 2.0 have structural differences (e.g., `requestBody` vs inline `body` parameter, `components` vs `definitions`). Adapt parsing to the declared format.
- If the spec was converted between formats, note any conversion artifacts that may affect accuracy.

### Ambiguous Examples
If the docs have multiple complex examples, ask the user which one to validate in Task 4, or pick the most representative one and state your choice.

---

## Example Output

### CLI Tool Example

```markdown
# CLI Documentation Audit: Podman

## Task 1: Command Tree Comparison

| Command | Status | Verdict |
|---------|--------|---------|
| `podman run` | Documented & in code | Verified |
| `podman exec` | Documented & in code | Verified |
| `podman snapshot` | Documented only | Ghost |
| `podman internal-debug` | Code only | Hidden |

## Task 2: Flag & Argument Audit

**Command:** `podman run`

### `--memory` flag
**Doc Claim:** Accepts values like "512m", "2g" with no default
**Source of Truth:** Defaults to 0 (unlimited) if not set; parser accepts m, g, b suffixes
**Verdict:** Mismatch
**File Path:** `libpod/container_config.go:145`

## Summary & Recommendations
- Update docs to clarify `--memory` default behavior
- Remove `podman snapshot` from docs (ghosted in v2.0)
- Consider documenting `podman internal-debug` if it's not truly internal

---

**Report Generated By:** Anthropic | Claude Sonnet 4.5 | Jun-05-2026 14:30 GMT
```

### Terraform Provider Example

```markdown
# Terraform Provider Documentation Audit: terraform-provider-acme

## Task 1: Resource & Data Source Registry Comparison

| Resource/Data Source | Status | Verdict |
|---------------------|--------|---------|
| `acme_certificate` | Documented & in schema | Verified |
| `acme_database` | Documented only | Ghost |
| `acme_internal_config` | Schema only | Hidden |

## Task 2: Schema Attribute Audit

**Resource:** `acme_certificate`

### `renewal_days` attribute
**Doc Claim:** Optional number, defaults to 30
**Source of Truth:** Optional TypeInt, no default specified (defaults to 0)
**Verdict:** Mismatch
**File Path:** `acme/resource_certificate.go:142`

## Summary & Recommendations
- Remove `acme_database` from docs (ghosted in v2.0)
- Fix `renewal_days` default documentation
- Consider documenting `acme_internal_config` if intended for public use

---

**Report Generated By:** Anthropic | Claude Sonnet 4.5 | Jun-05-2026 14:30 GMT
```

### API Documentation (OpenAPI) Example

```markdown
# API Documentation Audit: Acme API

## Task 1: Endpoint Inventory

| Endpoint | Status | Verdict |
|----------|--------|---------|
| `GET /users` | Documented & in spec | Verified |
| `POST /users` | Documented & in spec | Verified |
| `DELETE /users/{id}/archive` | Documented only | Ghost |
| `PATCH /users/{id}` | Spec only | Hidden |

## Task 2: Parameter & Schema Audit

**Endpoint:** `POST /users`

### `role` parameter
**Doc Claim:** Required string, one of "admin", "user", "viewer"
**Source of Truth:** Optional string enum ["admin", "user"], no "viewer" value
**Verdict:** Mismatch (required vs optional, extra enum value in docs)
**File Path:** openapi.yaml paths./users.post.requestBody

## Summary & Recommendations
- Remove `DELETE /users/{id}/archive` from docs (not in spec)
- Document `PATCH /users/{id}` endpoint
- Fix `role` parameter: update docs to show optional with correct enum values

---

**Report Generated By:** Anthropic | Claude Sonnet 4.5 | Jun-05-2026 14:30 GMT
```

---

## Key Reminders

1. **Ask before assuming** -- If context is unclear, ask the user.
2. **State gaps explicitly** -- "Information not found" is better than a guess.
3. **Flag contradictions, don't reconcile them** -- Let the user see the conflict.
4. **Auto-suffix on collision** -- If a timestamped file somehow already exists, append `-2` automatically without prompting.
5. **Include metadata footer** -- Always end the report with AI provider, model name, and timestamp.
6. **Deliver the report as Markdown** -- Save it, then show the user the path and key findings.
7. **Use domain-appropriate methods** -- Source code for CLI, schema inspection + Go code for Terraform, spec parsing for API.
8. **Framework auto-detection (CLI/Terraform):** Use `detect-cli-framework.py` to automatically identify which patterns to use. If detection fails or returns "unknown", ask the user to clarify the framework and offer manual options. Detection results guide pattern selection in Step 4.
9. **Search tool policy (CLI/Terraform):** Use `rg` (ripgrep) or `grep` for source code pattern search. Patterns are optimized for text search, not AST. The "Source Search Tool" and framework-specific sections provide patterns for each detected framework. API audits do not use code search tools.
10. **Verification pass required** -- Before writing any report section, run the 6 checks in "Verify Before Writing Report": traceability, direction accuracy, enumerated completeness, exclusivity gate, verdict consistency, entity type naming. All findings must cite search evidence inline. Spot-check mode (checks 1, 3, 4 only) applies to audits with >50 items.
11. **No emojis or icons** -- Use plain text verdicts and labels only. No decorative characters in the report or in conversational responses.

---

## Usage Example

**User:** "Can you audit our API docs to make sure they match the OpenAPI spec?"

**You:** "I can help with that. This sounds like an API documentation audit. I need some information first:
1. What API are you auditing?
2. Where is the OpenAPI/Swagger spec file?
3. What format is the spec -- OpenAPI 3.x or Swagger 2.0?
4. Where are the upstream API docs?
5. Are there downstream/enterprise docs to compare? (Optional)"

**User:** Provides all context + indicates they want a full audit.

**You:** Perform Tasks 1-4 with strict adherence, generate the report with metadata footer (AI provider, model, timestamp), save to timestamped filename, and share key findings with the user.

---

## Limitations (v1.1)

### Polyglot Project Detection

**Issue:** Projects with multiple languages may be misclassified if a secondary language has stronger detection markers than the primary language.

**Example:** A TypeScript/Node.js project (primary) with Python build scripts (secondary) may be detected as a "Python library" if `setup.py` and class definitions are present.

**Impact:** Audit findings apply to the detected type. If type is wrong, findings may not match the project's actual structure.

**Workaround:** Manually verify project type before running audit. If project type seems wrong, re-run with `--type <correct-type>` flag to override auto-detection.

**Status:** Documented for v1.1. Fix planned for v1.2 (root manifest precedence + multi-factor evidence weighting).

### Semantic Type Detection

**Issue:** grep patterns cannot distinguish between class and function definitions across all languages.

**Impact:** If documentation claims a class but code implements a function (or vice versa), the audit reports a type mismatch but cannot auto-correct it.

**Mitigation:** User review required for type mismatches. AST-based detection planned for v1.2.

### Private vs Public Symbols

**Issue:** Patterns find all symbol definitions (public + private). Library audit cannot filter private symbols without `__all__` or naming conventions.

**Impact:** "Hidden items" list may include intentionally private classes/functions.

**Mitigation:** Check `__all__` exports or ignore symbols starting with `_` (underscore).

### Schema Version Validity (v2 Deferred)

**Issue:** v1 audits CLI tools, Python libraries, and VS Code extensions. Schema-based auditing (Terraform providers, OpenAPI/Swagger specs) is deferred to v2.

**Note for v2:** When auditing Terraform or API schemas, verify the schema version (e.g., JSON Schema draft, OpenAPI version) before validating keyword presence. A keyword valid in JSON Schema draft-2020-12 may not exist in draft-07. This check will be required before any schema attribute audit.

**Status:** Not applicable to v1. Will be implemented in v1.2+ (Terraform/OpenAPI support).

---
