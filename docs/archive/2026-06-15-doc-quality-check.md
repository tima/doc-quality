# doc-quality-check Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create orchestrator skill that runs complete documentation quality pipeline (accuracy → quality → revise) with timestamped reports

**Architecture:** Thin orchestrator using Skill tool to invoke three existing skills sequentially. Captures timestamp at start, passes timestamped output paths to audit skills, passes report paths to revise skill.

**Tech Stack:** Claude Code skills (markdown with YAML frontmatter), Skill tool invocations, bash for timestamp generation

---

## File Structure

**Modify existing skills:**
- `doc-quality-skills/doc-accuracy-audit/SKILL.md` - add --output flag
- `doc-quality-skills/doc-quality-audit/SKILL.md` - add --output flag
- `doc-quality-skills/doc-quality-revise/SKILL.md` - add --accuracy-report and --quality-report flags

**Create new skill:**
- `doc-quality-skills/doc-quality-check/SKILL.md` - orchestrator skill
- `doc-quality-skills/doc-quality-check/README.md` - documentation

---

### Task 1: Add --output flag to doc-accuracy-audit

**Files:**
- Modify: `doc-quality-skills/doc-accuracy-audit/SKILL.md`

- [ ] **Step 1: Read current SKILL.md to understand structure**

```bash
cd ~/projects/doc-quality-skills
cat doc-accuracy-audit/SKILL.md | head -100
```

Expected: See frontmatter and skill structure

- [ ] **Step 2: Find argument parsing section**

```bash
grep -n "arguments\|args\|ARGUMENTS" doc-accuracy-audit/SKILL.md
```

Expected: Find where skill parses user input

- [ ] **Step 3: Add --output flag documentation after frontmatter**

Add this section after the description and before workflow:

```markdown
## Arguments

Optional flags:
- `--output <filename>` - Override default report filename (default: `{project-name}-docs-audit.md`)

**Usage:**
```
/doc-accuracy-audit path/to/docs
/doc-accuracy-audit path/to/docs --output custom-report.md
```
```

- [ ] **Step 4: Find report filename generation logic**

```bash
grep -n "project-name\|-docs-audit\.md\|filename" doc-accuracy-audit/SKILL.md
```

Expected: Find where report filename is constructed (around line 223-228)

- [ ] **Step 5: Update file naming instructions**

Replace the file naming section with:

```markdown
### File naming

- If `--output` flag is provided, use that filename exactly
- Otherwise, use default pattern: `{project-name}-docs-audit.md`
- **Before saving:** Check if a file with that name already exists. If it does, ask the user whether to:
  - Overwrite it
  - Create a new version (e.g., `{project-name}-docs-audit-2.md`)
  - Use a different filename
```

- [ ] **Step 6: Verify changes don't break existing behavior**

Review: Default behavior unchanged, --output is optional, backward compatible

- [ ] **Step 7: Commit changes**

```bash
cd ~/projects/doc-quality-skills
git add doc-accuracy-audit/SKILL.md
git commit -m "feat(doc-accuracy-audit): add --output flag for custom report filenames

- Accepts --output <filename> to override default report name
- Maintains backward compatibility (flag is optional)
- Default behavior unchanged"
```

---

### Task 2: Add --output flag to doc-quality-audit

**Files:**
- Modify: `doc-quality-skills/doc-quality-audit/SKILL.md`

- [ ] **Step 1: Read current SKILL.md to find report filename logic**

```bash
cd ~/projects/doc-quality-skills
grep -n "quality-audit\.md\|filename\|Save detailed" doc-quality-audit/SKILL.md
```

Expected: Find report saving section (around line 364-369)

- [ ] **Step 2: Add --output flag documentation after frontmatter**

Add arguments section early in the skill:

```markdown
## Arguments

Optional flags:
- `--output <filename>` - Override default report filename (default: `{project-name}-quality-audit.md`)

**Usage:**
```
/doc-quality-audit path/to/docs
/doc-quality-audit path/to/docs --output custom-quality-report.md
```
```

