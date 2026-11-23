import json
import os
import sys

TASKS_FILE = os.environ.get("TASKS_FILE", "tasks.json")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def load():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE) as f:
        return json.load(f)


def save(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title, priority="medium"):
    tasks = load()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    task = {"id": new_id, "title": title, "priority": priority, "done": False}
    tasks.append(task)
    save(tasks)
    return task


def list_tasks(sort_by=None):
    tasks = load()
    if sort_by == "priority":
        tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER[t["priority"]])
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


def main(argv):
    if len(argv) < 2:
        print("Usage: todo.py add|list|done|delete ...")
        return 1
    cmd = argv[1]
    if cmd == "add":
        priority = argv[3] if len(argv) > 3 else "medium"
        t = add_task(argv[2], priority)
        print(f"Added #{t['id']}: {t['title']} ({t['priority']})")
    elif cmd == "list":
        sort_by = argv[2] if len(argv) > 2 else None
        for t in list_tasks(sort_by):
            mark = "x" if t["done"] else " "
            print(f"[{mark}] #{t['id']} {t['title']} ({t['priority']})")
    elif cmd == "done":
        if mark_done(int(argv[2])):
            print("Done.")
        else:
            print("Task not found.")
    elif cmd == "delete":
        if delete_task(int(argv[2])):
            print("Deleted.")
        else:
            print("Task not found.")
    else:
        print("Unknown command")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
