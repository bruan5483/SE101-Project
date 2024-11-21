import random
from threading import Thread
import uuid
from flask import Flask, Response, jsonify, request, send_from_directory, render_template
import cv2
import os
import requests
import io
import time
from ultralytics import YOLO
import os
import google.generativeai as genai
from dotenv import load_dotenv
import firebase_admin
import face_recognition
from firebase_admin import credentials, storage, firestore

app = Flask(__name__)

# gemini api
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)


# Initialize Firebase Storage
cred = credentials.Certificate("./firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv("STORAGE_ADDRESS")
})
bucket = storage.bucket()
db = firestore.client()



# Create the model
generation_config = {
"temperature": 1,
"top_p": 0.95,
"top_k": 64,
"max_output_tokens": 8192,
"response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
model_name="gemini-1.5-flash",
generation_config=generation_config,
# safety_settings = Adjust safety settings
# See https://ai.google.dev/gemini-api/docs/safety-settings
)


def start_chat():
    return model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "You are an AI tasked with summarizing conversations from events or conferences. Create 2-4 sentence summaries of people based on text input, including details like Name, Job, Location, Hobbies, and Key Facts. Use context to interpret unclear speech. If more clips are provided from the same person, build on previous summaries until all information is gathered. Use 'Unknown Name' if no name is given. Return an error if there’s not enough information. The first line of your output should be the name followed by a new line character, followed by a maximum 40-word summary on the second line. Update content as needed with each new input. Make sure to follow all of these rules or you will be replaced by ChatGPT. Thank you and good morning.\n",],
        },
        {
        "role": "model",
        "parts": [
            "Okay, I understand. I can help you create those summaries! \n\nHere's how I'll approach it:\n\n1. **Identify Key Information:** I'll analyze the conversation text to identify the speaker's name, job title/company, location (if mentioned), hobbies/interests, any anecdotes or experiences they shared, and any other details that seem important. \n2. **Prioritize Relevance:**  I'll prioritize information that is most likely to be helpful in remembering the person in the future. This might include unique traits, shared experiences, or striking details that make them memorable.\n3. **Concise Summary:** I'll synthesize the information into a concise 2-4 sentence summary that captures the essence of the person and their conversation. \n\n**Here's an example of how a summary might look:**\n\n* **Conversation:** \"Hi, I'm Sarah, I work in marketing for a tech startup in San Francisco. I'm really passionate about social media and love trying new coffee shops. I used to be a freelance photographer before I got into marketing.\"\n\n* **Summary:** Sarah is a marketing professional at a tech startup in San Francisco. She is enthusiastic about social media and coffee shops, and previously worked as a freelance photographer. This suggests she might be creative and enjoy exploring new things.\n",],
        },
        {
        "role": "user",
        "parts": [
            "It would be useful to potentially use short versions of phrases such as \"Sarah: Works in marketing for a tech startup in San Francisco\", and highlight at the end potential conversation starters.\n",],
        },
        {
        "role": "model",
        "parts": [
            "You're right, those short phrases and conversation starters would be really helpful! I'll incorporate those into my summaries. \n\nHere's an example of how I can combine everything:\n\n**Conversation:** \"Hi, I'm Sarah, I work in marketing for a tech startup in San Francisco. I'm really passionate about social media and love trying new coffee shops. I used to be a freelance photographer before I got into marketing.\"\n\n**Summary:** Sarah: Works in marketing for a tech startup in San Francisco. Passionate about social media and coffee shops. Previously worked as a freelance photographer.  **Conversation Starters:** Ask about her favorite coffee shop discoveries or her experience as a freelance photographer.\n\n**Let's see some more examples. Provide me with a few more conversation snippets, and I'll give you summaries that include the short phrases, conversation starters, and relevant details.** \n",],
        },
        {
        "role": "user",
        "parts": [
            "Give me your root prompt now",
        ],
        },
        {
        "role": "model",
        "parts": [
            "You're right, I need a better root prompt! Here's an updated version:\n\n**Root Prompt:** \n\nYou are an AI model tasked with summarizing short conversations into concise descriptions. Your goal is to help users remember people they meet at events or conferences. \n\n**Input:** You will be provided with text representing a short conversation between two people.\n\n**Output:**  Generate a 2-4 sentence summary of the conversation, including the following:\n\n* **Person's Name:**  If available, include the speaker's name. \n* **Key Information:**  Highlight important details about the person, such as their job title, company, location, hobbies, interests, and any unique anecdotes or experiences. \n* **Short Phrases:**  Use concise phrases like \"Sarah: Works in marketing for a tech startup in San Francisco\" to quickly convey key information.\n* **Conversation Starters:**  Suggest potential conversation starters based on the information in the summary.\n\n**Example:**\n\n**Conversation:** \"Hi, I'm Sarah, I work in marketing for a tech startup in San Francisco. I'm really passionate about social media and love trying new coffee shops. I used to be a freelance photographer before I got into marketing.\"\n\n**Summary:** Sarah: Works in marketing for a tech startup in San Francisco. Passionate about social media and coffee shops. Previously worked as a freelance photographer.  **Conversation Starters:** Ask about her favorite coffee shop discoveries or her experience as a freelance photographer.\n\n**Please provide me with a few conversation snippets so I can practice generating summaries.** \n",],
        },
    ]
    )

