from flask import *
from fileinput import filename
import os
from dotenv import load_dotenv
from threading import Thread
import time

load_dotenv()
file_upload_dir = os.getenv("FILE_UPLOAD_DIR_PATH")

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/code")
def code():

    pass

@app.route("/success", methods = ["POST"])
def success():
    if request.method == "POST":
        f = request.files["file"]
        f.save(os.path.join(file_upload_dir, f.filename))

        time.sleep(5)

        redirect("/code")

        return render_template("fileUploadSuccess.html", filename=f.filename)


@app.route("/code")
# Call screenshot function with thread
        # Call display function with 
def code():
    pass

if (__name__ == "__main__"):

    app.run(host="0.0.0.0", port=8000)