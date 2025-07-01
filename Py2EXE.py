import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sv_ttk  # Tema moderno para Tkinter
import subprocess
import threading
import os
from pyinstaller_config import PyInstallerConfig

class PyInstallerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔥 PyInstaller GUI Builder")
        self.geometry("650x700")
        self.option_add("*Font", ("Segoe UI", 10))
        self.config = PyInstallerConfig()

        # Aplica tema moderno escuro
        self.style = ttk.Style(self)
        sv_ttk.set_theme("dark")

        # Função para adicionar tooltips
        def add_tooltip(widget, text):
            def on_enter(e):
                self.tooltip = tk.Toplevel(widget)
                self.tooltip.wm_overrideredirect(True)
                self.tooltip.wm_geometry(f"+{widget.winfo_rootx()+20}+{widget.winfo_rooty()+20}")
                label = tk.Label(self.tooltip, text=text, background="#222", foreground="#0ff", relief="solid", borderwidth=1, font=("Segoe UI", 9))
                label.pack(ipadx=4, ipady=2)
            def on_leave(e):
                if hasattr(self, 'tooltip'):
                    self.tooltip.destroy()
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

        # INPUT SCRIPT
        ttk.Label(self, text="Arquivo Python principal:").pack(anchor="w", padx=10, pady=(10,0))
        frame_script = ttk.Frame(self)
        frame_script.pack(fill="x", padx=10)
        self.script_entry = ttk.Entry(frame_script)
        self.script_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=3)
        btn_script = ttk.Button(frame_script, text="Selecionar", command=self.select_script)
        btn_script.pack(side="right", pady=3)
        add_tooltip(self.script_entry, "Selecione o arquivo principal do seu projeto Python.")
        add_tooltip(btn_script, "Clique para escolher o arquivo .py principal.")

        # OPÇÕES
        self.opt_frame = ttk.LabelFrame(self, text="Opções", padding=(5,5))
        self.opt_frame.pack(fill="x", padx=10, pady=5)

        self.onefile = tk.BooleanVar(value=True)
        self.windowed = tk.BooleanVar()
        self.noconfirm = tk.BooleanVar(value=True)
        self.clean = tk.BooleanVar(value=True)
        self.noupx = tk.BooleanVar()

        for text, var, dica in [
            ("--onefile", self.onefile, "Gera um único arquivo .exe"),
            ("--windowed", self.windowed, "Sem console ao abrir o .exe"),
            ("--noconfirm", self.noconfirm, "Não pede confirmação para sobrescrever arquivos"),
            ("--clean", self.clean, "Limpa pastas temporárias antes de compilar"),
            ("--noupx", self.noupx, "Não usa UPX para compactação"),
        ]:
            chk = ttk.Checkbutton(self.opt_frame, text=text, variable=var)
            chk.pack(anchor="w", padx=10)
            add_tooltip(chk, dica)

        # NOME
        ttk.Label(self, text="--name (nome do .exe):").pack(anchor="w", padx=10)
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.pack(fill="x", padx=10, pady=3)
        add_tooltip(self.name_entry, "Nome do arquivo .exe gerado.")

        # ÍCONE
        ttk.Label(self, text="--icon (.ico):").pack(anchor="w", padx=10, pady=(10,0))
        frame_icon = ttk.Frame(self)
        frame_icon.pack(fill="x", padx=10)
        self.icon_entry = ttk.Entry(frame_icon)
        self.icon_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=3)
        btn_icon = ttk.Button(frame_icon, text="Selecionar", command=self.select_icon)
        btn_icon.pack(side="right", pady=3)
        add_tooltip(self.icon_entry, "Caminho para o arquivo .ico do ícone.")
        add_tooltip(btn_icon, "Clique para escolher o ícone .ico.")

        # ADD DATA
        ttk.Label(self, text="--add-data (arquivos/pastas extras):").pack(anchor="w", padx=10)
        frame_data = ttk.Frame(self)
        frame_data.pack(fill="x", padx=10)
        self.data_entry = ttk.Entry(frame_data)
        self.data_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=3)
        btn_data = ttk.Button(frame_data, text="Adicionar", command=self.add_data)
        btn_data.pack(side="right", pady=3)
        add_tooltip(self.data_entry, "Arquivos ou pastas adicionais para incluir no .exe.")
        add_tooltip(btn_data, "Clique para adicionar arquivos/pastas extras.")

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
