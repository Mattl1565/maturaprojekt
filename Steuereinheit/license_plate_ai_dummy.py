import json
import paho.mqtt.client as mqtt
import Utils.find_ipv4_adress as ip

# MQTT broker address and port
broker_address = ip.useful_functions.get_ip_address()
port = 1884


topic32 = "Steuereinheit/kennzeichen_foto"

topic51 = "Steuereinheit/commands_to_licence_plate_ai"
topic52 = "Steuereinheit/kennzeichen_string"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic51)
    client.subscribe(topic32)

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")
    if message.topic == topic32:
        #car_licence_plate = message_to_steuereinheit = analzye(...)
        json_message = json_message_to_influx(5, "SL623JM")
        client.publish(topic52, json_message, qos=1)

def json_message_to_influx(overtake_count, licence_plate):
    data = {
        "overtake_count": overtake_count,
        "licence_plate": licence_plate
    }
    json_message = json.dumps(data)
    client.publish(topic52, json_message, qos=1)
    json_message = json.dumps(data)
    return json_message

client = mqtt.Client("License Plate AI")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)

client.loop_start()

input("Press Enter to exit...\n")
