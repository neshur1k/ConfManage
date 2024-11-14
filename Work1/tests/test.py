import os
import unittest
from io import StringIO
from main import ShellEmulator
import tkinter as tk


class OutputStub(StringIO):
    def __init__(self):
        super().__init__()
        self.contents = ""

    def insert(self, _, text):
        self.write(text)

    def mark_set(self, mark, index):
        pass

    def see(self, index):
        pass

    def index(self, index_name):
        return "1.0"

    def get(self, start, end=None):
        return self.contents


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

    def test_load_archive_dirs(self):
        fs_contents = self.emulator.load_archive()
        self.assertIn("a", fs_contents)
        self.assertIn("b", fs_contents)

    def test_load_archive_files(self):
        fs_contents = self.emulator.load_archive()
        self.assertIn("a/c/file1.txt", fs_contents)
        self.assertIn("a/c/file2.txt", fs_contents)

    def test_load_startup_script(self):
        with open("test_script.txt", "w") as f:
            f.write("ls\ncd a\n")
        self.emulator.script_path = "test_script.txt"
        self.emulator.load_startup_script()
        self.assertIn("ls", self.emulator.history)
        self.assertIn("cd a", self.emulator.history)
        os.remove("test_script.txt")

    def test_load_startup_script_empty(self):
        with open("test_script_empty.txt", "w") as f:
            pass
        self.emulator.script_path = "test_script_empty.txt"
        self.emulator.load_startup_script()
        self.assertEqual(self.emulator.history, [])
        os.remove("test_script_empty.txt")

    def test_execute_command(self):
        self.emulator.output.insert(tk.END, "ls")
        self.emulator.execute_command()
        output = self.output_stub.getvalue()
        self.assertIn("a", output)

    def test_execute_command_invalid(self):
        self.emulator.output.insert(tk.END, "")
        self.emulator.execute_command()
        output = self.output_stub.getvalue()
        self.assertIn("sh: : command not found", output)

    def test_process_command(self):
        self.emulator.process_command("ls")
        output = self.output_stub.getvalue()
        self.assertIn("a", output)
        self.assertIn("b", output)

    def test_process_command_invalid(self):
        self.emulator.process_command("unknown_command")
        output = self.output_stub.getvalue()
        self.assertIn("sh: unknown_command: command not found", output)

    def test_display_prompt_root(self):
        self.emulator.current_dir = ""
        self.emulator.display_prompt()
        output = self.output_stub.getvalue()
        self.assertIn("/$ ", output)

    def test_display_prompt_subdirectory(self):
        self.emulator.current_dir = "a/b"
        self.emulator.display_prompt()
        output = self.output_stub.getvalue()
        self.assertIn("/a/b$ ", output)

    def test_get_absolute_path_root(self):
        self.emulator.current_dir = ""
        self.assertEqual(self.emulator.get_absolute_path(), "/")

    def test_get_absolute_path_subdirectory(self):
        self.emulator.current_dir = "a/b"
        self.assertEqual(self.emulator.get_absolute_path(), "/a/b")


if __name__ == "__main__":
    unittest.main()
