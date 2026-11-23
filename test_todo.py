import os
import tempfile
import unittest

import todo


class TodoTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)
        todo.TASKS_FILE = self.path

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add(self):
        t = todo.add_task("Buy milk", "high")
        self.assertEqual((t["id"], t["title"], t["priority"], t["done"]), (1, "Buy milk", "high", False))

    def test_done(self):
        todo.add_task("a")
        self.assertTrue(todo.mark_done(1))
        self.assertFalse(todo.mark_done(99))

    def test_delete(self):
        todo.add_task("a")
        self.assertTrue(todo.delete_task(1))
        self.assertFalse(todo.delete_task(1))

    def test_sort_priority(self):
        todo.add_task("l", "low")
        todo.add_task("h", "high")
        todo.add_task("m", "medium")
        order = [t["priority"] for t in todo.list_tasks("priority")]
        self.assertEqual(order, ["high", "medium", "low"])

    def test_persistence(self):
        todo.add_task("a")
        self.assertEqual(len(todo.load()), 1)


if __name__ == "__main__":
    unittest.main()
