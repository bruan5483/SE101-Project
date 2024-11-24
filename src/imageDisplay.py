import subprocess
import keyboard
import time
import os
import buffer

width = 1920
height = 1080

def open_image(image_path, buffer: buffer.Buffer):
    try:
        buffer.appendRequest("open-image")
        # wait until we reach buffer
        while (not buffer.isNext("open-image")):
            time.sleep(0.1)

        os.environ["DISPLAY"] = ":0"

        subprocess.Popen(["display", "-geometry", "1000x800+0+0", image_path]) 
        time.sleep(0.5)

        kb = keyboard.dyanmicKeyboard()
        kb.pressKey_f11()
        # kb.pressKey_esc()
        
        os.environ["DISPLAY"] = ":1"
        
        buffer.completeEvent()

    except FileNotFoundError:
        print("Image viewer not found! Please install 'eog' or a similar viewer.")
    except Exception as e:
        print(f"Failed to open the image: {e}")

# Example usage
# open_image("/home/ronak/Desktop/project-code/src/static/initial-image.png")
