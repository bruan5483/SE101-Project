#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS="/home/ronak/Desktop/project-code/utils/google_ocr_service_token.json"
export DISPLAY=":1"


while true; do
        if ping -c 1 google.com &> /dev/null; then
		echo "Connected to Wi-Fi. Running Python script"
		python3 /home/ronak/Desktop/project-code/src/app.py
		break
	else
		echo "Not connected to Wi-Fi. Retrying in 5 seconds..."
		sleep 5
	fi
done


