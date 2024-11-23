import subprocess
import keyboard
import time
import os

def open_image(image_path):
    try:
        subprocess.Popen(["eog", image_path]) 
        time.sleep(0.3)
        keyboard.pressKey_f11()
        print("full")
    except FileNotFoundError:
        print("Image viewer not found! Please install 'eog' or a similar viewer.")
    except Exception as e:
        print(f"Failed to open the image: {e}")

# Example usage
open_image("/home/ronak/Desktop/project-code/utils/codeImages/pic_2.png")
