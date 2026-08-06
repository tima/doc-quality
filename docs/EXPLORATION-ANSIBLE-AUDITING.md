# Exploration: Ansible Playbook/Role/EE/Collection Auditing

**Date:** 2026-08-06  
**Status:** Research/Planning — not yet implemented  
**Scope:** Investigate feasibility and patterns for auditing Ansible infrastructure-as-code artifacts

---

## Problem Statement

Ansible is declarative infrastructure-as-code: playbooks, roles, execution environments (EEs), and collections define system behavior. Like OpenAPI schemas, these are **not traditional code** but still have documentation that drifts from implementation.

**Example mismatches:**
- Playbook docs claim task `configure-firewall` exists; actual playbook has `setup-firewall`
- Role docs say it accepts `var_mode: 'enforce'` default; actual role defaults to `'permissive'`
- EE docs list Python packages that aren't in `requirements.txt`
- Collection docs document a module that's in v2.0 but removed in v2.1

Current tools (doc-accuracy-audit v1.2) handle code + schemas. **Ansible requires new detection logic and patterns.**

---

## Scope: What to Audit

### 1. Playbooks

**Structure:**
- YAML with plays, tasks, handlers, roles, vars, blocks, conditionals
- Top-level plays define scope, registered variables, tags
- Tasks reference modules from Galaxy collections or built-in Ansible modules

**Documentation targets:**
- Documented plays/tasks/handlers should exist in playbook YAML
- Documented variables (input: `vars/`, output: `register`) should match implementation
- Documented tags should be present in playbook
- Documented handlers should be invoked by notify clauses

**Ghost/Hidden detection:**
- Ghost: Docs say "task: Deploy App" but no `name: Deploy App` task in YAML
- Hidden: YAML has task `Configure Logging` but docs don't mention it
- Mismatch: Docs say handler triggers on `service-restart`, actual handler key is `restart-service`

---

### 2. Roles

**Structure:**
- Directories: `tasks/`, `handlers/`, `defaults/`, `vars/`, `meta/`, `templates/`, `files/`
- `meta/main.yml` defines role metadata (deps, tags, platforms)
- `defaults/main.yml` defines default variables with comments
- `tasks/main.yml` contains role logic

**Documentation targets:**
- Documented variables (especially in `defaults/`) match actual default values
- Documented dependencies in role docs match `meta/main.yml` dependencies
- Documented platforms/OS support match `meta/main.yml` metadata
- Documented role interface (inputs: vars) matches `defaults/main.yml` — **Note: Output variable detection deferred to Phase 2+; outputs are conditionally set, often via handlers, and lack standardized documentation in the Ansible ecosystem**

**Ghost/Hidden detection:**
- Ghost: Docs claim role accepts `redis_port` variable; no default defined
- Hidden: Role sets fact `app_version_detected` but docs don't document the output
- Mismatch: Docs say "works on CentOS 7+"; metadata lists only CentOS 8+

---

### 3. Execution Environments (EEs)

**Structure:**
- `execution-environment.yml` defines base image, Python, system packages, Galaxy requirements
- `requirements.txt` (Python dependencies)
- `requirements.yml` (Galaxy collections)
- `_build/` scripts (optional build customizations)

**Documentation targets:**
- Documented Python packages match `requirements.txt` versions/names
- Documented Galaxy collections match `requirements.yml` and versions
- Documented base image matches EE definition
- Documented system packages (if documented) match build scripts

**Ghost/Hidden detection:**
- Ghost: Docs list Python package `requests==2.28.0`; actual requirement is `requests==2.27.0`
- Hidden: `requirements.yml` includes collection `community.general` v5.0, but docs don't mention it
- Mismatch: Docs say "Python 3.11"; base image is `quay.io/ansible/creator-base:python3.10`

---

### 4. Collections

**Structure:**
- `galaxy.yml` defines collection metadata, version, namespace, dependencies
- `plugins/modules/` — module definitions (YAML + Python)
- `plugins/filters/`, `plugins/lookup/`, etc. — other plugin types
- `roles/` — bundled roles
- `docs/` — collection-level documentation

**Documentation targets:**
- Documented modules match files in `plugins/modules/`
- Documented module parameters match YAML/Python argument specs
- Documented roles match roles in `roles/` directory
- Documented dependencies in `galaxy.yml` match actual requirements
- Documented collection version matches `galaxy.yml` version

