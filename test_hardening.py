import json
import os
import tempfile
import unittest
from unittest import mock

import todo
from test_cli import run


class HardeningTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)
        todo.TASKS_FILE = self.path

    def tearDown(self):
        for p in (self.path, self.path + ".tmp"):
            if os.path.exists(p):
                os.remove(p)

    # R1
    def test_invalid_priority_rejected_and_not_stored(self):
        code, out = run("add", "x", "urgent")
        self.assertEqual(code, 1)
        self.assertIn("Invalid priority", out)
        self.assertFalse(os.path.exists(self.path))

    def test_valid_priorities_still_accepted(self):
        for p in ("high", "medium", "low"):
            self.assertEqual(run("add", p, p)[0], 0)

    def test_sort_survives_legacy_bad_priority(self):
        with open(self.path, "w") as f:
            json.dump([{"id": 1, "title": "a", "priority": "urgent", "done": False},
                       {"id": 2, "title": "b", "priority": "high", "done": False}], f)
        self.assertEqual([t["id"] for t in todo.list_tasks("priority")], [2, 1])

    # R3
    def test_corrupt_file_gives_clear_error_and_is_not_overwritten(self):
        with open(self.path, "w") as f:
            f.write('[{"id":1')
        for args in (("list",), ("add", "x")):
            code, out = run(*args)
            self.assertEqual(code, 2)
            self.assertTrue(out.startswith("Error:"))
        with open(self.path) as f:
            self.assertEqual(f.read(), '[{"id":1')

    def test_failed_write_keeps_old_data_and_leaves_no_tmp(self):
        todo.add_task("keep")
        with mock.patch("todo.json.dump", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                todo.add_task("lost")
        self.assertEqual([t["title"] for t in todo.load()], ["keep"])
        self.assertFalse(os.path.exists(self.path + ".tmp"))


if __name__ == "__main__":
    unittest.main()
