import subprocess
import keyboard
import time
import os

def open_image(image_path):
    try:

        os.environ["DISPLAY"] = ":0"
        # print("Current DISPLAY:", os.environ["DISPLAY"])
        # os.system("echo $DISPLAY")

        kb = keyboard.Keyboard()
        subprocess.Popen(["eog", image_path]) 
        time.sleep(0.5)
        kb.pressKey_f11()
        
        os.environ["DISPLAY"] = ":1"
        # os.system("echo $DISPLAY")
        # print("Current DISPLAY:", os.environ["DISPLAY"])

    except FileNotFoundError:
        print("Image viewer not found! Please install 'eog' or a similar viewer.")
    except Exception as e:
        print(f"Failed to open the image: {e}")

# Example usage
# open_image("/home/ronak/Desktop/project-code/src/static/initial-image.png")
