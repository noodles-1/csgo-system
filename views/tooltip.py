import os
import sys
import tkinter as tk

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current)
sys.path.append(parent_dir)

from customtkinter import *
from tkinter import ttk
from PIL import Image

class ToolTip:
    def __init__(self, widget, text, bg="white", fg="black"):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip or not self.text:
            return
        
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background=self.bg, foreground=self.fg, relief='solid', borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None