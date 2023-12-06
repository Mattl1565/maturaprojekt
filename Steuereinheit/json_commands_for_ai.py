import json


class AICommands:
    @staticmethod
    def check_for_overtake(video_path, height, drone_angle):
        data = {
            "command": "check_for_overtake",
            "video_path": video_path,
            "height": height,
            "angle": drone_angle
        }
        json_message = json.dumps(data)
        return json_message
