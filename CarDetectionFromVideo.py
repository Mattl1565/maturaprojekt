import cv2

# Load the cascade
haar_cascade = 'Resources/cars.xml'

# To use a video file as input
video = 'Resources/resized_video.avi'
cap = cv2.VideoCapture(video)

car_cascade = cv2.CascadeClassifier(haar_cascade)

while True:
    # read frames from the video
    ret, frames = cap.read()

    if not ret:
        break

    if frames is not None:
        # convert to gray scale of each frames
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

        # Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Dilate the gray image to get rid of false positives
        delated = cv2.dilate(blur, None, iterations=2)

        # Morphological Transform, Dilation
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
        closing = cv2.morphologyEx(delated, cv2.MORPH_CLOSE, kernel)


        # Detects cars of different sizes in the input image
        cars = car_cascade.detectMultiScale(closing, scaleFactor=1.27, minNeighbors=1, minSize=(150, 150))

    # To draw a rectangle in each cars
    for (x, y, w, h) in cars:
        cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Display frames in a window
    cv2.imshow('video', frames)

    if cv2.waitKey(33) == 27:
        break

# De-allocate any associated memory usage
cv2.destroyAllWindows()

