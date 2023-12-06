import cv2
import paho.mqtt.client as mqtt
import numpy as np
from Drohne.json_commands_for_drone import TelloCommands
from Steuereinheit.json_commands_for_ai import AICommands
import Utils.find_ipv4_adress as ip

video_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Resources\\Videos\\besteVideoGlaubstDuNichtDiese.mp4"

video_writer = None
take_fake_video_input = True
take_fake_photo_input = True

# MQTT broker address and port
broker_address = ip.useful_functions.get_ip_address()
port = 1884
#MQTT topics


commands_to_drone_topic = "Steuereinheit/commands_to_drone"
commands_to_ground_camera_topic = "Steuereinheit/commands_to_ground_camera"
commands_to_overtake_ai_topic = "Steuereinheit/commands_to_overtake_ai"
commands_to_licence_plate_ai_topic = "Steuereinheit/commands_to_licence_plate_ai"

drone_telemetry_topic = "Steuereinheit/drone_telemetry"
drone_stream_topic = "Steuereinheit/video_stream"
drone_stream_off_topic = "Steuereinheit/stream_off"
ground_camera_topic = "Steuereinheit/kennzeichen_foto"
car_left_topic = "Steuereinheit/take_pic"
drone_connected_topic = "Steuereinheit/drone_on"
licence_plate_string_topic = "Steuereinheit/kennzeichen_string"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(drone_telemetry_topic)
    client.subscribe(drone_stream_topic)
    client.subscribe(drone_stream_off_topic)
    client.subscribe(ground_camera_topic)
    client.subscribe(car_left_topic)
    client.subscribe(drone_connected_topic)
    client.subscribe(licence_plate_string_topic)

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

    if message.topic == drone_telemetry_topic: #IF we recieve telemetry from drone
        handle_telemetry(message) #THEN we handle it

    if message.topic == drone_stream_topic: #IF we recieve video from drone
        handle_video(message) #THEN we handle it

    if message.topic == drone_stream_off_topic: #IF the drone stopped sending video
        handle_video_stop(message) #THEN we handle it

    if message.topic == ground_camera_topic:   #IF we recieve picture from ground cam
        handle_ground_camera(message) #THEN we handle it

    if message.topic == car_left_topic: #IF a car left the street
        handle_car_leaving_street(message) #THEN we handle it

    if message.topic == drone_connected_topic: ##IF Drone connected to MQTT
        tag_der_offenen_tuer()

    if message.topic == licence_plate_string_topic: #IF we recieve the string of the licence plate
        handle_licence_plate_string(message) #THEN we handle it


def on_publish(client, userdata, mid):
    print("Publishing!")

def tag_der_offenen_tuer():
    client.publish(commands_to_drone_topic, TelloCommands.get_telemetry())
    client.publish(commands_to_drone_topic, TelloCommands.takeoff())
    client.publish(commands_to_drone_topic, TelloCommands.get_telemetry())
    client.publish(commands_to_drone_topic, TelloCommands.move_up(80))
    client.publish(commands_to_drone_topic, TelloCommands.get_telemetry())
    client.publish(commands_to_drone_topic, TelloCommands.move_forward(100))
    client.publish(commands_to_drone_topic, TelloCommands.get_telemetry())
    client.publish(commands_to_drone_topic, TelloCommands.move_back(100))
    client.publish(commands_to_drone_topic, TelloCommands.get_telemetry())
    client.publish(commands_to_drone_topic, TelloCommands.land())
def handle_telemetry(message):
    print(message.payload.decode())
def handle_video(message):
    if(take_fake_video_input):   #FAKE VIDEO INPUT CAME IN SO WE START THE ANALYSIS
        client.publish(commands_to_overtake_ai_topic, AICommands.check_for_overtake(video_path), qos=0)
    else:
        global video_writer
        print("Recieved jpg from drone")
        nparr = np.frombuffer(message.payload, np.uint8, count=-1)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if video_writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(video_path, fourcc, 30.0, (frame.shape[1], frame.shape[0]))

        video_writer.write(frame)

def handle_video_stop(message):
    if(take_fake_video_input):
        print("Detection finished!")

    else:
        print("Video finished!")
        client.publish(commands_to_overtake_ai_topic, AICommands.check_for_overtake(video_path), qos=1)
        video_writer.release()

def handle_ground_camera(message):
    image_data = np.frombuffer(message.payload, dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    cv2.imwrite("C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Steuereinheit\\kennzeichen_foto.jpg", image)
    cv2.imshow("Nummernschild", image)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()   #THEN we display it
    print("Officer, we recieved a pic!")

def handle_car_leaving_street(message):
    print("RasPi should be taking a pic now!")

def handle_licence_plate_string(message):
    print("License Plate String: " + message.payload.decode())

client = mqtt.Client("Steuereinheit")

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect(broker_address, port, 60)

client.loop_start()

input("Press Enter to exit...\n")
