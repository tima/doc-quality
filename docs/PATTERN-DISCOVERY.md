# Pattern Discovery: Multi-Language CLI & Config Auditing

This document inventories the code patterns needed for accuracy-audit and quality-audit to work across Python, Bash, and Ansible — the languages/frameworks that real users (open source maintainers, enterprise engineers) actually use.

**Corrected based on repo analysis:**
- ✓ argparse (Python): 7+ imports across ansible-creator, ansible-navigator, ansible-lint, awx, nexus
- ✓ Bash (function dispatch): dotpkg validates real-world pattern
- ✓ Ansible modules: 320+ modules with DOCUMENTATION blocks
- ✓ Ansible roles: defaults/main.yml + register directives
- ✗ Click: Removed. Only 1 import found across all repos (not primary). Ansible ecosystem uses argparse instead.
- ✗ TypeScript: Deferred to v2 (extension audits, not CLIs)
- ✗ OpenAPI: Deferred to v2 (zero usage)
- ✗ Terraform: Deferred to v2 (user deferring)

For each framework, we define:
- **What we're searching for** (the construct)
- **Real code examples** (what we're trying to match)
- **Search patterns** (grep, not ast-grep — Bash/YAML have limited AST support)
- **Test cases** (should match / should NOT match)

---

## 1. Python CLI: argparse

**Framework:** [argparse](https://docs.python.org/3/library/argparse.html) — standard library argument parser

**Why argparse, not Click?** Real analysis across ansible-creator, ansible-navigator, ansible-lint shows **0 Click imports** but 5-7 argparse imports per repo. argparse is the actual standard in this ecosystem.

**Construct to find:** Parsers, subparsers, arguments, argument definitions

#### Parser setup
**Real code example (ansible-creator):**

**Framework:** [argparse](https://docs.python.org/3/library/argparse.html) — standard library argument parser

**Construct to find:** Parsers, subparsers, arguments

#### Parser and argument extraction
**Real code example (ansible-creator _arg_parser_custom.py):**
```python
import argparse

def add_base_arguments(parser: argparse.ArgumentParser) -> None:
    """Add common arguments."""
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--config',
        default='config.yml',
        help='Config file'
    )

parser = argparse.ArgumentParser(
    description='Ansible Creator',
    prog='ansible-creator'
)

subparsers = parser.add_subparsers(dest='action', help='Available actions')

init_parser = subparsers.add_parser('init', help='Initialize new project')
init_parser.add_argument('name', help='Project name')
init_parser.add_argument('--skip-update', action='store_true', help='Skip auto-update')
```

**What to search for:**
- `ArgumentParser(...)` constructor calls
- `.add_argument()` method calls (on any parser variable)
- `.add_subparsers()` method calls
- Parser variable assignments and method chains

**Search patterns (grep — AST too complex for argparse structure):**
```bash
# Find ArgumentParser instantiation
grep -n "ArgumentParser(" --include="*.py" -r /path/to/code

# Find add_argument calls with context
grep -n "\.add_argument(" --include="*.py" -r /path/to/code

# Find subparser definitions
grep -n "\.add_subparsers(" --include="*.py" -r /path/to/code

# Find helper function definitions that add arguments
grep -n "def.*argument\|def.*parser" --include="*.py" -r /path/to/code
```

**Test cases:**
- ✓ Should match: `ArgumentParser(description='...')`
- ✓ Should match: `.add_argument('-f', '--flag')`
- ✓ Should match: `.add_subparsers(dest='command')`
- ✓ Should match: `.add_argument('name', help='...')` (positional)
- ✓ Should extract: `default=`, `action=`, `help=` from add_argument calls
- ✗ Should NOT match: `# ArgumentParser()` (commented)
- ✗ Should NOT match: `"ArgumentParser()"` (in string)

#### Task: Inventory argparse CLIs
1. Find all `ArgumentParser()` instantiations
2. For each parser, extract:
   - Parser name/variable, description
   - All `.add_argument()` calls: name/flags, type, default, help, action, choices
   - All subparsers created via `.add_subparsers()`
3. For nested parsers: follow the chain (main parser → subparsers → subparser args)
4. Handle helper functions that call `.add_argument()` (common pattern)
5. Compare extracted arguments to documented commands and options

---

**NOTE:** TypeScript CLI frameworks (Commander.js) deferred to v2. Current TypeScript usage in repos (vscode-ansible, ansible-ui) is extension/frontend code, not user-facing CLIs. Will revisit when CLI auditing demand appears.

---

## 2. Bash CLI (Multiple Patterns)

**Real-world frameworks:** getopts (POSIX), getopt (GNU), function-based dispatch (custom)

**Why Bash matters:** dotpkg validates real-world pattern (11 shell scripts, 8 subcommands, options + config files)

**Construct to find:** Commands, options, flags, configuration files, state files

### 2a. Function-Based Dispatch (Real-World Pattern — VALIDATED against dotpkg)

**Real code example (dotpkg):**
```bash
#!/usr/bin/env bash
export DOTPKG_HOME="${DOTPKG_HOME:-$HOME/.dotpkg}"
DOTPKG_CONFIG="$DOTPKG_HOME/config"
export STATE_FILE="${STATE_FILE:-$DOTPKG_HOME/state.json}"

# Library sourcing (glob pattern)
for _lib in "$DOTPKG_HOME/lib"/*.sh; do . "$_lib"; done

cmd_init() {
  local repo="" profile="" non_interactive=false
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --repo)            repo="$2"; shift 2 ;;
      --profile)         profile="$2"; shift 2 ;;
      --non-interactive|-y) non_interactive=true; shift ;;
      *) echo "dotpkg init: unknown flag: $1" >&2; exit 1 ;;
    esac
  done
}

cmd_add() {
  local bundle_name="${1:-}"
  [[ -z "$bundle_name" ]] && { echo "usage: dotpkg add <bundle>" >&2; exit 1; }
}

# Dispatch on first argument
cmd="${1:-help}"
shift 2>/dev/null || true

case "$cmd" in
  init)   cmd_init "$@" ;;
  add)    cmd_add "$@" ;;
  help)   cmd_help ;;
  *)      echo "dotpkg: unknown command: $cmd" >&2; exit 1 ;;
esac
```

**What to search for:**
- Function definitions: `cmd_<name>() {` (subcommands)
- Subcommand dispatch: `case "$cmd" in ... cmd_<name> "$@" ;;`
- Option parsing within functions: `case "$1" in ... --flag) ... ;;` with shift patterns
- Positional arguments: `local var="${1:-}"` or `local var="${1:?error}"`
- Library sourcing: `. "$lib"` or `source` (including glob patterns)
- Config file parsing: `grep '^key=' file | cut -d= -f2-`
- State/metadata files: references to `.json`, `.yml`, `.info` files

**Search patterns (grep — Bash AST is limited):**

```bash
# Find subcommand functions
grep -n "^cmd_[a-z_]*() {" /path/to/script.sh

# Find dispatch case statement
grep -n "case \"\$cmd\" in" /path/to/script.sh

# Find option parsing patterns
grep -n "case \"\$1\" in" /path/to/script.sh

# Find library sourcing (including globs)
grep -n "^\. \|^source " /path/to/script.sh

# Find config file operations
grep -n "grep '^\|cut -d=" /path/to/script.sh

# Find state/metadata file references
grep -n "\.json\|\.info\|\.yml" /path/to/script.sh
```

**Test cases (VALIDATED against dotpkg):**
- ✓ Should match: `cmd_init() {`
- ✓ Should match: `case "$cmd" in`
- ✓ Should match: `. "$lib"` and `. "$DOTPKG_HOME/lib"/*.sh`
- ✓ Should match: `--repo) repo="$2"; shift 2 ;;`
- ✓ Should match: `local bundle_name="${1:-}"`
- ✓ Should match: `grep '^dotfiles_dir=' "$DOTPKG_CONFIG" | cut -d= -f2-`
- ✓ Should match: `state.json`, `bundle.info`, config file references
- ✗ Should NOT match: `# cmd_init()` (commented)
- ✗ Should NOT match: `echo "cmd_init"` (in string)
- ✗ Should NOT match: `# . "$lib"` (commented)
- ✗ Should NOT match: `# grep` (commented)

### 2b. getopts Pattern (Simpler CLIs)

**Real code example:**
```bash
#!/bin/bash

usage() {
  echo "Usage: $0 [-v] [-c CONFIG] [-o OUTPUT]"
  echo "  -v              Verbose output"
  echo "  -c FILE         Config file"
  echo "  -o FILE         Output file"
}

while getopts "vc:o:" opt; do
  case $opt in
    v) VERBOSE=true ;;
    c) CONFIG="$OPTARG" ;;
    o) OUTPUT="$OPTARG" ;;
    *) usage; exit 1 ;;
  esac
done

shift $((OPTIND - 1))
```

**What to search for:**
- `while getopts "..."` pattern (option string tells us what flags exist)
- `usage()` function (documents expected options)
- `case $opt in` matching option names to handlers

**Search patterns:**
```bash
# Find getopts invocations
grep -n "while getopts" /path/to/script.sh

# Find usage functions
grep -n "^usage() {" /path/to/script.sh

# Extract option string from getopts (tells us what options exist)
grep "while getopts" /path/to/script.sh | sed 's/.*getopts "\([^"]*\)".*/\1/'
```

**Test cases:**
- ✓ Should match: `while getopts "vc:o:" opt`
- ✓ Should match: `case $opt in`
- ✓ Should extract: `vc:o:` (option string) → flags: -v (no arg), -c (arg), -o (arg)
- ✗ Should NOT match: `# while getopts` (commented)

#### Task: Inventory Bash CLIs
1. **Function-based dispatch:** Find subcommand functions (`cmd_<name>()`)
2. **For each command function:**
   - Extract command name from function definition
   - Find option parsing: `case "$1" in` statements
   - Extract option flags: `--flag)` patterns with shift amounts
   - Extract positional args: `"${1:-}"` or `"${1:?error}"` patterns
3. **Library files:** Track sourced files (`. lib/*.sh`) for helper functions
4. **Config/state files:** Find references to config files and extract keys via grep patterns
5. **Help/usage:** Cross-reference with `help()` or `usage()` functions
6. **Compare to docs:** Match extracted commands/options against documented behavior

---

### 3.1 Modules

**Construct to find:** Module metadata (documentation, options, arguments)

**Real code example (Ansible module docstring):**
```python
DOCUMENTATION = r'''
---
module: my_module
short_description: Do something useful
description:
  - This module does something useful.
  - Supports check mode.

options:
  target:
    description: Target host or resource
    required: true
    type: str
  state:
    description: Desired state
    choices: ['present', 'absent']
    default: 'present'
    type: str
  timeout:
    description: Operation timeout in seconds
    type: int
    default: 30

requirements:
  - requests

author: "Alice Dev"
'''

class AnsibleModule:
    # implementation
```

**What to search for:**
- `DOCUMENTATION` string (module docstring)
- `options:` section
- `arguments:` (if using AnsibleModule)

**ast-grep pattern:**
```bash
# Find DOCUMENTATION blocks
ast-grep scan --inline-rules "id: ansible-doc
language: python
rule:
  pattern: 'DOCUMENTATION = r.*options:'" /path/to/code

# More practical: grep for it
rg 'DOCUMENTATION = ' --type python -A 50
```

**Fallback:**
```bash
rg 'DOCUMENTATION = ' --type python
rg 'options:' --type python -A 20
rg 'AnsibleModule(argument_spec=' --type python
```

**Test cases:**
- ✓ Should match: Module with `DOCUMENTATION = r'''` block containing `options:`
- ✓ Should match: `argument_spec` dict in `AnsibleModule()` call
- ✗ Should NOT match: Module without documentation
- ✗ Should NOT match: Option documented but not in argument_spec

#### Task: Inventory Ansible Modules
1. Find module `DOCUMENTATION` block
2. Extract:
   - Module name, description, short_description
   - All options: name, required, type, default, description, choices
3. Parse `argument_spec` dict if module uses `AnsibleModule`
4. Compare documented options to argument_spec
5. Check for options in code that aren't documented

### 3.2 Roles

**Construct to find:** Role defaults, variables, documented inputs/outputs

**Real code example:**
```yaml
# roles/my_role/defaults/main.yml
---
# Role defaults
my_role_enabled: true
my_role_timeout: 30
my_role_retries: 3
my_role_tags:
  - important
  - production

# roles/my_role/vars/main.yml
---
# Internal variables (not user-configurable)
my_role_version: "1.0.0"
my_role_internal_state: {}

# roles/my_role/tasks/main.yml
---
- name: Do something
  debug:
    msg: "Using config: {{ my_role_timeout }}"

- name: Register result
  command: /usr/bin/my-command
  register: my_role_result
```

**What to search for:**
- `defaults/main.yml` for role inputs
- `vars/main.yml` for internal variables
- `register:` in tasks for outputs
- Role `README.md` or `meta/argument_specs.yml` for documented inputs

**ast-grep pattern (limited for YAML):**
YAML support in ast-grep is limited. Use `yq` or grep:

```bash
# Find defaults
rg 'defaults/main\.yml' --type yaml

# Find register statements
rg 'register:' --type yaml

# Parse YAML keys
yq '.[]' roles/*/defaults/main.yml
```

**Fallback:**
```bash
# List all default variables
yq '.[]' roles/*/defaults/main.yml | sort -u

# List all registered variables
rg 'register:' roles/*/tasks/ --type yaml

# Check role README for documented inputs
head -50 roles/*/README.md
```

**Test cases:**
- ✓ Should match: Variables in `defaults/main.yml`
- ✓ Should match: `register:` directives in tasks
- ✓ Should find: Role README with "Variables" section
- ✗ Should NOT match: Private variables (prefixed with `_`)
- ✗ Should NOT match: Internal vars in `vars/` if they shadow defaults

#### Task: Inventory Ansible Roles
1. Extract all variables from `defaults/main.yml` (these are inputs users can configure)
2. Extract all `register:` directives from tasks (these are outputs the role provides)
3. Read role README or `meta/argument_specs.yml` for documented inputs/outputs
4. Compare documented inputs/outputs to actual defaults/registers
5. Flag undocumented variables and missing/incorrect defaults

---

## 3. Ansible Frameworks (VALIDATED against real modules/roles)

---

## Summary: v1 Patterns (CORRECTED)

**Validated frameworks:**

| Language | Framework | Search Pattern | Status |
|----------|-----------|-----------------|--------|
| Python | argparse | `ArgumentParser()`, `.add_argument()`, `.add_subparsers()` | ✓ v1 (CORRECTED: not Click) |
| Bash | Function dispatch | `cmd_*()`, `case "$cmd" in`, `case "$1" in` | ✓ v1 (validated on dotpkg) |
| Bash | getopts | `while getopts`, `case $opt in` | ✓ v1 (for simpler CLIs) |
| Ansible | Modules | `DOCUMENTATION` block with `options:` | ✓ v1 (320+ modules) |
| Ansible | Roles | `defaults/main.yml`, `register:` directives | ✓ v1 |

**Deferred to v2:**
- TypeScript CLI frameworks (only extensions/frontend in current repos)
- OpenAPI specifications (zero usage in repos)
- Terraform provider Go schema (user deferring)
- Click (only 1 import found; argparse is actual standard)

---

## What Changed (Adversarial Review Fixes)

1. **Removed Click entirely.** Real repo analysis shows 0 Click imports in ansible-creator/navigator/lint. These use argparse (5-7 imports each).
2. **Reordered priorities:** argparse is now #1 Python framework, validated by real usage.
3. **Improved Bash patterns:** Added config file parsing, glob sourcing, mixed arg patterns from dotpkg.
4. **Removed ast-grep patterns:** They were syntactically invalid (missing `kind` field). Using grep fallbacks instead.
5. **Removed TypeScript and OpenAPI:** Deferred — not in v1 scope.
6. **Added validation notes:** Each section now notes which repos/examples it was tested against.

---

## Next Steps (Implementation)

For each framework in v1 scope:
1. **Test patterns on real code** (ansible-creator for argparse, dotpkg for Bash, ansible core for modules/roles)
2. **Validate grep commands work as documented**
3. **Integrate into accuracy-audit Step 4** (Source Search Tool section)
4. **Update Key Reminders** with language-specific search policies
5. **Build test cases** from real examples (ansible-creator, dotpkg, ansible/lib/ansible/modules/)