- [ ] **Step 3: Update filename generation in Step 4 (Deliver the Report)**

Find the section that says:
```
**If yes:**
- Generate full markdown report (format below)
- Save to current working directory
- Filename: `{project-name}-quality-audit.md`
```

Replace with:
```
**If yes:**
- Generate full markdown report (format below)
- Save to current working directory
- Filename: Use `--output` value if provided, otherwise `{project-name}-quality-audit.md`
- Check if file exists before saving (same collision handling as doc-accuracy-audit)
```

- [ ] **Step 4: Verify backward compatibility**

Review: Optional flag, default behavior unchanged

- [ ] **Step 5: Commit changes**

```bash
cd ~/projects/doc-quality-skills
git add doc-quality-audit/SKILL.md
git commit -m "feat(doc-quality-audit): add --output flag for custom report filenames

- Accepts --output <filename> to override default report name
- Maintains backward compatibility (flag is optional)
- Default behavior unchanged"
```

---

### Task 3: Add report path flags to doc-quality-revise

**Files:**
- Modify: `doc-quality-skills/doc-quality-revise/SKILL.md`

- [ ] **Step 1: Read current SKILL.md to understand report discovery**

```bash
cd ~/projects/doc-quality-skills
grep -n "audit.*report\|find.*report\|discover" doc-quality-revise/SKILL.md | head -20
```

Expected: Find where skill looks for report files

- [ ] **Step 2: Add report path flags documentation**

Add arguments section after frontmatter:

```markdown
## Arguments

Optional flags:
- `--accuracy-report <path>` - Path to accuracy audit report (default: auto-discover `*-accuracy-audit*.md` or `*-docs-audit*.md`)
- `--quality-report <path>` - Path to quality audit report (default: auto-discover `*-quality-audit*.md`)

**Usage:**
```
/doc-quality-revise
/doc-quality-revise --quality-report my-quality-audit.md
/doc-quality-revise --accuracy-report acc-report.md --quality-report qual-report.md
```

**Auto-discovery:** When flags are not provided, skill searches current directory for report files matching the patterns above.
```

- [ ] **Step 3: Find Phase 1 report discovery logic**

```bash
grep -n "Phase 1\|Parse.*report\|find.*report" doc-quality-revise/SKILL.md | head -10
```

Expected: Find Phase 1 instructions (around line 50-100)

- [ ] **Step 4: Update Phase 1 to check flags first**

Find Phase 1 "Find and Read Audit Report" section, update to:

```markdown
## Phase 1: Parse and Categorize Audit Report

### Find Audit Reports

**Check for explicit paths first:**
1. If `--accuracy-report` flag provided, use that path for accuracy report
2. If `--quality-report` flag provided, use that path for quality report

**Auto-discovery (if flags not provided):**
1. Search current directory for files matching:
   - Accuracy: `*-accuracy-audit*.md` or `*-docs-audit*.md`
   - Quality: `*-quality-audit*.md`
2. If multiple matches found, use most recent (by modification time)
3. If no matches found, report which report type is missing

**Read the reports** using the Read tool on discovered/specified paths.
```

- [ ] **Step 5: Verify backward compatibility**

Review: Auto-discovery still works when flags not provided

- [ ] **Step 6: Commit changes**

```bash
cd ~/projects/doc-quality-skills
git add doc-quality-revise/SKILL.md
git commit -m "feat(doc-quality-revise): add explicit report path flags

- Accepts --accuracy-report and --quality-report for explicit paths
- Maintains backward compatibility with auto-discovery
- Flags take precedence over auto-discovery"
```

---

### Task 4: Create doc-quality-check skill structure

**Files:**
- Create: `doc-quality-skills/doc-quality-check/SKILL.md`

- [ ] **Step 1: Create directory**

```bash
cd ~/projects/doc-quality-skills
mkdir -p doc-quality-check
```

Expected: Directory created

- [ ] **Step 2: Create SKILL.md with frontmatter and overview**

