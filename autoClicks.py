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
from random import randint
from platform import system
from webbrowser import open as web_open
from typing import Tuple
import tooltiptk1 as tttk

# ============================================================== #
# Declarations                                                   #
# ============================================================== #


URL = 'https://www.speedautoclicker.net/'
listener, held = None, 0

# ============================================================== #


class GUI:
    def __init__(self, root: tk.Tk):
        """
        renders UI elements, Starts workers and manages UI updates
        :param root: The parent window name
        :return: You know this already, don't you? of course it's None :D
        """
        with shl.open(os.path.join('data', 'config')) as cnfig:
            print('init: ', dict(cnfig))

        self.root = root
        self.root.title('SpeedAutoClicker')
        self.root.geometry('940x350+10+10')
        self.root.resizable(0, 0)
        self.root.config(bg='#1b2029')

        # variable declarations
        self.hotkey, self.cps, self.mode, self.limited, self.limit, self.vary, self.unlimited, self.key = get_config()

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
        self.frame2.pack(side=tk.LEFT, anchor=tk.NW)

        # adding child frames
        self.f1.pack(side=tk.TOP, anchor=tk.NW)
        self.f2.pack(side=tk.TOP, anchor=tk.NW, pady=2)
        self.f3.pack(side=tk.TOP, anchor=tk.NW)
        self.f4.pack(side=tk.TOP, anchor=tk.NW, pady=2)
        self.f5.pack(side=tk.TOP, anchor=tk.NW)
        self.f6.pack(side=tk.TOP, anchor=tk.NW, pady=2)
        self.ff1.pack(side=tk.TOP, anchor=tk.NW)
        self.ff2.pack(side=tk.TOP, anchor=tk.NW, padx=3)
        self.ff3.pack(side=tk.TOP, anchor=tk.NW, padx=3)
        self.ff4.pack(side=tk.TOP, anchor=tk.NW, padx=3)

        # widgets in frame1
        tk.Label(self.ff1, image=img, borderwidth=0, bg='#1b2029').pack(side=tk.TOP)

        clickImgLabel = tk.Label(self.ff2, image=clickImg, borderwidth=0, bg='#1b2029')
        clickImgLabel.pack(side=tk.LEFT, anchor=tk.NW)

        self.clickImgLabel2 = tk.Label(self.ff2, text='Auto Clicker                   ', bg='#1b2029', fg='#fff',
                                       borderwidth=0, font=('roboto', 15))
        self.clickImgLabel2.pack(side=tk.LEFT, anchor=tk.NE, padx=2)

        updateLabel = tk.Label(self.ff3, image=updateImg, borderwidth=0, bg='#1b2029')
        updateLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5)

        self.updateLabel2 = tk.Label(self.ff3, text='Updates                        ', borderwidth=0, bg='#1b2029',
                                     fg='#fff', font=('roboto', 15))
        self.updateLabel2.pack(side=tk.LEFT, anchor=tk.NW, pady=10)

        resetLabel = tk.Label(self.ff4, image=resetImg, borderwidth=0, bg='#1b2029')
        resetLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5)

        self.resetLabel2 = tk.Label(self.ff4, text='Reset All                       ', borderwidth=0,
                                    bg='#1b2029', fg='#fff', font=('roboto', 15))
        self.resetLabel2.pack(side=tk.LEFT, anchor=tk.NW, pady=3)

        # widgets in frame2
        # widgets in f1 - first row
        keyName = self.hotkey.name if isinstance(self.hotkey, Key) else self.hotkey
        self.hotkeyButton = tk.Button(self.f1, text=keyName, bg='#193b65', state=tk.DISABLED,
                                      width=35, font=('roboto', 10), fg='#fff', borderwidth=0)
        self.hotkeyButton.pack(side=tk.LEFT, anchor=tk.NW, padx=10, ipady=7, pady=10)
        self.hotkeyButton.config(disabledforeground='#fff')

        self.chooseKeyButton = tk.Button(self.f1, text='Choose Button', bg='#184a42', fg='#fff', font=('roboto', 10),
                                         width=20, borderwidth=0, command=self.choose_different_hotkey)
        self.chooseKeyButton.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=7)

        self.saveConfigButton = tk.Button(self.f1, text='Save Config', bg='#184a42', fg='#fff', font=('roboto', 10),
                                          width=25, borderwidth=0, command=self.save_all)
        self.saveConfigButton.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=7, padx=10, ipadx=2)

        # widgets in f2 - second row
        tk.Label(self.f2, text='Mouse Click Type', bg='#242d3c', fg='#fff',
                 font=('roboto', 10)).pack(side=tk.LEFT, anchor=tk.NW, pady=10, padx=10, ipady=4)

        self.left = tk.Button(self.f2, text='Left', bg='#184a42', fg='#fff', font=('roboto', 10),
                              width=20, borderwidth=0, command=lambda *args: self.click_type_changed('left'))
        self.left.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=7)

        self.middle = tk.Button(self.f2, text='Middle', bg='#184a42', fg='#fff', font=('roboto', 10),
                                width=20, borderwidth=0, command=lambda *args: self.click_type_changed('middle'))
        self.middle.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=7, padx=9)

        self.right = tk.Button(self.f2, text='Right', bg='#184a42', fg='#fff', font=('roboto', 10),
                               width=20, borderwidth=0, command=lambda *args: self.click_type_changed('right'))
        self.right.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=7)
        # just a filler
        tk.Label(self.f2, text='    ', bg='#242d3c').pack(side=tk.LEFT, pady=10)

        getattr(self, self.key).config(bg='#337362')

        # widgets in f3 - third row
        tk.Label(self.f3, text='Activation Mode' + ' ' * 44, bg='#242d3c', fg='#fff',
                 font=('roboto', 10)).pack(side=tk.LEFT, anchor=tk.NW, pady=10, padx=10, ipady=4)

        self.hold = tk.Button(self.f3, text='Hold', bg='#184a42', fg='#fff', font=('roboto', 10),
                              width=20, borderwidth=0, command=lambda *args: self.activation_mode_changed('hold'))
        self.hold.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=7, padx=10)

        self.switch = tk.Button(self.f3, text='Switch', bg='#184a42', fg='#fff', font=('roboto', 10),
                                width=20, borderwidth=0, command=lambda *args: self.activation_mode_changed('switch'))
        self.switch.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=7)
        # just a filler
        tk.Label(self.f3, text='    ', bg='#242d3c').pack(side=tk.LEFT, pady=10)

        getattr(self, self.mode).config(bg='#337362')

        # widgets in f4 - row 4
        tk.Label(self.f4, text='Click Rate' + ' ' * 25, bg='#242d3c', fg='#fff',
                 font=('roboto', 10)).pack(side=tk.LEFT, anchor=tk.NW, pady=10, padx=10, ipady=4)

        temp, temp2, temp3, temp4, temp5 = self.vary, self.limited, self.unlimited, self.cps, self.limit
        self.vary, self.limited, self.unlimited = tk.IntVar(self.root), tk.IntVar(self.root), tk.IntVar(self.root)
        self.limit, self.cps = tk.IntVar(self.root), tk.IntVar(self.root)

        self.vary.set(temp)
        self.unlimited.set(temp3)
        self.limited.set(temp2)
        self.limit.set(temp5)

        st = ttk.Style(self.root)  # style for Checkbutton
        st.configure('White.TCheckbutton', foreground='#fff', background='#242d3c', font=('roboto', 10))

        self.LoL = ttk.Checkbutton(self.f4, command=lambda *args: self.click_rate_changed('vary'),
                                   text='Variation (Anti-Detection)', style='White.TCheckbutton', variable=self.vary)
        self.LoL.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=5)

        self.LoL2 = ttk.Checkbutton(self.f4, command=lambda *args: self.click_rate_changed('unlimited'),
                                    text='Unlimited' + ' ' * 9, style='White.TCheckbutton', variable=self.unlimited)
        self.LoL2.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=5, padx=5)

        self.val_cmd, self.cps_val = self.LoL.register(self.validate_entries), float(1 / int(temp4))

        self.cps = tk.Entry(self.f4, font=('roboto', 10), bg='#193b65', fg='#fff', bd=0, disabledbackground='#1e3553',
                            justify=tk.CENTER, width=23, insertbackground='#fff', validate='key',
                            validatecommand=(self.val_cmd, '%W', '%P'))
        self.cps.pack(side=tk.LEFT, anchor=tk.NW, pady=10, padx=5, ipady=7)
        self.cps.insert(0, str(temp4))

        # widgets in f5 - row 5
        tk.Label(self.f5, text='Click Limitation' + ' ' * 60, bg='#242d3c', fg='#fff',
                 font=('roboto', 10)).pack(side=tk.LEFT, anchor=tk.NW, pady=10, padx=10, ipady=4)

        self.LoL3 = ttk.Checkbutton(self.f5, text='Active' + ' ' * 14, command=lambda *args: self.click_limit_changed(
            'limited'), style='White.TCheckbutton', variable=self.limited)
        self.LoL3.pack(side=tk.LEFT, anchor=tk.NW, pady=10, ipady=5, padx=5)

        self.limit = tk.Entry(self.f5, font=('roboto', 10), bg='#193b65', fg='#fff', bd=0, disabledbackground='#1e3553',
                              justify=tk.CENTER, width=22, insertbackground='#fff', validate='key',
                              validatecommand=(self.val_cmd, '%W', '%P'))

        self.limit.pack(side=tk.LEFT, anchor=tk.NW, pady=10, padx=5, ipady=7, ipadx=2)
        self.limit.insert(0, str(temp5))

        if not self.limited.get():
            self.limit.config(state=tk.DISABLED)

        # widgets in f6 - row 6
        tk.Label(self.f6, text=' ' * 88 + 'Currently' + ' ' * 12, bg='#242d3c', fg='#fff',
                 font=('roboto', 10)).pack(side=tk.LEFT, anchor=tk.NW, pady=10, padx=10, ipady=4)

        self.counter = tk.IntVar()
        self.counter.set(0)

        tk.Entry(self.f6, width=23, bd=0, bg='#1e3553', fg='#fff', font=('roboto', 10), disabledbackground='#1e3553',
                 textvariable=self.counter, state=tk.DISABLED,
                 justify=tk.CENTER).pack(side=tk.LEFT, anchor=tk.NW, ipady=8, pady=10, padx=10, ipadx=1)

        # binding events to menu items - frame1 children
        self.clickImgLabel2.bind('<Enter>', lambda *args: self.change_colors('clickImgLabel2'))
        self.updateLabel2.bind('<Enter>', lambda *args: self.change_colors('updateLabel2'))
        self.resetLabel2.bind('<Enter>', lambda *args: self.change_colors('resetLabel2'))
        self.clickImgLabel2.bind('<Leave>', lambda *args: self.reset_colors('clickImgLabel2'))
        self.updateLabel2.bind('<Leave>', lambda *args: self.reset_colors('updateLabel2'))
        self.resetLabel2.bind('<Leave>', lambda *args: self.reset_colors('resetLabel2'))
        self.ff2.bind('<Button-1>', lambda *args: web_open(URL))
        self.ff3.bind('<Button-1>', lambda *args: web_open(URL))
        self.ff4.bind('<Button-1>', self.reset_prefs)
        self.ff2.bind('<Enter>', lambda *args: self.change_colors('ff2'))
        self.ff3.bind('<Enter>', lambda *args: self.change_colors('ff3'))
        self.ff4.bind('<Enter>', lambda *args: self.change_colors('ff4'))
        self.ff2.bind('<Leave>', lambda *args: self.reset_colors('ff2'))
        self.ff3.bind('<Leave>', lambda *args: self.reset_colors('ff3'))
        self.ff4.bind('<Leave>', lambda *args: self.reset_colors('ff4'))

        self.cps.bind('<FocusOut>', lambda *args: self.save_all())
        self.limit.bind('<FocusOut>', lambda *args: self.save_all())

        for label in [clickImgLabel, self.clickImgLabel2, updateLabel, self.updateLabel2]:
            label.bind('<Button-1>', lambda *args: web_open(URL))

        for label in [self.resetLabel2, resetLabel]:
            label.bind('<Button-1>', self.reset_prefs)

        # binding events to control panel elements - frame2 children
        self.chooseKeyButton.bind('<Enter>', lambda *args: self.change_colors('chooseKeyButton'))
        self.saveConfigButton.bind('<Enter>', lambda *args: self.change_colors('saveConfigButton'))
        self.chooseKeyButton.bind('<Leave>', lambda *args: self.reset_colors('chooseKeyButton'))
        self.saveConfigButton.bind('<Leave>', lambda *args: self.reset_colors('saveConfigButton'))

        # adding Tool tip
        tttk.CreateToolTip(self.hotkeyButton, 'Press this key to start clicking.\nPress again to stop')

        # setting focus to primary parent window
        self.root.focus_set()

    def change_colors(self, widgetID: str):
        """
        Change colors on hover or click events
        :param widgetID: The widget name - as the attribute name string...
        :return: None
        """
        if widgetID in ['clickImgLabel2', 'updateLabel2', 'resetLabel2', 'ff2', 'ff3', 'ff4']:
            getattr(self, widgetID).config(bg='#000')
            for child in getattr(self, widgetID).winfo_children():
                child.config(bg='#000')

        if widgetID in ['chooseKeyButton', 'saveConfigButton']:
            getattr(self, widgetID).config(bg='#337362')

    def reset_colors(self, widgetID: str):
        """
        revert colors back to original states on hover or click event termination
        :param widgetID: The widget name - as the attribute name string...
        :return: None
        """
        if widgetID in ['clickImgLabel2', 'updateLabel2', 'resetLabel2', 'ff2', 'ff3', 'ff4']:
            getattr(self, widgetID).config(bg='#1b2029')
            for child in getattr(self, widgetID).winfo_children():
                child.config(bg='#1b2029')

        if widgetID in ['chooseKeyButton', 'saveConfigButton']:
            getattr(self, widgetID).config(bg='#184a42')

    @staticmethod
    def reset_prefs(*args):
        """
        resets preferences back to the default configuration.
        :param args: Just a filler to handle the event passed in by tcl on _button_press event
        :return: You know this already, don't you? of course it's None :D
        """
        print('reset called manually')
        init_default_config(nt=1)

    def choose_different_hotkey(self):
        """
        Allows the user to select a different hotkey to start/stop the clicker.
        :return: why would you even look for a return value in such method? like, come on!
        """
        def cancel_choose_hotkey():
            """
            executes when user cancels the selection of a new hotkey
            :return: Why the flip would it return anything 👀 ?
            """
            global listener
            keyName = self.hotkey.name if isinstance(self.hotkey, Key) else self.hotkey
            self.chooseKeyButton.config(text='Choose Button', command=self.choose_different_hotkey)
            self.hotkeyButton.config(text=keyName)
            listener.stop()
            th.Thread(target=worker, args=(self, clickThread,), daemon=True).start()
            return

        def look_for_hotkey():
            def detect_key(k):
                self.hotkey = k
                self.save_all()
                keyName = self.hotkey.name if isinstance(self.hotkey, Key) else self.hotkey
                self.chooseKeyButton.config(text='Choose Button', command=self.choose_different_hotkey)
                self.hotkeyButton.config(text=keyName)
                return False

            global listener
            listener.stop()
            with Listener(on_press=detect_key) as listener:
                listener.join()

            th.Thread(target=worker, args=(self, clickThread,), daemon=True).start()

        self.chooseKeyButton.config(text='Cancel Choose', command=cancel_choose_hotkey)
        self.hotkeyButton.config(text='Press Button')
        hotKeyThread = th.Thread(target=look_for_hotkey)
        hotKeyThread.daemon = True
        hotKeyThread.start()

    def choose_apps(self):
        """
        Let's the user select application to be affected by clicker action
        :return: None again LoL
        """
        pass

    def click_type_changed(self, clickType: str):
        """
        Applies the changes when a click type (what mouse button) change is detected. Saves the prefs.
        :param clickType: Name of new button selected.
        :return: None
        """
        for button in ['left', 'middle', 'right']:
            if button == clickType:
                getattr(self, button).config(bg='#337362')
            else:
                getattr(self, button).config(bg='#184a42')

        self.key = clickType
        self.save_all()
        pass

    def activation_mode_changed(self, mode: str):
        """
        Applies changes when an activation mode change is detected. Saves the prefs.
        :param mode: The new mode selected
        :return: None
        """
        global listener

        hotkey, cps, mode_s, limited, limit, vary, unlimited, key = get_config()

        self.mode = mode
        self.save_all()

        for button in ['hold', 'switch']:
            if button == mode:
                getattr(self, button).config(bg='#337362')
            else:
                getattr(self, button).config(bg='#184a42')

        self.mode = mode

        if mode != mode_s:
            if mode == 'hold':
                listener.stop()
                th.Thread(target=hold_worker, daemon=True).start()

            elif mode == 'switch':
                listener.stop()
                th.Thread(target=worker, args=(self, clickThread,), daemon=True).start()

        elif mode == mode_s:
            pass

    def click_rate_changed(self, rate: str):
        """
        Applies changes to the click rate when detected. Saves prefs too.
        :param rate: The new rate selected.
        :return: Of course it's None.
        """
        self.save_all()
        hotkey, cps, mode, limited, limit, vary, unlimited, key = get_config()

        if vary:
            self.LoL2.config(state=tk.DISABLED)
            self.cps.config(state=tk.DISABLED)
        elif unlimited:
            self.LoL.config(state=tk.DISABLED)
            self.cps.config(state=tk.DISABLED)
        else:
            self.LoL.config(state=tk.NORMAL)
            self.LoL2.config(state=tk.NORMAL)
            self.cps.config(state=tk.NORMAL)

    @staticmethod
    def validate_entries(name: str, value: str):
        try:
            value = int(value)
            return True
        except ValueError:
            return False

    def save_all(self):
        with shl.open(os.path.join('data', 'config')) as config:
            print('config already: ', dict(config))

            config['user'] = {'hotkey': self.hotkey,
                              'key': self.key,
                              'cps': int(self.cps.get()),
                              'mode': self.mode,
                              'limited':int( self.limited.get()),
                              'limit': int(self.limit.get()),
                              'vary': int(self.vary.get()),
                              'unlimited': int(self.unlimited.get())}

            print('config after changed: ', dict(config))

    def click_limit_changed(self, newLimit: str):
        self.save_all()
        hotkey, cps, mode, limited, limit, vary, unlimited, key = get_config()

        if limited:
            self.limit.config(state=tk.NORMAL)
        elif not limited:
            self.limit.config(state=tk.DISABLED)


