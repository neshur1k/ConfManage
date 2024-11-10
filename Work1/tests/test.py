import unittest
from io import StringIO
from main import ShellEmulator
import tkinter as tk


class OutputStub(StringIO):
    def insert(self, _, text):
        self.write(text)


class ShellEmulatorTest(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.output_stub = OutputStub()
        self.emulator = ShellEmulator(self.root, "archive.tar")
        self.emulator.output = self.output_stub

    def test_ls_current_directory(self):
        self.emulator.process_command("ls")
        output = self.output_stub.getvalue()
        self.assertIn("a", output)
        self.assertIn("b", output)

    def test_ls_specific_directory(self):
        self.emulator.process_command("ls a/c")
        output = self.output_stub.getvalue()
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)

    def test_cd(self):
        self.emulator.process_command("cd a")
        self.assertEqual(self.emulator.current_dir, "a")

    def test_cd_nonexistent_directory(self):
        self.emulator.process_command("cd /nonexistent")
        output = self.output_stub.getvalue()
        self.assertIn("sh: cd: /nonexistent: No such file or directory", output)

    def test_rev(self):
        self.emulator.process_command("rev a/c/file1.txt")
        output = self.output_stub.getvalue()
        self.assertEqual(output.strip(), "!dlroW ,olleH\neybdooG")

    def test_rev_nonexistent_file(self):
        self.emulator.process_command("rev nonexistent.txt")
        output = self.output_stub.getvalue()
        self.assertIn("rev: cannot open nonexistent.txt: No such file or directory", output)

    def test_history(self):
        self.emulator.process_command("ls")
        self.emulator.process_command("cd a")
        self.emulator.process_command("history")
        output = self.output_stub.getvalue()
        self.assertIn("    1  ls", output)
        self.assertIn("    2  cd a", output)
        self.assertIn("    3  history", output)

    def test_history_no_commands(self):
        self.emulator.process_command("history")
        output = self.output_stub.getvalue()
        self.assertIn("    1  history", output)

    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.emulator.process_command("exit")


if __name__ == "__main__":
    unittest.main()
