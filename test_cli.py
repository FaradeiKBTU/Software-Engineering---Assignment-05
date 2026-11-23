import contextlib
import io
import os
import tempfile
import unittest

import todo


def run(*args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = todo.main(["todo.py", *args])
    return code, out.getvalue().strip()


class CliTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)
        todo.TASKS_FILE = self.path

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_message(self):
        self.assertEqual(run("add", "Buy milk", "high"), (0, "Added #1: Buy milk (high)"))

    def test_done_and_delete_messages(self):
        run("add", "a")
        self.assertEqual(run("done", "1"), (0, "Done."))
        self.assertEqual(run("done", "99"), (0, "Task not found."))
        self.assertEqual(run("delete", "1"), (0, "Deleted."))
        self.assertEqual(run("delete", "1"), (0, "Task not found."))

    def test_list_sorted_by_priority(self):
        run("add", "l", "low")
        run("add", "h", "high")
        _, out = run("list", "priority")
        self.assertEqual([l.split()[-1] for l in out.splitlines()], ["(high)", "(low)"])

    def test_unknown_command(self):
        self.assertEqual(run("nope"), (1, "Unknown command"))


if __name__ == "__main__":
    unittest.main()
