import cv2
import requests
import io

cam = cv2.VideoCapture(0)
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width,frame_height))

while True:
    ret,frame = cam.read()
    out.write(frame)
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
out.release()
cv2.destroyAllWindows()

def transcribe(file_path):

    url = "https://symphoniclabs--symphonet-vsr-modal-htn-model-upload-static-htn.modal.run"

    with open('output.mp4', 'rb') as video_file:
        video = io.BytesIO(video_file.read())

    response = requests.post(url, files={'video': ('output.mp4', video, 'video/mp4')})

    return(response.text)
print(transcribe("output.mp4"))