**Ghost/Hidden detection:**
- Ghost: Docs document module `deploy_app`, but `plugins/modules/deploy_app.py` doesn't exist
- Hidden: Collection includes filter `expand_vars` but it's not documented
- Mismatch: Docs say module parameter `timeout` defaults to 30s; actual code defaults to 60s

---

## Key Differences from Code/Schemas

| Aspect | Code (Python/Go) | Schema (OpenAPI) | Ansible (Playbooks/Roles/EEs/Collections) |
|--------|------------------|------------------|-------------------------------------------|
| **Format** | Source language (Python, Go) | JSON/YAML spec | YAML declarative + Python module code |
| **Structure** | Functions, classes, files | Endpoint/schema definitions | Plays, tasks, roles, plugins, variables |
| **Variables** | Function signatures, defaults | Schema fields, defaults | Role input defaults (defaults/main.yml), role internal vars (vars/main.yml), runtime facts (set_fact) |
| **Behavior** | Logic in code body | Logic in spec rules | Logic in task order, conditionals, handlers |
| **Detection** | AST parsing, grep | YAML parsing, JSON parsing | YAML structure + built-in Ansible conventions (tasks/main.yml, meta/main.yml, defaults/) |
| **Ghost items** | "Function doesn't exist" | "Endpoint not in spec" | "Task name doesn't match", "Variable not defined" |
| **Hidden items** | "Function not documented" | "Spec field not in docs" | "Role has undocumented variable", "Collection includes undocumented module" |

---

## Detection Patterns

### Project Type Detection

**Signals for Ansible project:**
- `galaxy.yml` at root (collection)
- `ansible.cfg` in repo (playbook project or role collection)
- `playbooks/` directory with `*.yml` files (playbook project)
- `roles/` directory with subdirectories matching role structure (role collection or playbook project)
- `execution-environment.yml` (EE)
- `meta/main.yml` with `galaxy_info` section (role)

**Detection logic:**
```
1. If galaxy.yml exists → collection
2. If execution-environment.yml exists → execution environment
3. If roles/{name}/tasks/main.yml AND roles/{name}/meta/main.yml exist → role (or role collection)
4. If playbooks/ exists or *.yml with plays exist → playbook project
5. Else → ansible-project (generic)
```

**Confidence:** High if manifest + consistent structure (e.g., both tasks/ and meta/ present for roles); medium if only directory pattern or partial structure

---

### Task/Role/Variable Name Matching

**Current approach (code):** grep for function names, class definitions  
**Ansible approach:** Parse YAML for semantic structure

**Patterns to detect:**
- **Playbook tasks:** Search for `- name:` lines in YAML files
- **Role input variables:** Parse `defaults/main.yml` for `var_name:` keys (outputs deferred; see Limitations)
- **Role meta:** Parse `meta/main.yml` for dependencies, platforms, tags
- **Handlers:** Search for `- name:` in `handlers/main.yml`
- **Collection modules:** List files in `plugins/modules/*.py` and extract module names
- **EE packages:** Parse `requirements.txt`, `requirements.yml`, `execution-environment.yml`; system packages in `_build/` require regex/heuristic parsing (lower confidence)

**Tool options:**
- `rg`/`grep` for simple name searches (task name = "task-name")
- YAML parser (Python `yaml` lib or `jq`/`yq` for filtering)
- Ansible `galaxy.yml` + file enumeration for collections

---

### Documentation Mismatch Detection

**Accuracy check tasks (analog to doc-accuracy-audit):**

**Task 1: Task/Role/Module Inventory**
- Extract all documented tasks/roles/modules from docs
- Extract actual tasks/roles/modules from playbooks/roles/collections (via YAML parsing or file listing)
- Compare: ghost items (documented but missing), hidden items (exist but undocumented)

**Task 2: Variable/Parameter Audit**
- Extract documented variables (especially `defaults:` section docs)
- Extract actual variable definitions from role `defaults/main.yml` or module argument specs
- Compare defaults: mismatch if docs say `timeout: 30` but code says `timeout: 60`

**Task 3: Dependency/Metadata Audit**
- Extract documented dependencies/platforms/version constraints from docs
- Extract actual metadata from `galaxy.yml`, `meta/main.yml`, `execution-environment.yml`
- Compare: mismatch if docs require Python 3.9 but EE uses 3.8

