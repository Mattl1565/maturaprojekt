from collections import defaultdict
import Overtake_Detection
import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('../Model/yolov8n.pt')

# Open the video file
video_path = '/maturaprojekt/Resources/Videos/test3.mp4'
cap = cv2.VideoCapture(video_path)

# Store the track history
#track_history = defaultdict(lambda: [])



print(Overtake_Detection.are_cars_overtaking(1,4,2,2,1,3,1,2,1))



# # Loop through the video frames
# while cap.isOpened():
#     # Read a frame from the video
#     success, frame = cap.read()
#
#     if success:
#         # Run YOLOv8 tracking on the frame, persisting tracks between frames
#         results = model.track(frame, persist=True)
#
#         # Get the boxes and track IDs
#         boxes = results[0].boxes.xywh.cpu()
#         track_ids = results[0].boxes.id.int().cpu().tolist()
#
#         linkeObereEckenX = []
#         linkeObereEckenY = []
#
#         for box, track_id in zip(boxes, track_ids):
#             x, y, w, h = box
#             linkeObereEckenX.append(x - w / 2)
#             linkeObereEckenY.append(y - h / 2)
#             print("x: " + str(x) + " y: " + str(y) + " w: " + str(w) + " h: " + str(h))
#             print("track_id: " + str(track_id))
#
#         print("linkeObereEckenX: " + str(linkeObereEckenX))
#         print("linkeObereEckenY: " + str(linkeObereEckenY))
#
#         # Visualize the results on the frame
#         annotated_frame = results[0].plot()
#
#         # # Plot the tracks
#         # for box, track_id in zip(boxes, track_ids):
#         #     x, y, w, h = box
#         #     track = track_history[track_id]
#         #     track.append((float(x), float(y)))  # x, y center point
#         #     if len(track) > 30:  # retain 90 tracks for 90 frames / tracking lines length
#         #         track.pop(0)
#         #
#         #     # Draw the tracking lines
#         #     points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
#         #     cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)
#
#         # Display the annotated frame
#         cv2.imshow("YOLOv8 Tracking", annotated_frame)
#
#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     else:
#         # Break the loop if the end of the video is reached
#         break
#
# # Release the video capture object and close the display window
# cap.release()