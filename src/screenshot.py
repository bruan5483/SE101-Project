from PIL import ImageGrab
import pyautogui
from screeninfo import get_monitors
import keyboard
import time 
import os 

"""
Dependencies:
- pip install pillow
- pip install pyautogui
- pip install screeninfo
- pip install keyboard
"""

# file_path = "C:\\Users\\haris\\OneDrive\\Desktop\\SE101\\se101-f2024-triangles\\triangle.c"

# stops program if more 1 minute is taken 
MAX_ELAPSE_TIME = 60

# get size of screen
monitor = pyautogui.size()
width = monitor[0]
height = monitor[1]
print(f"Screen resolution: {width}x{height}")

def scroll(height):
    pyautogui.scroll(height)

def image_to_bytes(image):
    return list(image.getdata())

def screenshotCapture(file_path):
    os.system(f'code {file_path}')
    start_time = time.time()
    count = 1
    prev_screenshot = None
    time.sleep(5)
    while time.time() - start_time < MAX_ELAPSE_TIME:
        print(count)
        # fail safe, stops program if space bar is pressed 
        if keyboard.is_pressed('ctrl'):
            break

        # take screenshot 
        screenshot = ImageGrab.grab(bbox =(0.04 * width, 0.075 * height, 0.85 * width, 0.95 * height))
        # if the two screenshots are the same that means we've reached the end of our scrollable area 
        if image_to_bytes(screenshot) == prev_screenshot:
            print("stopped")
            break

        prev_screenshot = image_to_bytes(screenshot)
        img_path = f"..\\screenshots\\pic{count}.jpg"
        screenshot.save(img_path)
        scroll(-height)
        count += 1
        time.sleep(0.5)

# below is an example call of the function
# screenshotCapture("C:\\Users\\haris\\OneDrive\\Desktop\\SE101\\se101-f2024-triangles\\triangle.c")