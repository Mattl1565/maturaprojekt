import easyocr
from ultralytics import YOLO
import cv2

# Load a model
model = YOLO("Model\\best.pt")

img_path = 'C:\\Users\\matth\\PycharmProjects\\maturaprojekt\\Resources\\Images\\karim_busted.jpg'

img = cv2.imread(img_path)

# Use the model
results = model.track(img)

try:
    boxes = results[0].boxes.xywh.cpu()
except:
    print("No number plate detected")

for bbox in boxes:
    x, y, w, h = map(int, bbox[:4])
    print(x, y, w, h)

    #parse to int
    x, y, w, h = int(x), int(y), int(w), int(h)
    y = y - (h//2)
    x = x - (w//2)



    # Extract the region inside the bounding box
    extracted_region = img[y:y + h, x:x + w]

    # Display the extracted region
    # cv2.imshow(f"Extracted Image", extracted_region)

# preprocess the image
gray = cv2.cvtColor(extracted_region, cv2.COLOR_BGR2GRAY)
bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
_, thresh = cv2.threshold(bfilter, 100, 255, cv2.THRESH_BINARY) #Threshhold
# cv2.imshow("Image", thresh)
# cv2.waitKey(0)

# initialize the reader
reader = easyocr.Reader(['en'])

# extract text from the image
result = reader.readtext(img)

text, box, score = result[1]

print(box)
