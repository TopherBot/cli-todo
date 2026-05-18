#!/usr/bin/env python3
"""Simple command‑line todo manager.

Usage:
    python3 todo.py add "Buy milk"
    python3 todo.py list
    python3 todo.py complete 2
    python3 todo.py delete 3
"""

import argparse
import json
import os
import sys

DATA_FILE = "todos.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def add_task(description):
    tasks = load_tasks()
    tasks.append({"id": len(tasks) + 1, "desc": description, "done": False})
    save_tasks(tasks)
    print(f"Added task: {description}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        status = "✔" if task["done"] else "✗"
        print(f"{task['id']}. [{status}] {task['desc']}")

def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as completed.")
            return
    print(f"Task {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task {task_id} not found.")
        return
    # Re‑assign IDs to keep them sequential
    for idx, task in enumerate(new_tasks, start=1):
        task["id"] = idx
    save_tasks(new_tasks)
    print(f"Task {task_id} deleted.")

def parse_args():
    parser = argparse.ArgumentParser(description="Simple CLI todo manager")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("desc", nargs="+", help="Task description")

    # list
    subparsers.add_parser("list", help="List all tasks")

    # complete
    comp_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    comp_parser.add_argument("id", type=int, help="Task ID")

    # delete
    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("id", type=int, help="Task ID")

    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == "add":
        description = " ".join(args.desc)
        add_task(description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        print("No command provided. Use -h for help.")

if __name__ == "__main__":
    main()
