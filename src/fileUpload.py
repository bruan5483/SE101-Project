from flask import *
from fileinput import filename
import os
from dotenv import load_dotenv

load_dotenv()
file_upload_dir = os.getenv("FILE_UPLOAD_DIR_PATH")

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/success", methods = ["POST"])
def success():
    if request.method == "POST":
        f = request.files["file"]
        f.save(os.path.join(file_upload_dir, f.filename))
        return render_template("fileUploadSuccess.html", filename=f.filename)


if (__name__ == "__main__"):

    app.run(host="0.0.0.0", port=8000)