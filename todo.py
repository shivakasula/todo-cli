import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), "todos.json")


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def add(task):
    todos = load_todos()
    todos.append({"task": task, "done": False})
    save_todos(todos)
    print(f"Added: {task}")


def list_todos():
    todos = load_todos()
    if not todos:
        print("No todos yet. Add one with: python todo.py add <task>")
        return
    for i, t in enumerate(todos, 1):
        status = "x" if t["done"] else " "
        print(f"  {i}. [{status}] {t['task']}")


def complete(index):
    todos = load_todos()
    if index < 1 or index > len(todos):
        print(f"Invalid index: {index}")
        return
    todos[index - 1]["done"] = True
    save_todos(todos)
    print(f"Completed: {todos[index - 1]['task']}")


def delete(index):
    todos = load_todos()
    if index < 1 or index > len(todos):
        print(f"Invalid index: {index}")
        return
    removed = todos.pop(index - 1)
    save_todos(todos)
    print(f"Deleted: {removed['task']}")


def usage():
    print("Usage:")
    print("  python todo.py add <task>     Add a new task")
    print("  python todo.py list           List all tasks")
    print("  python todo.py done <number>  Mark task as complete")
    print("  python todo.py delete <number> Delete a task")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        usage()
    elif args[0] == "add" and len(args) > 1:
        add(" ".join(args[1:]))
    elif args[0] == "list":
        list_todos()
    elif args[0] == "done" and len(args) == 2:
        complete(int(args[1]))
    elif args[0] == "delete" and len(args) == 2:
        delete(int(args[1]))
    else:
        usage()
