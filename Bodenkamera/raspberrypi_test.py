import paho.mqtt.client as mqtt

# MQTT broker address and port
broker_address = "localhost"  # Replace this with your broker's address if it's different
port = 1883  # Default MQTT port

# Topic to which you want to publish the message
topic1 = "Steuereinheit/befehle"
topic2 = "Steuereinheit/kennzeichen_foto"


image_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Bodenkamera\\kennzeichen.jpg"


# Callback function to handle connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic1)
    with open(image_path, "rb") as file:
        image_data = file.read()
        client.publish(topic2, image_data, qos=1)

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")
    if message.topic == topic1:
        with open(image_path, "rb") as file:
            image_data = file.read()
            client.publish(topic2, image_data, qos=1)

client = mqtt.Client()

# Set the callback function
client.on_connect = on_connect

# Connect to the broker
client.connect(broker_address, port, 60)

# Loop to maintain the connection and handle messages
client.loop_start()

# Example: Wait for user input to exit the script
input("Press Enter to exit...\n")


client.loop_stop()
client.disconnect()