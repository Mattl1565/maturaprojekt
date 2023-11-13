import json
from djitellopy import Tello

tello = Tello()


def process_payload(given_payload):
    payload = json.loads(given_payload.decode('utf-8'))

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
