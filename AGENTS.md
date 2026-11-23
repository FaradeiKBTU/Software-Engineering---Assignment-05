# AGENTS.md — todo-cli

## Purpose
Small command-line to-do list in Python (standard library only). Tasks are stored in a JSON file (`tasks.json`, or the path in env `TASKS_FILE`).

## Architecture
| Path | Role |
| --- | --- |
| `todo.py` | Whole app: storage (`load`/`save`), task operations, CLI entry (`main`) |
| `test_todo.py` | unittest suite; each test points `todo.TASKS_FILE` at a temp file |
| `tasks.json` | Runtime data, git-ignored. Never read, edit or commit it |

## Setup
Python 3.10+; no dependencies, no build step. Do not add packages.

## Safe commands (run without asking)
- `python3 -m unittest -v`
- `python3 todo.py list` / `add` / `done` / `delete` **only with** `TASKS_FILE=/tmp/<name>.json`
- `git status`, `git diff`, `git log -n 5`

## Ask first
- Adding any dependency, config file or CI workflow
- Changing the `tasks.json` format (fields: id, title, priority, done)
- Renaming or moving files

## Forbidden
- Reading or writing real `tasks.json`; committing secrets or personal data
- `git push --force`, `git reset --hard`, `rm -rf`, deployments, network calls
- Weakening or deleting tests to make a check pass
- Claiming a test/lint result that was not actually run

## Conventions
- PEP 8, type-free plain Python, functions small and single-purpose
- User-facing messages are fixed text: `Added #N: T (P)`, `Done.`, `Deleted.`, `Task not found.`
- Priorities: `high` < `medium` < `low` (sort order)

## Test expectations
- Every behaviour change needs a test; run `python3 -m unittest -v` before and after
- Acceptance criteria AC1–AC5 (see assignment) must keep passing

## Review gates
A human reviews `git diff` before every commit. The agent never commits or pushes by itself.