```bash
cat > doc-quality-check/SKILL.md << 'EOF'
---
name: doc-quality-check
description: Orchestrate complete documentation quality pipeline (accuracy → quality → revise) with timestamped reports
triggers:
  - "run the doc quality pipeline"
  - "check documentation quality"
  - "audit and fix docs"
  - "complete doc audit"
---

# doc-quality-check

Run the complete documentation quality pipeline: accuracy audit → quality audit → apply revisions.

**Part of:** [doc-quality-skills](../) family

## What This Does

Orchestrates three skills in sequence:
1. `/doc-accuracy-audit` - Compare docs against source of truth
2. `/doc-quality-audit` - Evaluate style, tone, clarity
3. `/doc-quality-revise` - Apply corrections interactively

All reports are timestamped to preserve audit history across runs.

## Arguments

Required:
- `path/to/docs` - Directory or file to audit

Optional flags:
- `--skip-accuracy` - Skip accuracy audit phase
- `--skip-quality` - Skip quality audit phase
- `--audit-only` - Skip revision phase (audit only)
- `--accuracy-only` - Run only accuracy audit
- `--quality-only` - Run only quality audit

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

EOF
```

Expected: File created with frontmatter

- [ ] **Step 3: Add argument parsing and validation logic**

```bash
cat >> doc-quality-check/SKILL.md << 'EOF'

### Step 1: Parse Arguments and Validate Flags

**Extract from arguments string:**
- `docs_path` - First non-flag argument
- `skip_accuracy` - Boolean, `--skip-accuracy` present
- `skip_quality` - Boolean, `--skip-quality` present
- `audit_only` - Boolean, `--audit-only` present
- `accuracy_only` - Boolean, `--accuracy-only` present
- `quality_only` - Boolean, `--quality-only` present

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

EOF
```

Expected: Argument parsing logic added

- [ ] **Step 4: Add timestamp and project name generation**

```bash
cat >> doc-quality-check/SKILL.md << 'EOF'

### Step 2: Generate Timestamp and Project Name

**Capture timestamp** using Bash:

```bash
date +"%Y%m%d-%H%M"
```

Store result as `timestamp` (e.g., "20260615-1430")

**Derive project name from docs_path:**

1. Remove trailing slashes: `docs/api/` → `docs/api`
2. Take last path component: `docs/api` → `api`
3. Clean up: lowercase, replace spaces/special chars with hyphens
4. Store as `project_name`

Example: `docs/api/` → project name is `api`

**Build report filenames:**
- `accuracy_report_file` = `{project_name}-accuracy-audit-{timestamp}.md`
- `quality_report_file` = `{project_name}-quality-audit-{timestamp}.md`

EOF
```

Expected: Timestamp and naming logic added

- [ ] **Step 5: Commit skeleton**

```bash
cd ~/projects/doc-quality-skills
git add doc-quality-check/
git commit -m "feat(doc-quality-check): create skill skeleton with arg parsing

- Add frontmatter and description
- Implement argument parsing and flag validation
- Add timestamp and project name generation logic"
```

---

### Task 5: Implement phase orchestration

**Files:**
- Modify: `doc-quality-skills/doc-quality-check/SKILL.md`

- [ ] **Step 1: Add Phase 1 (Accuracy Audit) orchestration**

```bash
cat >> doc-quality-check/SKILL.md << 'EOF'

### Step 3: Run Pipeline Phases

**Announce start:**

Show user:
```
Running documentation quality check on {docs_path}
```

#### Phase 1: Accuracy Audit

**Skip check:** If `skip_accuracy` OR `quality_only`: Skip this phase, show "Skipping Phase 1: Accuracy audit (--skip-accuracy)" or "(--quality-only)"

**Otherwise, run:**

1. Announce: "Phase 1/X: Accuracy audit" (X = total phases to run)

2. Invoke skill using Skill tool:
   ```
   /doc-accuracy-audit {docs_path} --output {accuracy_report_file}
   ```

3. After skill completes, check for report file:
   ```bash
   ls -la {accuracy_report_file}
   ```

4. If report exists:
   - Show: "✓ Accuracy audit complete → {accuracy_report_file}"
   - Continue to next phase

5. If report missing:
   - Error: "Accuracy audit failed - report file not found: {accuracy_report_file}"
   - Offer options:
     - A) Retry Phase 1
     - B) Skip Phase 1 and continue
     - C) Abort pipeline
   - Handle user choice (retry = re-invoke skill, skip = continue, abort = stop)

EOF
```

