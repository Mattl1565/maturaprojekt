from ultralytics import YOLO

# Load the model and run the tracker with a custom configuration file
model = YOLO('Model/yolov8n.pt')
results = model.track(source="https://www.youtube.com/watch?v=QKtNW0Gc6uM", show = True)