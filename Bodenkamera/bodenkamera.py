import sys
import paho.mqtt.client as mqtt

# MQTT broker address and port
broker_address = "localhost"
port = 1883  # Default MQTT port

# Topic to which you want to publish the message
commands_to_ground_cam_topic = "Steuereinheit/commands_to_ground_camera"
license_plate_topic = "Steuereinheit/kennzeichen_foto"
topic42 = "Steuereinheit/take_pic"

image_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\TelloStuff\\picture.png"

# Check if the laptop IP address is provided as a command-line argument
# if len(sys.argv) < 2:
#     print("Please provide the laptop IP address as a command-line argument.")
#     sys.exit(1)

# laptop_ip_address = sys.argv[1]

# Callback function to handle connection
def on_connect(client, userdata, flags, rc):
    client.subscribe(commands_to_ground_cam_topic)
    print("Connected to MQTT broker with result code " + str(rc) + "\n")

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")
    if message.topic == commands_to_ground_cam_topic:
        with open(image_path, "rb") as file:
            image_data = file.read()
            client.publish(license_plate_topic, image_data, qos=1)

client = mqtt.Client("Bodenkamera")

# Set the callback function
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, 60)

client.loop_forever()