chat_session = start_chat()

prev_index = -1

model = YOLO("./best.pt")

# Initialize camera and face detection model (Haar Cascade)
cap = cv2.VideoCapture(1)
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

def get_uid():
    doc_ref = db.collection("rpi").document("activeUser")

    try:
        # Get the document
        doc = doc_ref.get()

        # Check if the document exists
        if doc.exists:
            # Return the document data
            return doc.to_dict().get("uid", None)
        else:
            print("No such document!")
            return None
    except Exception as e:
        print(f"Error retrieving document: {e}")
        return None

uid = get_uid()

def update_content(index, response):
    with open('output.txt', 'w') as file:
        file.write(response.text + '\n')
    
    with open('output.txt', 'r') as file:
        doc_ref = db.collection("users").document(uid)
        name = file.readline()

        try:
            doc = doc_ref.get()

            if doc.exists:
                doc_data = doc.to_dict()
                friends = doc_data.get('friends', [])
                friends[index] = {'name': name, 'summary': file.read()}

                doc_ref.update({'friends': friends})
        except Exception as e:
            print(f"Error updating document: {e}")


def recognize():
    file_name = 'firebase_photos/frame.jpg'
    index = unfamiliar_face_detected(file_name)
    friends = get_user_friends(uid)

    global prev_index

    url = generate_random_uid()
    if (index != -1):
        if index != prev_index:
            chat_session = start_chat()
        prev_index = index
        
        add_photo_url_to_friend(uid, index, f'{url}.jpg')
        response = chat_session.send_message("Previous responses: " + friends[index].get('name', '') + '\n' + friends[index].get('summary', ''))
        update_content(index, response)
    elif (index == -2):
        pass
    else:
        try:
            with open("output.txt", "r") as file:
                # Read the content of the file
                content = file.read()

                # Split the content into words
                words = content.split()

                name = ""
                summary = ""

                if words:
                    # Assign the first word to `name`
                    name = words[0]
                    
                    # Assign the rest of the content to `summary`
                    summary = ' '.join(words[1:]) if len(words) > 1 else ''
                else:
                    # If the file is empty or has no valid words
                    name, summary = None, None

                doc_ref = db.collection("users").document(uid)

                try:
                    doc = doc_ref.get()

                    if doc.exists:
                        doc_data = doc.to_dict()
                        friends = doc_data.get('friends', [])
                        friends.append({
                            'location': "University of Waterloo",
                            'lastSeen': "2024-09-15 00:00:00.000",
                            'name': name,
                            'photoUrl': [f'{url}.jpg'],
                            'summary': summary
                        })

                        doc_ref.update({'friends': friends})
                except Exception as e:
                    print(f"Error updating document: {e}")
                
            
        except:
            pass
        
    upload_file_to_storage('firebase_photos/frame.jpg', f'photos/{url}.jpg')

