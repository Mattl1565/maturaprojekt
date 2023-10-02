from collections import defaultdict
import Overtake_Detection
import cv2
import numpy as np
from ultralytics import YOLO
import time

# Load the YOLOv8 model
model = YOLO('../Model/yolov8n.pt')

# Open the video file
video_path = 'C:\\Users\\karim\\Documents\\Schule\\MaturaProjekt\\MATURAPROJEKT\\maturaprojekt\\Resources\\Videos\\highway_video_1.mp4'
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])



#print(Overtake_Detection.are_cars_overtaking(1,1,2,3,1,2,1,3,1))

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

        print("----------------------------------------------------------------")
        print("current_time_sec: " + str(current_time_sec))
        print("----------------------------------------------------------------")

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

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

        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            print("x: " + str(x) + " y: " + str(y) + " w: " + str(w) + " h: " + str(h))
            print("track_id: " + str(track_id))

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        smaller_annotated_frame = cv2.resize(annotated_frame, (0, 0), fx=0.6, fy=0.6)

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