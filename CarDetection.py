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

        # Detects cars of different sizes in the input image
        cars = car_cascade.detectMultiScale(gray, 1.3, 1)

    # To draw a rectangle in each cars
    for (x, y, w, h) in cars:
        cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Display frames in a window
    cv2.imshow('video', frames)

    if cv2.waitKey(33) == 27:
        break

# De-allocate any associated memory usage
cv2.destroyAllWindows()

