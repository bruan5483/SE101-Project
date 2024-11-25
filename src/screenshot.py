import os 
from dotenv import load_dotenv

load_dotenv()

from PIL import ImageGrab
import pyautogui
from screeninfo import get_monitors, Monitor
import keyboard
import time
import buffer

# from logger_config import log_function_calls
# from logger_config import setup_logger

# setup_logger()

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

def getScreenshots(code_file_path, images_dir_path, buffer: buffer.Buffer, MAX_ELAPSED_TIME=300):
    
    buffer.appendRequest("open-vscode")
    # wait until we reach buffer
    while (not buffer.isNext("open-vscode")):
        time.sleep(0.1)

    os.environ["DISPLAY"] = ":1"
    

    # * Enable on prod
    # os.system("sudo pkill code")
    os.system(f"code {code_file_path}")

    kb = keyboard.pynputKeyboard()
    time.sleep(10)
    kb.left_click()

    buffer.completeEvent()

    def image_to_bytes(image):
        return list(image.getdata())

    count = 0
    prev_screenshot = None
    first = True

    # while time.time() - start_time < MAX_ELAPSED_TIME:
    while True:
        buffer.appendRequest("screenshot")
        # wait until we reach buffer
        while (not buffer.isNext("screenshot")):
            time.sleep(0.3)

        os.environ["DISPLAY"] = ":1"
        
        kb = keyboard.pynputKeyboard()

        #debug
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
        time.sleep(5.3)
        # else:
        #     first = False
        kb.scroll(0, -13)
        # time.sleep(2)
        # pyautogui.scroll(5)
        count += 1

        buffer.completeEvent()

    print("done")


# below is an example call of the function
# getScreenshots("/home/ronak/Desktop/project-code/utils/files/app.py", "/home/ronak/Desktop/project-code/utils/codeImages/")