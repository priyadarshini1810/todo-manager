"""Entry point. Run with:  python main.py  [--file my_tasks.json]"""
import argparse
import sys

from todo.cli import run
from todo.manager import TaskManager
from todo.storage import JsonStorage, StorageError


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple CLI To-Do List Manager")
    parser.add_argument("--file", default="tasks.json",
                        help="where tasks are saved (default: tasks.json)")
    args = parser.parse_args()

    try:
        manager = TaskManager(JsonStorage(args.file))
        run(manager)
    except StorageError as err:
        print(f"Cannot start: {err}")
        return 1
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or Ctrl+D: exit politely. Tasks are already saved
        # after every change, so nothing is lost.
        print("\nGoodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