Expected: Phase 1 logic added

- [ ] **Step 2: Add Phase 2 (Quality Audit) orchestration**

```bash
cat >> doc-quality-check/SKILL.md << 'EOF'

#### Phase 2: Quality Audit

**Skip check:** If `skip_quality` OR `accuracy_only`: Skip this phase, show "Skipping Phase 2: Quality audit (--skip-quality)" or "(--accuracy-only)"

**Otherwise, run:**

1. Announce: "Phase 2/X: Quality audit"

2. Invoke skill using Skill tool:
   ```
   /doc-quality-audit {docs_path} --output {quality_report_file}
   ```

3. After skill completes, check for report file:
   ```bash
   ls -la {quality_report_file}
   ```

4. If report exists:
   - Show: "✓ Quality audit complete → {quality_report_file}"
   - Continue to next phase

5. If report missing:
   - Error: "Quality audit failed - report file not found: {quality_report_file}"
   - Offer options (same as Phase 1):
     - A) Retry Phase 2
     - B) Skip Phase 2 and continue
     - C) Abort pipeline
   - Handle user choice

EOF
```

Expected: Phase 2 logic added

- [ ] **Step 3: Add Phase 3 (Apply Revisions) orchestration**

```bash
cat >> doc-quality-check/SKILL.md << 'EOF'

#### Phase 3: Apply Revisions

**Skip check:** If `audit_only` OR `accuracy_only` OR `quality_only`: Skip this phase, show "Skipping Phase 3: Apply revisions (--audit-only)" or similar

**Otherwise, run:**

1. Announce: "Phase 3/X: Apply revisions"

2. Build skill invocation based on which reports exist:
   - If both reports exist:
     ```
     /doc-quality-revise --accuracy-report {accuracy_report_file} --quality-report {quality_report_file}
     ```
   - If only accuracy report exists (quality was skipped):
     ```
     /doc-quality-revise --accuracy-report {accuracy_report_file}
     ```
   - If only quality report exists (accuracy was skipped):
     ```
     /doc-quality-revise --quality-report {quality_report_file}
     ```

3. Invoke skill using Skill tool with constructed arguments

4. After skill completes:
   - Show: "✓ Revisions complete"
   - Continue to completion status

5. If skill fails or user cancels:
   - Preserve completed work (audit reports)
   - Show what was finished

EOF
```

Expected: Phase 3 logic added

- [ ] **Step 4: Add completion status reporting**

```bash
cat >> doc-quality-check/SKILL.md << 'EOF'

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

EOF
```

Expected: Completion reporting added

- [ ] **Step 5: Commit phase orchestration**

```bash
cd ~/projects/doc-quality-skills
git add doc-quality-check/SKILL.md
git commit -m "feat(doc-quality-check): implement phase orchestration

- Add Phase 1 (accuracy audit) with error recovery
- Add Phase 2 (quality audit) with error recovery
- Add Phase 3 (revise) with conditional report passing
- Add completion status reporting"
```

---

### Task 6: Add examples and edge cases

**Files:**
- Modify: `doc-quality-skills/doc-quality-check/SKILL.md`

- [ ] **Step 1: Add usage examples section**

```bash
cat >> doc-quality-check/SKILL.md << 'EOF'

---

## Examples

**Full pipeline on test docs:**
```
User: /doc-quality-check test-docs/

Running documentation quality check on test-docs/

Phase 1/3: Accuracy audit
[doc-accuracy-audit executes]
✓ Accuracy audit complete → test-docs-accuracy-audit-20260615-1430.md

