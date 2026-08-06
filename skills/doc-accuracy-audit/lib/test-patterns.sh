#!/bin/bash
# Test pattern suite for CLI framework detection
# Usage: bash test-patterns.sh [repo-path]
# Validates that discovered patterns return matches on real code

set -e

repo_path="${1:-.}"
log() { echo "[test-patterns] $*" >&2; }
pass() { echo "  ✓ $*"; }
fail() { echo "  ✗ $*"; }

log "Testing patterns on: $repo_path"
log ""

# Test 1: Detect framework
log "1. Framework detection"
framework=$(python3 "$(dirname "$0")/detect-cli-framework.py" "$repo_path" 2>/dev/null | grep '"framework"' | sed 's/.*": "\([^"]*\)".*/\1/')
log "   Detected: $framework"
echo ""

# Test 2: Run patterns for detected framework
case "$framework" in
  cobra-go)
    log "2. Cobra/Go patterns"

    cd "$repo_path"

    # Commands
    log "   Testing: grep -r 'AddCommand('"
    count=$(grep -r 'AddCommand(' --include='*.go' . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count AddCommand matches"
    else
      fail "No AddCommand matches"
    fi

    # Flags
    log "   Testing: grep -r '\\.Flags()'"
    count=$(grep -r '\.Flags()' --include='*.go' . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count Flags() matches"
    else
      fail "No Flags() matches"
    fi
    ;;

  argparse)
    log "2. argparse patterns"

    cd "$repo_path"

    # Parsers
    log "   Testing: grep -r 'ArgumentParser'"
    count=$(grep -r 'ArgumentParser' --include='*.py' . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count ArgumentParser matches"
    else
      fail "No ArgumentParser matches"
    fi

    # Arguments
    log "   Testing: grep -r '\\.add_argument('"
    count=$(grep -r '\.add_argument(' --include='*.py' . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count add_argument matches"
    else
      fail "No add_argument matches"
    fi
    ;;

  bash-dispatch)
    log "2. Bash dispatch patterns"

    cd "$repo_path"

    # Commands
    log "   Testing: grep -r '^cmd_'"
    count=$(grep -r '^cmd_' --include='*.sh' . 2>/dev/null | wc -l)
    count=$(( count + $(find . -type f ! -name '*.sh' ! -name '*.py' ! -name '*.go' -exec grep -l '^cmd_' {} \; 2>/dev/null | wc -l) ))
    if [[ $count -gt 0 ]]; then
      pass "Found $count cmd_ function definitions"
    else
      fail "No cmd_ functions found"
    fi

    # Dispatch
    log "   Testing: grep -r 'case.*in'"
    count=$(grep -r 'case' --include='*.sh' . 2>/dev/null | grep ' in' | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count case statements"
    else
      fail "No case statements found"
    fi
    ;;

  *)
    log "2. Unknown framework — skipping pattern tests"
    ;;
esac

log ""
log "Test complete."
