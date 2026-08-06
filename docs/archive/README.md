# Archive: Historical Design Documents

This directory contains pre-implementation design notes and early planning documents that are **no longer current**. These documents do not reflect the actual implementation and should not be used as a reference for understanding how the skills work.

## What's Here

- `2026-06-15-doc-quality-check-design.md` — Architectural design for the orchestrator skill (June 2026)
- `2026-06-15-doc-quality-check.md` — Early design notes and considerations

## Why Archived?

These documents predate the implementation of:
- Zero-hallucination verification passes (traceability, direction accuracy, exclusivity gate)
- CLI framework auto-detection (argparse, Cobra, Bash, Click)
- V1 scope clarification (CLI tools only; Terraform/OpenAPI deferred to v2)

The final implementation diverged significantly from these early designs as actual requirements became clearer.

## Current Documentation

For accurate, up-to-date documentation, see:
- **SKILL.md files** — Authoritative skill specifications
- **V1-SCOPE.md** — What v1 actually supports and why
- **PATTERN-DISCOVERY.md** — Code patterns used for CLI auditing
- **REPO-INVENTORY-FINDINGS.md** — Framework analysis across real repositories

## Future Considerations

These documents may be deleted entirely in a future release once v2 design is final (to avoid confusion). For now, they're preserved in this subdirectory to reduce clutter while maintaining git history.
