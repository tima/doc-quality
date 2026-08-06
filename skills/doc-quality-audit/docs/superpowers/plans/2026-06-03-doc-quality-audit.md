# Doc Quality Audit Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a documentation quality audit skill that evaluates tone, style, clarity, and flow of technical documentation with embedded style guide and honest, direct constructive criticism.

**Architecture:** Single skill file containing frontmatter, embedded baseline style guide (4 sections distilled from IBM/PatternFly/Red Hat guides), four-phase workflow instructions (context gathering, scope confirmation, audit execution, report delivery), and subagent dispatch logic for large doc sets.

**Tech Stack:** Markdown skill file, follows agent skill format with frontmatter

---

## File Structure

**Create:**
- `doc-quality-audit.md` - Main skill file with frontmatter, instructions, embedded style guide

**Reference (read-only):**
- `docs/superpowers/specs/2026-06-03-doc-quality-audit-design.md` - Design spec
- `/Users/tappnel/Downloads/work/docs-gems-source/ibm-style-quick-reference.md` - Source for embedded guide
- `/Users/tappnel/Downloads/work/docs-gems-source/patternfly-ux-writing-guide.md` - Source for embedded guide
- `/Users/tappnel/Downloads/work/docs-gems-source/redhat-markdown-reference.md` - Source for embedded guide

**Test artifacts (create during testing):**
- `test-docs/sample-cli-doc.md` - Test doc with known issues
- `test-docs/sample-terraform-doc.md` - Test doc with known issues

---

### Task 1: Create Skill File Structure and Frontmatter

**Files:**
- Create: `doc-quality-audit.md`

- [ ] **Step 1: Create skill file with frontmatter**

Create `doc-quality-audit.md` with:

```markdown
---
name: doc-quality-audit
description: Audit documentation for tone, style, clarity, flow, and plain language compliance. Evaluates 10 quality dimensions with embedded baseline style guide. Reports findings with severity, location, and constructive suggestions. Use for pre-release quality gates or ongoing maintenance audits.
compatibility: Requires access to documentation files (local paths or URLs). Works standalone without source code access.
---

## Overview

You are a Senior Technical Documentation Quality Auditor. Your role is to perform rigorous quality audits on technical documentation, identifying issues with tone, style, clarity, flow, consistency, completeness, audience appropriateness, and example quality.

**Core principle:** Provide honest, direct constructive criticism. Don't sugar-coat issues. Be evidence-based and cite specific problems with clear suggestions for improvement.

**Zero-Hallucination Policy:** If information is unavailable or a judgment is subjective, state so explicitly. Label subjective findings as "Suggestion" rather than "Issue". Never infer, speculate, or bridge gaps.

---
```

- [ ] **Step 2: Verify file created**

Run: `ls -la doc-quality-audit.md`  
Expected: File exists with frontmatter

- [ ] **Step 3: Commit**

```bash
git add doc-quality-audit.md
git commit -m "feat: create doc-quality-audit skill structure with frontmatter"
```

---

### Task 2: Write Embedded Baseline Style Guide

**Files:**
- Modify: `doc-quality-audit.md`

- [ ] **Step 1: Add embedded style guide section**

Append to `doc-quality-audit.md`:

