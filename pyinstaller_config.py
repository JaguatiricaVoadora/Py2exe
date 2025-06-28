import os
import shlex

class PyInstallerConfig:
    def __init__(self):
        self.py_file = ""
        self.icon_file = ""
        self.data_files = []
        self.hidden_imports = []
        self.extra_paths = []
        self.onefile = True
        self.windowed = False
        self.noconfirm = True
        self.clean = True
        self.noupx = False
        self.name = ""

    def build_command(self):
        cmd = ["pyinstaller"]
        if self.onefile:
            cmd.append("--onefile")
        if self.windowed:
            cmd.append("--windowed")
        if self.noconfirm:
            cmd.append("--noconfirm")
        if self.clean:
            cmd.append("--clean")
        if self.noupx:
            cmd.append("--noupx")
        if self.name:
            cmd.extend(["--name", self.name])
        if self.icon_file:
            cmd.extend(["--icon", self.icon_file])
        for item in self.data_files:
            cmd.extend(["--add-data", item])
        for item in self.hidden_imports:
            cmd.extend(["--hidden-import", item])
        for item in self.extra_paths:
            cmd.extend(["--paths", item])
        if self.py_file:
            cmd.append(self.py_file)
        return cmd

    def format_command(self):
        return " ".join(shlex.quote(c) for c in self.build_command())
