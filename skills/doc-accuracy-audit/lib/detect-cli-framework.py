#!/usr/bin/env python3
"""
Code Structure Detector
Identifies project type and patterns for accuracy auditing.
Detects: CLI (Cobra/Go, argparse, Click, Bash), Python libraries, TypeScript extensions.
Returns: {type, framework, confidence, patterns_to_use, files_found}
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


def detect_project_type(code_path):
    """
    Determine project type using root manifest priority (polyglot fix for v1.2).

    Priority order:
    1. package.json at root -> TypeScript/JavaScript (primary language)
    2. go.mod at root -> Go (primary language)
    3. Cargo.toml at root -> Rust (primary language)
    4. setup.py/pyproject.toml at root -> Python (primary language)
    5. CLI framework signatures (argparse, Cobra, Click, Bash)
    6. Python library structure (__init__.py, classes, functions)

    This prevents polyglot projects (e.g., TypeScript with Python build scripts)
    from being misclassified based on secondary language markers.
    """

    # TIER 1: Check root manifests (these define primary project type)
    # package.json at root with substantive content (not just devDependencies) indicates TS/JS primary
    if os.path.isfile(os.path.join(code_path, "package.json")):
        try:
            with open(os.path.join(code_path, "package.json")) as f:
                pkg_content = f.read()
                if '"contributes"' in pkg_content or '"activationEvents"' in pkg_content:
                    return "vscode-extension"
                # Check for substantive Node.js project markers
                # (not just build tools in devDependencies)
                has_main_entry = '"main"' in pkg_content or '"bin"' in pkg_content
                has_scripts = '"scripts"' in pkg_content
                has_deps = '"dependencies"' in pkg_content
                is_cli_indicator = "cli" in pkg_content.lower() or "command" in pkg_content.lower()

                # If it has actual project content (main, scripts, dependencies), it's TS/JS primary
                if has_main_entry or has_deps or (has_scripts and not "devDependencies" in pkg_content[:pkg_content.find('"scripts"')]):
                    if is_cli_indicator:
                        return "cli"
                    return "typescript-library"
                # If package.json only has devDependencies (build tool), skip to next tier
        except:
            pass

    # go.mod at root indicates Go primary
    if os.path.isfile(os.path.join(code_path, "go.mod")):
        return "cli"  # Go projects are typically CLI tools

    # Cargo.toml at root indicates Rust primary
    if os.path.isfile(os.path.join(code_path, "Cargo.toml")):
        return "cli"  # Rust projects typically CLI

    # setup.py/pyproject.toml at root indicates Python primary
    # (but check for CLI frameworks first within Python)
    if os.path.isfile(os.path.join(code_path, "setup.py")) or \
       os.path.isfile(os.path.join(code_path, "pyproject.toml")) or \
       os.path.isfile(os.path.join(code_path, "setup.cfg")):
        # Could be CLI (argparse/Click) or library; check framework signatures
        cli_count = 0
        arg_matches = run_cmd(f"grep -r 'ArgumentParser\\|@click\\.' --include='*.py' . 2>/dev/null | wc -l", code_path)
        if arg_matches and arg_matches[0].isdigit():
            cli_count += int(arg_matches[0])

        if cli_count > 0:
            return "cli"  # Python CLI
        return "python-library"  # Python library (default for setup.py)

    # TIER 2: Check for CLI framework signatures (no root manifest found)
    cli_count = 0
    # argparse/Click
    arg_matches = run_cmd(f"grep -r 'ArgumentParser\\|@click\\.' --include='*.py' . 2>/dev/null | wc -l", code_path)
    if arg_matches and arg_matches[0].isdigit():
        cli_count += int(arg_matches[0])
    # Cobra/Go
    cobra_matches = run_cmd(f"grep -r 'AddCommand(' --include='*.go' . 2>/dev/null | wc -l", code_path)
    if cobra_matches and cobra_matches[0].isdigit():
        cli_count += int(cobra_matches[0])
    # Bash
    bash_matches = run_cmd(f"grep -r '^cmd_' --include='*.sh' . 2>/dev/null | wc -l", code_path)
    if bash_matches and bash_matches[0].isdigit():
        cli_count += int(bash_matches[0])

    if cli_count > 0:
        return "cli"  # Found CLI framework markers

    # TIER 3: Check for Python library structure (__init__.py, classes, functions)
    init_count = len(run_cmd(f"find . -name '__init__.py' -type f 2>/dev/null", code_path))
    if init_count > 0:
        return "python-library"

    return "cli"  # Default to CLI detection


def detect_cli_framework(code_path):
    """Detect CLI framework (Cobra, argparse, Click, Bash)."""
    frameworks = [
        ("cobra-go", ["go"], ["cobra", "AddCommand"], r'\.AddCommand\('),
        ("argparse", ["py"], ["argparse", "ArgumentParser"], r'ArgumentParser'),
        ("click", ["py"], ["click", "@click"], r'@click|from click'),
        ("bash-dispatch", ["sh"], ["cmd_", "case"], r'^cmd_[a-z_]*\(\)'),
    ]

    results = {}

    for fw_name, exts, keywords, pattern in frameworks:
        count = 0
        for ext in exts:
            if fw_name == "cobra-go":
                cmd = f"grep -r 'AddCommand(' --include='*.{ext}' . 2>/dev/null | wc -l"
            elif fw_name == "bash-dispatch":
                cmd = f"grep -r '^cmd_' --include='*.sh' . 2>/dev/null | wc -l"
                try:
                    result = subprocess.run(
                        cmd, shell=True, cwd=code_path, capture_output=True, text=True, timeout=5
                    )
                    count += int(result.stdout.strip()) if result.stdout.strip() else 0
                except:
                    pass
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

    if not results:
        return None

    best_fw = max(results, key=results.get)
    confidence = "high" if results[best_fw] >= 5 else "medium" if results[best_fw] >= 2 else "low"

    return {
        "framework": best_fw,
        "confidence": confidence,
        "files_found": results[best_fw],
    }


def detect_python_library(code_path):
    """Detect Python library structure (classes, functions, public API)."""
    # Count class definitions
    classes = run_cmd(f"grep -r '^class ' --include='*.py' . 2>/dev/null | wc -l", code_path)
    class_count = int(classes[0]) if classes and classes[0].isdigit() else 0

    # Count function definitions (excluding methods)
    functions = run_cmd(f"grep -r '^def ' --include='*.py' . 2>/dev/null | wc -l", code_path)
    func_count = int(functions[0]) if functions and functions[0].isdigit() else 0

    # Count __all__ declarations (public API indicator)
    all_exports = run_cmd(f"grep -r '__all__' --include='*.py' . 2>/dev/null | wc -l", code_path)
    all_count = int(all_exports[0]) if all_exports and all_exports[0].isdigit() else 0

    confidence = "high" if class_count >= 3 or (func_count >= 5 and all_count > 0) else "medium"

    return {
        "framework": "python-library",
        "confidence": confidence,
        "classes_found": class_count,
        "functions_found": func_count,
        "all_exports_found": all_count,
    }


def detect_typescript_extension(code_path):
    """Detect VS Code extension structure (commands, settings, contributes)."""
    # Check package.json for contributes
    pkg_file = os.path.join(code_path, "package.json")
    contributes_count = 0
    activation_count = 0
    if os.path.isfile(pkg_file):
        try:
            with open(pkg_file) as f:
                content = f.read()
                contributes_count = content.count('"contributes"')
                activation_count = content.count('"activationEvents"')
        except:
            pass

    # Count TypeScript source files
    ts_files = run_cmd(f"find . -name '*.ts' -not -path './node_modules/*' -type f 2>/dev/null | wc -l", code_path)
    ts_count = int(ts_files[0]) if ts_files and ts_files[0].isdigit() else 0

    # Count command definitions in TypeScript
    commands = run_cmd(f"grep -r 'registerCommand' --include='*.ts' . 2>/dev/null | wc -l", code_path)
    cmd_count = int(commands[0]) if commands and commands[0].isdigit() else 0

    confidence = "high" if contributes_count > 0 and activation_count > 0 else "medium" if ts_count > 0 else "low"

    return {
        "framework": "vscode-extension",
        "confidence": confidence,
        "typescript_files": ts_count,
        "commands_found": cmd_count,
        "has_contributes": contributes_count > 0,
        "has_activation_events": activation_count > 0,
    }


def get_patterns_for_type(project_type, framework_info):
    """Return search patterns based on project type and framework."""
    patterns_map = {
        # CLI patterns
        "cobra-go": {
            "public_api": "rg '\\.(AddCommand|Flags|PersistentFlags)\\(' --type go",
            "commands": "grep -r 'AddCommand(' --include='*.go'",
            "flags": "grep -r '\\.Flags()' --include='*.go' | grep -E 'StringVar|BoolVar|IntVar'",
            "description": "Go CLI using Cobra framework"
        },
        "argparse": {
            "public_api": "rg '(ArgumentParser|add_argument|add_subparsers)' --type py",
            "parsers": "grep -r 'ArgumentParser' --include='*.py'",
            "arguments": "grep -r 'add_argument(' --include='*.py'",
            "subparsers": "grep -r 'add_subparsers(' --include='*.py'",
            "description": "Python CLI using argparse (standard library)"
        },
        "click": {
            "public_api": "rg '@click\\.(command|option|argument|group)' --type py",
            "decorators": "grep -r '@click\\.' --include='*.py'",
            "commands": "grep -r '@click\\.command()' --include='*.py'",
            "description": "Python CLI using Click framework"
        },
        "bash-dispatch": {
            "public_api": "grep -r '^cmd_' --include='*.sh'",
            "commands": "grep -n '^cmd_[a-z_]*() {' *.sh",
            "dispatch": "grep -n 'case' *.sh | grep ' in'",
            "description": "Bash CLI with function-based command dispatch"
        },
        # Python library patterns
        "python-library": {
            "public_api": "grep -r '__all__' --include='*.py'",
            "classes": "grep -r '^class ' --include='*.py'",
            "functions": "grep -r '^def ' --include='*.py' | grep -v '    def'",
            "exports": "grep -r 'from.*import\\|import ' --include='*.py' | head -20",
            "description": "Python library/package"
        },
        # TypeScript extension patterns
        "vscode-extension": {
            "public_api": "grep -r 'registerCommand\\|registerCodeLensProvider' --include='*.ts'",
            "commands": "grep 'commands' package.json",
            "settings": "grep 'configuration' package.json",
            "activation": "grep 'activationEvents' package.json",
            "exports": "grep -r 'export ' --include='*.ts' | head -20",
            "description": "VS Code extension"
        },
    }

    return patterns_map.get(framework_info.get("framework", "unknown"), {})


def detect_code_structure(code_path):
    """
    Main detection function.
    Returns: {
        type: str (cli/python-library/vscode-extension),
        framework: str,
        confidence: str (high/medium/low),
        patterns: dict,
        message: str
    }
    """
    if not os.path.isdir(code_path):
        return {
            "type": "unknown",
            "framework": "unknown",
            "confidence": "none",
            "error": f"Path does not exist: {code_path}"
        }

    project_type = detect_project_type(code_path)

    if project_type == "cli":
        fw_info = detect_cli_framework(code_path)
        if not fw_info:
            return {
                "type": "cli",
                "framework": "unknown",
                "confidence": "low",
                "message": "CLI project detected but framework not identified"
            }
        patterns = get_patterns_for_type("cli", fw_info)
        return {
            "type": "cli",
            "framework": fw_info["framework"],
            "confidence": fw_info["confidence"],
            "files_found": fw_info["files_found"],
            "patterns": patterns,
            "message": f"Detected {fw_info['framework']} CLI in {fw_info['files_found']} files ({fw_info['confidence']} confidence)"
        }

    elif project_type == "python-library":
        lib_info = detect_python_library(code_path)
        patterns = get_patterns_for_type("python-library", lib_info)
        return {
            "type": "python-library",
            "framework": "python-library",
            "confidence": lib_info["confidence"],
            "classes_found": lib_info["classes_found"],
            "functions_found": lib_info["functions_found"],
            "patterns": patterns,
            "message": f"Detected Python library with {lib_info['classes_found']} classes and {lib_info['functions_found']} functions ({lib_info['confidence']} confidence)"
        }

    elif project_type == "vscode-extension":
        ext_info = detect_typescript_extension(code_path)
        patterns = get_patterns_for_type("vscode-extension", ext_info)
        return {
            "type": "vscode-extension",
            "framework": "vscode-extension",
            "confidence": ext_info["confidence"],
            "typescript_files": ext_info["typescript_files"],
            "commands_found": ext_info["commands_found"],
            "patterns": patterns,
            "message": f"Detected VS Code extension with {ext_info['commands_found']} commands ({ext_info['confidence']} confidence)"
        }

    elif project_type == "typescript-library":
        # TypeScript/JavaScript library or application (secondary to CLI/extension detection)
        ts_files = run_cmd(f"find . -name '*.ts' -not -path './node_modules/*' -type f 2>/dev/null | wc -l", code_path)
        ts_count = int(ts_files[0]) if ts_files and ts_files[0].isdigit() else 0
        confidence = "high" if ts_count > 10 else "medium" if ts_count > 0 else "low"
        return {
            "type": "typescript-library",
            "framework": "typescript-library",
            "confidence": confidence,
            "typescript_files": ts_count,
            "message": f"Detected TypeScript/JavaScript library/application with {ts_count} TypeScript files ({confidence} confidence)"
        }

    else:
        return {
            "type": "generic",
            "framework": "generic",
            "confidence": "low",
            "message": "Generic code project detected (type not specifically identified)"
        }


if __name__ == "__main__":
    code_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = detect_code_structure(code_path)
    print(json.dumps(result, indent=2))
