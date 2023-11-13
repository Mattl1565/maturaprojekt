import json


class TelloCommands:
    @staticmethod
    def move_up(x):
        data = {
            "command": "move_up",
            "distance": x
        }
        json_message = json.dumps(data)
        return json_message

    @staticmethod
    def move_forward(x):
        data = {
            "command": "move_forward",
            "distance": x
        }
        json_message = json.dumps(data)
        return json_message

    @staticmethod
    def move_back(x):
        data = {
            "command": "move_back",
            "distance": x
        }
        json_message = json.dumps(data)
        return json_message

    @staticmethod
    def move_down(x):
        data = {
            "command": "move_down",
            "distance": x
        }
        json_message = json.dumps(data)
        return json_message

    @staticmethod
    def takeoff():
        data = {
            "command": "takeoff"
        }
        json_message = json.dumps(data)
        return json_message

    @staticmethod
    def land():
        data = {
            "command": "land"
        }
        json_message = json.dumps(data)
        return json_message

    @staticmethod
    def get_battery():
        data = {
            "command": "get_battery"
        }
        json_message = json.dumps(data)
        return json_message
