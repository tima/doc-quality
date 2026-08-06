# TODO: Phase 3 — sg Integration & Tool Dependency Documentation

**Context:** Adversarial review of code-intel handoff recommendations. Decision: defer sg integration to v1.2 (Terraform/OpenAPI), but document rg dependency NOW in README to prevent user confusion.

---

## TODO #3: Document rg Dependency

**File:** README.md

**Location:** New "### System Requirements" subsection under "## Installation"

**Content to add:**

```markdown
### System Requirements

**Required tools:**
- `rg` (ripgrep) — Fast regex search for source code. Install via:
  - macOS: `brew install ripgrep`
  - Ubuntu/Debian: `apt-get install ripgrep`
  - Windows: `choco install ripgrep`
  - See https://github.com/BurntSummaryxyz/ripgrep#installation

- `python3` — Required for project type detection and Python library auditing

**Optional tools:**
- `sg` (ast-grep) — Structural code search. Deferred to v1.2 (Terraform/OpenAPI auditing). Install via:
  - See https://ast-grep.github.io/guide/quick-start.html

**Note:** doc-accuracy-audit currently uses `rg` (v1). sg support is planned for v1.2 when auditing Terraform providers and OpenAPI/Swagger specs.
```

**Verification:** After adding, grep for "rg\|ripgrep" in README and confirm users see the requirement.

---

## TODO #4: Future — sg Integration (v1.2+)

**Deferred milestone:** When Terraform and OpenAPI project types are added (v1.2).

**Actions at that time:**
1. Update System Requirements: move sg from "Optional" to "Required for Terraform/OpenAPI audits"
2. Update SKILL.md (doc-accuracy-audit): Add sg availability check per handoff item #3
3. Update Key Reminder #9: Broaden from "rg or grep only" to "rg, grep, or sg depending on project type"
4. Add Limitations note: "v1.2 supports sg for Terraform (Go) and OpenAPI (YAML) searches. v1 (CLI/library/extension) continues to use rg/grep"

**Tracking:** Link this TODO to RELEASE-NOTES-v1.2.md "Deferred to v2" section once v1.2 is published.

---

## Rationale

**Why document rg now?**
- Users install skills but don't know rg is required until they run a skill and hit "command not found"
- Early failure messaging prevents confusion
- Keeps tool sprawl transparent: rg is committed tool for v1, sg added later when needed

**Why NOT add sg to v1?**
- v1 patterns (CLI tool definitions, library class names) are simple text searches; rg is sufficient and faster
- sg adds complexity for no v1 benefit
- Terraform/OpenAPI (where sg IS valuable) are deferred to v1.2+
- Keeps v1 installation lightweight

