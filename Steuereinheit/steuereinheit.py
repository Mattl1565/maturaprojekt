import json
import time
import cv2
import paho.mqtt.client as mqtt
import numpy as np
from MATURAPROJEKT.maturaprojekt.Drohne.json_commands_for_drone import TelloCommands
from MATURAPROJEKT.maturaprojekt.Steuereinheit.json_commands_for_ai import AICommands
import MATURAPROJEKT.maturaprojekt.Utils.find_ipv4_adress as ip
import pygame
from PIL import Image, ImageDraw, ImageFont

video_path = "C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\Resources\\Videos\\besteVideoGlaubstDuNichtDiese.mp4"
#video_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Steuereinheit\\stream_from_drone.mp4"
video_writer = None

drone_height = 0
drone_angle = 0
ground_cam_usage = False
overtake_detection = False
direction_detection = False
speed_detection = False
store_drone_telemetry = False
store_criminal_offences = False
take_fake_video_input = False
take_fake_picture_input = False
gta_effects = False

drone_connected = False

# MQTT broker address and port
broker_address = ip.useful_functions.get_ip_address()
port = 1883
#MQTT topics


commands_to_drone_topic = "Steuereinheit/commands_to_drone"
commands_to_ground_camera_topic = "Steuereinheit/commands_to_ground_camera"
commands_to_overtake_ai_topic = "Steuereinheit/commands_to_overtake_ai"
commands_to_licence_plate_ai_topic = "Steuereinheit/commands_to_licence_plate_ai"
commands_to_influxdb = "Steuereinheit/commands_to_influxdb"

drone_telemetry_topic = "Steuereinheit/drone_telemetry"
drone_stream_topic = "Steuereinheit/video_stream"
drone_stream_off_topic = "Steuereinheit/stream_off"
ground_camera_topic = "Steuereinheit/kennzeichen_foto"
car_left_topic = "Steuereinheit/take_pic"
drone_connected_topic = "Steuereinheit/drone_on"
licence_plate_string_topic = "Steuereinheit/kennzeichen_string"
graphical_steuereinheit_topic = "Steuereinheit/graphic_control"
store_car_data_topic = "Steuereinheit/store_car_data"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(drone_telemetry_topic)
    client.subscribe(drone_stream_topic)
    client.subscribe(drone_stream_off_topic)
    client.subscribe(ground_camera_topic)
    client.subscribe(car_left_topic)
    client.subscribe(drone_connected_topic)
    client.subscribe(licence_plate_string_topic)
    client.subscribe(graphical_steuereinheit_topic)
    #client.publish(graphical_steuereinheit_topic, "Start", qos=1)
    #client.publish(car_left_topic, "Take Pic!!!", qos=0)

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
        global drone_connected
        drone_connected = True

    if message.topic == licence_plate_string_topic: #IF we recieve the string of the licence plate
        handle_licence_plate_string(message) #THEN we handle it

    if message.topic == graphical_steuereinheit_topic:
        handle_graphic_control(message)


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
    if(store_drone_telemetry):
        client.publish(commands_to_influxdb, message, qos=1)
        print(message.payload.decode())

def handle_video(message):
    if(take_fake_video_input):   #FAKE VIDEO INPUT CAME IN SO WE START THE ANALYSIS
        client.publish(commands_to_drone_topic, TelloCommands.get_height(), qos=0) #getHEIGHT
        client.publish(commands_to_overtake_ai_topic, AICommands.check_for_overtake(video_path, drone_height, drone_angle), qos=0)
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
    file_path_mate = "C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\Steuereinheit\\Income\\kennzeichen.jpg"
    cv2.imwrite(file_path_mate, image)
    if(gta_effects):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\Steuereinheit\\GTA_Stuff\\busted_sound_effect.wav")
        font_path = "C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\Steuereinheit\\GTA_Stuff\\gta5.ttf"
        text = "Busted"
        text_color = (255,255,255)
        text_image = gta_busted_effect(text, font_path, 72, text_color)
        opencv_image = cv2.cvtColor(np.array(text_image), cv2.COLOR_RGB2BGR)
        gta_busted_image = cv2.resize(opencv_image, (image.shape[1], image.shape[0]))
        alpha = 0.3
        blended_image = cv2.addWeighted(image, alpha, gta_busted_image, 1 - alpha, 0)
        cv2.imshow("Nummernschild", blended_image)
        pygame.mixer.music.play()
        cv2.waitKey(7000)
        pygame.mixer.music.stop()
        cv2.destroyAllWindows()   #THEN we display it
        print("Officer, we recieved a pic!")
        with open(file_path_mate, "rb") as file:
            image_data = file.read()
            client.publish(commands_to_licence_plate_ai_topic, image_data, qos=1)
    else:
        cv2.imshow("Nummernschild", image)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()  # THEN we display it
        print("Officer, we recieved a pic!")
        with open(file_path_mate, "rb") as file:
            image_data = file.read()
            client.publish(commands_to_licence_plate_ai_topic, image_data, qos=1)

def handle_car_leaving_street(message):
    print(message.payload.decode())
    print("Ground Cam Usage:")
    print(ground_cam_usage)
    if(ground_cam_usage):
        client.publish(commands_to_ground_camera_topic, "Picture this!", qos=1)
        print("RasPi should be taking a pic now!")
    if(store_criminal_offences):
        client.publish(store_car_data_topic, message.payload, qos=1)


def handle_licence_plate_string(message):
    print("License Plate String: " + message.payload.decode())

def gta_busted_effect(text, font_path, font_size, text_color):
    image = Image.new("RGB", (500, 500), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text((150, 200), text, font=font, fill=text_color)
    return image

def play_busted(file_path):
    pygame.time.delay(7000)
    pygame.mixer.music.stop()
    pygame.quit()

def handle_graphic_control(message):

    print(message.payload.decode())

    global ground_cam_usage
    global drone_height
    global drone_angle
    global overtake_detection
    global direction_detection
    global speed_detection
    global gta_effects
    global take_fake_picture_input
    global take_fake_video_input
    global store_drone_telemetry
    global store_criminal_offences

    payload = json.loads(message.payload.decode('utf-8'))
    drone_height = payload["drone_height"]
    drone_angle = payload["drone_angle"]
    overtake_detection = payload["overtake_detection"]
    ground_cam_usage = payload["ground_cam_usage"]
    direction_detection = payload["direction_detection"]
    speed_detection = payload["speed_detection"]
    store_drone_telemetry = payload["store_drone_telemetry"]
    store_criminal_offences = payload["store_criminal_offences"]
    take_fake_video_input = payload["fake_vid_input"]
    take_fake_picture_input = payload["fake_pic_input"]
    gta_effects = payload["gta_effects"]
    client.publish(commands_to_overtake_ai_topic,AICommands.check_for_overtake(video_path, drone_height, drone_angle, overtake_detection,
                                                direction_detection, speed_detection), qos=0)

client = mqtt.Client("Steuereinheit")

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect(broker_address, port, 60)

client.loop_forever()