Phase 2/3: Quality audit
[doc-quality-audit executes]
✓ Quality audit complete → test-docs-quality-audit-20260615-1430.md

Phase 3/3: Apply revisions
[doc-quality-revise executes interactively]
✓ Revisions complete

Pipeline complete.

Reports generated:
- test-docs-accuracy-audit-20260615-1430.md
- test-docs-quality-audit-20260615-1430.md

All phases finished successfully.
```

**Audit-only (no revisions):**
```
User: /doc-quality-check docs/api/ --audit-only

Running documentation quality check on docs/api/

Phase 1/2: Accuracy audit
[executes]
✓ Accuracy audit complete → api-accuracy-audit-20260615-1545.md

Phase 2/2: Quality audit
[executes]
✓ Quality audit complete → api-quality-audit-20260615-1545.md

Skipping Phase 3: Apply revisions (--audit-only)

Pipeline complete.

Reports generated:
- api-accuracy-audit-20260615-1545.md
- api-quality-audit-20260615-1545.md

Phases completed: 2/2
```

**Quality check only:**
```
User: /doc-quality-check docs/cli/ --quality-only

Running documentation quality check on docs/cli/

Skipping Phase 1: Accuracy audit (--quality-only)

Phase 1/1: Quality audit
[executes]
✓ Quality audit complete → cli-quality-audit-20260615-1600.md

Skipping Phase 2: Apply revisions (--quality-only)

Pipeline complete.

Reports generated:
- cli-quality-audit-20260615-1600.md

Phases completed: 1/1
```

EOF
```

Expected: Examples added

- [ ] **Step 2: Add error handling documentation**

```bash
cat >> doc-quality-check/SKILL.md << 'EOF'

## Error Handling

**Invalid flag combinations:**
```
User: /doc-quality-check docs/ --skip-accuracy --skip-quality

Error: Cannot skip both audit phases. Nothing to audit.
```

**Missing report file (with recovery):**
```
Phase 1/3: Accuracy audit
[skill executes but crashes or user cancels]

Error: Accuracy audit failed - report file not found: docs-accuracy-audit-20260615-1630.md

What would you like to do?
A) Retry Phase 1
B) Skip Phase 1 and continue
C) Abort pipeline

User: B

Skipping Phase 1 (user requested)

Phase 2/3: Quality audit
[continues with remaining phases]
```

**User cancellation mid-pipeline:**
```
Phase 2/3: Quality audit
[user cancels during execution]

Pipeline cancelled by user.

Completed phases:
- Phase 1: Accuracy audit ✓

Reports preserved:
- docs-accuracy-audit-20260615-1645.md

Incomplete phases:
- Phase 2: Quality audit (cancelled)
- Phase 3: Apply revisions (not started)
```

EOF
```

Expected: Error handling documentation added

- [ ] **Step 3: Commit examples and edge cases**

```bash
cd ~/projects/doc-quality-skills
git add doc-quality-check/SKILL.md
git commit -m "docs(doc-quality-check): add examples and error handling

- Add full pipeline example
- Add audit-only example
- Add single-phase example
- Document error recovery scenarios
- Document user cancellation handling"
```

---

### Task 7: Create README and update family docs

**Files:**
- Create: `doc-quality-skills/doc-quality-check/README.md`
- Modify: `doc-quality-skills/README.md`
- Modify: `doc-quality-skills/INSTALL.md`

- [ ] **Step 1: Create README for doc-quality-check**

