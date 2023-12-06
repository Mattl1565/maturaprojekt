import paho.mqtt.client as mqtt
import json
from InfluxDB.functions import write_telemetry, write_overtake, write_string
import Utils.find_ipv4_adress as ip

broker_address = ip.useful_functions.get_ip_address()
broker_port = 1884

drone_telemetry_topic = "Steuereinheit/drone_telemetry"
take_picture_topic = "Steuereinheit/take_pic"
kennzeichen_string_topic = "Steuereinheit/kennzeichen_string"
influx_db_topic = "Steuereinheit/InfluxDB"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(drone_telemetry_topic)
    client.subscribe(kennzeichen_string_topic)
    client.subscribe(take_picture_topic)
    client.publish(influx_db_topic, "MQTT-Connection to InfluxDB established!", qos=0)

def on_message(client, userdata, message):
    print("Message recieved!")
    if(message.topic == drone_telemetry_topic):  #DRONE TELEMETRY
        payload = json.loads(message.payload.decode('utf-8'))
        write_telemetry(payload)

    if(message.topic == kennzeichen_string_topic):  # IF we recieve the string of the licence plate
        print(message.payload.decode())  # THEN we print it out
        payload = json.loads(message.payload.decode('utf-8'))
        write_string(payload)

    if(message.topic == take_picture_topic):
        write_overtake(message.payload.decode())

mqtt_client = mqtt.Client("InfluxDB")

mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

print("Connecting to MQTT broker")
mqtt_client.connect(broker_address, broker_port, 60)

mqtt_client.loop_forever()
