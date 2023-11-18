import time
import cv2
import numpy as np
import paho.mqtt.client as mqtt

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1883  # Default MQTT port

# Topic to which you want to subscribe for the video stream
topic23 = "Steuereinheit/video_stream"
topic42 = "Steuereinheit/take_pic"

# Path to save the received video
received_video_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Steuereinheit\\received_video.mp4"
video_writer = None

#dummies
car_id = 5
did_car_leave = True

# Callback function to handle connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic23)

# Callback function to handle message reception
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

    global video_writer

    # Decode the received data
    nparr = np.frombuffer(message.payload, np.uint8, count=-1)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Initialize video writer if not done already
    if video_writer is None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(received_video_path, fourcc, 30.0, (frame.shape[1], frame.shape[0]))

    # Write the frame to the video file
    video_writer.write(frame)




# Create an MQTT client with increased max_inflight_messages_set
client = mqtt.Client()  # Adjust the value as needed

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port, 60)

# Loop to maintain the connection and handle messages
client.loop_start()

if did_car_leave == True:
    client.publish(topic42, car_id, qos=1)

try:
    time.sleep(30)  # Adjust the duration based on your requirements
except KeyboardInterrupt:
    pass



# Stop the video writer and disconnect from MQTT
if video_writer is not None:
    video_writer.release()

# client.loop_stop()
# client.disconnect()
