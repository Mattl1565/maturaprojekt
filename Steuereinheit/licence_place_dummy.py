import cv2 as cv
import paho.mqtt.client as mqtt
import numpy as np

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1883  # Default MQTT port


topic32 = "Steuereinheit/kennzeichen_foto"

topic51 = "Steuereinheit/commands_to_licence_plate_ai"
topic52 = "Steuereinheit/kennzeichen_string"

topic100 = "Steuereinheit/test"

### dummys
car_licence_plate = "ABR2ZHE"

# Message to be published
message_to_steuereinheit = "Car ID " + car_licence_plate + " got busted!"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic51)
    client.subscribe(topic32)
    client.subscribe(topic100)

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")
    if message.topic == topic32:
        #message_to_steuereinheit = analzye(...)
        client.publish(topic52, message_to_steuereinheit, qos=1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)

client.loop_start()

#Here the logic for reading the licence plate with AI

input("Press Enter to exit...\n")

#client.loop_stop()
#client.disconnect()