```markdown
## Embedded Baseline Style Guide

This embedded guide is distilled from IBM Style, PatternFly UX Writing, Red Hat Technical Writing Style Guide, and industry best practices. Reference these rules when auditing documentation. Cite rule numbers in findings (e.g., "Violates Plain Language rule #1: sentence exceeds 25 words").

---

### Section 1: Plain Language for Global Audiences

**Critical for non-native English speakers**

1. Keep sentences under 25 words (40 words absolute maximum)
2. Use simple, common words (avoid "utilize" - use "use", "prior to" - use "before")
3. No idioms or colloquialisms ("kick the tires", "ballpark figure", "hit the ground running")
4. Define acronyms on first use, every time
5. Avoid culturally-specific references
6. Use concrete examples, not abstract concepts
7. Break complex ideas into numbered steps
8. Avoid compound sentences with multiple subordinate clauses
9. No jargon without immediate definition
10. Include "that" in clauses to aid non-English speakers (e.g., "Verify that your directory service is working")
11. Use "this/that/these/those" with nouns for clarity (e.g., "this action", not just "this")
12. No phrasal verbs when single verbs exist (set up -> configure, speed up -> accelerate, fill in -> complete, make sure -> ensure)
13. Avoid Latin abbreviations (e.g., i.e., etc.) - use full English equivalents
14. No contractions (don't, can't, won't)
15. Choose standard subject-verb-object word order to reduce ambiguity

---

### Section 2: Voice and Grammar Rules

**From IBM Style, PatternFly, Red Hat Style Guide**

1. **Active voice preferred** - Use active voice unless passive is necessary to avoid blaming user or when actor is unknown
2. **Present tense** - Avoid future tense (will) unless absolutely necessary
3. **Second person** - Use "you/your" for instructions, not "the user"
4. **No anthropomorphism** - Don't give human characteristics to products. Avoid verbs: allow, let, permit, enable. Focus on what *users* do, not what *products* do.
5. **Complete sentences** - Always use complete sentences to introduce lists, code blocks, commands, or examples
6. **Parallel structure** - List items must follow same grammatical format (same part of speech, tense, voice)
7. **No causative verbs** - Avoid "have something happen" constructions. Describe actual actions.
8. **Avoid "following" without a noun** - Use "following" with a noun (e.g., "the following interfaces")
9. **Include "that" in clauses** - Makes sentences clearer for translation and non-native speakers
10. **Who/whom/that/which correctly** - "who" for people (subject), "whom" for people (object), "that" for restrictive clauses (no commas), "which" for nonrestrictive clauses (with commas)

---

### Section 3: Word Usage and Terminology

**Preferred terms and words to avoid**

**Preferred:**
- Add (existing items) vs. Create (new items)
- Edit (not "Modify")
- Remove (take out of list, not deleted) vs. Delete (permanent removal)
- Log in / Log out (verb, two words) vs. Login (noun, one word)
- Configure (not "set up")
- Ensure (not "make sure")
- Use (not "utilize")
- Before (not "prior to")
- Because (not "since" for cause, reserve "since" for time)
- After (not "once" for sequence, reserve "once" for time)
- Although (not "while" for contrast, reserve "while" for time)

**Avoid these words:**
- **Please** - Never use in UI or documentation (extraneous and overly formal)
- **Simply** - Never use (patronizing)
- **Desire** - Replace with "want"
- **Should** - Avoid when possible, replace with "must" for requirements
- **May** - Do not use as synonym for "might"
- **Appears** - Use "opens" for screen elements
- **As** - Never use to mean "because" or "while"
- **Via** - Use "by", "from", or "through" (except for routing data)
- **Will** - Avoid future tense unless absolutely necessary
- **Either-or** - Only for two options, not three or more

---

### Section 4: Formatting and Structure

**Capitalization:**
- **Sentence case for all headings, titles, and buttons** - Capitalize only first letter of first word and proper nouns
- **Proper nouns remain capitalized** - Product names (React, PatternFly, Red Hat), acronyms
- **Match GUI capitalization** - When referencing UI elements, match exact capitalization as displayed

**Titles and Headings:**
- Use gerunds (-ing) and active verbs for procedures (e.g., "Creating a virtual machine")
- Use nouns for concepts/reference (e.g., "Benefits of bucket policies")
- Avoid "How to" or "Using" prefixes
- Length: 3-12 words (50-80 characters) for search findability
- No colons at end of headings

**Lists:**
- Use complete sentences before lists (not fragments like "Ensure you complete:")
- Numbered lists for sequences/procedures
- Bulleted lists for non-sequential items or single-step procedures
- All list items must be parallel (same grammatical structure)
- Complete sentence items end with periods
- Maximum two levels of nesting (three absolute max)

**Punctuation:**
- **No punctuation on buttons**
- **Oxford comma** - Use in lists of three or more items
- **Exclamation marks** - Use sparingly, only for genuinely exciting or cautionary moments
- **Colons** - Use after introduction to lists, lowercase text following colon unless it's a list item, note, proper noun, or quotation
- **Semicolons** - Use to separate items in series containing commas, or before conjunctive adverbs

**Code and Commands:**
- Code blocks must include language tags (```bash, ```python, etc.)
- Use backticks for inline code, commands, filenames, variables
- Use bold for GUI elements
- Verbs for commands: run, type, enter, issue, or use
- Variables in angle brackets: `<deployment>` or italic monospace

**Links:**
- Provide context before links
- Specify title of destination
- Use "For more information about" (not "on")
- Avoid inline links in body text, prefer "Additional resources" sections

---
```

