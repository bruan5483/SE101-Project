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

static_dir_path = os.getenv("STATIC_DIR_PATH")

def getScreenshots(code_file_path, images_dir_path, MAX_ELAPSED_TIME=300):
    
    
    # get size of screen

    # def scroll(height):
    #     pyautogui.scroll(height)

    # os.environ["DISPLAY"] = DISPLAY
    # * Enable on prod
    # os.system("sudo pkill code")
    os.system(f"code {code_file_path}")

    kb = keyboard.Keyboard()
    time.sleep(10)
    kb.left_click()

    def image_to_bytes(image):
        return list(image.getdata())

    count = 0
    prev_screenshot = None
    first = True

    # while time.time() - start_time < MAX_ELAPSED_TIME:
    while True:
        print(count)
        if (kb.terminate):
            break

        # take screenshot 
        screenshot = ImageGrab.grab(bbox =(0, 0, WIDTH, HEIGHT))
        
        # if the two screenshots are the same that means we've reached the end of our scrollable area 
        if count > 0 and image_to_bytes(screenshot) == prev_screenshot:
            break

        prev_screenshot = image_to_bytes(screenshot)
        img_path = os.path.join(images_dir_path, f"pic_{count}.png")
        static_img_path = os.path.join(static_dir_path, f"codeImages_pic_{count}.png")
        
        time.sleep(5.3)
        # if not first:
        screenshot.save(img_path)
        screenshot.save(static_img_path)
        # else:
        #     first = False
        kb.scroll(0, -13)
        # time.sleep(2)
        # pyautogui.scroll(5)
        count += 1
    print("done")


# below is an example call of the function
# getScreenshots("/home/ronak/Desktop/project-code/utils/files/app.py", "/home/ronak/Desktop/project-code/utils/codeImages/")