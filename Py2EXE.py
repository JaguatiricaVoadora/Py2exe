import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
from pyinstaller_config import PyInstallerConfig

class PyInstallerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # Black version (dark mode)
        self.title("🔥 PyInstaller GUI Builder")
        self.geometry("650x700")
        self.configure(bg="#111")  # Black background
        self.option_add("*Font", ("Courier New", 10, "bold"))
        self.option_add("*Button.Background", "#222")
        self.option_add("*Button.Foreground", "#0ff")
        self.option_add("*Button.Relief", "raised")
        self.option_add("*Button.BorderWidth", 3)
        self.option_add("*Entry.Background", "#222")
        self.option_add("*Entry.Foreground", "#fff")
        self.option_add("*Entry.Relief", "sunken")
        self.option_add("*Entry.BorderWidth", 2)
        self.option_add("*Label.Background", "#111")
        self.option_add("*Label.Foreground", "#0ff")
        self.option_add("*Checkbutton.Background", "#111")
        self.option_add("*Checkbutton.Foreground", "#0ff")
        self.option_add("*Frame.Background", "#111")

        self.config = PyInstallerConfig()

        # INPUT SCRIPT
        tk.Label(self, text="Codigo python principal:").pack(anchor="w", padx=10, pady=(10,0))
        frame_script = tk.Frame(self, relief="groove", borderwidth=3, bg="#222")
        frame_script.pack(fill="x", padx=10)
        self.script_entry = tk.Entry(frame_script, bg="#222", fg="#fff", insertbackground="#0ff")
        self.script_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=3)
        tk.Button(frame_script, text="Selecionar", command=self.select_script, bg="#222", fg="#0ff", activebackground="#333", activeforeground="#fff").pack(side="right", pady=3)

        # OPTIONS
        self.opt_frame = tk.LabelFrame(self, text="Opções", relief="ridge", borderwidth=3, padx=5, pady=5, bg="#111", fg="#0ff")
        self.opt_frame.pack(fill="x", padx=10, pady=5)

        self.onefile = tk.BooleanVar(value=True)
        self.windowed = tk.BooleanVar()
        self.noconfirm = tk.BooleanVar(value=True)
        self.clean = tk.BooleanVar(value=True)
        self.noupx = tk.BooleanVar()

        for text, var in [
            ("--onefile", self.onefile),
            ("--windowed", self.windowed),
            ("--noconfirm", self.noconfirm),
            ("--clean", self.clean),
            ("--noupx", self.noupx),
        ]:
            tk.Checkbutton(self.opt_frame, text=text, variable=var, anchor="w", padx=10, bg="#111", fg="#0ff", selectcolor="#222").pack(anchor="w")

        # Name
        tk.Label(self, text="--name (nome do .exe):").pack(anchor="w", padx=10)
        self.name_entry = tk.Entry(self, width=30, bg="#222", fg="#fff", insertbackground="#0ff")
        self.name_entry.pack(fill="x", padx=10, pady=3)

        # Icon
        tk.Label(self, text="--icon (.ico):").pack(anchor="w", padx=10, pady=(10,0))
        frame_icon = tk.Frame(self, relief="groove", borderwidth=2, bg="#222")
        frame_icon.pack(fill="x", padx=10)
        self.icon_entry = tk.Entry(frame_icon, bg="#222", fg="#fff", insertbackground="#0ff")
        self.icon_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=3)
        tk.Button(frame_icon, text="Selecionar", command=self.select_icon, bg="#222", fg="#0ff", activebackground="#333", activeforeground="#fff").pack(side="right", pady=3)

        # ADD DATA
        tk.Label(self, text="--add-data (arquivos/pastas extras):").pack(anchor="w", padx=10)
        frame_data = tk.Frame(self, relief="groove", borderwidth=2, bg="#222")
        frame_data.pack(fill="x", padx=10)
        self.data_entry = tk.Entry(frame_data, bg="#222", fg="#fff", insertbackground="#0ff")
        self.data_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=3)
        tk.Button(frame_data, text="Adicionar", command=self.add_data, bg="#222", fg="#0ff", activebackground="#333", activeforeground="#fff").pack(side="right", pady=3)

        # HIDDEN IMPORTS
        tk.Label(self, text="--hidden-import (módulos ocultos):").pack(anchor="w", padx=10)
        frame_hidden = tk.Frame(self, relief="groove", borderwidth=2, bg="#222")
        frame_hidden.pack(fill="x", padx=10)
        self.hidden_entry = tk.Entry(frame_hidden, bg="#222", fg="#fff", insertbackground="#0ff")
        self.hidden_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=3)
        tk.Button(frame_hidden, text="Adicionar", command=self.add_hidden, bg="#222", fg="#0ff", activebackground="#333", activeforeground="#fff").pack(side="right", pady=3)

        # EXTRA PATHS
        tk.Label(self, text="--paths (pastas com código):").pack(anchor="w", padx=10)
        frame_paths = tk.Frame(self, relief="groove", borderwidth=2, bg="#222")
        frame_paths.pack(fill="x", padx=10)
        self.paths_entry = tk.Entry(frame_paths, bg="#222", fg="#fff", insertbackground="#0ff")
        self.paths_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=3)
        tk.Button(frame_paths, text="Adicionar", command=self.add_path, bg="#222", fg="#0ff", activebackground="#333", activeforeground="#fff").pack(side="right", pady=3)

        # COMPILAR
        tk.Button(self, text="🚀 Compilar para EXE", command=self.compile, bg="#222", fg="#0ff", relief="raised", borderwidth=4, font=("Courier New", 11, "bold"), activebackground="#333", activeforeground="#fff").pack(pady=10)

        # LOG
        self.log = tk.Text(self, height=18, bg="#111", fg="#0f0", insertbackground="#0ff", relief="sunken", borderwidth=3, font=("Courier New", 10))
        self.log.pack(fill="both", padx=10, pady=10, expand=True)

    def select_script(self):
        path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if path:
            self.config.py_file = path
            self.script_entry.delete(0, tk.END)
            self.script_entry.insert(0, path)

    def select_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if path:
            self.config.icon_file = path
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, path)

    def add_data(self):
        path = filedialog.askopenfilename()
        if not path:
            path = filedialog.askdirectory()
        if path:
            sep = ";" if os.name == "nt" else ":"
            formatted = f"{path}{sep}{os.path.basename(path)}"
            self.config.data_files.append(formatted)
            current = self.data_entry.get()
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, current + " " + formatted)

    def add_hidden(self):
        module = self.hidden_entry.get()
        if module:
            self.config.hidden_imports.append(module)
            self.hidden_entry.delete(0, tk.END)

    def add_path(self):
        path = filedialog.askdirectory()
        if path:
            self.config.extra_paths.append(path)
            self.paths_entry.delete(0, tk.END)
            self.paths_entry.insert(0, " ".join(self.config.extra_paths))

    def compile(self):
        if not self.script_entry.get():
            messagebox.showerror("Erro", "Seleciona o script .py primeiro.")
            return

        # Sync GUI state to config
        self.config.onefile = self.onefile.get()
        self.config.windowed = self.windowed.get()
        self.config.noconfirm = self.noconfirm.get()
        self.config.clean = self.clean.get()
        self.config.noupx = self.noupx.get()
        self.config.name = self.name_entry.get().strip()
        self.config.icon_file = self.icon_entry.get().strip()
        self.config.py_file = self.script_entry.get().strip()

        cmd = self.config.build_command()

        self.log.delete("1.0", tk.END)
        self.log.insert(tk.END, "Compilando com comando:\n" + self.config.format_command() + "\n\n")

        def run():
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                self.log.insert(tk.END, line)
                self.log.see(tk.END)
            process.wait()
            if process.returncode == 0:
                self.log.insert(tk.END, "\n✅ EXE criado com sucesso em /dist\n")
            else:
                self.log.insert(tk.END, f"\n❌ Erro. Código: {process.returncode}\n")

        threading.Thread(target=run).start()

if __name__ == "__main__":
    PyInstallerGUI().mainloop()
