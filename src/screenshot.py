import os 
from dotenv import load_dotenv

load_dotenv()

DISPLAY = os.getenv('DISPLAY')
os.environ['DISPLAY'] = DISPLAY

from PIL import ImageGrab
import pyautogui
from screeninfo import get_monitors, Monitor
import keyboard
import time

from logger_config import log_function_calls
from logger_config import setup_logger

setup_logger()

"""
Dependencies:
- pip install pillow
- pip install pyautogui
- pip install screeninfo
- pip install keyboard
"""
WIDTH = 1024
HEIGHT = 768
X_POSITION = 10
Y_POSITION = 10

monitor = Monitor(
        x=X_POSITION,
        y=Y_POSITION,
        width=WIDTH,
        height=HEIGHT
    )

@log_function_calls()
def getScreenshots(code_file_path, images_dir_path, MAX_ELAPSED_TIME=300):
    # get size of screen

    # def scroll(height):
    #     pyautogui.scroll(height)

    os.system(f"export DISPLAY={DISPLAY}")
    # * Enable on prod
    # os.system("sudo pkill code")
    os.system(f"code {code_file_path}")


    time.sleep(10)
    keyboard.left_click()
    
    start_time = time.time()


    def image_to_bytes(image):
        return list(image.getdata())

    count = 0
    prev_screenshot = None


    # while time.time() - start_time < MAX_ELAPSED_TIME:
    while True:
        if (keyboard.terminate):
            break

        # take screenshot 
        screenshot = ImageGrab.grab(bbox =(0, 0, WIDTH, HEIGHT))
        
        # if the two screenshots are the same that means we've reached the end of our scrollable area 
        if count > 0 and image_to_bytes(screenshot) == prev_screenshot:
            break

        prev_screenshot = image_to_bytes(screenshot)
        img_path = os.path.join(images_dir_path, f"pic_{count}.png")
        
        time.sleep(5)
        screenshot.save(img_path)
        keyboard.scroll(0, -13)
        # time.sleep(2)
        # pyautogui.scroll(5)
        count += 1


# below is an example call of the function
# getScreenshots("/home/ronak/Desktop/project-code/utils/files/app.py", "/home/ronak/Desktop/project-code/utils/codeImages/")