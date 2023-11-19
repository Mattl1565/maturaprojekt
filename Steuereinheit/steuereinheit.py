import cv2 as cv
import paho.mqtt.client as mqtt
import numpy as np

from TelloStuff.json_commands_for_drone import TelloCommands

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1884  # Default MQTT port

topic21 = "Steuereinheit/commands_to_drone"
topic31 = "Steuereinheit/commands_to_ground_camera"
topic41 = "Steuereinheit/commands_to_overtake_ai"
topic51 = "Steuereinheit/commands_to_licence_plate_ai"


topic22 = "Steuereinheit/drone_telemetry"
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
    client.subscribe(topic32)
    client.subscribe(topic42)
    client.subscribe(topic43)
    client.subscribe(topic52)

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

    if message.topic == topic32:   #IF we recieve picture from ground cam
        #image_data = np.frombuffer(message.payload, dtype=np.uint8)
        #image = cv.imdecode(image_data, cv.IMREAD_COLOR)
        #cv.imshow("Nummernschild", image)
        #cv.waitKey(0)
        #cv.destroyAllWindows()   #THEN we display it
        print("Officer, we recieved a pic!")

    if message.topic == topic42: #IF a car left the street
        print(message.payload.decode())  # THEN we print it out

    if message.topic == topic43: ##IF Drone connected to MQTT
        client.publish(topic41, TelloCommands.takeoff(), qos=1) #THEN it should take off

    if message.topic == topic52: #IF we recieve the string of the licence plate
        print(message.payload.decode()) #THEN we print it out


# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, 60)

# Loop to maintain the connection and handle messages
client.loop_start()


# Example: Wait for user input to exit the script
input("Press Enter to exit...\n")

# Stop the MQTT client loop and disconnect from the broker
#client.loop_stop()
#client.disconnect()
