import easyocr
import numpy as np
from ultralytics import YOLO
import cv2
import paho.mqtt.client as mqtt
import Utils.useful_functions as ip

broker_address = ip.useful_functions.get_ip_address()
port = 1883
licence_plate_string_topic = "Steuereinheit/kennzeichen_string"
commands_to_licence_plate_ai_topic = "Steuereinheit/commands_to_licence_plate_ai"

def read_license_plate(payload):
    model = YOLO("Model\\best.pt")
    # img_path = 'C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Resources\\Images\\karim_busted.jpg'
    image_data = np.frombuffer(payload, dtype=np.uint8)
    img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Use the model
    results = model.track(img)

    try:
        boxes = results[0].boxes.xywh.cpu()
    except:
        print("No number plate detected")

    for bbox in boxes:
        x, y, w, h = map(int, bbox[:4])
        print(x, y, w, h)

        # parse to int
        x, y, w, h = int(x), int(y), int(w), int(h)
        y = y - (h // 2)
        x = x - (w // 2)

        # Extract the region inside the bounding box
        extracted_region = img[y:y + h, x:x + w]

        # Display the extracted region
        # cv2.imshow(f"Extracted Image", extracted_region)

    # preprocess the image
    gray = cv2.cvtColor(extracted_region, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
    _, thresh = cv2.threshold(bfilter, 100, 255, cv2.THRESH_BINARY)  # Threshhold
    # cv2.imshow("Image", thresh)
    # cv2.waitKey(0)
    # initialize the reader
    reader = easyocr.Reader(['en'])
    # extract text from the image
    result = reader.readtext(img)
    text, box, score = result[1]
    print(box)
    client.publish(licence_plate_string_topic, box, qos=1)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc) + "\n")
    client.subscribe(commands_to_licence_plate_ai_topic)

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}")
    if message.topic == commands_to_licence_plate_ai_topic:
        read_license_plate(message.payload)

def on_publish(client, userdata, mid):
    print("Publishing!")

client = mqtt.Client("License Plate Detection AI")

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect(broker_address, port, 60)

client.loop_forever()