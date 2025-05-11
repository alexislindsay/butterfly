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
import hashlib
import shutil
from PIL import Image, ImageTk
import tkinter.scrolledtext as st

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
    ".html", ".css", ".js", ".py", ".json", ".csv"
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
        self.style.configure('.', font=font_normal)

    def create_widgets(self):
        pass  # Placeholder to avoid error for this snippet

    def preview_file(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        path = self.tree.item(item, 'values')[2]
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            self.preview_image(path)
        elif ext == '.pdf':
            webbrowser.open(path)
        elif ext in ['.txt', '.json', '.md', '.py', '.csv']:
            self.preview_text_file(path)

    def preview_image(self, path):
        preview = tk.Toplevel(self.master)
        preview.title(f"Anteprima: {os.path.basename(path)}")
        canvas = tk.Canvas(preview)
        canvas.pack(fill='both', expand=True)
        scrollbar_y = ttk.Scrollbar(preview, orient='vertical', command=canvas.yview)
        scrollbar_y.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar_y.set)
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')
        img = Image.open(path)
        img.thumbnail((1600, 1600))
        tk_img = ImageTk.PhotoImage(img)
        label = tk.Label(frame, image=tk_img)
        label.image = tk_img
        label.pack()
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def preview_text_file(self, path):
        preview = tk.Toplevel(self.master)
        preview.title(f"Anteprima Testo: {os.path.basename(path)}")
        text_area = st.ScrolledText(preview, wrap='word', width=100, height=40)
        text_area.pack(fill='both', expand=True)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='latin1') as f:
                content = f.read()
        text_area.insert('1.0', content)
        text_area.config(state='disabled')

    def run(self):
        self.master.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = FileSearcherGUI(root)
    app.run()