---

## Known Limitations (Phase 1+)

### Role Output Detection
Role outputs (facts/variables set via `set_fact:`, `register:`, handlers) are **not automatically detectable** in Phase 1. Reasons:
- Variables are conditionally set (not all code paths set all outputs)
- Handlers also set facts (scattered across files)
- Loop variables and transient registers pollute `register:` lists
- Ansible ecosystem has no standardized output documentation format

**Mitigation:** Phase 1 focuses on **input variable validation** (defaults/main.yml). Output validation requires:
- Explicit role interface documentation (README or role spec file)
- Manual audit by role author
- Deferred to Phase 2+ if formal Ansible output specs emerge

### EE System Package Parsing
System packages documented in `_build/` build scripts (e.g., `dnf install`, `apt-get install`) are harder to parse than `requirements.txt`:
- Script format varies by base image (dnf, apt-get, yum, apk)
- Package names may have version constraints or repository specs
- Regex detection has lower confidence than YAML parsing

**Mitigation:** Phase 1 handles `requirements.txt` and `requirements.yml` (YAML/text parsing). System package auditing uses heuristic grep with explicit confidence downgrade or deferred to Phase 2.

### Playbook Multi-File Import/Include
Playbooks split across multiple files via `import_playbooks:` or `include:` are not fully traceable without execution context. Detection must either:
- Require a single playbook entry point, or
- Scan all `*.yml` files in `playbooks/` and accept potential false positives (e.g., non-playbook YAML)

**Decision deferred to Phase 1:** Will define scope based on test projects.

---

## Open Questions

1. **Multi-file playbooks:** How to handle playbooks split across multiple files (imports, includes)? Should we require a single entry point, or scan all `*.yml` in `playbooks/`?

2. **Variable scope:** Ansible variables have scope (play, role, host, global). Should accuracy audit check variable availability in scope, or just presence?

3. **Conditionals:** Documented task might be conditional (`when: condition`). Should audit report missing task even if it's conditional (i.e., docs should say "task runs if X")?

4. **Module parameters:** Ansible modules have YAML argument specs. Should audit extract and validate parameter defaults from module code, or require them to be documented separately?

5. **Idempotence:** Ansible emphasizes idempotence. Should audit check if documented behavior matches idempotent execution (e.g., "ensures X" not "creates X")?

6. **Plugins vs modules:** Collections bundle plugins (modules, filters, lookups, etc.). Should audit treat all plugin types uniformly, or specialize per plugin type?

7. **Testing interaction:** Ansible uses molecule for testing roles. Should audit consider test playbooks as part of role documentation, or separate concern?

---

## Integration Path (If Implemented)

### v1.2+ (Candidate for future release)

**Phase 1: Research & Prototyping**
- Build YAML parser for playbook/role/EE detection
- Test detection on 5 real Ansible projects (collections, roles, EEs)
- Validate ghost/hidden/mismatch patterns against sample docs

**Phase 2: Implement Detection**
- Add `ansible-playbook`, `ansible-role`, `ansible-collection`, `ansible-ee` project types
- Implement task/variable/module enumeration via YAML parsing
- Integrate with existing accuracy-audit framework

**Phase 3: Validation & Release**
- Create test audit on production Ansible repo (e.g., ansible/ansible, ansible-core/ansible-core)
- Document patterns and limitations
- Release as v1.2+ or v2.0 feature

### Deferred Decisions
- Should Ansible auditing use `sg` (ast-grep) for Python module argument specs, or YAML parsing only?
- Should separate skills exist for playbooks vs roles vs collections, or unified skill?
- How to handle Ansible Tower/AWX inventory docs (cluster config, credentials) — out of scope?

---

## References

- Ansible playbook structure: https://docs.ansible.com/ansible/latest/playbook_guide/playbooks.html
- Role structure: https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html
- Collections: https://docs.ansible.com/ansible/latest/collections.html
- Execution Environments: https://docs.ansible.com/automation-platform/latest/execution-environment-guide/
- galaxy.yml spec: https://docs.ansible.com/ansible/latest/galaxy/reference_galaxy_yml.html

---

## Decision Log

**2026-08-06:** Created exploration doc. No implementation commitment. Next step: prototype detection on 2-3 real Ansible projects to validate patterns.

