import tkinter as tk
from tkinter import ttk
import textwrap

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title=None, message=None):
        super().__init__(parent)
        
        self.title(' ')
        self.resizable(False, False)
        self.configure(bg='white')

        self.style = ttk.Style()
        self.style.configure('CustomDialog.TFrame', background='white')
        self.style.configure('CustomDialog.TLabel', background='white')
        self.style.configure('CustomDialog.TButton', background='#2596be', foreground='white',font=("Arial", 10, "bold"), padding=2)
        self.style.configure('Title.TLabel', background='white', font=("Arial", 12, "bold"))

        self.frame = ttk.Frame(self, style='CustomDialog.TFrame')
        self.frame.pack(padx=10, pady=10)

        self.title_label = ttk.Label(self.frame, text=title, style='Title.TLabel')
        self.title_label.pack(padx=10, pady=10)

        message = textwrap.fill(message, 50)

        self.message = ttk.Label(self.frame, text=message, style='CustomDialog.TLabel')
        self.message.pack(padx=10, pady=10)

        self.button_frame = ttk.Frame(self.frame, style='CustomDialog.TFrame')
        self.button_frame.pack(pady=10)

        btn = ttk.Button(self.button_frame, text="OK", command=self.destroy, cursor="hand2", style='CustomDialog.TButton')
        btn.pack(side="left", padx=5)

        self.transient(parent)
        self.grab_set()
        self.wait_window(self)