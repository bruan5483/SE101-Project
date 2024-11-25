import subprocess
import keyboard
import time
import os
import buffer
import cv2
from threading import Thread

width = 1920
height = 1080

def display_fullscreen_image(image_path):

    # Read the image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        return

    # Create a named window and set it to fullscreen
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Display the image
    cv2.imshow('Image', image)
    # cv2.waitKey(10000)  # Wait for a key press
    cv2.waitKey()  # Wait for a key press
    cv2.destroyAllWindows()  # Close the window


def open_image(image_path, buffer: buffer.Buffer):
    try:
        buffer.appendRequest("open-image")
        # wait until we reach buffer
        while (not buffer.isNext("open-image")):
            time.sleep(0.1)

        os.environ["DISPLAY"] = ":0"

        global thread
        thread = Thread(target=display_fullscreen_image, args=[image_path])
        thread.start()

        # subprocess.Popen(["display", "-geometry", "1000x1000+0+0", image_path]) 
        start_time = time.time()
        while time.time()-start_time < 2:
            time.sleep(0.3)

        kb = keyboard.dyanmicKeyboard()
        # kb.pressKey_f11()
        # kb.pressKey_esc()
        
        os.environ["DISPLAY"] = ":1"
        
        buffer.completeEvent()

    except FileNotFoundError:
        print("Image viewer not found! Please install 'eog' or a similar viewer.")
    except Exception as e:
        print(f"Failed to open the image: {e}")

# Example usage
# open_image("/home/ronak/Desktop/project-code/src/static/initial-image.png")
