import os
os.system("export DISPLAY=:0")

from flask import *
from fileinput import filename
from dotenv import load_dotenv
from threading import Thread
import time

# import custom modules
import screenshot

import imageProcessing

# Variables
load_dotenv()

MAX_ELAPSED_TIME = 1
CODE_IMAGES_DIR_PATH = os.getenv("IMAGES_DIR_PATH")
FILE_UPLOAD_DIR = os.getenv("FILE_UPLOAD_DIR_PATH")
# end Variables

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/success", methods = ["POST"])
def success():
    if request.method == "POST":
        # remove all images in images dir
        imageProcessing.pruneDir(CODE_IMAGES_DIR_PATH)
        
        f = request.files["file"]
        f.save(os.path.join(FILE_UPLOAD_DIR, f.filename))

        return render_template("fileUploadSuccess.html", filename=f.filename)


@app.route("/code/<filename>/<imageIndex>")
def code(filename, imageIndex):
    file_path = os.path.join(FILE_UPLOAD_DIR, filename)
    imageIndex = int(imageIndex)
        
    imageIndex = imageProcessing.validateImageIndex(CODE_IMAGES_DIR_PATH, imageIndex)

    def background_task():
        screenshot.getScreenshots(
            MAX_ELAPSED_TIME=MAX_ELAPSED_TIME,
            code_file_path=file_path,
            images_dir_path=CODE_IMAGES_DIR_PATH
        )
    
    thread = Thread(target=background_task)
    thread.start()
    
    return render_template("code.html", filename=filename, imageIndex=imageIndex, maxIndex=len(os.listdir(CODE_IMAGES_DIR_PATH)))



if (__name__ == "__main__"):
    
    # kill exisiting instances of code
    # os.system("sudo pkill code")
    #* enable on prod
    # os.system("tigervncserver")

    port = 8000
    while 1:
        try: 
            app.run(host="0.0.0.0", port=port)
        except:
            port += 1
            continue
        break