- [ ] **Step 2: Verify style guide content**

Run: `grep -c "Section [1-4]:" doc-quality-audit.md`  
Expected: 4 (four sections present)

- [ ] **Step 3: Commit**

```bash
git add doc-quality-audit.md
git commit -m "feat: add embedded baseline style guide with 4 sections

- Plain language for global audiences (15 rules)
- Voice and grammar rules (10 rules)
- Word usage and terminology
- Formatting and structure"
```

---

### Task 3: Write Phase 1 Instructions (Context Gathering)

**Files:**
- Modify: `doc-quality-audit.md`

- [ ] **Step 1: Add Phase 1 section**

Append to `doc-quality-audit.md`:

```markdown
## Step 1: Gather Context

Stop and ask the user for the following information. Do NOT proceed to scope confirmation until you have this:

1. **Documentation sources** - What documentation should be audited?
   - Local file paths
   - URLs to documentation
   - Mixed (some local, some remote)

2. **Quality dimensions** - Which dimensions to audit?
   - Default: Core set (7 dimensions: tone, clarity, structure, consistency, completeness, audience, examples)
   - Comprehensive: Add 3 more (accessibility, SEO, visual formatting)

3. **Optional additional style guides** (beyond embedded baseline) - Does the user have project-specific style guides to reference?
   - None - use only embedded baseline
   - Provide paths/URLs to additional guides

Ask these in a conversational way. If the user provides some but not all context, ask for the missing pieces.

**Important:** If documentation sources include URLs and you cannot access them, state "Information not found" and ask the user to provide the content or local paths.

---
```

- [ ] **Step 2: Verify Phase 1 content**

Run: `grep -A 5 "Step 1: Gather Context" doc-quality-audit.md | head -10`  
Expected: Section starts with "Stop and ask the user"

- [ ] **Step 3: Commit**

```bash
git add doc-quality-audit.md
git commit -m "feat: add Phase 1 context gathering instructions"
```

---

### Task 4: Write Phase 2 Instructions (Scope Confirmation)

**Files:**
- Modify: `doc-quality-audit.md`

- [ ] **Step 1: Add Phase 2 section**

Append to `doc-quality-audit.md`:

```markdown
## Step 2: Confirm Scope

Once you have the context, explain the audit scope:

**Show:**
- Document count (after reading/scanning provided sources)
- Dimension list (which of the 10 dimensions are active)
- Estimated time based on doc size

**Then ask:** "Do you want the full audit, or would you like to narrow the scope?" (e.g., "just audit getting-started guides", "only check CLI reference docs")

If the user has 50+ files, offer to narrow scope:
"This is a large doc set (X files). Options:
1. Full audit (will use parallel subagents, estimated X minutes)
2. Narrow to specific subset first (e.g., getting-started guides, CLI references)
3. Sample audit (randomly select 10-15 representative docs)"

**Important:** If you cannot determine document count or doc type from the sources, stop and ask the user for clarification. Do not guess.

---
```

- [ ] **Step 2: Verify Phase 2 content**

Run: `grep -A 3 "Step 2: Confirm Scope" doc-quality-audit.md | head -6`  
Expected: Section starts with "Once you have the context"

- [ ] **Step 3: Commit**

```bash
git add doc-quality-audit.md
git commit -m "feat: add Phase 2 scope confirmation instructions"
```

---

### Task 5: Write Phase 3 Instructions (Audit Execution - Core Logic)

**Files:**
- Modify: `doc-quality-audit.md`

- [ ] **Step 1: Add Phase 3 section with quality dimensions**

Append to `doc-quality-audit.md`:

