import os
os.system("export DISPLAY=:1")

from flask import *
from fileinput import filename
from dotenv import load_dotenv
from threading import Thread
import time
import imageDisplay
import shutil 


# import custom modules
import screenshot
import imageProcessing
import buffer
import keyboard
import camera
import mergeFile


# Variables
load_dotenv()

buffer = buffer.Buffer()
MAX_ELAPSED_TIME = 1
RELATIVE_CODE_IMAGES_DIR_PATH = os.getenv("IMAGES_DIR_RELATIVE_PATH")
CODE_IMAGES_DIR_PATH = os.getenv("CODE_IMAGES_DIR_PATH")
ANNOTATIONS_IMAGES_DIR_PATH = os.getenv("ANNOTATIONS_IMAGES_DIR_PATH")
FILE_UPLOAD_DIR = os.getenv("FILE_UPLOAD_DIR_PATH")
STATIC_DIR_PATH = os.getenv("STATIC_DIR_PATH")
MERGE_FILE_PATH = os.getenv("MERGE_FILE_PATH")
DRAWING_ANNOTATIONS_IMAGES_DIR_PATH=os.getenv("DRAWING_ANNOTATIONS_IMAGES_DIR_PATH")


# end Variables

app = Flask(__name__)

@app.route("/")
def main():
    os.system("sudo pkill display")
    time.sleep(0.1)
    imageDisplay.open_image(os.path.join(STATIC_DIR_PATH, "initial-image.png"), buffer)
    return render_template("index.html")


@app.route("/success", methods = ["POST"])
def success():
    if request.method == "POST":
        # remove all images in images dir
        imageProcessing.pruneDir(CODE_IMAGES_DIR_PATH)
        imageProcessing.pruneDir(ANNOTATIONS_IMAGES_DIR_PATH)
        
        f = request.files["file"]
        f.save(os.path.join(FILE_UPLOAD_DIR, f.filename))
        
        file_path = os.path.join(FILE_UPLOAD_DIR, f.filename)
        def screenshot_task():
            screenshot.getScreenshots(
                MAX_ELAPSED_TIME=MAX_ELAPSED_TIME,
                code_file_path=file_path,
                images_dir_path=CODE_IMAGES_DIR_PATH,
                buffer=buffer
            )
        global screenshot_thread
        screenshot_thread = Thread(target=screenshot_task)
        screenshot_thread.start()
        
        return render_template("fileUploadSuccess.html", filename=f.filename)

@app.route("/capturePicture/<filename>/<imageIndex>", methods=["POST"])
def capturePicture(filename, imageIndex):
    annotation_image_path = os.path.join(ANNOTATIONS_IMAGES_DIR_PATH, f"img_{imageIndex}.png")
    # print(annotation_image_path)
    annotation_static_image_path = os.path.join(STATIC_DIR_PATH, f"img_{imageIndex}.png")
    camera_display_image_path = os.path.join(STATIC_DIR_PATH, "camera_display.png")

    paths = [annotation_image_path, annotation_static_image_path, camera_display_image_path]

    # create thread to take a picture with the webcam
    global annotation_image_thread
    annotation_image_path = Thread(target=camera.capture_picture, args=[paths])
    annotation_image_path.start()
    #camera.capture_picture(annotation_image_path)
    
    return jsonify({
        "status": "success",
        "filename": filename,
        "imageIndex": imageIndex
    })

@app.route("/mergeAnnotations/<filename>", methods=["POST"])
def mergeAnnotations(filename):
    codefile_path = os.path.join(FILE_UPLOAD_DIR, filename)
    #mergeFile.main(ANNOTATIONS_IMAGES_DIR_PATH, codefile_path)
    global mergefile_thread
    mergeFile_thread = Thread(target = mergeFile.main, args=[ANNOTATIONS_IMAGES_DIR_PATH, codefile_path])
    mergeFile_thread.start()

    return jsonify({
        "status": "success",
        "filename": filename
    })

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(FILE_UPLOAD_DIR, filename)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)
    
@app.route('/download-images')
def download_image():
    file_path = os.path.join(FILE_UPLOAD_DIR, "zip-img")
    shutil.make_archive(file_path, 'zip', DRAWING_ANNOTATIONS_IMAGES_DIR_PATH)

    try:
        return send_file(file_path + ".zip", as_attachment=True)
    except Exception as e:
        return str(e)
    
@app.route("/code/<filename>/<imageIndex>")
def code(filename, imageIndex):

    
    imageIndex = int(imageIndex)
    imageIndex = imageProcessing.validateImageIndex(CODE_IMAGES_DIR_PATH, imageIndex)
    image_path = os.path.join(STATIC_DIR_PATH, f"codeImages_pic_{imageIndex}.png")
    
    # annotation_image_path = os.path.join(STATIC_DIR_PATH, "camera_display.png")
    
    #global annotation_image_thread_display
    #annotation_image_thread_display = Thread(target=camera.capture_picture, args=[annotation_image_path])
    #annotation_image_thread_display.start()

    
    def open_image():
        # os.system("sudo pkill display")
        time.sleep(0.5)
        imageDisplay.open_image(image_path=image_path, buffer=buffer)
    
    if len(os.listdir(CODE_IMAGES_DIR_PATH)) > 0:
        global open_image_thread
        open_image_thread = Thread(target=open_image)
        open_image_thread.start()
        # open_image(image_path)

    return render_template("code.html", filename=filename, imageIndex=imageIndex, maxIndex=len(os.listdir(CODE_IMAGES_DIR_PATH)),
                        #    filepath=os.path.join("/utils/codeImages", filename)
                        )

if (__name__ == "__main__"):
    
    #* enable on prod
    #os.system("sudo pkill code")

    # open blank image
    # async def open_initial_image():
    #     await imageDisplay.open_image(os.path.join(STATIC_DIR_PATH, "initial-image.png"))
    # open_initial_image()
    
    port = 8000

    imageDisplay.open_image(os.path.join(STATIC_DIR_PATH, "initial-image.png"), buffer)
    # app.run(host="0.0.0.0", port=port)

    while 1:
        try: 
            app.run(host="0.0.0.0", port=port)
        except:
            port += 1
            continue
        break
