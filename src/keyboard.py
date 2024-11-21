import pynput
# from pynput.keyboard import Key, Listener, Controller
from threading import Thread

global terminate
terminate = False

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()

def on_press(key):
    #print('{0} pressed'.format(
        #key))
    check_key(key)

def on_release(key):
    #print('{0} release'.format(
       # key))
    if key == pynput.keyboard.Key.esc:
        # Stop listener
        return False

def check_key(key):
    if key == pynput.keyboard.Key.ctrl:
        terminate = True

def listen():
    # Collect events until released
    with pynput.keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

def pressKey_f11():
    keyboard.press(pynput.keyboard.Key.f11)

def pressKey_esc():
    keyboard.press(pynput.keyboard.Key.esc)

def scroll(x, y):
    mouse.scroll(x, y)

def left_click():
    mouse.click(pynput.mouse.Button.left)


thread = Thread(target=listen)
