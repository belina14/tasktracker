import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)
    
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def add_task(description):
    tasks = load_tasks()
    new_id = max([task["id"] for task in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully: {new_task}")

def delete_task(task_id):
    tasks = load_tasks()
    if task_id not in [t["id"] for t in tasks]:
        print(f"Error: Task with ID {task_id} not found.")
        return
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task with ID {task_id} deleted successfully.")

def update_task(task_id, new_description):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if not found:
        print(f"Error: Task with ID {task_id} not found.")
        return
    save_tasks(tasks)
    print(f"Task with ID {task_id} updated successfully.")

def mark_progress(task_id):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if not found:
        print(f"Error: Task with ID {task_id} not found.")
        return
    save_tasks(tasks)
    print(f"Task with ID {task_id} marked as in-progress.")

def mark_done(task_id):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if not found:
        print(f"Error: Task with ID {task_id} not found.")
        return
    save_tasks(tasks)
    print(f"Task with ID {task_id} marked as done.")

def list_tasks(status_filter=None):
    tasks = load_tasks()
    if status_filter:
        tasks = [task for task in tasks if task["status"] == status_filter]
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
        

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tasks_cli.py <command> [arguments]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: python tasks_cli.py add 'Task description'")
            sys.exit(1)
        add_task(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python tasks_cli.py delete <task_id>")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("Invalid task ID. Please provide a valid integer.")
            sys.exit(1)
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: python tasks_cli.py update <task_id> 'New task description'")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
            new_description = sys.argv[3]
            update_task(task_id, new_description)
        except ValueError:
            print("Invalid task ID. Please provide a valid integer.")
            sys.exit(1)
    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Usage: python tasks_cli.py mark-in-progress <task_id>")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
            mark_progress(task_id)
        except ValueError:
            print("Invalid task ID. Please provide a valid integer.")
            sys.exit(1)
    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Usage: python tasks_cli.py mark-done <task_id>")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
            mark_done(task_id)
        except ValueError:
            print("Invalid task ID. Please provide a valid integer.")
            sys.exit(1)
    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()  
        elif len(sys.argv) == 3:
            status_arg = sys.argv[2]
            if status_arg not in ["done", "todo", "in-progress"]:
                print("Invalid status. Use 'done', 'todo', or 'in-progress'.")
                sys.exit(1)
            list_tasks(status_arg)
        else:
            print("Usage: python tasks_cli.py list [done|todo|in-progress]")
    else:
        print(f"Unknown command: {command}")