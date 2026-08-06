#!/bin/bash
# Test pattern suite for code structure detection
# Usage: bash test-patterns.sh [repo-path]
# Validates that discovered patterns return matches on real code

set -e

repo_path="${1:-.}"
log() { echo "[test-patterns] $*" >&2; }
pass() { echo "  ✓ $*"; }
fail() { echo "  ✗ $*"; }

log "Testing patterns on: $repo_path"
log ""

# Test 1: Detect project type
log "1. Project type & framework detection"
detection=$(python3 "$(dirname "$0")/detect-cli-framework.py" "$repo_path" 2>/dev/null)
project_type=$(echo "$detection" | grep '"type"' | head -1 | sed 's/.*": "\([^"]*\)".*/\1/')
framework=$(echo "$detection" | grep '"framework"' | head -1 | sed 's/.*": "\([^"]*\)".*/\1/')
log "   Type: $project_type, Framework: $framework"
echo ""

# Test 2: Run patterns for detected type
cd "$repo_path"

case "$project_type" in
  cli)
    log "2. CLI patterns ($framework)"

    case "$framework" in
      cobra-go)
        log "   Testing: grep -r 'AddCommand('"
        count=$(grep -r 'AddCommand(' --include='*.go' . 2>/dev/null | wc -l)
        if [[ $count -gt 0 ]]; then
          pass "Found $count AddCommand matches"
        else
          fail "No AddCommand matches"
        fi

        log "   Testing: grep -r '\\.Flags()'"
        count=$(grep -r '\.Flags()' --include='*.go' . 2>/dev/null | wc -l)
        if [[ $count -gt 0 ]]; then
          pass "Found $count Flags() matches"
        else
          fail "No Flags() matches"
        fi
        ;;

      argparse)
        log "   Testing: grep -r 'ArgumentParser'"
        count=$(grep -r 'ArgumentParser' --include='*.py' . 2>/dev/null | wc -l)
        if [[ $count -gt 0 ]]; then
          pass "Found $count ArgumentParser matches"
        else
          fail "No ArgumentParser matches"
        fi

        log "   Testing: grep -r '\\.add_argument('"
        count=$(grep -r '\.add_argument(' --include='*.py' . 2>/dev/null | wc -l)
        if [[ $count -gt 0 ]]; then
          pass "Found $count add_argument matches"
        else
          fail "No add_argument matches"
        fi
        ;;

      bash-dispatch)
        log "   Testing: grep -r '^cmd_'"
        count=$(grep -r '^cmd_' --include='*.sh' . 2>/dev/null | wc -l)
        count=$(( count + $(find . -type f ! -name '*.sh' ! -name '*.py' ! -name '*.go' -exec grep -l '^cmd_' {} \; 2>/dev/null | wc -l) ))
        if [[ $count -gt 0 ]]; then
          pass "Found $count cmd_ function definitions"
        else
          fail "No cmd_ functions found"
        fi

        log "   Testing: grep -r 'case.*in'"
        count=$(grep -r 'case' --include='*.sh' . 2>/dev/null | grep ' in' | wc -l)
        if [[ $count -gt 0 ]]; then
          pass "Found $count case statements"
        else
          fail "No case statements found"
        fi
        ;;
    esac
    ;;

  python-library)
    log "2. Python library patterns"

    log "   Testing: grep -r '^class '"
    count=$(grep -r '^class ' --include='*.py' . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count class definitions"
    else
      fail "No class definitions"
    fi

    log "   Testing: grep -r '^def '"
    count=$(grep -r '^def ' --include='*.py' . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count function definitions"
    else
      fail "No function definitions"
    fi

    log "   Testing: grep -r '__all__'"
    count=$(grep -r '__all__' --include='*.py' . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count __all__ declarations (public API)"
    else
      pass "No __all__ declarations (optional for libraries)"
    fi
    ;;

  vscode-extension)
    log "2. VS Code extension patterns"

    if [[ -f package.json ]]; then
      log "   Testing: grep 'contributes' in package.json"
      if grep -q '"contributes"' package.json 2>/dev/null; then
        pass "Found contributes declaration"
      else
        fail "No contributes in package.json"
      fi

      log "   Testing: grep 'activationEvents' in package.json"
      if grep -q '"activationEvents"' package.json 2>/dev/null; then
        pass "Found activationEvents"
      else
        fail "No activationEvents in package.json"
      fi
    fi

    log "   Testing: grep -r 'registerCommand' in TypeScript"
    count=$(grep -r 'registerCommand' --include='*.ts' . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
      pass "Found $count registerCommand calls"
    else
      pass "No registerCommand calls (optional for extensions)"
    fi
    ;;

  *)
    log "2. Unknown project type — skipping pattern tests"
    ;;
esac

log ""
log "Test complete."
