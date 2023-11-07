import cv2 as cv
import paho.mqtt.client as mqtt
import numpy as np

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1883  # Default MQTT port

# Topic to which you want to publish the message
topic1 = "Steuereinheit/befehle"
topic2 = "Steuereinheit/kennzeichen_foto"


# Message to be published
message = "Work harder, child!"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic2)


def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")
    if message.topic == topic2:
        # Convert the received image data (payload) to a NumPy array
        image_data = np.frombuffer(message.payload, dtype=np.uint8)
        # Decode the image data to an OpenCV image
        image = cv.imdecode(image_data, cv.IMREAD_COLOR)
        # Display the image (you can modify this part based on your requirements)
        cv.imshow("Received Image", image)
        cv.waitKey(0)
        cv.destroyAllWindows()


# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, 60)

# Loop to maintain the connection and handle messages
client.loop_start()

# Publish a message to topic1
client.publish(topic1, message, qos=1)

# Example: Wait for user input to exit the script
input("Press Enter to exit...\n")

# Stop the MQTT client loop and disconnect from the broker
client.loop_stop()
client.disconnect()
