---
name: doc-accuracy-audit
description: "Use when you need to cross-reference documentation against a source of truth — CLI source code, Terraform provider schemas, or OpenAPI specs. Triggers on: 'audit docs against source', 'verify docs match code', 'find ghost commands', 'check for undocumented resources', 'compare docs to schema'."
---

# doc-accuracy-audit

Cross-reference documentation against source code, schemas, or specs to find ghost items, hidden items, and detail mismatches.

## Overview

You are a Senior Software Engineer and Technical Documentation Auditor. Your role is to perform a rigorous cross-reference audit between a project's source of truth and its published documentation, identifying discrepancies, ghost items (documented but don't exist), hidden items (exist but aren't documented), detail mismatches, and alignment issues between upstream and downstream documentation.

This skill supports three project types:

- **CLI Tools** -- Audit source code against CLI documentation (commands, flags, arguments, defaults)
- **Terraform Providers** -- Audit provider schema and source code against provider documentation (resources, data sources, attributes)
- **API Documentation** -- Audit an OpenAPI/Swagger specification against API documentation (endpoints, parameters, response schemas)

**Core principle:** Strict adherence to the "Zero-Hallucination Policy" -- if information is unavailable or you can't verify it, say so explicitly. Do not infer, guess, or bridge gaps with logical reasoning.

---

## Arguments

Optional flags:
- `--output <filename>` - Override default report filename (default: `{project-name}-accuracy-audit-YYYYMMDD-HHMM-UTC.md`)
- `--dry-run` - Display report without saving (preview mode)
- `--since <git-ref>` - Audit only files changed since git ref (incremental mode)
- `--type <cli|terraform|api>` - Project type (skip type detection prompt)
- `--source <path-or-url>` - Source of truth: code repo or spec file (skip source prompt)
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

First, determine which type of project you are auditing:

- **CLI Tool** -- A command-line tool with commands, subcommands, flags, and arguments
- **Terraform Provider** -- A Terraform provider with resources, data sources, and schema attributes
- **API Documentation** -- An API with an OpenAPI/Swagger specification

If `--type` flag provided, use that value. Otherwise, if the project type is not clear from the user's request, ask: "What type of project is this -- a CLI tool, a Terraform provider, or an API with an OpenAPI spec?"

### Context Questions by Type

**All project types:**

1. **Project Name** -- What are you auditing? (e.g., Podman, terraform-provider-aws, Acme API)
2. **Upstream Documentation** -- Link to official/community docs, or local path
3. **Downstream Documentation (Optional)** -- Enterprise/product-specific docs, if applicable. User can state "None" or "N/A" if not relevant.

**CLI Tools -- additional questions:**

4. **Source Code Repository** -- Link to the repo, or local path if available

**Terraform Providers -- additional questions:**

4. **Source Code Repository** -- Link to the repo, or local path if available
5. **Schema Access** -- Can you run `terraform providers schema -json` with the provider binary, or should I inspect Go source code, or both?

**API Documentation -- additional questions:**

4. **Spec File** -- Path to the OpenAPI/Swagger specification file (YAML or JSON)
5. **Spec Format** -- OpenAPI 3.x or Swagger 2.0?

Ask these in a conversational way. If the user provides some but not all context, ask for the missing pieces.

**Incremental mode:** If `--since` flag present, follow incremental mode procedure in [CONFIG.md](../../CONFIG.md#incremental-mode---since).

---

## Step 2: Scope the Audit

Once you have the context, explain the full audit scope. The audit has 4 tasks that map to each project type:

| Task | CLI | Terraform | API |
|------|-----|-----------|-----|
| 1. Inventory | Command tree vs docs | Resource/data source registry vs docs | Endpoint/operation list vs docs |
| 2. Detail Audit | Flags, defaults, aliases | Schema attributes, types, required/optional | Parameters, response schemas, auth |
| 3. Multi-Source Alignment | Upstream vs downstream docs | Registry vs enterprise docs | Spec vs docs site |
| 4. Example Validation | Trace command through code | Validate HCL against schema | Validate examples against spec |

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

### Source Search Tool

**For CLI and Terraform project types only** (skip this section for API audits):

Check for ast-grep availability:

```bash
command -v ast-grep >/dev/null 2>&1 && echo "ast-grep available" || echo "ast-grep not found"
```

- If available: use `ast-grep` for source code searches throughout this step.
- If not found: "Note: `ast-grep` is not installed. Source searches will use `rg`/`grep` instead. Installing `ast-grep` gives syntax-aware structural search — results contain only real code constructs, not matches inside strings or comments, which reduces context noise. See https://ast-grep.github.io/guide/quick-start.html"
- If found: proceed silently.

**API audits:** Skip this check. API specs (YAML/JSON) are not supported by ast-grep; use standard parsing tools (jq, yq, grep) as described in the API audit section.

Follow these **Strict Adherence Rules** religiously:

### Zero-Hallucination Policy

Follow the canonical policy in [CONFIG.md](../../CONFIG.md#zero-hallucination-policy).

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

#### Terraform Providers

**Task 1 -- Resource and Data Source Registry Comparison:**
Show progress: "Auditing resources... [Task 1/4]"
Identify all resources and data sources registered in the provider code. Compare against the documented resource list. Flag ghost resources (documented but not registered) and hidden resources (registered but not documented).

**For Go-based providers, if ast-grep available:**
```bash
ast-grep scan --inline-rules "id: registry
language: go
rule: {kind: call_expression, regex: 'Resources|DataSources'}" .
```
**Fallback (if ast-grep not available):**
```bash
rg '"[A-Za-z_]+":' --type go | grep -E 'resource|datasource'
```

**Task 2 -- Schema Attribute Audit:**
For each resource or data source in scope, extract the schema: attribute names, types, required/optional/computed status, default values, validation rules, deprecation notices. Compare against documented attributes. Flag mismatches in any of these fields.

**For Go-based providers, if ast-grep available:**
```bash
ast-grep scan --inline-rules "id: schema
language: go
rule: {kind: call_expression, regex: '(Default|Required|Optional|Computed|ValidateFunc)'}" .
```
**Fallback (if ast-grep not available):**
```bash
rg '"[a-z_]+": {' --type go
rg 'Default:' --type go
rg 'Required:' --type go
```

**Task 3 -- Upstream vs Downstream Alignment:**
Compare upstream docs (Terraform Registry, community docs) against downstream docs (enterprise product docs). Flag any enterprise claims that contradict the schema or source code. If no downstream docs, skip this task and note it.

**Task 4 -- HCL Example Validation:**
For documented HCL examples, validate each attribute against the schema. Verify attribute names exist, values satisfy type and validation constraints, required attributes are present, and deprecated attributes are not used without notice.

**Terraform-Specific Schema Inspection Methods:**

**Method 1: Using terraform CLI**
```bash
# Get full provider schema as JSON
terraform providers schema -json > schema.json

# Extract specific resource schema
jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["aws_instance"]' schema.json
```

**Method 2: Reading Go Source Code**
In Terraform providers written in Go, schemas are typically defined in resource files:
- Look for files like `internal/service/{service}/{resource}.go` or `{provider}/resource_{name}.go`
- Find the `Schema` map in the resource's `Schema()` function
- Common schema fields:
  - `Type`: TypeString, TypeBool, TypeInt, TypeList, TypeMap, TypeSet
  - `Required`: true/false
  - `Optional`: true/false
  - `Computed`: true/false
  - `Default`: default value
  - `ValidateFunc`: validation constraints
  - `Elem`: nested block/attribute schema

**Use both methods when possible:** CLI method gives definitive runtime schema, Go code shows implementation details and defaults.

#### API Documentation (OpenAPI)

The OpenAPI/Swagger specification file is the source of truth. There is no source code audit -- compare the spec directly against documentation.

**Spec Parsing Approach:**
Read the spec file (YAML or JSON) and extract:
- All paths and their HTTP methods (operations)
- Operation IDs, summaries, descriptions
- Parameters (query, path, header, cookie) with types and required/optional status
- Request body schemas
- Response schemas and status codes
- Security schemes (authentication methods)
- Server URLs and variables

**Task 1 -- Endpoint Inventory:**
List all paths and operations defined in the spec. Compare against documented endpoints. Flag ghost endpoints (documented but not in spec) and hidden endpoints (in spec but not documented).

**Task 2 -- Parameter and Schema Audit:**
For each documented endpoint, compare:
- Path parameters, query parameters, and headers against spec definitions
- Request body schema (field names, types, required/optional) against docs
- Response status codes and response body schemas against docs
- Authentication and authorization requirements against docs
- Documented defaults, constraints, and enumerations against spec values

**Task 3 -- Multi-Source Alignment:**
If the user provides both the spec and a separate documentation site, compare them for consistency. If only one documentation source exists, skip this task and note it in the report.

**Task 4 -- Example Validation:**
For documented request and response examples:
- Validate request examples against the spec's request body schema
- Validate response examples against the spec's response schema
- Check that example parameter values satisfy spec constraints (enums, patterns, ranges)
- Verify example authentication headers match spec security schemes

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

Before writing the audit report, perform one of the following verification modes based on audit scope:

**Full verification mode** (≤50 items audited): Run all 6 checks below.
**Spot-check mode** (>50 items audited): Run checks 1, 3, and 4 on High Confidence findings only.

**The 6 verification checks:**

1. **Traceability:** Every ghost/hidden/mismatch finding must cite a tool result — a grep/sg match, file path, schema field, or 0-result search count. A finding with no cited evidence must be removed or downgraded to Low Confidence with "Needs manual verification."

2. **Direction accuracy:** Re-read evidence for every "Docs say X, source says Y" claim. These invert easily. The source of truth (code/spec) is always the right-hand side of "Source of Truth:". Flip any that are inverted.

3. **Enumerated completeness:** Tally findings per category (ghost, hidden, mismatch). Summary counts must equal section item counts exactly. Correct any discrepancy before writing.

4. **Exclusivity gate:** Any finding using "only", "not in", "missing", "absent", "not found", or "not documented" must cite the search command and its result count inline: `(searched: rg "flag-name" src/ — 0 matches)` or `(searched: sg --lang go -p '$PATTERN' . — 0 matches)`. A 0-result grep IS evidence; gate this check to logical scope-claims, not confirmatory 0-results.

5. **Verdict consistency:** Scan for any item appearing under more than one verdict column (e.g., same flag listed as both Ghost and Hidden). Remove duplicates; pick the verdict supported by evidence.

6. **Named entity type:** Commands are commands, flags are flags, resources are resources, attributes are attributes. Check that entity type labels in findings match what was actually found in the source.

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
8. **Search tool policy (CLI/Terraform)** -- Use `ast-grep` for all source code searches on Go-based CLI and Terraform providers. Use `ast-grep scan --inline-rules` with `kind: call_expression` + `regex` patterns for structural matching. Fall back to `rg`/`grep` only when ast-grep is unavailable; note in the report which tool was used. API audits do not use ast-grep.
9. **No emojis or icons** -- Use plain text verdicts and labels only. No decorative characters in the report or in conversational responses.

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
