import json


class AICommands:
    @staticmethod
    def check_for_overtake(video_path):
        data = {
            "command": "check_for_overtake",
            "video_path": video_path
        }
        json_message = json.dumps(data)
        return json_message