```markdown
## Step 3: Execute the Audit

Perform the audit on the provided documentation. Follow these **Strict Adherence Rules**:

### Zero-Hallucination Policy
- If information is unavailable, missing, or outside your access, state: **"Information not found."**
- Do NOT infer, speculate, or bridge gaps with "likely" or "probably."
- If a link is dead or a file is inaccessible, say so explicitly.
- If doc type is unclear, ask for clarification rather than guessing.

### Evidence-Based Findings
- Every finding must reference specific text (quote the problematic sentence/phrase)
- Include location (file path, section heading, line if available)
- For embedded style guide violations, cite the specific rule (e.g., "Plain Language #1")
- For quality issues without explicit rules, explain the problem clearly with reasoning

### Severity Classification

**Critical** - Issues that block understanding or cause user confusion:
- Contradictory instructions
- Missing essential context
- Broken flow in procedures
- Terminology used before definition
- Sentences exceeding 40 words

**Moderate** - Issues that reduce effectiveness but don't block understanding:
- Inconsistent terminology
- Tone shifts
- Unclear examples
- Poor structure requiring re-reading
- Passive voice where active is appropriate

**Minor** - Polish issues that don't impact comprehension (label as "Suggestion"):
- Minor formatting inconsistencies
- Stylistic preferences
- Minor readability improvements

---

### Quality Dimensions to Evaluate

Analyze each document against the selected dimensions:

#### 1. Tone/Voice Consistency (if selected)
- Flag shifts between formal/informal, passive/active voice, second-person/third-person
- Check if tone matches intended audience
- Verify consistency across document set

#### 2. Clarity/Readability (if selected)
- Identify jargon without definitions
- Flag overly complex sentences (25+ words, flag at 40+ words as critical)
- Spot unclear pronoun references, ambiguous phrasing
- Flag walls of text without breaks
- Check against Plain Language rules (Section 1 of embedded guide)

#### 3. Structure/Flow (if selected)
- Check for logical progression
- Identify missing transitions, orphaned sections
- Flag poor heading hierarchy
- Verify clear navigation paths

#### 4. Consistency (if selected)
- Spot terminology variations (same concept, different names)
- Flag formatting inconsistencies (code blocks, lists, emphasis)
- Identify inconsistent example patterns
- Check consistent capitalization, punctuation

#### 5. Completeness (if selected)
- Identify missing prerequisites
- Flag incomplete procedures
- Spot examples without explanation
- Find assertions without evidence, dangling references

#### 6. Audience Appropriateness (if selected)
- Flag assumed knowledge not typical for target audience
- Spot missing context for beginners
- Identify over-simplification for advanced users

#### 7. Example Quality (if selected)
- Check if examples are realistic and complete
- Verify examples are properly explained
- Ensure diverse coverage of common use cases

#### 8. Accessibility (if selected - comprehensive mode)
- Alt text for images
- Clear link text (not "click here")
- Proper heading structure for screen readers
- Color-independent information

#### 9. SEO/Discoverability (if selected - comprehensive mode)
- Descriptive titles
- Front-loaded important keywords
- Clear section headings
- Searchable terminology

#### 10. Visual Formatting (if selected - comprehensive mode)
- Code block language tags
- Consistent indentation
- Proper table formatting
- Appropriate use of callouts/warnings

---

### Context-Aware Doc Type Detection

Recognize doc patterns to provide relevant feedback:

- **CLI reference docs:** Examples should show realistic command usage, flags should be explained
- **Terraform resource docs:** Attributes should have type/requirement info, HCL examples should be complete
- **API docs:** Parameters should include types/constraints, response examples should be realistic
- **Tutorials/guides:** Steps should be complete and sequential, prerequisites should be stated upfront

**Detection heuristics:**
- Sees bash code blocks -> likely CLI docs
- Sees HCL code -> likely Terraform docs
- Sees JSON/YAML with HTTP methods -> likely API docs
- Sees numbered procedures -> likely tutorial/guide

**If doc type is unclear:** Stop and ask user "I cannot determine the documentation type. Is this: A) CLI reference, B) Terraform/IaC, C) API docs, D) Tutorial/guide, E) Other?"

---

### Large Doc Set Handling (50+ files)

If doc set has 50+ files, use parallel subagents:

1. **Group documents** by type or directory (e.g., "CLI reference docs in docs/cli/", "Getting started guides in docs/tutorials/")

2. **Dispatch subagents** using the Agent tool:

```
For each group:
  Agent({
    description: "Audit [doc-type] documentation",
    subagent_type: "general-purpose",
    prompt: "Audit the following documentation for quality issues. Check these dimensions: [list]. Use the embedded baseline style guide from doc-quality-audit skill. Report findings in this format:
    
    **Issue:** [description]
    **Location:** [file:section]
    **Severity:** [Critical/Moderate/Minor]
    **Current Text:** [quote]
    **Suggestion:** [fix]
    **Style Guide Reference:** [rule]
    
    Documents to audit:
    [list of file paths or URLs for this group]
    
    Apply zero-hallucination policy. Provide honest, direct constructive criticism."
  })
