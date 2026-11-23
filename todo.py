import json
import os
import sys

TASKS_FILE = os.environ.get("TASKS_FILE", "tasks.json")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class StorageError(Exception):
    """The tasks file exists but cannot be used."""


def load():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise StorageError(f"{TASKS_FILE} is not valid JSON ({e}). Fix or remove it.")


def save(tasks):
    tmp = TASKS_FILE + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(tasks, f, indent=2)
        os.replace(tmp, TASKS_FILE)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def add_task(title, priority="medium"):
    if priority not in PRIORITY_ORDER:
        raise ValueError(f"Invalid priority: {priority}. Use high, medium or low.")
    tasks = load()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    task = {"id": new_id, "title": title, "priority": priority, "done": False}
    tasks.append(task)
    save(tasks)
    return task


def list_tasks(sort_by=None):
    tasks = load()
    if sort_by == "priority":
        tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t["priority"], len(PRIORITY_ORDER)))
    return tasks


def mark_done(task_id):
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save(tasks)
            return True
    return False


def delete_task(task_id):
    tasks = load()
    remaining = [t for t in tasks if t["id"] != task_id]
    if len(remaining) == len(tasks):
        return False
    save(remaining)
    return True


def cmd_add(args):
    if not args:
        print("Usage: todo.py add TITLE [PRIORITY]")
        return 1
    priority = args[1] if len(args) > 1 else "medium"
    try:
        t = add_task(args[0], priority)
    except ValueError as e:
        print(e)
        return 1
    print(f"Added #{t['id']}: {t['title']} ({t['priority']})")
    return 0


def cmd_list(args):
    sort_by = args[0] if args else None
    for t in list_tasks(sort_by):
        mark = "x" if t["done"] else " "
        print(f"[{mark}] #{t['id']} {t['title']} ({t['priority']})")
    return 0


def cmd_done(args):
    print("Done." if mark_done(int(args[0])) else "Task not found.")
    return 0


def cmd_delete(args):
    print("Deleted." if delete_task(int(args[0])) else "Task not found.")
    return 0


COMMANDS = {"add": cmd_add, "list": cmd_list, "done": cmd_done, "delete": cmd_delete}


def main(argv):
    if len(argv) < 2:
        print("Usage: todo.py add|list|done|delete ...")
        return 1
    handler = COMMANDS.get(argv[1])
    if handler is None:
        print("Unknown command")
        return 1
    try:
        return handler(argv[2:])
    except StorageError as e:
        print(f"Error: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
