import json

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt

from InfluxDB.functions import write_telemetry


broker_address = "localhost"
broker_port = 1884
topic42 = "Steuereinheit/drone_telemetry"
topic61 = "Steuereinheit/InfluxDB"

token = "fhRnIAFrxsfcIHc3rmzmb4aCw1k9nWCCkx4JCVK4A5XkNh_6Fe6FIOK1ji6zh4ltmvvhhneK6F0wrXz3ThMZsw=="
#token_pc = "QV9n46Bpf4I8IUeiwi746ZR2zQwJdDE0FVLNfav3TnNTy2_-TOzO0rVyJxnC2HR4IUTgZuQqQAMLkKJkNV_x2Q=="
org = "Maturaprojekt"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "drone_telemetry"

write_api = write_client.write_api(write_options=SYNCHRONOUS)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic42)
    client.publish(topic61, "MQTT-Connection to InfluxDB established!", qos=0)

def on_message(client, userdata, message):
    if(message.topic == topic42):  #DRONE TELEMETRY
        payload = json.loads(message.payload.decode('utf-8'))
        write_telemetry(payload)

mqtt_client = mqtt.Client("InfluxDB")

mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

print("Connecting to MQTT broker")
mqtt_client.connect(broker_address, broker_port, 60)

mqtt_client.loop_forever()





