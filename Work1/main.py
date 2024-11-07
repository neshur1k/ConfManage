import tkinter as tk
import tarfile
import os
import argparse


class ShellEmulator:
    def __init__(self, root, fs_path, script_path=None):
        self.root = root
        self.fs_path = fs_path
        self.script_path = script_path
        self.history = []
        self.current_dir = ''
        self.is_script_execution = False
        self.fs_contents = self.load_archive()
        self.output = tk.Text(root, height=20, width=80)
        self.output.pack()
        self.output.bind('<Return>', self.execute_command)
        if self.script_path:
            self.load_startup_script()
        else:
            self.display_prompt()

    def load_archive(self):
        fs_contents = {}
        with tarfile.open(self.fs_path) as tar:
            for member in tar.getmembers():
                fs_contents[member.name] = member
        return fs_contents

    def load_startup_script(self):
        if self.script_path and os.path.exists(self.script_path):
            self.is_script_execution = True
            for line in open(self.script_path, 'r'):
                command = line.strip()
                if command:
                    pass
                    # self.process_command(command)
            self.is_script_execution = False
            self.display_prompt()

    def execute_command(self, event=None):
        command_index = self.output.index("insert linestart")
        command = self.output.get(command_index, "end").strip().replace(f"{self.get_absolute_path()}$ ", "")
        self.output.insert(tk.END, "\n")
        # self.process_command(command)
        if not self.is_script_execution:
            self.display_prompt()
        return "break"

    def display_prompt(self):
        if not self.is_script_execution:
            self.output.insert(tk.END, f"{self.get_absolute_path()}$ ")
            self.output.mark_set("insert", "end")
            self.output.see("end")

    def get_absolute_path(self):
        return '/' + self.current_dir if self.current_dir else '/'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fs_path')
    parser.add_argument('--script', default=None)
    args = parser.parse_args()
    root = tk.Tk()
    root.title('Shell Emulator')
    emulator = ShellEmulator(root, args.fs_path, args.script)
    root.mainloop()
