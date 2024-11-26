import os
from dotenv import load_dotenv
import cv2
# from cv2 import

load_dotenv()

CAMERA_PORT = int(os.getenv("CAMERA_PORT"))

cam = cv2.VideoCapture(0)

def capture_picture(image_path):

    if not (cam.isOpened()):
        print("Not open")

    res, img = cam.read()

    if res:
        cv2.imwrite(image_path, img)

        print(image_path)
        print("done saving picture")


capture_picture("utils/annotationImages/img.png")