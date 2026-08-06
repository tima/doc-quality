---
name: doc-quality-check
description: "Use when you want to run the complete documentation quality pipeline in one command: accuracy audit → quality audit → revisions. Triggers on: 'run the doc quality pipeline', 'check documentation quality', 'audit and fix docs', 'complete doc audit'."
compatibility: Requires all three component skills installed
---

# doc-quality-check

Run the complete documentation quality pipeline: accuracy audit -> quality audit -> apply revisions.

**Part of:** [doc-quality-skills](../) family

## What This Does

Orchestrates three skills in sequence:
1. `/doc-accuracy-audit` - Compare docs against source of truth (auto-detects CLI framework or Terraform provider)
2. `/doc-quality-audit` - Evaluate style, tone, clarity
3. `/doc-quality-revise` - Apply corrections interactively

All reports are timestamped to preserve audit history across runs.

**Note:** For accuracy audit, you don't need to specify `--type` — the skill will auto-detect whether your code is a CLI tool (Cobra, argparse, Click, Bash) or Terraform provider. Provide `--type` only if auto-detection fails.

## Arguments

Required:
- `path/to/docs` - Directory or file to audit

Optional flags:
- `--skip-accuracy` - Skip accuracy audit phase
- `--skip-quality` - Skip quality audit phase
- `--audit-only` - Skip revision phase (audit only)
- `--accuracy-only` - Run only accuracy audit
- `--quality-only` - Run only quality audit
- `--parallel` - Run accuracy + quality audits concurrently (faster)
- `--dry-run` - Preview mode, no files modified (passed to all skills)
- `--since <git-ref>` - Incremental mode, audit only changed files (passed to audit skills)
- `--type <cli|terraform|api>` - Project type (optional; accuracy audit will auto-detect if not provided)
- `--source <path-or-url>` - Source of truth (passed to accuracy audit, skip source prompt)
- `--dimensions <core|comprehensive>` - Quality dimensions (passed to quality audit, skip dimension prompt)

**Flag validation:** Cannot combine `--skip-accuracy` + `--skip-quality` (nothing to audit)

## Usage

Full pipeline:
```
/doc-quality-check docs/api/
```

Skip phases:
```
/doc-quality-check docs/api/ --skip-accuracy
/doc-quality-check docs/api/ --audit-only
```

Single phase:
```
/doc-quality-check docs/api/ --accuracy-only
```

---

## Workflow


### Step 1: Parse Arguments and Validate Flags

**Extract from arguments string:**
- `docs_path` - First non-flag argument
- `skip_accuracy` - Boolean, `--skip-accuracy` present
- `skip_quality` - Boolean, `--skip-quality` present
- `audit_only` - Boolean, `--audit-only` present
- `accuracy_only` - Boolean, `--accuracy-only` present
- `quality_only` - Boolean, `--quality-only` present
- `parallel` - Boolean, `--parallel` present
- `dry_run` - Boolean, `--dry-run` present
- `since_ref` - String, value after `--since`
- `type_flag` - String, value after `--type`
- `source_flag` - String, value after `--source`
- `dimensions_flag` - String, value after `--dimensions`

**If `dry_run`:** Show "DRY RUN MODE - no files will be modified" at start

**Validate flags:**

1. Check for invalid combinations:
   - If `skip_accuracy` AND `skip_quality`: Error "Cannot skip both audit phases. Nothing to audit."
   - If `audit_only` AND any `*_only` flag: Error "Cannot combine --audit-only with --accuracy-only or --quality-only"

2. Determine which phases to run:
   - If `accuracy_only`: Run only Phase 1
   - If `quality_only`: Run only Phase 2
   - If `audit_only`: Run Phase 1 + Phase 2, skip Phase 3
   - If `skip_accuracy`: Run Phase 2 + Phase 3
   - If `skip_quality`: Run Phase 1 + Phase 3
   - Default (no flags): Run all three phases

3. If `docs_path` not provided: Error "Please provide a path to documentation files"


### Step 2: Generate Timestamp and Project Name

**Capture UTC timestamp** using Bash:

```bash
date -u +"%Y%m%d-%H%M-UTC"
```

Store result as `timestamp` (e.g., "20260615-1430-UTC")

**Derive project name from docs_path:**

1. Remove trailing slashes: `docs/api/` -> `docs/api`
2. Take last path component: `docs/api` -> `api`
3. Clean up: lowercase, replace spaces/special chars with hyphens
4. Store as `project_name`

Example: `docs/api/` -> project name is `api`

**Build report filenames:**
- `accuracy_report_file` = `{project_name}-accuracy-audit-{timestamp}.md`
- `quality_report_file` = `{project_name}-quality-audit-{timestamp}.md`


### Step 3: Run Pipeline Phases

**Announce start:**

Show user:
```
Running documentation quality check on {docs_path}
```

#### Parallel Mode (if `--parallel` flag present)

**Conditions:** `--parallel` flag AND both accuracy + quality audits enabled (not skipped)

