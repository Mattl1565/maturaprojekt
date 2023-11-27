import time
from threading import Thread

import cv2
from djitellopy import Tello
import paho.mqtt.client as mqtt
import json

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

connected = False


broker_address = "10.22.253.0"
broker_port = 1884

topic23 = "Steuereinheit/video_stream"
topic24 = "Steuereinheit/stream_off"
topic41 = "Steuereinheit/commands_to_drone"
topic42 = "Steuereinheit/drone_telemetry"
topic43 = "Steuereinheit/drone_on"


#EINGESCHLEUSTES VIDEO
video_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Resources\\Videos\\test3.mp4"
chunk_size = 1024
cap = cv2.VideoCapture(video_path)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic41)
    client.publish(topic43, "Tello in da house", qos=0)

def on_message(client, userdata, message):
    if(message.topic == topic41):
        payload = json.loads(message.payload.decode('utf-8'))
        if "command" in payload:
            command = payload["command"]
            if command == "move_up":
                distance = payload.get("distance", 0)
                tello.move_up(distance)
                print("Moving up by ", distance)
            elif command == "move_forward":
                distance = payload.get("distance", 0)
                tello.move_forward(distance)
                print("Moving forward by ", distance)
            elif command == "move_back":
                distance = payload.get("distance", 0)
                tello.move_back(distance)
                print("Moving back by ", distance)
            elif command == "move_down":
                distance = payload.get("distance", 0)
                tello.move_down(payload.get(distance))
                print("Moving down by ", distance)
            elif command == "takeoff":
                tello.takeoff()
                print("Taking off!")
            elif command == "land":
                tello.land()
                print("Landing!")
            elif command == "get_battery":
                tello.get_battery()
                print("Battery:", tello.get_battery())
            elif command == "do_flip":
                tello.flip_left()
                tello.flip_right()
                print("Doing a flip!")
            elif command == "get_single_pic":
                #cv2.imwrite("/TelloStuff/tello_output.jpg", frame_read.frame)
                with open("/TelloStuff/tello_output.jpg", "rb") as file:
                    image_data = file.read()
                    client.publish(topic23, image_data, qos=1)
            elif command == "get_camera_feed":
                print("READING IN THE VIDEO!!!")
                if not cap.isOpened():
                    print("Error: Could not open video file.")
                    exit()

                frame_buffer = 450

                for _ in range(frame_buffer):
                    ret, frame = cap.read()
                    print("Reading in frame")
                    if not ret:
                        break  # Break the loop if the video is finished
                    compression_quality = 30
                    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), compression_quality])
                    data = buffer.tobytes()
                    print("Sending frame")
                    client.publish(topic23, data, qos=0)

                    #time.sleep(0.1)

                client.publish(topic24, "I am finished like CR7", qos=0)
                print("FINISHED SENDING!")
                cap.release()


            elif command == "get_telemetry":
                tello.get_battery()
                tello.get_temperature()
                tello.get_speed_x()
                tello.get_speed_y()
                tello.get_speed_z()
                tello.get_height()
                tello.get_flight_time()
                tello.get_barometer()

                time.sleep(1)  ##DELAY FOR INFLUX DB

                client.publish(topic42, json.dumps({
                    "battery": tello.get_battery(),
                    "temperature": (tello.get_temperature() - 32) * 5/9,
                    "speed_x": tello.get_speed_x(),
                    "speed_y": tello.get_speed_y(),
                    "speed_z": tello.get_speed_z(),
                    "height": tello.get_height(),
                    "flight_time": tello.get_flight_time(),
                    "barometer": tello.get_barometer()
                }), qos=0)

                print("Telemetry: -------------------------")
                print("Battery:", tello.get_battery(), "%")
                print("Temperature:", (tello.get_temperature() - 32) * 5/9, "°C")
                print("Speed_x:", tello.get_speed_x())
                print("Speed_y:", tello.get_speed_y())
                print("Speed_z:", tello.get_speed_z())
                print("Height:", tello.get_height(), "cm")
                print("Flight time:", tello.get_flight_time(), "s")
                print("Barometer:", tello.get_barometer(), "hPa")
                print("------------------------------------")
            else:
                print("Unknown command in payload")


def on_publish(client, userdata, mid):

    print("Publishing!")



client = mqtt.Client("Drone")

client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish

#if(tello.connect() == True):
print("Connecting to MQTT broker")
client.connect(broker_address, broker_port, 60)

client.loop_forever()
