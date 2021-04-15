# ============================================================== #
import os
import threading as th, time
import tkinter as tk
import tkinter.ttk as ttk
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key, HotKey
import shelve as shl
from PIL import ImageTk, Image
import tkinter.messagebox as msg
import tooltiptk as ttt
from platform import system
from webbrowser import open as web_open

# ============================================================== #
# Declarations                                                   #
# ============================================================== #


URL = 'https://www.speedautoclicker.net/'


# ============================================================== #


class GUI:
    def __init__(self, root):
        """
        render UI elements. Start workers and manage UI updates
        :param root: The parent window name
        """
        self.root = root
        self.root.title('SpeedAutoClicker')
        self.root.geometry('950x350+180+100')
        self.root.resizable(0, 0)
        self.root.config(bg='#1b2029')

        # main frames
        self.frame1 = tk.Frame(self.root, bg='#1b2029')
        self.frame2 = tk.Frame(self.root, bg='#1b2029')

        # child frames inside frame1
        self.ff1 = tk.Frame(self.frame1, bg='#1b2029')
        self.ff2 = tk.Frame(self.frame1, bg='#1b2029')
        self.ff3 = tk.Frame(self.frame1, bg='#1b2029')
        self.ff4 = tk.Frame(self.frame1, bg='#1b2029')

        # child frames inside frame2
        self.f1 = tk.Frame(self.frame2, bg='#242d3c')
        self.f2 = tk.Frame(self.frame2, bg='#242d3c')
        self.f3 = tk.Frame(self.frame2, bg='#242d3c')
        self.f4 = tk.Frame(self.frame2, bg='#242d3c')
        self.f5 = tk.Frame(self.frame2, bg='#242d3c')
        self.f6 = tk.Frame(self.frame2, bg='#242d3c')

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
        self.ff1.pack(side=tk.TOP, anchor=tk.NW)
        self.ff2.pack(side=tk.TOP, anchor=tk.NW, padx=3)
        self.ff3.pack(side=tk.TOP, anchor=tk.NW, padx=3)
        self.ff4.pack(side=tk.TOP, anchor=tk.NW, padx=3)

        # widgets in frame1
        tk.Label(self.ff1, image=img, borderwidth=0, bg='#1b2029').pack(side=tk.TOP)

        clickImgLabel = tk.Label(self.ff2, image=clickImg, borderwidth=0, bg='#1b2029')
        clickImgLabel.pack(side=tk.LEFT, anchor=tk.NW)

        clickImgLabel2 = tk.Label(self.ff2, text='Auto Clicker', bg='#1b2029', fg='#fff',
                                  borderwidth=0, font=('roboto', 15))
        clickImgLabel2.pack(side=tk.LEFT, anchor=tk.NE, padx=2)

        updateLabel = tk.Label(self.ff3, image=updateImg, borderwidth=0, bg='#1b2029')
        updateLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5)

        updateLabel2 = tk.Label(self.ff3, text='Updates', borderwidth=0, bg='#1b2029', fg='#fff', font=('roboto', 15))
        updateLabel2.pack(side=tk.LEFT, anchor=tk.NW, pady=10)

        resetLabel = tk.Label(self.ff4, image=resetImg, borderwidth=0, bg='#1b2029')
        resetLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5)

        resetLabel2 = tk.Label(self.ff4, text='Reset All', borderwidth=0, bg='#1b2029', fg='#fff', font=('roboto', 15))
        resetLabel2.pack(side=tk.LEFT, anchor=tk.NW, pady=3)

        # binding events to frame1 children - menu items
        self.ff2.bind('<Button-1>', lambda *args: web_open(URL))
        self.ff3.bind('<Button-1>', lambda *args: web_open(URL))
        self.ff4.bind('<Button-1>', self.reset_prefs)

        for label in [clickImgLabel, clickImgLabel2, updateLabel, updateLabel2]:
            label.bind('<Button-1>', lambda *args: web_open(URL))

        for label in [resetLabel2, resetLabel]:
            label.bind('<Button-1>', self.reset_prefs)

        # setting focus to primary parent window
        self.root.focus_set()

    def change_colors(self, widgetID):
        if widgetID in ['ff2', 'ff3', 'ff4']:
            getattr(self, widgetID).config(bg='#1b1018')

    def reset_colors(self, widgetID):
        if widgetID in ['ff2', 'ff3', 'ff4']:
            getattr(self, widgetID).config(bg='#1b2029')

    def reset_prefs(self, *args):
        print('reset called manually')
        init_default_config(nt=1)


# ============================================================== #


def set_icon(window):
    """
    determines the platform OS and sets the icon file accordingly.
    exits if unable to determine
    :param window: The root window
    :return: None
    """
    if system() == 'Linux':
        window.iconbitmap('imgs\\logo.xbm')

    elif system() == 'Windows':
        window.iconbitmap('imgs\\logo.ico')

    elif system() == 'Darwin':
        window.iconbitmap('imgs\\logo.icons')

    else:
        msg.showerror('Could not determine the Platform OS',
                      'We were not able to determine your system OS.')
        os._exit(0)


# ============================================================== #


def init_default_config(**kwargs):
    """
    Sets the default configuration and writes it to system for persistence.
    Also runs when Reset All is used...
    :param kwargs: Optional keyWord arg to specify whenever called from within the UI manually.
    :return: None
    """
    if kwargs.get('nt'):
        with shl.open('data\\config') as config:
            config['user'] = defaultConfig
        return

    with shl.open('data\\config') as config:
        config['default'] = defaultConfig
        config['user'] = defaultConfig


# ============================================================== #


defaultConfig = {'hotkey': Key.f7,
                 'cps': 200,
                 'mode': 'switch',
                 'limited': 0,
                 'limit': 500,
                 'vary': 0,
                 'unlimited': 0}


# ============================================================== #


if __name__ == '__main__':
    if not os.path.exists('\data\\nft.bat'):
        init_default_config()
        try:
            os.mkdir('data')
            with open('nft.bat', 'w') as file:
                pass
        except OSError:
            pass

    win = tk.Tk()
    set_icon(win)
    img = ImageTk.PhotoImage(Image.open('imgs\img.png'))
    clickImg = ImageTk.PhotoImage(Image.open('imgs\clicks.png'))
    updateImg = ImageTk.PhotoImage(Image.open('imgs\\update.png'))
    resetImg = ImageTk.PhotoImage(Image.open('imgs\\reset.png'))
    gui = GUI(win)
    win.mainloop()

# ============================================================== #
