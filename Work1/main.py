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
            with open(self.script_path, 'r') as script:
                for line in script:
                    command = line.strip()
                    if command:
                        self.process_command(command)
            self.is_script_execution = False
            self.display_prompt()

    def execute_command(self, event=None):
        command_index = self.output.index("insert linestart")
        command = self.output.get(command_index, "end").strip().replace(f"{self.get_absolute_path()}$ ", "")
        self.output.insert(tk.END, "\n")
        self.process_command(command)
        if not self.is_script_execution:
            self.display_prompt()
        return "break"

    def process_command(self, command):
        self.history.append(command)
        if command.startswith('ls'):
            self.ls()
        elif command.startswith('cd'):
            self.cd(command)
        elif command == 'exit':
            self.root.quit()
            raise SystemExit
        elif command.startswith('rev'):
            self.rev(command)
        elif command == 'history':
            self.show_history()
        else:
            self.output.insert(tk.END, f"sh: {command}: command not found\n")

    def display_prompt(self):
        if not self.is_script_execution:
            self.output.insert(tk.END, f"{self.get_absolute_path()}$ ")
            self.output.mark_set("insert", "end")
            self.output.see("end")

    def get_absolute_path(self):
        return '/' + self.current_dir if self.current_dir else '/'

    def ls(self):
        parts = self.history[-1].split(maxsplit=1)
        path = parts[1] if len(parts) > 1 else ""
        if path.startswith('/'):
            full_path = path[1:]
        else:
            path_components = (self.current_dir.split('/') if self.current_dir else []) + path.split('/')
            resolved_path = []
            for component in path_components:
                if component == "..":
                    if resolved_path:
                        resolved_path.pop()
                elif component:
                    resolved_path.append(component)
            full_path = "/".join(resolved_path)
        prefix = full_path + '/' if full_path else ''
        files = [
            name[len(prefix):] for name in self.fs_contents
            if name.startswith(prefix) and '/' not in name[len(prefix):]
        ]
        if files:
            self.output.insert(tk.END, '\n'.join(files) + '\n')
        else:
            if full_path in self.fs_contents:
                self.output.insert(tk.END, '\n')
            else:
                self.output.insert(tk.END, f"ls: cannot access '{path}': No such file or directory\n")

    def cd(self, command):
        _, path = command.split()
        if path.startswith('/'):
            current_path = []
            path_components = path[1:].split('/')
        else:
            current_path = self.current_dir.split('/') if self.current_dir else []
            path_components = path.split('/')
        for component in path_components:
            if component == "..":
                if current_path:
                    current_path.pop()
            elif component and ("/".join(current_path + [component]) in self.fs_contents) and \
                    self.fs_contents["/".join(current_path + [component])].isdir():
                current_path.append(component)
            else:
                self.output.insert(tk.END, f"sh: cd: {path}: No such file or directory\n")
                return
        self.current_dir = "/".join(current_path)

    def rev(self, command):
        _, path = command.split()
        if path.startswith('/'):
            full_path = path[1:]
        else:
            full_path_components = (self.current_dir.split('/') if self.current_dir else []) + path.split('/')
            resolved_path = []
            for component in full_path_components:
                if component == "..":
                    if resolved_path:
                        resolved_path.pop()
                elif component:
                    resolved_path.append(component)
            full_path = "/".join(resolved_path)
        if full_path in self.fs_contents:
            with tarfile.open(self.fs_path) as tar:
                file_member = tar.getmember(full_path)
                with tar.extractfile(file_member) as f:
                    lines = f.read().decode('utf-8').splitlines()
                    reversed_lines = [line[::-1] for line in lines]
                    self.output.insert(tk.END, '\n'.join(reversed_lines) + '\n')
        else:
            self.output.insert(tk.END, f"rev: cannot open {path}: No such file or directory\n")

    def show_history(self):
        numbered_history = [f"    {i + 1}  {command}" for i, command in enumerate(self.history)]
        self.output.insert(tk.END, '\n'.join(numbered_history) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fs_path')
    parser.add_argument('--script', default=None)
    args = parser.parse_args()
    root = tk.Tk()
    root.title('Shell Emulator')
    emulator = ShellEmulator(root, args.fs_path, args.script)
    root.mainloop()
