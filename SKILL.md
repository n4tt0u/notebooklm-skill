---
name: notebooklm
description: |
  Query Google NotebookLM for document-grounded answers with minimal hallucinations.
  Use this skill whenever the user asks about documents, knowledge bases, research notes,
  or mentions NotebookLM. Even if they don't explicitly say "NotebookLM", trigger this
  skill when they want to search their notes, query uploaded documents, or get answers
  from their personal knowledge base. Phrases like "check my docs", "search my notes",
  "what does my documentation say", or "ask my knowledge base" should all trigger this skill.
---

# NotebookLM Skill

Query NotebookLM for document-based answers with source grounding. Each question opens a browser, gets the answer, and closes.

## First-Time Setup

The skill automatically creates a virtual environment and installs dependencies on first use. Just run any command and it will set itself up.

## When to Use

Trigger this skill when:
- User mentions **NotebookLM** or shares a NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- User asks to query their **documents**, **notes**, or **knowledge base**
- Phrases like: "check my docs", "search my notes", "what do my documents say"
- User wants **source-grounded answers** without hallucinations
- User references **uploaded PDFs** or **research materials**
- User wants to search their **personal library** of documents

## Critical: Always Use run.py

```shell
# ✅ CORRECT:
python scripts/run.py auth_manager.py status
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG:
python scripts/auth_manager.py status  # Fails!
```

## Workflow

### 1. Check Authentication

```shell
python scripts/run.py auth_manager.py status
```

### 2. Authenticate (One-Time)

```shell
python scripts/run.py auth_manager.py setup
```

Browser opens for manual Google login.

### 3. Manage Notebooks

```shell
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

```shell
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

Every answer includes a reminder to consider follow-up questions.

**Before responding to user:**

1. **STOP** - Analyze if the answer fully addresses the user's request
2. **Check for gaps** - Are there related aspects not covered?
3. **Ask follow-up if needed** - Each question opens a new browser session, so include all context in follow-up questions
4. **Synthesize** - Combine multiple answers before responding to user

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
| `ModuleNotFoundError` | Always use `run.py` wrapper: `python scripts/run.py <script>` |
| Authentication fails | Run `auth_manager.py setup` with visible browser |
| Rate limit (50/day) | Wait or switch Google account |
| Browser crashes | Run `cleanup_manager.py --preserve-library` |
| First run is slow | Normal - virtual environment setup takes ~1 minute |

## Data Storage

All data in `~/.claude/skills/notebooklm/data/`:

- `library.json` - Notebook metadata
- `auth_info.json` - Auth status
- `browser_state/` - Browser cookies

**Never commit data/ to git.**
