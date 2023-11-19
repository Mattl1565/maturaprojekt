from djitellopy import Tello
import paho.mqtt.client as mqtt
import json

tello = Tello()
tello.connect()
connected = False


broker_address = "10.0.0.17"
broker_port = 1884

topic41 = "Steuereinheit/commands_to_drone"
topic42 = "Steuereinheit/drone_telemetry"
topic43 = "Steuereinheit/drone_on"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(topic41)
    client.publish(topic43, "Tello in da house", qos=0)

def on_message(client, userdata, message):
    if(message.topic == topic41):
        payload = json.loads(message.payload.decode('utf-8'))
        if "command" in payload:
            command = payload["command"]
            if command == "move_up":
                distance = payload.get("distance", 0)
                tello.move_up(distance)
                print("Moving up by ", distance)
            elif command == "move_forward":
                distance = payload.get("distance", 0)
                tello.move_forward(distance)
                print("Moving forward by ", distance)
            elif command == "move_back":
                distance = payload.get("distance", 0)
                tello.move_back(distance)
                print("Moving back by ", distance)
            elif command == "move_down":
                distance = payload.get("distance", 0)
                tello.move_down(payload.get(distance))
                print("Moving down by ", distance)
            elif command == "takeoff":
                tello.takeoff()
                print("Taking off!")
            elif command == "land":
                tello.land()
                print("Landing!")
            elif command == "get_battery":
                tello.get_battery()
                print("Battery:", tello.get_battery())
            else:
                print("Unknown command in payload")

client = mqtt.Client()

client.on_message = on_message
client.on_connect = on_connect

#if(tello.connect() == True):
print("Connecting to MQTT broker")
client.connect(broker_address, broker_port, 60)

client.loop_forever()
