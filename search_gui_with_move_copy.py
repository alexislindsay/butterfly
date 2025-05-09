# search_gui_final_refined.pyw
import sys
import os
import traceback
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
from threading import Thread, Event
import subprocess
import datetime
from functools import partial

# --- Configurazione Logging ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()
log_filename = os.path.join(script_dir, "search_gui_app.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# --- Costanti e Stili ---
DEFAULT_PLACEHOLDER = "(Digita estensione o scegli tipo)"
ALL_MARKER = "[Tipo] Tutte le estensioni"
IMG_MARKER = "[Tipo] Immagini (.jpg, .png...)"
VID_MARKER = "[Tipo] Video (.mp4, .avi...)"
ARC_MARKER = "[Tipo] Archivi (.zip, .rar...)"
EXE_MARKER = "[Tipo] Eseguibili (.exe, .msi...)"
DEFAULT_EXT_VALUES = [
    DEFAULT_PLACEHOLDER, ALL_MARKER, IMG_MARKER, VID_MARKER, ARC_MARKER, EXE_MARKER,
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".ico",
    ".mp4", ".avi", ".mkv", ".mov", ".wmv",
    ".zip", ".rar", ".7z", ".tar", ".gz",
    ".exe", ".msi", ".bat", ".cmd",
    ".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".html", ".css", ".js", ".py",".json", ".csv"
]
MARKER_TO_EXT = { IMG_MARKER: ".jpg", VID_MARKER: ".mp4", ARC_MARKER: ".zip", EXE_MARKER: ".exe" }
CHECK_BOX_UNCHECKED = "☐"
CHECK_BOX_CHECKED = "☑"

class FileSearcherGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Searcher Pro")
        master.geometry("1200x700")
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except:
            pass
        self.configure_styles()
        self.file_info = []
        self.checked_items = {}
        self.stop_event = Event()
        self.search_thread = None
        self.default_extensions = list(DEFAULT_EXT_VALUES)
        self.sort_column = None
        self.sort_direction = False
        self.create_widgets()

    def configure_styles(self):
        font_normal = ("Arial", 12)
        font_input_bold = ("Arial", 12, "bold")
        font_label_bold = ("Arial", 14, "bold")
        font_button_bold = ("Arial", 11, "bold")
        font_treeview_bold = ("Arial", 12, "bold")
        color_bg_light = "#F5F5F5"; color_bg_frame = "#ECECEC"; color_text = "#212529"
        color_green = "#28a745"; color_green_active = "#218838"
        color_yellow = "#ffc107"; color_yellow_active = "#e0a800"
        color_red = "#dc3545"; color_red_active = "#c82333"
        color_blue = "#007bff"; color_blue_active = "#0056b3"
        color_text_light = "#FFFFFF"
        disabled_fg = "#6c757d"; disabled_bg = "#ced4da"
        treeview_bg = "black"; treeview_fg = "#00E600"

        self.style.configure('.', background=color_bg_light, foreground=color_text, font=font_normal)
        self.style.configure('TFrame', background=color_bg_frame)
        self.style.configure('TLabel', background=color_bg_frame, foreground=color_text)
        self.style.configure('Title.TLabel', font=font_label_bold, background=color_bg_frame)
        self.style.configure('TEntry', fieldbackground="#FFFFFF", foreground=color_text, insertcolor=color_text, padding=(5, 5))
        self.style.configure('TCombobox', padding=(5, 5))
        self.style.configure('TButton', font=font_button_bold, padding=(10, 6), relief=tk.RAISED)
        self.style.map('TButton', background=[('active', color_bg_light)])
        self.style.configure('Success.TButton', foreground=color_text_light, background=color_green)
        self.style.map('Success.TButton', background=[('active', color_green_active)])
        self.style.configure('Warning.TButton', foreground=color_text, background=color_yellow)
        self.style.map('Warning.TButton', background=[('active', color_yellow_active)])
        self.style.configure('Danger.TButton', foreground=color_text_light, background=color_red)
        self.style.map('Danger.TButton', background=[('active', color_red_active)])
        self.style.configure('Neutral.TButton', foreground=color_text_light, background=color_blue)
        self.style.map('Neutral.TButton', background=[('active', color_blue_active)])
        self.style.configure("SelectAll.TButton", font=("Arial", 10, "bold"), background=color_blue, foreground=color_text_light)
        self.style.map("SelectAll.TButton", background=[('active', color_blue_active)])
        self.style.configure("Treeview", rowheight=28, background=treeview_bg, fieldbackground=treeview_bg, foreground=treeview_fg, font=font_treeview_bold)
        self.style.map("Treeview", background=[('!selected', treeview_bg)], foreground=[('!selected', treeview_fg)])
        self.style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), padding=(10, 8), background=color_bg_frame)
        self.style.map("Treeview.Heading", background=[('active', color_bg_light)])
        self.style.configure('Status.TLabel', font=("Arial", 10), padding=5, background=color_bg_frame, relief=tk.SUNKEN)

    def create_widgets(self):
        input_frame = ttk.Frame(self.master, padding=(20, 10, 20, 10))
        input_frame.pack(pady=10, padx=20, fill='x')
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Estensione/Tipo File:", style='Title.TLabel').grid(row=0, column=0, sticky='w')
        self.ext_combobox = ttk.Combobox(input_frame, values=self.default_extensions, width=30)
        self.ext_combobox.grid(row=1, column=0, padx=5, pady=5)
        self.ext_combobox.set(DEFAULT_PLACEHOLDER)

        ttk.Label(input_frame, text="Testo nel nome:", style='Title.TLabel').grid(row=0, column=1, sticky='w')
        self.text_entry = ttk.Entry(input_frame)
        self.text_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')

        ttk.Label(input_frame, text="Percorsi di Ricerca:", style='Title.TLabel').grid(row=0, column=2, sticky='w')
        self.paths_entry = ttk.Entry(input_frame)
        self.paths_entry.grid(row=1, column=2, padx=5, pady=5, sticky='we')

        self.browse_btn = ttk.Button(input_frame, text="Sfoglia...", command=self.browse_paths, style='Neutral.TButton')
        self.browse_btn.grid(row=1, column=3, padx=5, pady=5)

        btn_frame = ttk.Frame(self.master)
        btn_frame.pack()
        ttk.Button(btn_frame, text="Cerca File", command=self.start_search, style='Success.TButton').pack(side='left', padx=5, pady=5)
        ttk.Button(btn_frame, text="Ferma", command=self.stop_search, style='Danger.TButton').pack(side='left', padx=5, pady=5)
        ttk.Button(btn_frame, text="Svuota", command=self.clear_fields, style='Warning.TButton').pack(side='left', padx=5, pady=5)

        ttk.Button(btn_frame, text="Sposta File", command=self.move_files_prompt, style='Neutral.TButton').pack(side='left', padx=5, pady=5)
        ttk.Button(btn_frame, text="Copia File", command=self.copy_files_prompt, style='Neutral.TButton').pack(side='left', padx=5, pady=5)


        self.tree = ttk.Treeview(self.master, columns=("check", "name", "path", "created", "modified"), show='headings', selectmode='none')
        for col, text, width in zip(("check", "name", "path", "created", "modified"), ("", "Nome", "Percorso", "Creato", "Modificato"), (40, 200, 500, 150, 150)):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.tree.bind('<Button-1>', self.on_treeview_click)

        self.status_var = tk.StringVar()
        self.status = ttk.Label(self.master, textvariable=self.status_var, style='Status.TLabel', anchor='w')
        self.status.pack(fill='x')
        self.status_var.set("Pronto.")

    def browse_paths(self):
        directory = filedialog.askdirectory()
        if directory:
            current = self.paths_entry.get()
            sep = ',' if current else ''
            self.paths_entry.insert(tk.END, sep + directory)

    def start_search(self):
        ext = self.ext_combobox.get()
        if ext == DEFAULT_PLACEHOLDER or ext == ALL_MARKER:
            ext = None
        elif ext in MARKER_TO_EXT:
            ext = MARKER_TO_EXT[ext]
        elif ext and not ext.startswith('.'):
            ext = '.' + ext

        text = self.text_entry.get().strip().lower()
        paths = [p.strip() for p in self.paths_entry.get().split(',') if os.path.isdir(p.strip())]
        if not paths:
            messagebox.showerror("Errore", "Inserisci almeno un percorso valido.")
            return

        self.ext_filter = ext
        self.text_filter = text
        self.valid_paths = paths
        self.file_info.clear()
        self.checked_items.clear()
        self.tree.delete(*self.tree.get_children())
        self.status_var.set("Ricerca in corso...")

        self.stop_event.clear()
        self.search_thread = Thread(target=self.search_files, daemon=True)
        self.search_thread.start()
        self.master.after(100, self.check_thread)

    def search_files(self):
        count = 0
        fmt = '%Y-%m-%d %H:%M:%S'
        for path in self.valid_paths:
            for root, _, files in os.walk(path):
                for name in files:
                    if self.stop_event.is_set(): return
                    if self.ext_filter and not name.lower().endswith(self.ext_filter):
                        continue
                    if self.text_filter and self.text_filter not in name.lower():
                        continue
                    fp = os.path.join(root, name)
                    try:
                        stat = os.stat(fp)
                        created = datetime.datetime.fromtimestamp(getattr(stat, 'st_birthtime', stat.st_ctime)).strftime(fmt)
                        modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime(fmt)
                    except:
                        created = modified = "?"
                    self.master.after(0, self.add_result, name, fp, created, modified)
                    count += 1
                    if count % 10 == 0:
                        self.master.after(0, lambda c=count: self.status_var.set(f"Trovati {c} file..."))
        self.master.after(0, lambda: self.status_var.set(f"Ricerca completata: {count} file trovati."))

    def add_result(self, name, path, created, modified):
        iid = self.tree.insert('', 'end', values=(CHECK_BOX_UNCHECKED, name, path, created, modified))
        self.checked_items[iid] = False

    def on_treeview_click(self, event):
        col = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)
        if col == '#1' and row:
            current = self.checked_items.get(row, False)
            self.checked_items[row] = not current
            vals = list(self.tree.item(row, 'values'))
            vals[0] = CHECK_BOX_CHECKED if not current else CHECK_BOX_UNCHECKED
            self.tree.item(row, values=vals)

    def stop_search(self):
        self.stop_event.set()
        self.status_var.set("Ricerca interrotta dall'utente.")

    def clear_fields(self):
        self.ext_combobox.set(DEFAULT_PLACEHOLDER)
        self.text_entry.delete(0, tk.END)
        self.paths_entry.delete(0, tk.END)
        self.tree.delete(*self.tree.get_children())
        self.status_var.set("Campi puliti. Pronto.")

    def check_thread(self):
        if self.search_thread and self.search_thread.is_alive():
            self.master.after(100, self.check_thread)


    def move_files_prompt(self):
        dest = filedialog.askdirectory(title="Seleziona cartella di destinazione")
        if dest:
            self.move_or_copy_files(dest, move=True)

    def copy_files_prompt(self):
        dest = filedialog.askdirectory(title="Seleziona cartella di destinazione")
        if dest:
            self.move_or_copy_files(dest, move=False)

    def move_or_copy_files(self, destination, move=True):
        action = "Spostati" if move else "Copiati"
        try:
            for iid, checked in self.checked_items.items():
                if not checked:
                    continue
                vals = self.tree.item(iid, 'values')
                src_path = vals[2]
                if not os.path.isfile(src_path):
                    continue
                file_name = os.path.basename(src_path)
                dest_path = os.path.join(destination, file_name)
                if move:
                    os.rename(src_path, dest_path)
                else:
                    import shutil
                    shutil.copy2(src_path, dest_path)
            self.status_var.set(f"File {action} in {destination}")
            messagebox.showinfo("Operazione completata", f"File {action} con successo.")
        except Exception as e:
            self.status_var.set("Errore durante l'operazione.")
            logger.error("Errore nel copiare/spostare file", exc_info=True)
            messagebox.showerror("Errore", str(e))


if __name__ == '__main__':
    root = tk.Tk()
    app = FileSearcherGUI(root)
    root.mainloop()
