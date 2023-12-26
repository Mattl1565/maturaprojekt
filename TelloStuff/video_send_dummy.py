import cv2
import paho.mqtt.client as mqtt
import time

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1883  # Default MQTT port

# Topic to which you want to publish the video stream

topic21 = "Steuereinheit/commands_to_drone"
topic22 = "Steuereinheit/drone_telemetry"
topic23 = "Steuereinheit/video_stream"

# Path to your video file
video_path = "/Resources/Videos/test3.mp4"


# Chunk size in bytes (adjust according to your requirements)
chunk_size = 1024

# Callback function to handle connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic21)

# Callback function to handle message publication
def on_publish(client, userdata, mid):
    print("Message Published")

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")


# Create an MQTT client
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port, 60)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file is opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

try:
    frame_buffer = 200

    for _ in range(frame_buffer):
        # Read a frame from the video
        ret, frame = cap.read()

        if not ret:
            break  # Break the loop if the video is finished

        # Convert the frame to bytes
        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()

        # Publish the frame data to the MQTT topic
        client.publish(topic23, data, qos=0)

        # Wait for a short time to control the streaming rate
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # Release the video capture object and disconnect from MQTT
    cap.release()
    #client.disconnect()
