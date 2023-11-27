import paho.mqtt.client as mqtt
import json
from InfluxDB.functions import write_telemetry, write_overtake
import Utils.find_ipv4_adress as ip

broker_address = ip.useful_functions.get_ip_address()
broker_port = 1884

topic42 = "Steuereinheit/drone_telemetry"
topic52 = "Steuereinheit/kennzeichen_string"
topic61 = "Steuereinheit/InfluxDB"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic42)
    client.subscribe(topic52)
    client.publish(topic61, "MQTT-Connection to InfluxDB established!", qos=0)

def on_message(client, userdata, message):
    if(message.topic == topic42):  #DRONE TELEMETRY
        payload = json.loads(message.payload.decode('utf-8'))
        write_telemetry(payload)

    if(message.topic == topic52):  # IF we recieve the string of the licence plate
        print(message.payload.decode())  # THEN we print it out
        payload = json.loads(message.payload.decode('utf-8'))
        write_overtake(payload)

mqtt_client = mqtt.Client("InfluxDB")

mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

print("Connecting to MQTT broker")
mqtt_client.connect(broker_address, broker_port, 60)

mqtt_client.loop_forever()





