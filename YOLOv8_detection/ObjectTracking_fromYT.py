from collections import defaultdict

import cv2
import numpy as np
import pytube as pt
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('Model/yolov8n.pt')

yt_url = "https://www.youtube.com/watch?v=TE2tfavIo3E"
yt = pt.YouTube(yt_url)

# Get the highest resolution stream (you can choose a different stream if needed)
stream = yt.streams.filter(adaptive=True, file_extension="mp4").first()

# Open the video file
cap = cv2.VideoCapture(stream.url)

# Store the track history
track_history = defaultdict(lambda: [])

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # # Plot the tracks
        # for box, track_id in zip(boxes, track_ids):
        #     x, y, w, h = box
        #     track = track_history[track_id]
        #     track.append((float(x), float(y)))  # x, y center point
        #     if len(track) > 50:  # retain 90 tracks for 90 frames / length of the tail
        #         track.pop(0)
        #
        #     # Draw the tracking lines
        #     points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
        #     cv2.polylines(annotated_frame, [points], isClosed=False, color=(244, 210, 32), thickness=5)

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