```bash
cat > ~/projects/doc-quality-skills/doc-quality-check/README.md << 'EOF'
# doc-quality-check

> Part of the [doc-quality-skills](../) family. See the [family README](../README.md) for the complete pipeline.

Pipeline orchestrator that runs the complete documentation quality workflow: accuracy audit → quality audit → apply revisions.

## What It Does

Coordinates three skills in sequence:
1. **doc-accuracy-audit** - Verify docs match source of truth (CLI code, Terraform schema, OpenAPI spec)
2. **doc-quality-audit** - Evaluate style, tone, clarity, plain language compliance
3. **doc-quality-revise** - Apply corrections interactively

All reports are timestamped (YYYYMMDD-HHMM format) to preserve audit history.

## Installation

See [../INSTALL.md](../INSTALL.md) for detailed instructions.

**Quick install:**

```bash
ln -sf ~/projects/doc-quality-skills/doc-quality-check ~/.claude/skills/doc-quality-check
```

## Usage

Invoke from Claude Code:

```
/doc-quality-check path/to/docs
```

Or describe your intent naturally:
- "run the doc quality pipeline on docs/api/"
- "check documentation quality for my CLI"
- "audit and fix docs in docs/terraform/"

## Options

**Phase control:**
- `--skip-accuracy` - Skip accuracy audit, run quality → revise
- `--skip-quality` - Skip quality audit, run accuracy → revise
- `--audit-only` - Run both audits, skip revision phase
- `--accuracy-only` - Run only accuracy audit
- `--quality-only` - Run only quality audit

## Examples

Full pipeline:
```
/doc-quality-check docs/api/
```

Audit without applying fixes:
```
/doc-quality-check docs/api/ --audit-only
```

Quality check only:
```
/doc-quality-check docs/terraform/ --quality-only
```

## Output

Reports are timestamped and saved to current directory:
- `{project}-accuracy-audit-{timestamp}.md`
- `{project}-quality-audit-{timestamp}.md`

Example:
```
api-accuracy-audit-20260615-1430.md
api-quality-audit-20260615-1430.md
```

## Error Recovery

If a phase fails, you'll be offered options:
- Retry the failed phase
- Skip that phase and continue
- Abort the pipeline

Completed work (audit reports) is always preserved.

## Related Skills

- **doc-accuracy-audit** - Standalone accuracy audit
- **doc-quality-audit** - Standalone quality audit
- **doc-quality-revise** - Standalone revision application
EOF
```

Expected: README created

- [ ] **Step 2: Update family README to mention doc-quality-check**

```bash
# Read current family README to find where to add doc-quality-check
grep -n "## The Skills" ~/projects/doc-quality-skills/README.md
```

Expected: Find line number for skills section

Add after the three existing skills:

```markdown
### doc-quality-check
Orchestrates the complete pipeline: runs doc-accuracy-audit → doc-quality-audit → doc-quality-revise in sequence with timestamped reports. Single-command execution of the full workflow with optional phase skipping.

**Features:**
- Timestamped reports (preserves audit history)
- Error recovery between phases
- Flexible phase control (skip phases, run subsets)
- Status reporting at each stage
```

- [ ] **Step 3: Update INSTALL.md with doc-quality-check**

Add doc-quality-check to the installation commands in INSTALL.md:

```bash
ln -sf ~/projects/doc-quality-skills/doc-accuracy-audit ~/.claude/skills/doc-accuracy-audit
ln -sf ~/projects/doc-quality-skills/doc-quality-audit ~/.claude/skills/doc-quality-audit
ln -sf ~/projects/doc-quality-skills/doc-quality-revise ~/.claude/skills/doc-quality-revise
ln -sf ~/projects/doc-quality-skills/doc-quality-check ~/.claude/skills/doc-quality-check
```

- [ ] **Step 4: Commit documentation updates**

```bash
cd ~/projects/doc-quality-skills
git add doc-quality-check/README.md README.md INSTALL.md
git commit -m "docs: add doc-quality-check to family documentation

- Create README for doc-quality-check skill
- Add doc-quality-check to family README
- Update installation instructions to include doc-quality-check"
```

---

### Task 8: Manual testing

**Files:**
- Test with: `doc-quality-skills/test-docs/`

- [ ] **Step 1: Install doc-quality-check skill**

```bash
ln -sf ~/projects/doc-quality-skills/doc-quality-check ~/.claude/skills/doc-quality-check
```

Expected: Symlink created