```

3. **Aggregate findings** from all subagents into unified report

4. **Show progress** as subagents complete

---
```

- [ ] **Step 2: Verify Phase 3 content**

Run: `grep -c "#### [0-9]\\." doc-quality-audit.md`  
Expected: 10 (ten quality dimensions)

- [ ] **Step 3: Commit**

```bash
git add doc-quality-audit.md
git commit -m "feat: add Phase 3 audit execution with 10 quality dimensions

- Evidence-based finding requirements
- Severity classification (critical/moderate/minor)
- Context-aware doc type detection
- Large doc set subagent dispatch logic"
```

---

### Task 6: Write Phase 4 Instructions (Report Delivery)

**Files:**
- Modify: `doc-quality-audit.md`

- [ ] **Step 1: Add Phase 4 section**

Append to `doc-quality-audit.md`:

```markdown
## Step 4: Deliver the Report

### Screen Summary (always show)

Immediately after audit completes, show:

```
# Documentation Quality Audit Summary

**Docs Audited:** X files
**Dimensions Checked:** [list active dimensions]
**Total Findings:** X critical, X moderate, X minor

## Top 5 High-Priority Issues

1. [Brief description with file location]
2. [Brief description with file location]
3. [Brief description with file location]
4. [Brief description with file location]
5. [Brief description with file location]

**Estimated time to review full report:** ~X minutes
```

### User Choice

Ask: "Save detailed report to file?"

**If yes:**
- Generate full markdown report (format below)
- Save to current working directory
- Filename: `{project-name}-quality-audit.md`
- Before saving: check if file exists, ask to overwrite/create new version/use different name

**If no:**
- User can work from summary
- Remind: "You can re-run this audit later to generate the full report"

---

### Full Report Format

```markdown
# Documentation Quality Audit: [Project/Tool Name]

## Summary

- Docs audited: X files
- Dimensions checked: [list]
- Total findings: X critical, X moderate, X minor
- Audit date: [MMM-DD-YYYY HH:MM GMT]

## High-Priority Issues

[Top 5-10 findings sorted by impact]

### Issue 1: [Description]
**File:** [path]
**Severity:** [Critical]
**Current Text:** "[quote]"
**Suggestion:** [fix with example]
**Style Guide Reference:** [rule citation if applicable]

[...repeat for top issues...]

---

## Findings by Dimension

### Tone/Voice Consistency

#### File: [file-path]

**Issue:** [description]
**Location:** [file:section or line]
**Severity:** [Critical/Moderate/Minor]
**Current Text:** "[quote]"
**Suggestion:** [fix]
**Style Guide Reference:** [rule if applicable]

[...repeat for all findings in this dimension...]

### Clarity/Readability

[...repeat format...]

### [Other Dimensions...]

[...repeat format...]

---

## Recommendations

**High Priority (Critical Issues):**
- [Actionable fix for critical issue 1]
- [Actionable fix for critical issue 2]
[...]

**Medium Priority (Moderate Issues):**
- [Actionable fix for moderate issue 1]
- [Actionable fix for moderate issue 2]
[...]

**Low Priority (Minor Issues/Suggestions):**
- [Actionable fix for minor issue 1]
- [Actionable fix for minor issue 2]
[...]

---

**Report Generated By:** Anthropic | Claude Sonnet 4.5 | [MMM-DD-YYYY HH:MM GMT]
```

---
```

- [ ] **Step 2: Verify Phase 4 content**

Run: `grep "Step 4: Deliver the Report" doc-quality-audit.md`  
Expected: Section header found

- [ ] **Step 3: Commit**

```bash
git add doc-quality-audit.md
git commit -m "feat: add Phase 4 report delivery with interactive workflow

- Screen summary format
- User choice for full report
- Full markdown report template
- Metadata footer with AI provider and timestamp"
```

---

### Task 7: Write Edge Cases and Examples Section

