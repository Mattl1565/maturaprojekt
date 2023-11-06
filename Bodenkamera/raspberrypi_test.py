import paho.mqtt.client as mqtt

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1883  # Default MQTT port

# Topic to which you want to publish the message
topic1 = "Steuereinheit/befehle"
topic2 = "Steuereinheit/kennzeichen_foto"


# Path to the JPG file you want to publish
image_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Bodenkamera\\kennzeichen.jpg"


# Callback function to handle connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

    # Read the image file as binary data
    with open(image_path, "rb") as file:
        image_data = file.read()

    # Publish the image data as the payload of the MQTT message
    client.publish(topic2, image_data, qos=1)  # Set qos to 1 for message acknowledgment


# Create an MQTT client instance
client = mqtt.Client()

# Set the callback function
client.on_connect = on_connect

# Connect to the broker
client.connect(broker_address, port, 60)

# Loop to maintain the connection and handle messages
client.loop_start()

# You can continue your program logic here
print("Das war ein Befehl:", client.subscribe(topic1))
# Example: Wait for user input to exit the script
input("Press Enter to exit...\n")


client.loop_stop()
client.disconnect()