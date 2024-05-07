import os
import sys
import tkinter as tk
from customtkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class AnalyticsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "pink")
        label = tk.Label(self, text = "This is the Analaytics Page", font = ('Helvetica', 14))
        label.pack(pady = 10, padx = 10)
        button = tk.Button(self, text = "Dashboard" , command = lambda: parent.show_frame(parent.dashboardFrame))
        button.pack()