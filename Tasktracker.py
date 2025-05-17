#!/usr/bin/env python
from datetime import datetime
import argparse
import json
import os

TASKS_FILE = "tasks.json"

# Cargar tareas desde archivo
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

# Guardar tareas en archivo
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Obtener el siguiente ID disponible
def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

# Agregar tarea
def add_task():
    tasks = load_tasks()
    task_id = get_next_id(tasks)
    description = input("Enter task description: ").strip()
    if description:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task = {
            "id": task_id,
            "description": description,
            "status": "todo",
            "createdAt": now,
            "updatedAt": now
        }
        tasks.append(task)
        save_tasks(tasks)
        print(f"✅ Task added with ID: {task['id']}")
    else:
        print("⚠️ Description cannot be empty.")

# Actualizar tarea
def update_task():
    tasks = load_tasks()
    try:
        task_id = int(input("Enter the task ID to update: "))
        for task in tasks:
            if task["id"] == task_id:
                new_description = input("Enter the new description: ").strip()
                if new_description:
                    task["description"] = new_description
                    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_tasks(tasks)
                    print("✅ Task updated successfully.")
                else:
                    print("⚠️ Description cannot be empty.")
                return
        print("⚠️ Task ID not found.")
    except ValueError:
        print("⚠️ Please enter a valid task ID.")

# Eliminar tarea
def remove_task():
    tasks = load_tasks()
    try:
        task_id = int(input("Enter the task ID to remove: "))
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                save_tasks(tasks)
                print(f"✅ Removed task: {task['description']}")
                return
        print("⚠️ Task ID not found.")
    except ValueError:
        print("⚠️ Please enter a valid task ID.")

# Cambiar estado
def mark_task_status():
    tasks = load_tasks()
    try:
        task_id = int(input("Enter the task ID to update status: "))
        for task in tasks:
            if task["id"] == task_id:
                print(f"Current status: {task['status']}")
                new_status = input("Enter new status (todo, in-progress, done): ").strip().lower()
                if new_status in ["todo", "in-progress", "done"]:
                    task["status"] = new_status
                    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_tasks(tasks)
                    print(f"✅ Task marked as {new_status}.")
                else:
                    print("⚠️ Invalid status.")
                return
        print("⚠️ Task ID not found.")
    except ValueError:
        print("⚠️ Please enter a valid task ID.")

# Ver todas las tareas
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks available.")
    else:
        print("\n📋 Task List:")
        for task in tasks:
            print(f"- ID: {task['id']}, Description: {task['description']}, "
                  f"Status: {task['status']}, Created At: {task['createdAt']}, "
                  f"Updated At: {task['updatedAt']}")

# Filtrar por estado
def list_tasks_by_status():
    tasks = load_tasks()
    status = input("Enter the status to filter by (todo, in-progress, done): ").strip().lower()
    filtered = [task for task in tasks if task["status"] == status]
    if filtered:
        print(f"\n📂 Tasks with status '{status}':")
        for task in filtered:
            print(f"- ID: {task['id']}, Description: {task['description']}, "
                  f"Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
    else:
        print(f"📭 No tasks with status '{status}'.")

# Menú principal
def main():
    parser = argparse.ArgumentParser(description="🛠 Task Tracker CLI")
    parser.add_argument("command", help="Command to execute", choices=[
        "add", "update", "delete", "mark", "list"
    ])
    args = parser.parse_args()

    if args.command == "add":
        add_task()
    elif args.command == "update":
        update_task()
    elif args.command == "delete":
        remove_task()
    elif args.command == "mark":
        mark_task_status()
    elif args.command == "list":
        choice = input("Do you want to filter by status? (y/n): ").strip().lower()
        if choice == "y":
            list_tasks_by_status()
        else:
            view_tasks()

if __name__ == "__main__":
    main()