**If conditions met:**

1. Announce: "Running accuracy + quality audits in parallel"

2. Invoke BOTH skills concurrently (single message, two skill tool calls):
   ```
   /doc-accuracy-audit {docs_path} --output {accuracy_report_file} {--dry-run if dry_run} {--since <ref> if since_ref} {--type <val> if type_flag} {--source <val> if source_flag}
   /doc-quality-audit {docs_path} --output {quality_report_file} {--dry-run if dry_run} {--since <ref> if since_ref} {--dimensions <val> if dimensions_flag}
   ```

3. After both complete, check for both report files:
   ```bash
   ls -la {accuracy_report_file} {quality_report_file}
   ```

4. If both exist:
   - Show: "COMPLETE Both audits complete"
   - Skip to Phase 3 (or completion if `--audit-only`)

5. If either missing:
   - Error: "One or both audits failed"
   - Offer retry or skip options
   - Fall back to sequential mode if retrying

**If conditions NOT met** (one audit skipped or no `--parallel` flag):
- Run sequentially (Phase 1 then Phase 2)

#### Phase 1: Accuracy Audit (Sequential Mode)

**Skip check:** If `skip_accuracy` OR `quality_only` OR (parallel mode active): Skip this phase

**Otherwise, run:**

1. Announce: "Phase 1/X: Accuracy audit" (X = total phases to run)

2. Invoke skill using skill tool:
   ```
   /doc-accuracy-audit {docs_path} --output {accuracy_report_file} {--dry-run if dry_run} {--since <ref> if since_ref} {--type <val> if type_flag} {--source <val> if source_flag}
   ```

3. After skill completes, check for report file:
   ```bash
   ls -la {accuracy_report_file}
   ```

4. If report exists:
   - Show: "COMPLETE Accuracy audit complete -> {accuracy_report_file}"
   - Continue to next phase

5. If report missing:
   - Error: "Accuracy audit failed - report file not found: {accuracy_report_file}"
   - Offer options:
     - A) Retry Phase 1
     - B) Skip Phase 1 and continue
     - C) Abort pipeline
   - Handle user choice (retry = re-invoke skill, skip = continue, abort = stop)


#### Phase 2: Quality Audit (Sequential Mode)

**Skip check:** If `skip_quality` OR `accuracy_only` OR (parallel mode active): Skip this phase

**Otherwise, run:**

1. Announce: "Phase 2/X: Quality audit"

2. Invoke skill using skill tool:
   ```
   /doc-quality-audit {docs_path} --output {quality_report_file} {--dry-run if dry_run} {--since <ref> if since_ref} {--dimensions <val> if dimensions_flag}
   ```

3. After skill completes, check for report file:
   ```bash
   ls -la {quality_report_file}
   ```

4. If report exists:
   - Show: "COMPLETE Quality audit complete -> {quality_report_file}"
   - Continue to next phase

5. If report missing:
   - Error: "Quality audit failed - report file not found: {quality_report_file}"
   - Offer options (same as Phase 1):
     - A) Retry Phase 2
     - B) Skip Phase 2 and continue
     - C) Abort pipeline
   - Handle user choice


#### Phase 3: Apply Revisions

**Skip check:** If `audit_only` OR `accuracy_only` OR `quality_only`: Skip this phase, show "Skipping Phase 3: Apply revisions (--audit-only)" or similar

**Otherwise, run:**

1. Announce: "Phase 3/X: Apply revisions"

2. Build skill invocation based on which reports exist:
   - If both reports exist:
     ```
     /doc-quality-revise --accuracy-report {accuracy_report_file} --quality-report {quality_report_file} {--dry-run if dry_run flag}
     ```
   - If only accuracy report exists (quality was skipped):
     ```
     /doc-quality-revise --accuracy-report {accuracy_report_file} {--dry-run if dry_run flag}
     ```
   - If only quality report exists (accuracy was skipped):
     ```
     /doc-quality-revise --quality-report {quality_report_file} {--dry-run if dry_run flag}
     ```

3. Invoke skill using Skill tool with constructed arguments

4. After skill completes:
   - Show: "COMPLETE Revisions complete"
   - Continue to completion status

5. If skill fails or user cancels:
   - Preserve completed work (audit reports)
   - Show what was finished


### Step 4: Report Completion Status

**Show summary:**

```
Pipeline complete.

Reports generated:
- {accuracy_report_file} (if Phase 1 ran)
- {quality_report_file} (if Phase 2 ran)

Phases completed: X/Y
```

If any phases were skipped, note which ones and why (e.g., "--skip-accuracy flag" or "user aborted")

If all phases completed successfully:
```
All phases finished successfully.
```


---

## Examples

Four worked examples covering full pipeline, audit-only, skip-accuracy, and quality-only invocations with expected output. See [references/examples.md](references/examples.md)

---

## Error Handling

Covers missing report files, invalid flag combinations, missing docs path, skill invocation failure, and user cancellation during interactive revision. See [references/error-handling.md](references/error-handling.md)
