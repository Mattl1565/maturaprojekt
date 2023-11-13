import paho.mqtt.client as mqtt
from json_commands_for_drone import TelloCommands

# MQTT broker configuration
broker_address = "localhost"
broker_port = 1883
topic41 = "Steuereinheit/commands_to_drone"
topic42 = "Steuereinheit/drone_telemetry"
topic43 = "Steuereinheit/drone_on"

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic42)
    client.subscribe(topic43)

def on_message(client, userdata, message):
    print(f"Received message: On topic {message.topic}")
    if message.topic == topic43:
        client.publish(topic41, TelloCommands.takeoff(), qos=1)

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, broker_port, 60)

client.loop_forever()
