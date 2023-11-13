from djitellopy import Tello
import paho.mqtt.client as mqtt
import json
import function_interpreter

tello = Tello()
connected = False

broker_address = "xx.xx.xx.xx:1883"
broker_port = 1883
topic41 = "Steuereinheit/commands_to_drone"
topic42 = "Steuereinheit/drone_telemetry"
topic43 = "Steuereinheit/drone_on"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic41)
    client.publish(topic43, "Tello in da house", qos=0)

def on_message(client, userdata, message):
    function_interpreter.process_payload(message.payload)

client = mqtt.Client()

client.on_message = on_message
client.on_connect = on_connect

if(tello.connect() == True):
    client.connect(broker_address, broker_port, 60)

client.loop_forever()
