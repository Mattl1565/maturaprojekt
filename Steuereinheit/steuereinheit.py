import threading
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips
import cv2
import cv2 as cv
import paho.mqtt.client as mqtt
import numpy as np

from Steuereinheit.json_commands_for_ai import AICommands
from TelloStuff.json_commands_for_drone import TelloCommands


received_video_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Steuereinheit\\received_video.mp4"
video_writer = None

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1884  # Default MQTT port

topic21 = "Steuereinheit/commands_to_drone"
topic31 = "Steuereinheit/commands_to_ground_camera"
topic41 = "Steuereinheit/commands_to_overtake_ai"
topic51 = "Steuereinheit/commands_to_licence_plate_ai"


topic22 = "Steuereinheit/drone_telemetry"
topic23 = "Steuereinheit/video_stream"
topic32 = "Steuereinheit/kennzeichen_foto"
topic42 = "Steuereinheit/take_pic"
topic43 = "Steuereinheit/drone_on"
topic52 = "Steuereinheit/kennzeichen_string"

topic100 = "Steuereinheit/test"

# Message to be published
message_to_licence_plate_ai = "Analyze now!"
message_to_ground_cam = "Take a pic!"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic22)
    client.subscribe(topic23)
    client.subscribe(topic32)
    client.subscribe(topic42)
    client.subscribe(topic43)
    client.subscribe(topic52)
    #client.publish(topic41, AICommands.check_for_overtake(received_video_path), qos=1)

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

    if message.topic == topic22: #IF we recieve telemetry from drone
        print(message.payload.decode()) #THEN we print it out

    if message.topic == topic23: #IF we recieve video from drone
        global video_writer
        print("Recieved jpg from drone")
        nparr = np.frombuffer(message.payload, np.uint8, count=-1)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if video_writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(received_video_path, fourcc, 30.0, (frame.shape[1], frame.shape[0]))

        video_writer.write(frame)

        timer_thread = threading.Thread(target=timer_function)
        timer_thread.start()

    if message.topic == topic32:   #IF we recieve picture from ground cam
        image_data = np.frombuffer(message.payload, dtype=np.uint8)
        image = cv.imdecode(image_data, cv.IMREAD_COLOR)
        cv.imshow("Nummernschild", image)
        cv.waitKey(0)
        cv.destroyAllWindows()   #THEN we display it
        print("Officer, we recieved a pic!")

    if message.topic == topic42: #IF a car left the street
        print(message.payload.decode())  # THEN we print it out

    if message.topic == topic43: ##IF Drone connected to MQTT
        #client.publish(topic21, TelloCommands.get_telemetry())
        #client.publish(topic21, TelloCommands.takeoff(), qos=1) #THEN it should take off
        #client.publish(topic21, TelloCommands.get_telemetry())
        #client.publish(topic21, TelloCommands.move_up(120))
        #client.publish(topic21, TelloCommands.get_telemetry())
        #client.publish(topic21, TelloCommands.move_forward(250))
        #client.publish(topic21, TelloCommands.get_telemetry())
        #client.publish(topic21, TelloCommands.move_back(270))
        #client.publish(topic21, TelloCommands.get_telemetry())
        #client.publish(topic21, TelloCommands.land())

        client.publish(topic21, TelloCommands.get_camera_feed())


    if message.topic == topic52: #IF we recieve the string of the licence plate
        print(message.payload.decode()) #THEN we print it out


def on_publish(client, userdata, mid):
    print("Publishing!")

def timer_function():
    time.sleep(3)
    video_writer.release()
    clip1 = VideoFileClip("C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Steuereinheit\\last_15_seconds.mp4")
    clip2 = VideoFileClip("C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Steuereinheit\\received_video.mp4")
    final_clip = concatenate_videoclips([clip1, clip2])
    final_clip.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")
    clip1.close()
    clip2.close()
    #client.publish(topic41, AICommands.check_for_overtake(received_video_path), qos=1)

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to the broker
client.connect(broker_address, port, 60)

# Loop to maintain the connection and handle messages
client.loop_start()


# Example: Wait for user input to exit the script
input("Press Enter to exit...\n")

# Stop the MQTT client loop and disconnect from the broker
#client.loop_stop()
#client.disconnect()

