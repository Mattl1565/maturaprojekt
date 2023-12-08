import json


class AICommands:
    @staticmethod
    def check_for_overtake(video_path, height, drone_angle,overtake_detection,direction_detection,speed_detection):
        data = {
            "command": "check_for_overtake",
            "video_path": video_path,
            "height": height,
            "angle": drone_angle,
            "overtake_detection": overtake_detection,
            "direction_detection": direction_detection,
            "speed_detection": speed_detection
        }
        json_message = json.dumps(data)
        return json_message
