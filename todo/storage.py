"""Storage: saving and loading tasks from a JSON file.

Design choice: storage is a separate class so the rest of the app does not
care HOW tasks are saved. Later you could swap JSON for a database by
writing a new storage class with the same two methods (load, save).
"""
import json
import os
import tempfile


class StorageError(Exception):
    """Raised when the file cannot be read or written."""


class JsonStorage:
    def __init__(self, path: str = "tasks.json"):
        self.path = path

    def load(self) -> dict:
        """Return {"next_id": int, "tasks": [dicts]}. Empty data if no file yet."""
        if not os.path.exists(self.path):
            return {"next_id": 1, "tasks": []}  # First run: that is fine.
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                # Older/simple format: just a list of tasks.
                return {"next_id": 1, "tasks": data}
            if not isinstance(data, dict) or not isinstance(data.get("tasks"), list):
                raise ValueError("Unexpected file layout")
            return data
        except (json.JSONDecodeError, ValueError):
            # Corrupt file: keep a backup so the user's data is not lost,
            # then start fresh instead of crashing.
            backup = self.path + ".corrupt"
            try:
                os.replace(self.path, backup)
            except OSError:
                pass
            print(f"Warning: '{self.path}' was damaged. "
                  f"Saved a copy as '{backup}' and started a new list.")
            return {"next_id": 1, "tasks": []}
        except OSError as err:
            raise StorageError(f"Could not read '{self.path}': {err}") from err

    def save(self, data: dict) -> None:
        """Write the data dictionary to disk safely.

        Design choice: write to a temporary file first, then rename it.
        If the program crashes mid-write, the old file stays intact.
        """
        directory = os.path.dirname(os.path.abspath(self.path))
        try:
            fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp_path, self.path)
        except OSError as err:
            raise StorageError(f"Could not save '{self.path}': {err}") from err
