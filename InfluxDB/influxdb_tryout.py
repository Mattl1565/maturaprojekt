import json

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from paho import mqtt

from InfluxDB.functions import write_telemetry


broker_address = "10.22.253.0"
broker_port = 1884
topic42 = "Steuereinheit/drone_telemetry"
topic61 = "Steuereinheit/InfluxDB"

token = "GxIxdhdibmd-xgl_0uK996cw4ta_9M0INkrjVFqbLILccQIfFUYatmcanJG_7ARcbL0qTifpHO0DJg2-O_ZxBg=="
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

mqtt_client = mqtt.Client()

mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

#if(tello.connect() == True):
print("Connecting to MQTT broker")
mqtt_client.connect(broker_address, broker_port, 60)

mqtt_client.loop_forever()





