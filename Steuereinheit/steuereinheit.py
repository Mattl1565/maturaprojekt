import paho.mqtt.client as mqtt

# MQTT broker configuration
broker_address = "mqtt.eclipse.org"
port = 1883
topic = "example/topic"

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Publish a message when connected
    client.publish(topic, "Hello, MQTT!")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect

# Connect to the broker
client.connect(broker_address, port, 60)

# Loop to process network and broker messages
client.loop()

# Disconnect from the broker
client.disconnect()
