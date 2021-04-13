# ============================================================== #
import threading, time
import tkinter as tk
import tkinter.ttk as ttk
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import shelve as shl

# ============================================================== #
# Declarations                                                   #
# ============================================================== #


BASE = 'LoL'


# ============================================================== #


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('SpeedAutoClicker')
        self.root.geometry('950x380+20+20')
        self.root.resizable(0, 0)

        # main frames
        self.frame1 = ttk.Frame(self.root)
        self.frame2 = ttk.Frame(self.root)

        # child frames inside frame2
        self.f1 = ttk.Frame(self.frame2)
        self.f2 = ttk.Frame(self.frame2)
        self.f3 = ttk.Frame(self.frame2)
        self.f4 = ttk.Frame(self.frame2)
        self.f5 = ttk.Frame(self.frame2)
        self.f6 = ttk.Frame(self.frame2)

        # adding main frames
        self.frame1.pack(side=tk.LEFT, anchor=tk.NW)
        self.frame2.pack(side=tk.RIGHT, anchor=tk.NE)

        # adding child frames
        self.f1.pack(side=tk.TOP)
        self.f2.pack(side=tk.TOP)
        self.f3.pack(side=tk.TOP)
        self.f4.pack(side=tk.TOP)
        self.f5.pack(side=tk.TOP)
        self.f6.pack(side=tk.TOP)

        


# ============================================================== #


if __name__ == '__main__':
    GUI().root.mainloop()


# ============================================================== #
