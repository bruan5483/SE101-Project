import os
from dotenv import load_dotenv
import cv2
import time

load_dotenv()

# CAMERA_PORT = int(os.getenv("CAMERA_PORT"))

# cam = cv2.VideoCapture(0)

def init_cam():
    cam_port = -1
    while cam_port <= 10:
        cam = cv2.VideoCapture(cam_port)
        if cam.isOpened():
            return cam
        else:
            cam.release()
            cam_port+=1
            time.sleep(1)

cam = init_cam() 

def capture_picture(image_paths):

    if not (cam.isOpened()):
        print("Not open")

    res, img = cam.read()

    if res:
        for image_path in image_paths:
            cv2.imwrite(image_path, img)

        # print(image_path)
        # print("done saving picture")

# capture_picture("./img.png")