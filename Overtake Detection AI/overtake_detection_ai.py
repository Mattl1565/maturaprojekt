import json
import subprocess
from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import time
import paho.mqtt.client as mqtt


# MQTT broker address and port
broker_address = "localhost"
port = 1884

topic23 = "Steuereinheit/video_stream"
topic41 = "Steuereinheit/commands_to_overtake_ai"
topic42 = "Steuereinheit/take_pic"

video_path_drone = "/Steuereinheit/stream_from_drone.mp4"
video_path_test = "/Resources/Videos/besteVideoGlaubstDuNichtDiese.mp4"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic23)
    client.subscribe(topic41)

# Callback function to handle message reception
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

    if(message.topic == topic41):
        payload = json.loads(message.payload.decode('utf-8'))
        if "command" in payload:
            command = payload["command"]
            if command == "check_for_overtake":
                #video_path = payload.get("video_path", 0)
                print("Overtake Detection started!")
                process = subprocess.Popen(['python3', 'detect_ai_test.py'])
                #return_code = process.returncode

client = mqtt.Client("Overtake Detection AI")

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port, keepalive=120)


# Loop to maintain the connection and handle messages
client.loop_start()

input("Press Enter to exit...\n")
