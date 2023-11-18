import cv2 as cv
import paho.mqtt.client as mqtt
import numpy as np

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1883  # Default MQTT port

# Topic to which you want to publish the message
topic1 = "Steuereinheit/befehle"
topic2 = "Steuereinheit/kennzeichen_foto"

### dummys
car_id = 5
did_car_leave = True

# Message to be published
message = "Car ID " + str(car_id) + " left the street!"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")


def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)

client.loop_start()

if did_car_leave == True:
    client.publish(topic2, message, qos=1)

input("Press Enter to exit...\n")

client.loop_stop()
client.disconnect()
