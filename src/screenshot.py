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

def getScreenshots(MAX_ELAPSED_TIME=60):
    # get size of screen
    monitor = get_monitors()[0]
    width = monitor.width
    height = monitor.height
    print(f"Screen resolution: {width}x{height}")
    def scroll(height):
        pyautogui.scroll(height)


    file_path = "./screenshot.py"
    os.system(f'code {file_path}')
    start_time = time.time()


    def image_to_bytes(image):
        return list(image.getdata())

    count = 1
    prev_screenshot = None
    while time.time() - start_time < MAX_ELAPSED_TIME:
        print(count)
        # fail safe, stops program if control key is pressed 
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
        time.sleep(0.1)