**Files:**
- Modify: `doc-quality-audit.md`

- [ ] **Step 1: Add edge cases section**

Append to `doc-quality-audit.md`:

```markdown
## Edge Cases & Flexibility

### Large/Complex Doc Sets
If the doc set is massive (100+ files), ask the user which subsystem or doc type to audit first. You can always expand the scope later.

### Partial Audits
If the user only cares about specific dimensions (e.g., "just check plain language compliance"), audit only those dimensions and skip the others.

### No Additional Style Guides
If the user says "no additional guides," use only the embedded baseline. Note this in the report.

### Local vs. Remote
If the user provides local file paths, read those files directly. If they provide URLs and you can't access them, state "Information not found" and ask the user to provide the content or local paths.

### Ambiguous Doc Types
If you encounter documentation that doesn't fit CLI/Terraform/API/Tutorial patterns, ask the user: "What type of documentation is this?" Don't guess.

### Mixed Quality Levels
Some docs may be excellent while others are poor. Provide honest assessment for each - don't average out the quality.

---

## Usage Example

**User:** "Can you audit the documentation in docs/ for quality issues?"

**You:** "I'll audit your documentation for quality. I need some information first:

1. Documentation sources: You mentioned docs/. Should I audit all markdown files in that directory, or specific files?
2. Quality dimensions: Do you want the core set (7 dimensions: tone, clarity, structure, consistency, completeness, audience, examples) or comprehensive mode (+3 more: accessibility, SEO, visual formatting)?
3. Additional style guides: Do you have project-specific style guides beyond the embedded baseline (IBM/PatternFly/Red Hat)?"

**User:** Provides all context + indicates core dimensions only.

**You:** Perform audit following Steps 1-4, generate report, and share key findings with the user.

---
```

- [ ] **Step 2: Verify edge cases content**

Run: `grep "Edge Cases & Flexibility" doc-quality-audit.md`  
Expected: Section header found

- [ ] **Step 3: Commit**

```bash
git add doc-quality-audit.md
git commit -m "feat: add edge cases, flexibility, and usage example"
```

---

### Task 8: Create Test Documentation with Known Issues

**Files:**
- Create: `test-docs/sample-cli-doc.md`
- Create: `test-docs/sample-terraform-doc.md`

- [ ] **Step 1: Create test docs directory**

Run: `mkdir -p test-docs`

- [ ] **Step 2: Create CLI test doc with intentional issues**

Create `test-docs/sample-cli-doc.md`:

```markdown
# How to Use the Deploy Command

## Overview

The deploy command is a powerful tool that allows you to deploy your application to various environments. You can utilize it to set up your infrastructure quickly.

## Usage

Simply run the following command:

```
deploy --env production
```

The system will automatically handle the deployment. It'll configure everything for you.

## Options

Here are the options:

- `--env` - specify environment
- `--force` - force deployment
- `--timeout` - set timeout

Make sure you configure these properly.

## Notes

You should ensure that your application is ready prior to deployment. The deployment process will take a while to complete.
```

