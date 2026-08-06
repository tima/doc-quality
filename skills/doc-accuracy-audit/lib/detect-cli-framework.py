#!/usr/bin/env python3
"""
CLI Framework Detector
Identifies framework (Cobra/Go, argparse, Click, Bash) from source code.
Returns: {framework, confidence, patterns_to_use, files_found}
"""

import os
import subprocess
import json
import sys
from pathlib import Path
from collections import defaultdict


def run_cmd(cmd, cwd=None):
    """Run shell command, return stdout lines."""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except (subprocess.TimeoutExpired, Exception):
        return []


def count_files_with_pattern(code_path, patterns_by_lang):
    """
    Count files matching framework indicators.
    patterns_by_lang: {extension: [grep patterns]}
    Returns: {framework: file_count}
    """
    counts = defaultdict(int)

    for ext, patterns in patterns_by_lang.items():
        for pattern in patterns:
            # Use rg if available, fall back to grep
            cmd = f"rg {pattern} --type {ext} --files-with-matches . 2>/dev/null | wc -l"
            try:
                result = subprocess.run(
                    cmd, shell=True, cwd=code_path, capture_output=True, text=True, timeout=5
                )
                count = int(result.stdout.strip()) if result.stdout.strip() else 0
                if count > 0:
                    counts[ext] += count
            except:
                pass

    return counts


def detect_framework(code_path):
    """
    Detect CLI framework from code_path.
    Returns: {
        framework: str,
        confidence: str (high/medium/low),
        patterns: dict,
        files_found: int,
        message: str
    }
    """
    if not os.path.isdir(code_path):
        return {
            "framework": "unknown",
            "confidence": "none",
            "error": f"Path does not exist: {code_path}"
        }

    # Framework signatures: (name, file_extensions, key_patterns, rg_pattern)
    frameworks = [
        ("cobra-go", ["go"], ["cobra", "AddCommand"], r'\.AddCommand\('),
        ("argparse", ["py"], ["argparse", "ArgumentParser"], r'ArgumentParser'),
        ("click", ["py"], ["click", "@click"], r'@click|from click'),
        ("bash-dispatch", ["sh"], ["cmd_", "case"], r'^cmd_[a-z_]*\(\)'),
    ]

    results = {}

    # Count framework indicators
    for fw_name, exts, keywords, pattern in frameworks:
        count = 0
        for ext in exts:
            # Use grep with literal pattern (not regex) for simplicity
            if fw_name == "cobra-go":
                cmd = f"grep -r 'AddCommand(' --include='*.{ext}' . 2>/dev/null | wc -l"
            elif fw_name == "bash-dispatch":
                # Look for cmd_ functions in .sh files AND executable bash scripts (no extension)
                cmd = f"grep -r '^cmd_' --include='*.sh' . 2>/dev/null | wc -l"
                try:
                    result = subprocess.run(
                        cmd, shell=True, cwd=code_path, capture_output=True, text=True, timeout=5
                    )
                    count += int(result.stdout.strip()) if result.stdout.strip() else 0
                except:
                    pass
                # Also check executable bash files
                cmd = f"find . -type f ! -name '*.sh' ! -name '*.py' ! -name '*.go' -exec grep -l '^cmd_' {{}} \\; 2>/dev/null | wc -l"
            else:
                cmd = f"grep -r '{keywords[1]}' --include='*.{ext}' . 2>/dev/null | wc -l"

            try:
                result = subprocess.run(
                    cmd, shell=True, cwd=code_path, capture_output=True, text=True, timeout=5
                )
                count += int(result.stdout.strip()) if result.stdout.strip() else 0
            except:
                pass

        if count > 0:
            results[fw_name] = count

    # Determine winner
    if not results:
        return {
            "framework": "unknown",
            "confidence": "low",
            "message": "No CLI framework detected in code"
        }

    best_fw = max(results, key=results.get)
    confidence = "high" if results[best_fw] >= 5 else "medium" if results[best_fw] >= 2 else "low"

    # Map framework to patterns
    patterns_map = {
        "cobra-go": {
            "commands": "rg '\\.AddCommand\\(' --type go",
            "flags": "rg '\\.Flags\\(\\)\\.' --type go",
            "description": "Go CLI using Cobra framework"
        },
        "argparse": {
            "parsers": "rg 'ArgumentParser' --type py",
            "arguments": "rg '\\.add_argument\\(' --type py",
            "subparsers": "rg '\\.add_subparsers\\(' --type py",
            "description": "Python CLI using argparse (standard library)"
        },
        "click": {
            "decorators": "rg '@click\\.' --type py",
            "commands": "rg '@click\\.command\\(\\)' --type py",
            "description": "Python CLI using Click framework"
        },
        "bash-dispatch": {
            "commands": "grep -n '^cmd_[a-z_]*() {' *.sh",
            "dispatch": "grep -n 'case.*in' *.sh",
            "description": "Bash CLI with function-based command dispatch"
        }
    }

    return {
        "framework": best_fw,
        "confidence": confidence,
        "files_found": results[best_fw],
        "all_results": results,
        "patterns": patterns_map.get(best_fw, {}),
        "message": f"Detected {best_fw} in {results[best_fw]} files ({confidence} confidence)"
    }


if __name__ == "__main__":
    code_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = detect_framework(code_path)
    print(json.dumps(result, indent=2))
