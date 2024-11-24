import pynput
# from pynput.keyboard import Key, Listener, Controller
from threading import Thread

from logger_config import log_function_calls
from logger_config import setup_logger

setup_logger()

global terminate
terminate = False

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()

@log_function_calls()
def on_press(key):
    #print('{0} pressed'.format(
        #key))
    check_key(key)

@log_function_calls()
def on_release(key):
    #print('{0} release'.format(
       # key))
    if key == pynput.keyboard.Key.esc:
        # Stop listener
        return False

@log_function_calls()
def check_key(key):
    if key == pynput.keyboard.Key.ctrl:
        terminate = True

@log_function_calls()
def listen():
    # Collect events until released
    with pynput.keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

@log_function_calls()
def pressKey_f11():
    keyboard.press(pynput.keyboard.Key.f11)

@log_function_calls()
def pressKey_esc():
    keyboard.press(pynput.keyboard.Key.esc)

@log_function_calls()
def scroll(x, y):
    mouse.scroll(x, y)

@log_function_calls()
def left_click():
    mouse.click(pynput.mouse.Button.left)


thread = Thread(target=listen)
