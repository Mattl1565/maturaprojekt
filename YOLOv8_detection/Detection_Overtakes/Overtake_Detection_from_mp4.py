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
video_path = 'C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\Resources\\Videos\\cars_on_highway (1080p).mp4'
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])

# initialize the lists for the cars
CarDict = {}
AllCars = []
VisibleCars = []

overtakes = 0
help = 0


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
                car.setY(y)
            else:
                x, y, w, h = box
                x = x.numpy()
                y = y.numpy()
                tempCar = Car(x, y, track_id)
                AllCars.append(tempCar)
                CarDict[track_id] = tempCar


        if help == 0:
            # Update VisibleCars list with visible cars
            VisibleCars = [car for car in AllCars if func.is_car_visible(car, track_ids)]
            # Sort Visible Cars by y-coordinate
            VisibleCars.sort(key=lambda car: car.getY(), reverse=True)
            help = 1

        #Check if a Car took over
        if not func.isSorted(VisibleCars):
            overtakes = overtakes + 1

        # Update VisibleCars list with visible cars
        VisibleCars = [car for car in AllCars if func.is_car_visible(car, track_ids)]
        
        # Sort VisibleCars by y-coordinate
        VisibleCars.sort(key=lambda car: car.getY(), reverse=True)


        # Print the currently visible cars
        print("----------------------------------------------------------------")
        for car in VisibleCars:
            print(car)
        print("----------------------------------------------------------------")
        print("Overtakes: " + str(overtakes))
        print("----------------------------------------------------------------")


        # Resize the bounding boxes
        scaled_boxes = boxes * scaling_factor
        scaled_boxes[:, 2:4] *= scaling_factor  # Resize width and height

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        small_annotated_frame = annotated_frame.copy()  # Make a copy to avoid modifying the original frame

        # Plot the scaled tracks
        for box, track_id in zip(scaled_boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            scaled_x, scaled_y = x * scaling_factor, y * scaling_factor
            track.append((float(scaled_x), float(scaled_y)))  # x, y center point (scaled)
            if len(track) > 30:  # retain 90 tracks for 90 frames / tracking lines length
                track.pop(0)

            # Draw the scaled tracking lines
            points = np.array(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(small_annotated_frame, [points], isClosed=False, color=(230, 230, 230),thickness=5)  # Adjust thickness if needed

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Resize the frame
        smaller_annotated_frame = cv2.resize(annotated_frame, (0, 0), fx=0.65, fy=0.65)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", smaller_annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()