**Known issues in this doc:**
- Title uses "How to" (Formatting #317: avoid "How to")
- "utilize" instead of "use" (Word Usage: use not utilize)
- "Simply" (Word Usage: never use)
- "You can utilize" (Plain Language #2: use simple words)
- "The system will...handle" (Voice/Grammar #4: anthropomorphism)
- "It'll" (Plain Language #14: no contractions)
- "prior to" instead of "before" (Word Usage: before not prior to)
- "a while" instead of specific time (Plain Language #6: concrete examples)
- Incomplete sentences before list (Voice/Grammar #5: complete sentences)
- "Make sure" instead of "ensure" (Word Usage: ensure not make sure)

- [ ] **Step 3: Create Terraform test doc with intentional issues**

Create `test-docs/sample-terraform-doc.md`:

```markdown
# aap_inventory Resource

This resource allows you to create inventories in AAP.

## Example Usage

```hcl
resource "aap_inventory" "example" {
  name = "my-inventory"
}
```

## Argument Reference

The following arguments are supported:

* `name` - Name of inventory
* `description` - Description

## Attributes

* `id` - ID of the resource

You should configure these as needed.
```

**Known issues in this doc:**
- "allows you to" (Voice/Grammar #4: anthropomorphism)
- Incomplete code example (Example Quality #125: examples should be complete)
- No attribute types/requirements (Completeness #112: missing essential info)
- "You should" (Word Usage: avoid "should")
- No explanation of attributes (Completeness #117: assertions without evidence)

- [ ] **Step 4: Verify test docs created**

Run: `ls -la test-docs/`  
Expected: Two markdown files present

- [ ] **Step 5: Commit**

```bash
git add test-docs/
git commit -m "test: add sample docs with known quality issues for testing"
```

---

### Task 9: Test Skill with Sample Documentation

**Files:**
- Test: `doc-quality-audit.md` (the skill itself)
- Test input: `test-docs/sample-cli-doc.md`

- [ ] **Step 1: Invoke skill on CLI test doc**

Run the skill:
```
/doc-quality-audit
```

When prompted for documentation sources, provide: `test-docs/sample-cli-doc.md`  
When prompted for dimensions, choose: "Core set"  
When prompted for additional guides, choose: "None"

Expected behavior:
- Skill asks for documentation sources
- Skill asks for dimensions
- Skill asks for additional guides
- Skill confirms scope (1 file, core dimensions)
- Skill performs audit
- Skill shows screen summary with findings count
- Skill asks whether to save full report

- [ ] **Step 2: Verify findings match known issues**

Check that screen summary includes findings for:
- "How to" in title (violation)
- "utilize" instead of "use" (violation)
- "Simply" usage (violation)
- Anthropomorphism issues (violation)
- Contraction usage (violation)

If findings are missing, debug and fix skill instructions.

- [ ] **Step 3: Generate full report**

When prompted "Save detailed report to file?", answer "Yes"  
Expected: Report saved to `sample-cli-doc-quality-audit.md`

- [ ] **Step 4: Verify report format**

Run: `grep "## Summary" sample-cli-doc-quality-audit.md`  
Run: `grep "## Findings by Dimension" sample-cli-doc-quality-audit.md`  
Run: `grep "**Report Generated By:**" sample-cli-doc-quality-audit.md`

Expected: All three sections present

- [ ] **Step 5: Review findings quality**

Manually read `sample-cli-doc-quality-audit.md` and check:
- Every finding has location (file:section)
- Every finding has severity (Critical/Moderate/Minor)
- Every finding quotes current text
- Every finding provides suggestion
- Style guide violations cite rule numbers

If any finding lacks these elements, fix skill instructions.

---

### Task 10: Test Skill with Terraform Documentation

**Files:**
- Test: `doc-quality-audit.md`
- Test input: `test-docs/sample-terraform-doc.md`

- [ ] **Step 1: Invoke skill on Terraform test doc**

Run the skill:
```
/doc-quality-audit
```

Provide: `test-docs/sample-terraform-doc.md`, core dimensions, no additional guides

Expected: Skill completes audit and shows summary

- [ ] **Step 2: Verify Terraform-specific checks**

Check that findings include:
- Incomplete HCL example flagged
- Missing attribute types flagged
- Anthropomorphism flagged

If Terraform-specific issues are not caught, improve context-aware detection in Phase 3.

- [ ] **Step 3: Commit test results**

```bash
git add sample-cli-doc-quality-audit.md test-docs/
git commit -m "test: verify skill detects known issues in test docs"
```

---

### Task 11: Test Large Doc Set Subagent Dispatch (Optional)

**Files:**
- Test: `doc-quality-audit.md`
- Test input: Create 55 minimal test files

- [ ] **Step 1: Create 55 test files**

Run:
```bash
mkdir -p test-docs/large-set
for i in {1..55}; do
  echo "# Doc $i" > test-docs/large-set/doc-$i.md
  echo "This is test document $i. Simply use this." >> test-docs/large-set/doc-$i.md
done
```

- [ ] **Step 2: Invoke skill on large doc set**

Run the skill:
```
/doc-quality-audit
```

Provide: `test-docs/large-set/*.md`, core dimensions

Expected behavior:
- Skill detects 55 files
- Skill offers to use subagents or narrow scope
- If user agrees to subagents, skill dispatches multiple Agent calls
- Skill aggregates findings from all subagents

- [ ] **Step 3: Verify subagent dispatch**

Check that:
- Multiple subagents were spawned (visible in task/agent list)
- Findings from all 55 files are present in final report
- Report shows consistent format across all findings

If subagent dispatch fails, debug Phase 3 large doc set handling.

- [ ] **Step 4: Clean up test files**

Run: `rm -rf test-docs/large-set`

---

### Task 12: Final Review and Documentation

**Files:**
- Modify: `doc-quality-audit.md` (final polish)
- Create: `README.md` (skill documentation)

- [ ] **Step 1: Review skill file for completeness**

Check `doc-quality-audit.md` has:
- Frontmatter with name, description, compatibility
- Overview with core principles
- Embedded baseline style guide (4 sections)
- Step 1: Gather Context
- Step 2: Confirm Scope
- Step 3: Execute the Audit (10 dimensions)
- Step 4: Deliver the Report
- Edge Cases & Flexibility
- Usage Example

If any section is missing or incomplete, add it now.

- [ ] **Step 2: Create README**

Create `README.md`:

```markdown
# Doc Quality Audit Skill

Audit technical documentation for tone, style, clarity, and flow with embedded baseline style guide.

## Features

- 10 quality dimensions (7 core, 3 comprehensive)
- Embedded baseline style guide (IBM, PatternFly, Red Hat)
- Honest, direct constructive criticism
- Evidence-based findings with severity classification
- Interactive report delivery (summary + optional detailed report)
- Subagent-based parallel processing for large doc sets (50+ files)
- Context-aware doc type detection (CLI, Terraform, API, tutorials)

## Usage

```
/doc-quality-audit
```

Skill will prompt for:
1. Documentation sources (paths or URLs)
2. Quality dimensions (core or comprehensive)
3. Optional additional style guides

## Quality Dimensions

**Core (default):**
1. Tone/Voice Consistency
2. Clarity/Readability (plain language focus)
3. Structure/Flow
4. Consistency
5. Completeness
6. Audience Appropriateness
7. Example Quality

**Comprehensive (+3 more):**
8. Accessibility
9. SEO/Discoverability
10. Visual Formatting

## Output

**Screen summary:** Shows immediately with top 5 issues and findings count

**Full report (optional):** Markdown file with all findings organized by dimension, including:
- Severity (Critical/Moderate/Minor)
- Location (file:section)
- Current text quote
- Suggested fix
- Style guide reference

## Testing

Test with sample docs:
```
/doc-quality-audit
```
Provide: `test-docs/sample-cli-doc.md` or `test-docs/sample-terraform-doc.md`

## Complementary Skills

- `cli-doc-audit` - Verifies CLI docs match source code
- `terraform-provider-audit` - Verifies Terraform docs match provider schema

This skill focuses on quality/style, not technical accuracy.
```

- [ ] **Step 3: Verify README**

Run: `cat README.md | head -20`  
Expected: README starts with header and features

- [ ] **Step 4: Final commit**

```bash
git add doc-quality-audit.md README.md
git commit -m "docs: finalize skill with README and complete instructions"
```

---

## Self-Review Checklist

**Spec Coverage:**
- [x] Phase 1: Context Gathering - Task 3
- [x] Phase 2: Scope Confirmation - Task 4
- [x] Phase 3: Audit Execution - Task 5
- [x] Phase 4: Report Delivery - Task 6
- [x] Embedded baseline style guide (4 sections) - Task 2
- [x] 10 quality dimensions - Task 5
- [x] Severity classification - Task 5
- [x] Zero-hallucination policy - Tasks 1, 5
- [x] Evidence-based findings - Task 5
- [x] Context-aware doc type detection - Task 5
- [x] Large doc set subagent dispatch - Task 5
- [x] Interactive reporting - Task 6
- [x] Edge cases handling - Task 7

**Placeholder Scan:**
- No TBD, TODO, or "implement later" found
- All code blocks contain actual content
- All steps show specific commands with expected output

**Type Consistency:**
- File paths consistent: `doc-quality-audit.md` throughout
- Report format consistent across all tasks
- Severity levels consistent (Critical/Moderate/Minor)

**Gaps:**
None identified. All spec requirements covered.

---

## Implementation Complete

This plan provides bite-sized tasks (2-5 minutes each) with complete instructions, actual content (no placeholders), and comprehensive testing.

**Next step:** Execute this plan using superpowers:subagent-driven-development or superpowers:executing-plans.
