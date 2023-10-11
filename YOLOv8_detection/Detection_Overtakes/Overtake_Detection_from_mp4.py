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
video_path = 'C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\Resources\\Videos\\highway_video_1.mp4'
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
Y_THRESHOLD = 0.5
ListOfCarsAtFirstSight = {}

# initialize the variables for the overtakes
overtakes_down = 0
overtakes_up = 0
tempVariableForFirstIteration = 0


#define a scaling factor
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
        print("current_time_sec: " + str(current_time_sec)) # Print timestamp
        print("**********************************************")

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        #  - new car gets detected -> add car.ID + coords to AllCars (list)      ✓
        #  - make sure to save the visible cars in a list (VisibleCars)          ✓
        #  - Create a list to store currently visible cars                       ✓
        #  - sort the visible cars by the y coordinate                           ✓

        # Iterate through detected boxes and track IDs
        # Create a Car object for each track_id and add it to the CarDict
        for box, track_id in zip(boxes, track_ids):
            # Check if the track_id is already in the CarDict
            if track_id in CarDict:
                car = CarDict[track_id]
                x, y, w, h = box
                x = x.numpy()
                y = y.numpy()
                car.setX(x)
                car.setY(y)
            else:
                x, y, w, h = box
                x = x.numpy()
                y = y.numpy()
                tempCar = Car(x, y, track_id)
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
            overtakes_down = overtakes_down + 1
        if not func.isSortedUp(VisibleCars_up):
            overtakes_up = overtakes_up + 1

        # Update VisibleCars list with visible cars
        VisibleCars = [car for car in AllCars if func.is_car_visible(car, track_ids)]

        # CHECK IF A CAR CHANGED DIRECTION
        # listofCars at the frame they get visible for the tracking algorithm
        # listofCars at the actual frame (VisibleCars)
        # if a car reached a sertain threshold of y-coordinates in either positive or negative direction
        # it direction gets set to up or down, before it was unknown

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
                    if (ListOfCarsAtFirstSight[car].getY() + Y_THRESHOLD) <= car_act.getY():
                        ListOfCarsAtFirstSight[car].setDirection(DOWN)
                        car_act.setDirection(DOWN)
                    elif (ListOfCarsAtFirstSight[car].getY() - Y_THRESHOLD) >= car_act.getY():
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
        # for car in VisibleCars_up:
        #     print(car)
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # for car in VisibleCars_down:
        #     print(car)
        print("VisibleCars: ")
        for car in VisibleCars:
            print(car)
        print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("ListOfCarsAtFirstSight: ")
        for car in ListOfCarsAtFirstSight:
            print(ListOfCarsAtFirstSight[car])

        print("----------------------------------------------------------------")
        print("Overtakes_UP: " + str(overtakes_up))
        print("Overtakes_DOWN: " + str(overtakes_down))
        print("----------------------------------------------------------------")


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
            # cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 0, 255),thickness=4)  # Adjust thickness if needed

            # Get the direction of the car
            direction = func.get_direction(track_id, VisibleCars)
            # Add the direction label at the bottom of the box
            direction_label = f"Direction: {direction}"
            cv2.putText(annotated_frame, direction_label, (int(x - (w/2)), int(y + (h/2) + 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()