# Installation Guide

Install doc-quality skills from any AI tool supporting agent skills.

## Installation via npx skills (Recommended)

**All skills, user scope — available in all sessions:**
```bash
npx skills add tima/doc-quality -g
```

**All skills, project scope — this project only:**
```bash
npx skills add tima/doc-quality
```

**Specific skills only:**
```bash
npx skills add tima/doc-quality --skill doc-accuracy-audit -g
npx skills add tima/doc-quality --skill doc-quality-audit -g
npx skills add tima/doc-quality --skill doc-quality-revise -g
npx skills add tima/doc-quality --skill doc-quality-check -g
```

**Skills become available as:**
- `/doc-accuracy-audit` — Cross-reference docs against source code, schemas, or specs
- `/doc-quality-audit` — Evaluate documentation quality across 10 dimensions
- `/doc-quality-revise` — Apply audit corrections with user approval
- `/doc-quality-check` — Run full pipeline: accuracy → quality → revisions

## Local Development Install

For development or offline use:

```bash
git clone https://github.com/tima/doc-quality.git ~/projects/doc-quality
ln -sf ~/projects/doc-quality/skills/doc-accuracy-audit ~/.claude/skills/doc-accuracy-audit
ln -sf ~/projects/doc-quality/skills/doc-quality-audit ~/.claude/skills/doc-quality-audit
ln -sf ~/projects/doc-quality/skills/doc-quality-revise ~/.claude/skills/doc-quality-revise
ln -sf ~/projects/doc-quality/skills/doc-quality-check ~/.claude/skills/doc-quality-check
```

Local symlinks point to development branches and reload without re-installation.

## System Requirements

See [README.md](README.md#system-requirements) for required tools (rg, python3, optional sg).

## Uninstallation

**Registry installed (npx skills):**
```bash
npx skills remove doc-accuracy-audit --global
npx skills remove doc-quality-audit --global
npx skills remove doc-quality-revise --global
npx skills remove doc-quality-check --global
```

**Locally symlinked (development):**
```bash
rm ~/.claude/skills/doc-accuracy-audit
rm ~/.claude/skills/doc-quality-audit
rm ~/.claude/skills/doc-quality-revise
rm ~/.claude/skills/doc-quality-check
```

## Updating

**Registry installed:**
```bash
npx skills update tima/doc-quality
```

**Locally symlinked:**
```bash
cd ~/projects/doc-quality
git pull
```

Symlinks automatically point to updated versions on next use.

## Verification

Test installation:
```bash
/doc-quality-audit
```

Should prompt for project path and documentation location, then run the skill.

---

**Note:** These skills work with any AI tool supporting agent skills. Installation method (npx skills vs symlink) doesn't affect compatibility.
