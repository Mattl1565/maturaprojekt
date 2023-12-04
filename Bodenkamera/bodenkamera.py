import paho.mqtt.client as mqtt
import Utils.find_ipv4_adress as ip
# MQTT broker address and port

broker_address = ip.useful_functions.get_ip_address()
port = 1884  # Default MQTT port

# Topic to which you want to publish the message
topic31 = "Steuereinheit/commands_to_ground_camera"
topic32 = "Steuereinheit/kennzeichen_foto"
topic42 = "Steuereinheit/take_pic"

image_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Resources\\Images\\karim_busted.jpg"



# Callback function to handle connection
def on_connect(client, userdata, flags, rc):
    client.subscribe(topic31)
    client.subscribe(topic42)
    print("Connected to MQTT broker with result code " + str(rc) + "\n")

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")
    if (message.topic == topic42) or (message.topic == topic31):
        with open(image_path, "rb") as file:
            image_data = file.read()
            client.publish(topic32, image_data, qos=1)

client = mqtt.Client("Bodenkamera")

# Set the callback function
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, 60)

# Loop to maintain the connection and handle messages
client.loop_start()

# Example: Wait for user input to exit the script
input("Press Enter to exit...\n")


#client.loop_stop()
#client.disconnect()