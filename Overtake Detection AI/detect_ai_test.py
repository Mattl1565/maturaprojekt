
import time
from YOLOv8_detection.Detection_Overtakes.Car import Car
import YOLOv8_detection.Detection_Overtakes.Functions as func
import json
from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import paho.mqtt.client as mqtt

class AI_Overtake_Detection:
    def __init__(self):
        # MQTT broker address and port
        self.broker_address = "localhost"
        self.port = 1884

        self.topic23 = "Steuereinheit/video_stream"
        self.topic41 = "Steuereinheit/commands_to_overtake_ai"
        self.topic42 = "Steuereinheit/take_pic"

        self.video_path_drone = "/Steuereinheit/stream_from_drone.mp4"
        self.video_path_test = "/Resources/Videos/besteVideoGlaubstDuNichtDiese.mp4"

        self.init_mqtt()
        self.init_yolo()

    def init_mqtt(self):
        self.client = mqtt.Client("Overtake Detection AI")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, self.port, keepalive=120)

    def init_yolo(self):
        self.video_path = "C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Steuereinheit\\stream_from_drone.mp4"
        self.model = YOLO('yolov8n.pt')
        self.model.fuse()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code " + str(rc) + "\n")
        self.client.subscribe(self.topic23)
        self.client.subscribe(self.topic41)

    def on_message(self, client, userdata, message):
        print(f"Received message on topic {message.topic}")

        if message.topic == self.topic41:
            payload = json.loads(message.payload.decode('utf-8'))
            if "command" in payload:
                command = payload["command"]
                if command == "check_for_overtake":
                    print("Overtake Detection started!")
                    self.run_overtake_detection()

    def run_overtake_detection(self):
        cap = cv2.VideoCapture(self.video_path)

        # Store the track history
        track_history = defaultdict(lambda: [])
        CarDict = {}
        AllCars = []
        VisibleCars = []
        VisibleCars_up = []
        VisibleCars_down = []
        UP = 1
        DOWN = 0
        UNKNOWN = 2
        Y_THRESHOLD = 1
        ListOfCarsAtFirstSight = {}
        VisibleCarsBeforeUpdate = []
        overtakes_down = 0
        overtakes_up = 0
        tempVariableForFirstIteration = 0
        scaling_factor = 1

        while cap.isOpened():
            success, frame = cap.read()

            if success:
                current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                current_time_sec = current_time_ms / 1000.0
                print("**********************************************")
                print("current_time_sec: " + str(current_time_sec))
                print("**********************************************")

                height, width = frame.shape[:2]
                imgsz = max(width, height)
                print(f'YOLOv8 imgsz: {imgsz}')

                results = self.model.track(frame, persist=True)
                try:
                    boxes = results[0].boxes.xywh.cpu()
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                except:
                    track_ids = []

                for box, track_id in zip(boxes, track_ids):
                    if track_id in CarDict:
                        car = CarDict[track_id]
                        x, y, w, h = box
                        x = x.numpy()
                        y = y.numpy()
                        car.setX(x)
                        y_arr = [1]
                        y_arr[0] = y
                        car.setY(y_arr)
                    else:
                        x, y, w, h = box
                        x = x.numpy()
                        y = y.numpy()
                        y_arr = [1]
                        y_arr[0] = y
                        tempCar = Car(x, y_arr[0], track_id)
                        AllCars.append(tempCar)
                        CarDict[track_id] = tempCar

                if tempVariableForFirstIteration == 0:
                    VisibleCars = [car for car in AllCars if self.is_car_visible(car, track_ids)]
                    VisibleCars.sort(key=lambda x: x.getY())
                    tempVariableForFirstIteration = 1

                if not self.isSortedDown(VisibleCars_down):
                    overtakes_up = overtakes_up + 1

                if not self.isSortedUp(VisibleCars_up):
                    overtakes_down = overtakes_down + 1

                VisibleCarsBeforeUpdate = list(VisibleCars)

                VisibleCars = [car for car in AllCars if self.is_car_visible(car, track_ids)]

                for box, track_id in zip(boxes, track_ids):
                    if track_id not in ListOfCarsAtFirstSight:
                        x, y, w, h = box
                        x = x.numpy()
                        y = y.numpy()
                        tempCar = Car(x, y, track_id)
                        ListOfCarsAtFirstSight[track_id] = tempCar

                for car in ListOfCarsAtFirstSight:
                    for car_act in VisibleCars:
                        if ListOfCarsAtFirstSight[car].getID() == car_act.getID():
                            if ((ListOfCarsAtFirstSight[car].getY() + Y_THRESHOLD) <= car_act.getY()) and car_act.getScreenTime() > 7:
                                ListOfCarsAtFirstSight[car].setDirection(DOWN)
                                car_act.setDirection(DOWN)
                            elif (ListOfCarsAtFirstSight[car].getY() - Y_THRESHOLD) >= car_act.getY() and car_act.getScreenTime() > 7:
                                ListOfCarsAtFirstSight[car].setDirection(UP)
                                car_act.setDirection(UP)

                VisibleCars_up = [car for car in VisibleCars if car.getDirection() == 0]
                VisibleCars_down = [car for car in VisibleCars if car.getDirection() == 1]

                VisibleCars_up.sort(key=lambda car: car.getY(), reverse=False)
                VisibleCars_down.sort(key=lambda car: car.getY(), reverse=True)
                VisibleCars.sort(key=lambda car: car.getY(), reverse=True)

                print("----------------------------------------------------------------")
                for car in VisibleCars_down:
                    print(str(car))
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                for car in VisibleCars_up:
                    print(str(car))
                print("----------------------------------------------------------------")
                print("Overtakes_UP: " + str(overtakes_up))
                print("Overtakes_DOWN: " + str(overtakes_down))
                print("----------------------------------------------------------------")

                annotated_frame = results[0].plot()

                for box, track_id in zip(boxes, track_ids):
                    print("LOOOOOOOOOOOOOOOOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPPP")
                    x, y, w, h = box
                    track = track_history[track_id]
                    track.append((float(x), float(y)))
                    if len(track) > 15:
                        track.pop(0)

                    points = np.array(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 0, 255), thickness=4)

                    direction = func.get_direction_from_Dict(track_id, CarDict)
                    overtaking = func.get_overtaking(track_id, CarDict)
                    id = func.get_id(track_id, CarDict)
                    direction_label = f"Direction: {direction}"
                    cv2.putText(annotated_frame, direction_label, (int(x - (w/2)), int(y + (h/2) + 40)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    overtaking_label = f"Overtaking: {overtaking}"
                    cv2.putText(annotated_frame, overtaking_label, (int(x - (w / 2)), int(y + (h / 2) + 60)),
                                cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)
                    id_label = f"ID: {id}"
                    cv2.putText(annotated_frame, id_label, (int(x - (w / 2)), int(y + (h / 2) + 20)),
                                cv2.FONT_ITALIC, 1.0, (153, 255, 255), 2)

                    cv2.putText(annotated_frame, "Overtakes_UP: " + str(overtakes_up), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)
                    cv2.putText(annotated_frame, "Overtakes_DOWN: " + str(overtakes_down), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)

                annotated_frame = cv2.resize(annotated_frame, (1080, 720))
                cv2.imshow("Overtake detection assisted by YOLOv8", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        cap.release()


# Create an instance of the AI_Overtake_Detection class
ai_overtake_detection = AI_Overtake_Detection()

# Start the MQTT loop
ai_overtake_detection.client.loop_start()

# Wait for user input to exit
input("Press Enter to exit...\n")
