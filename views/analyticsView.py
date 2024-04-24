import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import os
import sys

currentDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(currentDirectory)
sys.path.append(parentDirectory)

from controllers import controller

busiestTargetDate = "2024-08-10" # mock variable (YYYY-DD-MM)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automated Congestion Pricing by CSGO")
        self.attributes("-fullscreen", True)

        ax, canvas = controller.generateReport(master=self, targetDate=busiestTargetDate)
    
    def updateGraph(self, ax, canvas):
        ax.clear()

        ax, canvas = controller.generateReport(master=self, targetDate=busiestTargetDate)

        canvas.draw()

    def updateAndRepeat(self, ax, canvas):
        self.updateGraph(ax, canvas)

        self.after(3600000, self.updateAndRepeat, ax, canvas)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
