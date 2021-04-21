# this program is just to create an MCVE and to test the detection code. It's not an actual program.
import threading, time
from pynput.keyboard import KeyCode, Listener, Key
from pynput.mouse import Button, Controller

delay = 0.2
button = Button.left
start_stop_key = Key.f8
exit_key = KeyCode(char='e')

held = 0  # declared a global. I know using globals is not a good practice. and this is just an MCVE

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.daemon = True
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        print('about to run')
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.2)


mouse = Controller()
click_thread = ClickMouse(delay, button)
print('thread created')
click_thread.start()
print('\nthread started')


def on_press(key):
    global held
    print('Key: ', key, ' was held')
    if key == start_stop_key:
        held = 1
        if click_thread.running:
            print('already clicking')
            pass
        else:
            print('starting clicks')
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


def on_release(key):
    global held
    print('Key: ', key, ' was released')
    if key == start_stop_key:
        if held:
            print('key released. stopping')
            click_thread.stop_clicking()


with Listener(on_press=on_press, on_release=on_release) as listener:
    print('listener starts')
    listener.join()
