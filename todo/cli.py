"""Command line interface: everything the user sees and types.

Design choice: this file only handles input/output. It asks the manager to
do the real work and prints friendly messages when something goes wrong.
"""
from .manager import TaskManager, TaskError
from .storage import StorageError

MENU = """
===== To-Do List Manager =====
1. Add a task
2. View all tasks
3. View pending tasks
4. View completed tasks
5. Mark a task as completed
6. Remove a task
7. Quit
"""


def read_int(prompt: str) -> int:
    """Keep asking until the user types a whole number."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a number (for example: 3).")


def show_tasks(tasks) -> None:
    if not tasks:
        print("  (no tasks to show)")
        return
    for t in tasks:
        mark = "[x]" if t.completed else "[ ]"
        print(f"  {t.id:>3}. {mark} {t.title}  (added {t.created_at})")


def confirm(prompt: str) -> bool:
    return input(prompt + " (y/n): ").strip().lower() in ("y", "yes")


def run(manager: TaskManager) -> None:
    """Main loop: show menu, read choice, do the action, repeat."""
    while True:
        print(MENU)
        choice = input("Choose an option (1-7): ").strip()
        try:
            if choice == "1":
                title = input("Task title: ")
                task = manager.add_task(title)
                print(f"  Added task {task.id}: {task.title}")
            elif choice == "2":
                show_tasks(manager.list_tasks())
            elif choice == "3":
                show_tasks(manager.list_tasks(completed=False))
            elif choice == "4":
                show_tasks(manager.list_tasks(completed=True))
            elif choice == "5":
                show_tasks(manager.list_tasks(completed=False))
                if manager.list_tasks(completed=False):
                    task = manager.complete_task(read_int("Task id to complete: "))
                    print(f"  Completed: {task.title}")
            elif choice == "6":
                show_tasks(manager.list_tasks())
                if manager.list_tasks():
                    task_id = read_int("Task id to remove: ")
                    if confirm("  Really remove it?"):
                        task = manager.remove_task(task_id)
                        print(f"  Removed: {task.title}")
                    else:
                        print("  Cancelled.")
            elif choice == "7":
                print("Goodbye!")
                return
            else:
                print("  Invalid option. Please type a number from 1 to 7.")
        except TaskError as err:
            # Expected problems (empty title, wrong id...): just explain.
            print(f"  Error: {err}")
        except StorageError as err:
            # File problems: tell the user, but keep the app running.
            print(f"  File problem: {err}")
