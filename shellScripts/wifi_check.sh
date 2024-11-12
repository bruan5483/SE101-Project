#!/bin/bash


while true; do
        if ping -c 1 google.com &> /dev/null; then
		echo "Connected to Wi-Fi. Running Python script"
		python3 /home/ronak/Desktop/project-code/src/fileUpload.py
		break
	else
		echo "Not connected to Wi-Fi. Retrying in 5 seconds..."
		sleep 5
	fi
done


