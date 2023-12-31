from collections import defaultdict
import Overtake_Detection
import cv2
import numpy as np
from ultralytics import YOLO
import time
from Car import Car
import Functions as func

# Load the YOLOv8 model
model = YOLO('../Model/yolov8n.pt')

# Open the video file
video_path = 'C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\Resources\\Videos\\Oberirnprechting_video.mp4'
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])

# initialize the lists for the cars
CarDict = {}
AllCars = []
VisibleCars = []
VisibleCars_up = []
VisibleCars_down = []

# initialize the variables for the direction detection
UP = 1
DOWN = 0
UNKNOWN = 2
Y_THRESHOLD = 1
ListOfCarsAtFirstSight = {}

#test for direction detection
VisibleCarsBeforeUpdate = []

overtakes_down = 0
overtakes_up = 0
tempVariableForFirstIteration = 0


#define a scaling factor
scaling_factor = 1

# Define the output video path
output_video_path = 'C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\YOLOv8_detection\\Detection_Overtakes\\output.mp4'

# Get the frames per second (fps) of the input video
fps = cap.get(cv2.CAP_PROP_FPS)

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs like 'XVID' or 'MJPG'
video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (1080, 720))  # Adjust the resolution if needed

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()


    if success:
        # Get the current frame's timestamp
        current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)  # Get timestamp in milliseconds
        current_time_sec = current_time_ms / 1000.0  # Convert to seconds


        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

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

        # First Iteration
        if tempVariableForFirstIteration == 0:
            # Update VisibleCars list with visible cars
            VisibleCars = [car for car in AllCars if func.is_car_visible(car, track_ids)]
            # Sort Visible Cars by y-coordinate
            VisibleCars.sort(key=lambda x: x.getY())
            tempVariableForFirstIteration = 1

        #Check if a Car took over
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
        #if len(VisibleCarsBeforeUpdate) == len(VisibleCars):

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

        # divide all the visible cars into _up and _down
        VisibleCars_up = [car for car in VisibleCars if car.getDirection() == 0]
        VisibleCars_down = [car for car in VisibleCars if car.getDirection() == 1]

        # Sort VisibleCars by y-coordinate
        VisibleCars_up.sort(key=lambda car: car.getY(), reverse=False)
        VisibleCars_down.sort(key=lambda car: car.getY(), reverse=True)
        VisibleCars.sort(key=lambda car: car.getY(), reverse=True)

        # Print the currently visible cars
        # print("----------------------------------------------------------------")
        # for car in VisibleCars_down:
        #     print(str(car))
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # for car in VisibleCars_up:
        #     print(str(car))
        # print("----------------------------------------------------------------")
        # print("Overtakes_UP: " + str(overtakes_up))
        # print("Overtakes_DOWN: " + str(overtakes_down))
        # print("----------------------------------------------------------------")


        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Plot the scaled tracks and draw the tracking lines
        # draw the Direction of the cars (up or down) at the bottom of the box (x,y,w,h) -> (x,y+h)

        for box, track_id in zip(boxes, track_ids):

            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            if len(track) > 15:  # retain 90 tracks for 90 frames / tracking lines length
                track.pop(0)

            # Draw the tracking lines
            points = np.array(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 0, 255),thickness=4)  # Adjust thickness if needed

            # Get the direction of the car
            direction = func.get_direction_from_Dict(track_id, CarDict)
            overtaking = func.get_overtaking(track_id,CarDict)
            id = func.get_id(track_id, CarDict)
            # Add the direction label at the bottom of the box
            direction_label = f"Direction: {direction}"
            cv2.putText(annotated_frame, direction_label, (int(x - (w/2)), int(y + (h/2) + 40)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # Add the direction label at the bottom of the box
            overtaking_label = f"Overtaking: {overtaking}"
            cv2.putText(annotated_frame, overtaking_label, (int(x - (w / 2)), int(y + (h / 2) + 60)),
                        cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)
            id_label = f"ID: {id}"
            cv2.putText(annotated_frame, id_label, (int(x - (w / 2)), int(y + (h / 2) + 20)),
                        cv2.FONT_ITALIC, 1.0, (153, 255, 255), 2)

            cv2.putText(annotated_frame, "Overtakes_UP: " + str(overtakes_up), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)
            cv2.putText(annotated_frame, "Overtakes_DOWN: " + str(overtakes_down), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)


        annotated_frame = cv2.resize(annotated_frame, (1080, 720))
        # Display the annotated frame
        cv2.imshow("Overtake detection assisted by YOLOv8", annotated_frame)

        # Write the annotated frame to the output video file
        # video_writer.write(annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture and writer object and close the display window
video_writer.release()
cap.release()