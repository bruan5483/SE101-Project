#!/bin/bash

while true; do
        if ping -c 1 google.com &> /dev/null; then
		echo "Connected to Wi-Fi. Running Python script"
		echo "Activating venv"
		source /home/ronak/Desktop/project-code/venv/bin/activate
		echo "Creating vnc server"
		tigervncserver
		export DISPLAY=:1
		xhost +
		python3 /home/ronak/Desktop/project-code/src/app.py
		break
	else
		echo "Not connected to Wi-Fi. Retrying in 5 seconds..."
		sleep 5
	fi
done