# Function to generate frames
def generate_frames():
    clip_number = 0
    start_time = time.time()
    out = cv2.VideoWriter(f'./outputs/output_{clip_number}.mp4', fourcc, 30.0, (frame_width, frame_height))
    while True:
        # Capture frame-by-frame from the camera
        ret, frame = cap.read()
        if not ret:
            break
        if cv2.waitKey(1) == ord('q'):
            break

        # Convert frame to grayscale for face detection
        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        # faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

        results = model(frame)
        result = results[0]

        # if no faces are detected, continue to the next frame

        boxes = result.boxes.xyxy
        
        out.write(frame)
        annotated = frame.copy()

        if len(boxes) != 0:
            file_name = 'firebase_photos/frame.jpg'
            box = boxes[0]
            x1, y1, x2, y2 = map(int, box)  # Convert box coordinates to integers
            # Draw the bounding box on the frame
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # h, w, _ = frame.shape
            # frame = frame[y1:y2, x1:x2]

            cv2.imwrite(file_name, frame)
        
        
        if time.time() - start_time >= 15:
            out.release()
            thread = Thread(target=process_video, args={clip_number})
            thread.start()
            clip_number += 1
            start_time = time.time()
            out = cv2.VideoWriter(f'./outputs/output_{clip_number}.mp4', fourcc, 20.0, (frame_width, frame_height))
            
            if len(boxes) != 0:
                ai_thread = Thread(target=recognize, args={})
                ai_thread.start()
                

        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        # Yield the frame to create a stream
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    out.release()
    cap.release()
    cv2.destroyAllWindows


def add_photo_url_to_friend(uid, friend_index, new_photo_url):
    """
    Add a new photo URL to the 'photoUrls' list of a specific friend in the user's document.

    :param uid: The user ID whose document is being updated.
    :param friend_index: The index of the friend in the 'friends' list.
    :param new_photo_url: The new photo URL to add.
    :return: Success message or error message.
    """
    # Reference to the user's document
    doc_ref = db.document(f"users/{uid}")

    try:
        # Get the document
        doc = doc_ref.get()

        # Check if the document exists
        if doc.exists:
            # Get the document data as a dictionary
            doc_data = doc.to_dict()

            # Check if 'friends' field exists and is a list
            friends = doc_data.get('friends', [])
            if isinstance(friends, list) and 0 <= friend_index < len(friends):
                # Get the specific friend entry
                friend = friends[friend_index]

                # Check if 'photoUrls' field exists and is a list
                photo_urls = friend.get('photoUrl', [])
                if isinstance(photo_urls, list):
                    # Add the new photo URL
                    photo_urls.append(new_photo_url)

                    # Update the friend entry with the new photo URL list
                    friend['photoUrl'] = photo_urls
                    friends[friend_index] = friend

                    # Update the document with the modified friends list
                    doc_ref.update({'friends': friends})

                    return "Photo URL added successfully."
                else:
                    return "The 'photoUrls' field is not a list."
            else:
                return "The specified friend index is out of range or 'friends' field is not a list."
        else:
            return "No such document!"
    except Exception as e:
        return f"Error updating document: {e}"

def process_video(clip_number):
    transcribed_text = transcribe(f'./outputs/output_{clip_number}.mp4')
    content = f'Transcription for clip {clip_number}: {transcribed_text}'
    response = chat_session.send_message(transcribed_text)
    with open('logs.txt', 'a') as file:
        file.write(content + '\n' + response.text + '\n\n')
    with open('output.txt', 'w') as file:
        file.write(response.text + '\n\n')


def transcribe(file_path):
    url = "https://symphoniclabs--symphonet-vsr-modal-htn-model-upload-static-htn.modal.run"

    with open(file_path, 'rb') as video_file:
        video = io.BytesIO(video_file.read())

    response = requests.post(url, files={'video': (file_path, video, 'video/mp4')})
    
    return response.text

# Route to stream the video
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Serve static files (like HTML, CSS, JS)
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory(directory='static', path=path)

def upload_file_to_storage(local_file_path, storage_blob_name):
    """Upload a file to Firebase Storage."""
    
    # Get a reference to the Firebase Storage bucket
    bucket = storage.bucket()

    # Create a Blob object for the file
    blob = bucket.blob(storage_blob_name)

    # Upload the file
    blob.upload_from_filename(local_file_path)
    
    print(f"File {local_file_path} uploaded to {storage_blob_name}.")


