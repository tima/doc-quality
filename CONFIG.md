# Shared Configuration Reference

Shared procedures used by multiple doc-quality-skills. Individual SKILL.md files reference sections here to avoid duplication.

## Loading .doc-quality.yml

All skills check for `.doc-quality.yml` in the current directory at startup.

### Detection

```bash
test -f .doc-quality.yml && echo "FOUND" || echo "NOT_FOUND"
```

### Parsing

If found, read and extract relevant fields:

```bash
cat .doc-quality.yml
```

Extract individual values with:

```bash
grep "^key:" .doc-quality.yml | cut -d: -f2- | xargs
```

### Display

- If found: Show "Using config: .doc-quality.yml"
- If not found: Show "Using defaults (no config found)"

### Relevant Fields by Skill

| Field | accuracy-audit | quality-audit | quality-revise |
|-------|---------------|---------------|----------------|
| style_guide | YES | YES | - |
| rules.contractions | - | - | YES |
| rules.word_replacements | - | - | YES |
| rules.skip_rules | - | YES | YES |
| severity_thresholds | - | YES | - |
| incremental.enabled | YES | YES | - |
| incremental.since | YES | YES | - |
| output.path | YES | YES | YES |

**Full schema example:** See [`.doc-quality.yml.example`](.doc-quality.yml.example) in the repository root for all supported fields, defaults, and usage examples.

---

## Incremental Mode (--since)

When `--since <git-ref>` flag is present:

1. Verify git repo: `git rev-parse --git-dir`
   - If not a git repo: Error "Incremental mode requires git repository"
2. Get changed files: `git diff --name-only <ref> HEAD`
3. Filter to doc files: keep *.md, *.mdx, *.rst, files under docs/
4. Store as `changed_files` list
5. Show: "Incremental audit since {ref} - found X changed doc files"

During audit execution, only process files in `changed_files`.

In scope confirmation, show: "Incremental audit will check only X changed files"

In final report, note: "Incremental audit since {ref} - audited X of Y total files"

---

## Zero-Hallucination Policy

All skills follow this policy:

- If information is unavailable, missing, or outside your access: state "Information not found."
- Do NOT infer, speculate, or bridge gaps with "likely" or "probably."
- If a link is dead or a file is inaccessible, say so explicitly.
- Label subjective findings as "Suggestion" rather than "Issue".
- If doc type or intent is unclear, ask for clarification rather than guessing.
- Better to skip a revision than apply the wrong change.

---

## Confidence Levels

All audit findings are annotated with confidence based on verification method:

- **High Confidence** — Direct source verification, unambiguous evidence (e.g., code search confirms absence, schema field exists, example runs without error)
- **Medium Confidence** — Indirect evidence, minor ambiguity (e.g., comment-stated behavior vs actual code, partial match)
- **Low Confidence** — Uncertain, requires manual review (e.g., parse failure, documentation ambiguity, tool unavailable)

Every finding must cite its evidence source and state its confidence level before output.