# ============================================================== #


class MouseClicks(th.Thread):
    def __init__(self, theGUI: GUI, mouse: Controller):
        super(MouseClicks, self).__init__()
        # theGUI.cps_val = float(1 / int(theGUI.cps.get()))
        self.running = False
        self.mouse = mouse
        self.daemon = True

    def start_clicks(self):
        self.running = True

    def stop_clicks(self):
        self.running = False

    def run(self):
        global gui
        while 1:
            while self.running:
                # logging.warn('clicking left now')
                hotkey, cps, mode, limited, limit, vary, unlimited, key = get_config()

                if vary:
                    # varying CPS
                    print('varying cps applied')
                    cps_s = randint(5, 200)
                    self.mouse.click(getattr(Button, key))
                    time.sleep(float(1 / cps_s))
                    gui.counter.set(gui.counter.get() + 1)

                    if limited:
                        # there is a limit
                        print('limited. varying')
                        if gui.counter.get() >= int(limit):  # Limit Reached
                            print('limited. varying. gotta stop')
                            self.stop_clicks()

                    continue

                elif unlimited:
                    # Unlimited CPS.
                    print('unlimited cps detected')
                    self.mouse.click(getattr(Button, gui.key))
                    gui.counter.set(gui.counter.get() + 1)

                    if limited:
                        # There is a limit
                        if gui.counter.get() >= int(limit):  # limit reached
                            print('unlimited. gotta stop')
                            self.stop_clicks()

                    continue

                # Normal clicks
                self.mouse.click(getattr(Button, key))
                print('normal clicks')
                time.sleep(float(1 / int(cps)))
                gui.counter.set(gui.counter.get() + 1)

                if limited:
                    if gui.counter.get() >= int(limit):
                        print('normal clicks. gotta stop')
                        self.stop_clicks()

            time.sleep(0.5)