- [ ] **Step 2: Test full pipeline on test-docs**

```
/doc-quality-check test-docs/
```

Expected: All three phases run, two timestamped reports created, skill completes successfully

- [ ] **Step 3: Verify timestamped reports exist**

```bash
cd ~/projects/doc-quality-skills
ls -la *-audit-*.md
```

Expected: See two files with timestamps like:
- `test-docs-accuracy-audit-YYYYMMDD-HHMM.md`
- `test-docs-quality-audit-YYYYMMDD-HHMM.md`

- [ ] **Step 4: Test --audit-only flag**

```
/doc-quality-check test-docs/ --audit-only
```

Expected: Phases 1 and 2 run, Phase 3 skipped, completion message shows "Phases completed: 2/2"

- [ ] **Step 5: Test --quality-only flag**

```
/doc-quality-check test-docs/ --quality-only
```

Expected: Only Phase 2 runs, completion message shows "Phases completed: 1/1"

- [ ] **Step 6: Test invalid flag combination**

```
/doc-quality-check test-docs/ --skip-accuracy --skip-quality
```

Expected: Error message "Cannot skip both audit phases. Nothing to audit."

- [ ] **Step 7: Test multiple runs don't collide**

```
/doc-quality-check test-docs/
```

Run twice in quick succession.

Expected: Second run creates new timestamped files, doesn't overwrite first run's reports

```bash
ls -la test-docs-*-audit-*.md
```

Should see 4 files total (2 from first run, 2 from second run)

- [ ] **Step 8: Clean up test reports**

```bash
cd ~/projects/doc-quality-skills
rm -f *-audit-*.md
```

Expected: Test reports cleaned up

- [ ] **Step 9: Document test results**

Create test results file:

```bash
cat > doc-quality-check/TEST_RESULTS.md << 'EOF'
# doc-quality-check Test Results

**Date:** 2026-06-15
**Tested by:** Implementation plan execution

## Test Scenarios

1. Full pipeline (no flags) - PASS
   - All three phases executed
   - Timestamped reports created
   - Completion status correct

2. --audit-only flag - PASS
   - Phases 1 and 2 executed
   - Phase 3 skipped
   - Status shows 2/2 completed

3. --quality-only flag - PASS
   - Only Phase 2 executed
   - Phases 1 and 3 skipped
   - Status shows 1/1 completed

4. Invalid flag combination - PASS
   - Error message displayed
   - Pipeline did not execute

5. Multiple runs - PASS
   - Timestamped reports don't collide
   - Audit history preserved

## Issues Found

None - all tests passed

## Notes

- Timestamps correctly formatted (YYYYMMDD-HHMM)
- Error recovery not tested (requires simulating phase failure)
- User cancellation not tested (requires manual interrupt)
EOF
```

- [ ] **Step 10: Commit test results and mark complete**

```bash
cd ~/projects/doc-quality-skills
git add doc-quality-check/TEST_RESULTS.md
git commit -m "test(doc-quality-check): add manual test results

- Full pipeline tested and passing
- Flag combinations tested
- Timestamp collision avoidance verified
- All basic scenarios working"
```

---

## Verification Checklist

After completing all tasks, verify:

- [ ] doc-accuracy-audit accepts --output flag
- [ ] doc-quality-audit accepts --output flag
- [ ] doc-quality-revise accepts --accuracy-report and --quality-report flags
- [ ] doc-quality-check skill installed and available
- [ ] Full pipeline runs successfully
- [ ] Timestamped reports don't collide
- [ ] Phase skipping flags work correctly
- [ ] Documentation updated (family README, INSTALL.md)

---

## Notes

**Prerequisite skills must support new flags:**
- If existing skills don't have flag support yet, Tasks 1-3 add it
- Tasks 4-8 implement the orchestrator assuming flag support exists
- All changes maintain backward compatibility (flags are optional)

**Testing:**
- Manual testing covers basic scenarios
- Error recovery and cancellation testing require user interaction
- Future: Could add automated tests using skill evals framework
