# Not a Smartboard

## Description
Our product aims to be a tool to help developers during peer code review sessions. Rather than screen shares, it allows for a more immersive and interactive way to provide feedback. The product allows developers to upload a desired code file and project it onto a whiteboard or equivalent. This allows reviewers to handwrite comments, which will all be captured and saved, allowing the feedback process to be smooth and efficient, especially in group environments. 

## Installation
For this project, you will need:
- Raspberry Pi (Raspbian)
- USB Webcam
- Monitor/Projector
- Micro-HDMI to HDMI Cable

#### Clone repository
```
git clone https://git.uwaterloo.ca/hkhawja/se101-team-21.git
cd se101-team-21
```

#### Create Python venv
```
python -m venv ./venv
source ./venv/bin/activate
```

#### Dependencies
```
pip install flask 
pip install opencv-python
pip install pillow 
pip install python-dotenv
pip install screeninfo
pip install keyboard
pip install pynput
pip install pyautogui
pip install shutils
pip install google-cloud-vision
```

#### Google Cloud API Key
Follow Google Cloud Vision setup here: https://cloud.google.com/vision/docs/setup
Download the API_KEY and put it in ```./utils/google_ocr_service_token.json```

#### Run the App
Navigate to the shellScripts directory and run the script
```
cd shellScripts
chmod +x ./wifi_check.sh
./wifi_check.sh
```

## Usage
By using this product, users agree to follow the following policies:
1. Users must not use this product for unlawful or fraudulent purposes
2. Users must not use our product to violate the privacy or intellectual property rights of others, or use it on data that falls under third-party copyrights

Refer to example usage here:
https://drive.google.com/file/d/1h-a4Zw946FFNwTKIcn3T0HXxlNzyXM1y/view?usp=sharing

## License
The MIT Licence applies to this project. Refer to LICENSE.md
