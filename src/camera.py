import os
from dotenv import load_dotenv
import cv2
# from cv2 import

load_dotenv()

CAMERA_PORT = int(os.getenv("CAMERA_PORT"))

cam = cv2.VideoCapture(CAMERA_PORT)

def capture_picture(image_path):

    res, img = cam.read()

    if res:
        
        cv2.imwrite(image_path, res)


# take_picture("utils/annotationImages/img.png")