# ============================================================== #


def key_pressed(key, listen: Listener, theGUI: GUI, clickTh: MouseClicks):
    if key == theGUI.hotkey:
        if clickTh.running:
            clickTh.stop_clicks()
        elif not clickTh.running:
            clickTh.start_clicks()
    else:
        print('no hotkey. pressed: ', key)

# ============================================================== #


def worker(theGUI, clickTh):
    print('worker starts')
    global listener
    with Listener(on_press=lambda event: key_pressed(event, listener, theGUI, clickTh)) as listener:
        listener.join()


# ============================================================== #


def key_held(key):
    global held, clickThread, gui

    if key == gui.hotkey:
        held = 1
        if clickThread.running:
            print('already clicking')
            pass
        else:
            print('starting clicks')
            clickThread.start_clicks()


# ============================================================== #


def key_released(key):
    global held, clickThread, gui

    if key == gui.hotkey:
        if held:
            print('key released. stopping')
            clickThread.stop_clicks()


# ============================================================== #


def hold_worker():
    print('hold worker starts')
    global listener
    with Listener(on_press=key_held, on_release=key_released) as listener:
        listener.join()

# ============================================================== #


def set_icon(window: tk.Tk) -> None:
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
        with shl.open(os.path.join('data', 'config')) as config:
            config['user'] = defaultConfig
        return

    with shl.open(os.path.join('data', 'config')) as config:
        config['default'] = defaultConfig
        config['user'] = defaultConfig


