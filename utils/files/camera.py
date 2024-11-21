import cv2
import requests
import time

# Initialize webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

# Server URL for POST requests
server_url = "http://0.0.0.0:8000/video_feed"  # Replace with your server IP address

while True:
    # Capture frame-by-frame from webcam
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture video")
        break

    # Encode the frame as a JPEG image
    _, img_encoded = cv2.imencode('.jpg', frame)

    # Prepare the file to send
    files = {
        'video': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')
    }

    # Send the image frame to the server via POST
    try:
        response = requests.post(server_url, files=files)
        print("Server response:", response.json())
    except Exception as e:
        print(f"Error sending frame to server: {e}")

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.2)

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
