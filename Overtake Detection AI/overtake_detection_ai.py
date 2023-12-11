import json
import threading
import time
import paho.mqtt.client as mqtt
from ultralytics import YOLO
from MATURAPROJEKT.maturaprojekt.YOLOv8_detection.Detection_Overtakes.Car import Car
import MATURAPROJEKT.maturaprojekt.YOLOv8_detection.Detection_Overtakes.Functions as func
from collections import defaultdict
import numpy as np
import MATURAPROJEKT.maturaprojekt.Utils.useful_functions as ip
import cv2

# MQTT broker address and port
broker_address = ip.useful_functions.get_ip_address()
port = 1883

video_stream_topic = "Steuereinheit/video_stream"
commands_to_overtake_ai_topic = "Steuereinheit/commands_to_overtake_ai"
take_picture_topic = "Steuereinheit/take_pic"


def run_overtake_detection(client, video_path, model, drone_height, drone_angle, overtaking_detection, direction_detection, speed_detection, file_index):

    cap = cv2.VideoCapture(video_path)
    print(video_path)
    model.fuse()
    # Store the track history
    track_history = defaultdict(lambda: [])

    line_start = (400, 900)
    line_end = (1600, 900)
    # initialize the lists for the cars
    CarDict = {}
    AllCars = []
    VisibleCars = []
    VisibleCars_up = []
    VisibleCars_down = []

    angle_in_radians = np.radians(drone_angle)

    distance_covered = drone_height * np.tan(angle_in_radians)

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("drone_height: " + str(drone_height))
    print("drone_angle: " + str(drone_angle))
    print("distance_covered: " + str(distance_covered))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    # initialize the variables for the direction detection
    UP = 1
    DOWN = 0
    UNKNOWN = 2
    Y_THRESHOLD = 1
    ListOfCarsAtFirstSight = {}

    # test for direction detection
    VisibleCarsBeforeUpdate = []

    overtakes_down = 0
    overtakes_up = 0
    current_overtaking_car_count = 0
    tempVariableForFirstIteration = 0

    publish_flag = False
    # define a scaling factor
    scaling_factor = 1
    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Get the current frame's timestamp
            current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)  # Get timestamp in milliseconds
            current_time_sec = current_time_ms / 1000.0  # Convert to seconds
            print("**********************************************")
            print("current_time_sec: " + str(current_time_sec))  # Print timestamp
            print("**********************************************")

            height, width = frame.shape[:2]
            imgsz = max(width, height)
            print(f'YOLOv8 imgsz: {imgsz}')

            pixel_per_meter = width / distance_covered

            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(source=frame, persist=True)
            # Get the boxes and track IDs
            try:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()
            except:
                track_ids = []

            #  - new car gets detected -> add car.ID + coords to AllCars (list)      ✓
            #  - make sure to save the visible cars in a list (VisibleCars)
            #  - Create a list to store currently visible cars
            #  - sort the visible cars by the y coordinate

            # Iterate through detected boxes and track IDs
            for box, track_id in zip(boxes, track_ids):
                # Check if the track_id is already in the CarDict
                if track_id in CarDict:
                    car = CarDict[track_id]
                    x, y, w, h = box
                    x = x.numpy()
                    y = y.numpy()
                    car.setX(x)
                    y_arr = [1]
                    y_arr[0] = y
                    car.setTime(current_time_ms)
                    car.setY(y_arr, pixel_per_meter)
                else:
                    x, y, w, h = box
                    x = x.numpy()
                    y = y.numpy()
                    y_arr = [1]
                    y_arr[0] = y
                    tempCar = Car(x, y_arr[0], track_id)
                    AllCars.append(tempCar)
                    CarDict[track_id] = tempCar

            # First Iteration
            if tempVariableForFirstIteration == 0:
                # Update VisibleCars list with visible cars
                VisibleCars = [car for car in AllCars if func.is_car_visible(car, track_ids)]
                # Sort Visible Cars by y-coordinate
                VisibleCars.sort(key=lambda x: x.getY())
                tempVariableForFirstIteration = 1

            # Check if a Car took over
            if not func.isSortedDown(VisibleCars_down):
                overtakes_up = overtakes_up + 1

            if not func.isSortedUp(VisibleCars_up):
                overtakes_down = overtakes_down + 1

            VisibleCarsBeforeUpdate = list(VisibleCars)

            # Update VisibleCars list with visible cars
            VisibleCars = [car for car in AllCars if func.is_car_visible(car, track_ids)]



            # Check if a car changed direction
            # if (visible cars vorher < visible cars nachher) -> auto fährt nach unten
            # if (visible cars vorher > visible cars nachher) -> auto fährt nach oben
            # if len(VisibleCarsBeforeUpdate) == len(VisibleCars):

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
                        if ((ListOfCarsAtFirstSight[
                                 car].getY() + Y_THRESHOLD) <= car_act.getY()) and car_act.getScreenTime() > 7:
                            ListOfCarsAtFirstSight[car].setDirection(DOWN)
                            car_act.setDirection(DOWN)
                        elif (ListOfCarsAtFirstSight[
                                  car].getY() - Y_THRESHOLD) >= car_act.getY() and car_act.getScreenTime() > 7:
                            ListOfCarsAtFirstSight[car].setDirection(UP)
                            car_act.setDirection(UP)

            # divide all the visible cars into _up and _down
            VisibleCars_up = [car for car in VisibleCars if car.getDirection() == 0]
            VisibleCars_down = [car for car in VisibleCars if car.getDirection() == 1]

            # Sort VisibleCars by y-coordinate
            VisibleCars_up.sort(key=lambda car: car.getY(), reverse=False)
            VisibleCars_down.sort(key=lambda car: car.getY(), reverse=True)
            VisibleCars.sort(key=lambda car: car.getY(), reverse=True)

            # Print the currently visible cars
            print("----------------------------------------------------------------")
            for car in VisibleCars_down:
                print(str(car))
                if(car.getOvertaking() == True and func.check_if_passed_line(car, line_start[1]) and car.getBusted() == False):
                    client.publish(take_picture_topic, (overtakes_up + overtakes_down), qos=0)
                    print("ERRGTRGEGEGEGREWERGEWGRGEWRG")
                    car.setBusted(True)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            for car in VisibleCars_up:
                print(str(car))

                if car.getOvertaking() == True and func.check_if_passed_line(car, line_start[1]) and car.getBusted() == False:
                    client.publish(take_picture_topic, (overtakes_up + overtakes_down), qos=0)
                    print("Gorbtchow")
                    car.setBusted(True)
            print("----------------------------------------------------------------")
            print("Overtakes_UP: " + str(overtakes_up))
            print("Overtakes_DOWN: " + str(overtakes_down))
            print("----------------------------------------------------------------")

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Plot the scaled tracks and draw the tracking lines
            # draw the Direction of the cars (up or down) at the bottom of the box (x,y,w,h) -> (x,y+h)
            for box, track_id in zip(boxes, track_ids):
                print("LOOOOOOOOOOOOOOOOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPPP")
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                if len(track) > 15:  # retain 90 tracks for 90 frames / tracking lines length
                    track.pop(0)

                # Draw the tracking lines
                points = np.array(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 0, 255),
                              thickness=4)  # Adjust thickness if needed

                # Get the direction of the car
                direction = func.get_direction_from_Dict(track_id, CarDict)
                overtaking = func.get_overtaking(track_id, CarDict)
                id = func.get_id(track_id, CarDict)
                speed = func.get_speed(track_id, CarDict)

                # Add the direction label at the bottom of the box
                if(direction_detection):
                    direction_label = f"Direction: {direction}"
                    cv2.putText(annotated_frame, direction_label, (int(x - (w / 2)), int(y + (h / 2) + 40)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                # Add the direction label at the bottom of the box
                if(overtaking_detection):
                    overtaking_label = f"Overtaking: {overtaking}"
                    cv2.putText(annotated_frame, overtaking_label, (int(x - (w / 2)), int(y + (h / 2) + 60)),
                                cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)
                id_label = f"ID: {id}"
                cv2.putText(annotated_frame, id_label, (int(x - (w / 2)), int(y + (h / 2) + 20)),
                            cv2.FONT_ITALIC, 1.0, (153, 255, 255), 2)
                if(speed_detection):
                    speed_label = f"Speed: {speed} km/h"
                    cv2.putText(annotated_frame, speed_label, (int(x - (w / 2)), int(y + (h / 2)) - 20),
                                cv2.FONT_ITALIC, 1.0, (153, 0, 255), 2)

                if(overtaking_detection):
                    cv2.putText(annotated_frame, "Overtakes_UP: " + str(overtakes_up), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (255, 0, 255), 2)
                    cv2.putText(annotated_frame, "Overtakes_DOWN: " + str(overtakes_down), (10, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)

                cv2.line(annotated_frame, line_start, line_end, (255, 255, 0), thickness= 5)

            annotated_frame = cv2.resize(annotated_frame, (1080, 720))
            # Display the annotated frame
            cv2.imshow("Overtake detection assisted by YOLOv8", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()


def overtaking_thread(client, video_file1, drone_height, drone_angle,overtaking_detection, direction_detection, speed_detection):
    model1 = YOLO('yolov8n.pt')
    run_overtake_detection(client, video_file1, model1, drone_height, drone_angle,overtaking_detection, direction_detection, speed_detection, 1)

def mqtt_thread():
    client = mqtt.Client("Overtake Detection AI", clean_session=True, userdata=None)

    # Set the callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    # Connect to the MQTT broker
    client.connect(broker_address, port, keepalive=120)

    # Start the MQTT loop
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(video_stream_topic)
    client.subscribe(commands_to_overtake_ai_topic)


# Callback function to handle message reception
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")

    if(message.topic == commands_to_overtake_ai_topic):
        payload = json.loads(message.payload.decode('utf-8'))
        if "command" in payload:
            command = payload["command"]
            if command == "check_for_overtake":
                video_path = payload.get("video_path", 0)
                print("Overtake Detection started!")
                drone_height = payload.get("height", 0)
                drone_angle = payload.get("angle", 0)
                overtaking_detection = payload.get("overtake_detection", 0)
                direction_detection = payload.get("direction_detection", 0)
                speed_detection = payload.get("speed_detection", 0)
                overtake_thread = threading.Thread(target=overtaking_thread, args=(client, video_path, drone_height, drone_angle, overtaking_detection, direction_detection, speed_detection), daemon=True)
                overtake_thread.start()

def on_publish(client, userdata, mid):
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Publishing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# Start the MQTT thread
mqtt_thread = threading.Thread(target=mqtt_thread, daemon=True)
mqtt_thread.start()

# Wait for a moment to ensure the MQTT thread has connected
time.sleep(2)

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    print("Exiting program.")

