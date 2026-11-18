"""Run with:  python -m unittest discover tests"""
import os
import tempfile
import unittest

from todo.manager import (TaskManager, InvalidTaskError,
                          TaskNotFoundError, TaskError)
from todo.storage import JsonStorage


class TodoTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "t.json")
        self.m = TaskManager(JsonStorage(self.path))

    def tearDown(self):
        self.dir.cleanup()

    def test_add_and_list(self):
        self.m.add_task("Buy milk")
        self.assertEqual(len(self.m.list_tasks()), 1)

    def test_empty_title_rejected(self):
        with self.assertRaises(InvalidTaskError):
            self.m.add_task("   ")

    def test_long_title_rejected(self):
        with self.assertRaises(InvalidTaskError):
            self.m.add_task("x" * 101)

    def test_complete(self):
        t = self.m.add_task("Study")
        self.m.complete_task(t.id)
        self.assertEqual(len(self.m.list_tasks(completed=True)), 1)
        with self.assertRaises(TaskError):
            self.m.complete_task(t.id)  # already done

    def test_remove_and_missing_id(self):
        t = self.m.add_task("Temp")
        self.m.remove_task(t.id)
        with self.assertRaises(TaskNotFoundError):
            self.m.remove_task(t.id)

    def test_ids_not_reused(self):
        a = self.m.add_task("A")
        self.m.remove_task(a.id)
        b = self.m.add_task("B")
        self.assertNotEqual(a.id, b.id)

    def test_ids_not_reused_after_restart(self):
        a = self.m.add_task("A")
        self.m.remove_task(a.id)
        again = TaskManager(JsonStorage(self.path))
        self.assertNotEqual(a.id, again.add_task("B").id)

    def test_persistence(self):
        self.m.add_task("Saved")
        again = TaskManager(JsonStorage(self.path))
        self.assertEqual(again.list_tasks()[0].title, "Saved")

    def test_corrupt_file(self):
        with open(self.path, "w") as f:
            f.write("{not json")
        m = TaskManager(JsonStorage(self.path))
        self.assertEqual(m.list_tasks(), [])


if __name__ == "__main__":
    unittest.main()
