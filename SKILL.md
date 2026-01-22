---
name: notebooklm
description: Query your Google NotebookLM notebooks from Claude Code. Source-grounded answers from Gemini with minimal hallucinations.
---

# NotebookLM Skill

Query NotebookLM for document-based answers. Each question opens a browser, gets the answer, and closes.

## When to Use

- User mentions NotebookLM or shares URL (`https://notebooklm.google.com/notebook/...`)
- User asks to query notebooks/documentation
- Phrases like "ask my NotebookLM", "check my docs"

## Critical: Always Use run.py

```bash
# ✅ CORRECT:
python scripts/run.py auth_manager.py status
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG:
python scripts/auth_manager.py status  # Fails!
```

## Workflow

### 1. Check Authentication

```bash
python scripts/run.py auth_manager.py status
```

### 2. Authenticate (One-Time)

```bash
python scripts/run.py auth_manager.py setup
```

Browser opens for manual Google login.

### 3. Manage Notebooks

```bash
# List notebooks
python scripts/run.py notebook_manager.py list

# Add notebook (SMART: query first to discover content)
python scripts/run.py ask_question.py --question "What is this notebook about? Brief overview" --notebook-url "[URL]"
# Then add with discovered info:
python scripts/run.py notebook_manager.py add --url "[URL]" --name "Name" --description "Description" --topics "topic1,topic2"

# Activate notebook
python scripts/run.py notebook_manager.py activate --id notebook-id

# Search notebooks
python scripts/run.py notebook_manager.py search --query "keyword"
```

### 4. Ask Questions

```bash
# Basic (uses active notebook)
python scripts/run.py ask_question.py --question "Your question"

# Specific notebook
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# Direct URL
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Debug mode
python scripts/run.py ask_question.py --question "..." --show-browser
```

## Follow-Up Behavior

Every answer ends with: **"Is that ALL you need to know?"**

**Required:** Before responding to user:

1. STOP - Analyze if answer is complete
2. If gaps exist, ask follow-up questions
3. Synthesize all answers before responding

## Script Reference

| Script | Commands |
|--------|----------|
| `auth_manager.py` | `setup`, `status`, `reauth`, `clear` |
| `notebook_manager.py` | `add`, `list`, `search`, `activate`, `remove`, `stats` |
| `ask_question.py` | `--question`, `--notebook-id`, `--notebook-url`, `--show-browser` |
| `cleanup_manager.py` | `--confirm`, `--preserve-library`, `--force` |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Use `run.py` wrapper |
| Authentication fails | Browser must be visible for setup |
| Rate limit (50/day) | Wait or switch Google account |
| Browser crashes | `cleanup_manager.py --preserve-library` |

## Data Storage

All data in `~/.claude/skills/notebooklm/data/`:

- `library.json` - Notebook metadata
- `auth_info.json` - Auth status
- `browser_state/` - Browser cookies

**Never commit data/ to git.**
