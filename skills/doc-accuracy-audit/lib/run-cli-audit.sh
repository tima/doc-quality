#!/bin/bash
# CLI Audit Runner: Detect framework, then execute pattern-based audit
# Usage: bash run-cli-audit.sh <code-path> <doc-path>

set -euo pipefail

code_path="${1:-.}"
doc_path="${2:-docs}"

log() { echo "[cli-audit] $*" >&2; }
section() { echo ""; log "=== $* ==="; }

if [[ ! -d "$code_path" ]]; then
  log "ERROR: Code path not found: $code_path"
  exit 1
fi

# Get script dir
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

section "Framework Detection"
framework_json=$(python3 "$script_dir/detect-cli-framework.py" "$code_path" 2>&1)
framework=$(echo "$framework_json" | grep '"framework"' | sed 's/.*": "\([^"]*\)".*/\1/')
confidence=$(echo "$framework_json" | grep '"confidence"' | sed 's/.*": "\([^"]*\)".*/\1/')

if [[ "$framework" == "unknown" ]]; then
  log "ERROR: Could not detect CLI framework in $code_path"
  exit 1
fi

log "Detected: $framework ($confidence confidence)"
echo "$framework_json" | grep '"message"' | sed 's/.*": "\([^"]*\)".*/\1/' | sed 's/^/  /'

section "Running Patterns"
cd "$code_path"

case "$framework" in
  argparse)
    log "Python argparse CLI detected"
    log "Task 1: Finding all ArgumentParser instantiations..."
    count=$(grep -r 'ArgumentParser' --include='*.py' . 2>/dev/null | wc -l)
    log "  Found: $count parsers"

    log "Task 2: Finding all add_argument calls..."
    count=$(grep -r '\.add_argument(' --include='*.py' . 2>/dev/null | wc -l)
    log "  Found: $count arguments defined"

    log "Task 3: Finding subparsers..."
    count=$(grep -r '\.add_subparsers(' --include='*.py' . 2>/dev/null | wc -l)
    log "  Found: $count subparser groups"
    ;;

  cobra-go)
    log "Go Cobra CLI detected"
    log "Task 1: Finding all AddCommand calls..."
    count=$(grep -r 'AddCommand(' --include='*.go' . 2>/dev/null | wc -l)
    log "  Found: $count commands"

    log "Task 2: Finding flag definitions..."
    count=$(grep -r '\.Flags()' --include='*.go' . 2>/dev/null | wc -l)
    log "  Found: $count flag references"
    ;;

  bash-dispatch)
    log "Bash function-dispatch CLI detected"
    log "Task 1: Finding all cmd_* functions..."
    count=$(grep -r '^cmd_' . 2>/dev/null | wc -l)
    log "  Found: $count command functions"

    log "Task 2: Finding option parsing (case statements)..."
    count=$(grep -r 'case' . 2>/dev/null | grep ' in' | wc -l)
    log "  Found: $count case statements (option parsing)"
    ;;

  *)
    log "ERROR: No audit patterns defined for $framework"
    exit 1
    ;;
esac

section "Summary"
log "Framework: $framework"
log "Code path: $code_path"
log "Ready for detailed audit (Task 1-4 in skill)"