# ============================================================== #


def get_config() -> Tuple[Key, int, str, int, int, int, int, str]:
    """
    a helper function to get the saved preferences whenever needed - reusable component.
    :returns: Tuple: an 8-tuple describing the preferences.
    """
    with shl.open(os.path.join('data', 'config')) as config:
        data = config['user']

    return data['hotkey'], data['cps'], data['mode'], data['limited'], data['limit'], data['vary'], \
           data['unlimited'], data['key']


# ============================================================== #


defaultConfig = {'hotkey': Key.f7,
                 'key': 'left',
                 'cps': 200,
                 'mode': 'switch',
                 'limited': 0,
                 'limit': 500,
                 'vary': 0,
                 'unlimited': 0}


# ============================================================== #


if __name__ == '__main__':
    # # print(get_config())
    # if not os.path.exists('\data\\nft.bat'):
    #     init_default_config()
    #     try:
    #         os.mkdir('data')
    #         with open('nft.bat', 'w') as file:
    #             pass
    #     except OSError:
    #         pass

    win = tk.Tk()
    set_icon(win)
    img = ImageTk.PhotoImage(Image.open('imgs\img.png'))
    clickImg = ImageTk.PhotoImage(Image.open('imgs\clicks.png'))
    updateImg = ImageTk.PhotoImage(Image.open('imgs\\update.png'))
    resetImg = ImageTk.PhotoImage(Image.open('imgs\\reset.png'))
    gui = GUI(win)
    mouseControl = Controller()
    clickThread = MouseClicks(gui, mouseControl)
    clickThread.start()
    workerThread = th.Thread(target=worker, args=(gui, clickThread,))
    workerThread.daemon = True
    workerThread.start()
    win.mainloop()

# ============================================================== #