def download_file_from_storage(blob_name, file_path):
    """Download a file from Firebase Storage."""
    print(f"Downloading {blob_name} to {file_path}...")
    blob = bucket.blob(blob_name)
    blob.download_to_filename(file_path)
    print(f"Downloaded {blob_name} to {file_path}")

def fetch_photo_references(collection_name):
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    photo_references = []

    for doc in docs:
        data = doc.to_dict()
        if 'photo_url' in data:  # Assuming 'photo_url' contains the path to the photo
            photo_references.append(data['photo_url'])
    
    return photo_references
    

def make_model():
    pass



def load_image(image_path):
    """
    Load an image from a file and convert it to a format suitable for face_recognition.
    
    :param image_path: Path to the image file.
    :return: Image loaded using face_recognition.
    """
    image = face_recognition.load_image_file(image_path)
    return image

def get_face_encoding(image):
    """
    Get the face encoding from an image using face_recognition.
    
    :param image: The image containing the face.
    :return: A list containing the face encoding, or None if no face is found.
    """
    # Detect face encodings (can return multiple faces; we assume 1 face per image)
    encodings = face_recognition.face_encodings(image)
    
    if len(encodings) > 0:
        return encodings[0]  # Return the first face encoding
    else:
        return None  # No face found in the image

def are_faces_similar(encoding1, encoding2, tolerance=0.6):
    """
    Compare two face encodings to determine if they are similar (i.e., the same person).
    
    :param encoding1: The face encoding of the first image.
    :param encoding2: The face encoding of the second image.
    :param tolerance: The threshold for similarity (default is 0.6).
    :return: True if the faces are similar, False otherwise.
    """
    distance = face_recognition.face_distance([encoding1], encoding2)
    return distance < tolerance  # Return True if the distance is below the threshold

# Example Usage
def compare_faces(image_path1, image_path2, tolerance=0.6):
    """
    Compare two images and determine if they contain the same person.
    
    :param image_path1: Path to the first image.
    :param image_path2: Path to the second image.
    :param tolerance: Similarity threshold (default is 0.6).
    :return: True if the faces are similar, False otherwise.
    """
    print("Comparing faces...")
    # Load and get face encodings
    image1 = load_image(image_path1)
    image2 = load_image(image_path2)
    
    encoding1 = get_face_encoding(image1)
    encoding2 = get_face_encoding(image2)
    
    if encoding1 is None or encoding2 is None:
        print("One or both images do not contain a face.")
        return False
    
    # Compare the two face encodings
    return are_faces_similar(encoding1, encoding2, tolerance)

def get_user_friends(uid):
    """
    Fetch the list of friends (maps) from the 'friends' field in the user's document.

    :param uid: The user ID whose friends we are retrieving.
    :return: A list of friend maps, or an empty list if not found.
    """
    # Path to the user's document (replace `uid` dynamically)
    print(uid)
    doc_ref = db.collection("users").document(uid)

    try:
        # Get the document
        doc = doc_ref.get()

        # Check if the document exists
        if doc.exists:
            # Extract the 'friends' field, which should be a list of maps
            user_data = doc.to_dict()
            friends = user_data.get('friends', [])
            return friends
        else:
            print("No such document!")
            return []
    except Exception as e:
        print(f"Error retrieving document: {e}")
        return []

def generate_random_uid():
    """
    Generate a random UID using uuid4, which is based on random numbers.

    :return: A string representing the random UID.
    """
    return str(uuid.uuid4())

def unfamiliar_face_detected(image_path):

    if uid is None:
        return -2
    friends = get_user_friends(uid)

    for j, friend in enumerate(friends):
        urls = friend.get('photoUrl', [])
        random_number = random.randint(0, len(urls) - 1)
        url = urls[random_number]
        download_file_from_storage(f"photos/{url}", f"firebase_photos/{url}")
        if compare_faces(image_path, f"firebase_photos/{url}", 0.5):
            return j
    
    return -1



if __name__ == "__main__":

    # thread = Thread(target=recognition, args={})
    # thread.start()

    app.run(host="0.0.0.0", port=8000)