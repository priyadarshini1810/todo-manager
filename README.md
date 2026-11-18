# To-Do List Manager (CLI)

A simple command line app to add, view, complete and remove tasks.
Tasks are saved in a JSON file, so they are still there next time you open it.

## Requirements
- Python 3.8 or newer
- **No extra packages to install** (only the Python standard library is used)

## How to run
1. Unzip the folder and open a terminal inside it.
2. Start the app:
   ```
   python main.py
   ```
   (On some systems use `python3 main.py`.)
3. Optional: use a different save file:
   ```
   python main.py --file my_tasks.json
   ```
4. Run the tests:
   ```
   python -m unittest discover tests
   ```

## Features
| Menu option | What it does |
|---|---|
| 1 | Add a task |
| 2 / 3 / 4 | View all / pending / completed tasks |
| 5 | Mark a task as completed |
| 6 | Remove a task (asks "are you sure?") |
| 7 | Quit |

## Project structure
```
todo_manager/
├── main.py            # starts the app, reads --file option
├── todo/
│   ├── task.py        # Task class (one to-do item)
│   ├── storage.py     # JsonStorage class (save/load file)
│   ├── manager.py     # TaskManager class (rules and logic)
│   └── cli.py         # menu, input and printing
├── tests/test_todo.py # unit tests
└── README.md
```

## Design decisions (in simple words)
1. **Separate files for separate jobs.** The screen code (`cli.py`), the
   rules (`manager.py`) and the saving (`storage.py`) do not mix. If one
   changes, the others stay the same.
2. **Object-oriented design.** `Task`, `JsonStorage` and `TaskManager` are
   classes. Each has one clear responsibility.
3. **No `input()`/`print()` in the manager.** This makes it easy to test
   and to reuse with a different interface later.
4. **Save after every change.** If the program closes suddenly, nothing is lost.
5. **Safe saving.** The file is written to a temp file first and then renamed,
   so a crash cannot leave a half-written file.
6. **IDs are never reused.** A counter (`next_id`) is saved in the file and only
   goes up, so an old id never points to a different task after a delete.
7. **Custom exceptions** (`InvalidTaskError`, `TaskNotFoundError`) let the
   CLI show clear messages instead of crashing.

## Error handling
| Problem | What happens |
|---|---|
| Empty or too long title (over 100 chars) | Error message, nothing added |
| Typing letters instead of a task id | Asks again until a number is given |
| Id that does not exist | "No task with id X." |
| Completing an already completed task | Friendly error message |
| Menu choice outside 1-7 | "Invalid option" message |
| Missing save file | Starts with an empty list |
| Damaged JSON file | Backed up as `.corrupt`, app starts fresh |
| Ctrl+C / Ctrl+D | Exits politely |
| Cannot read/write file | Message shown, app keeps running |

## Pseudo-code
```
start:
    read --file option
    storage = JsonStorage(file)
    manager = TaskManager(storage)      # loads saved tasks
    loop forever:
        show menu
        read choice
        if choice == 1: ask title -> manager.add_task(title)
        if choice == 2/3/4: manager.list_tasks(filter) -> print
        if choice == 5: show pending -> ask id -> manager.complete_task(id)
        if choice == 6: show all -> ask id -> confirm -> manager.remove_task(id)
        if choice == 7: say goodbye, stop
        else: print "invalid option"
        on any expected error: print the message and go back to the menu
```

## Flow diagram
```
        +-------------+
        |  Start app  |
        +------+------+
               |
      Load tasks from JSON file
               |
               v
        +-------------+  <--------------------------+
        |  Show menu  |                              |
        +------+------+                              |
               |                                     |
        Read user choice                             |
               |                                     |
   +-----+-----+-----+-----+------+                  |
   |     |     |     |     |      |                  |
  Add  View  Done  Remove Invalid Quit -> Exit       |
   |     |     |     |     |                         |
   +-----+-----+-----+-----+-------------------------+
     (errors are caught and shown, then back to menu)
```

## Possible future improvements
- Due dates and priorities
- Edit a task title
- Search tasks by keyword
