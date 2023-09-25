import cv2

# Load the cascade classifier for car detection
cascade_file = '../Resources/cars.xml'
car_cascade = cv2.CascadeClassifier(cascade_file)

# Load the image
image_path = '../Resources/Images/ParkinglotPicture.jpg'
image = cv2.imread(image_path)
image = cv2.resize(image, (640, 480))
# convert to gray scale of each frames
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Dilate the gray image to get rid of false positives
delated = cv2.dilate(blur, None, iterations=2)

# Morphological Transform, Dilation
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
closing = cv2.morphologyEx(delated, cv2.MORPH_CLOSE, kernel)


# Perform car detection
cars = car_cascade.detectMultiScale(closing, scaleFactor=1.05, minNeighbors=3, minSize=(10, 10), maxSize=(80, 80))

# Draw rectangles around the detected cars
for (x, y, w, h) in cars:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the image with the car detections
cv2.imshow('Car Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()