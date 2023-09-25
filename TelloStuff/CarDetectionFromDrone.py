import cv2
import cv2 as cv
import numpy as np
from djitellopy import tello
from maturaprojekt.Resources import KeyPressModule as kp
from time import sleep

height = 480
width = 640
blank_image = np.zeros((height, width, 3), np.uint8)

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()

cascade_file = '../Resources/cars.xml'
car_cascade = cv.CascadeClassifier(cascade_file)


def getKeyboarInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yv = speed
    elif kp.getKey("d"): yv = -speed

    if kp.getKey("q"): me.land()
    if kp.getKey("e"): me.takeoff()

    return [lr, fb, ud, yv]


while True:

    if (me.get_battery() < 5):
        me.land()
    vals = getKeyboarInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.1)

    frame = me.get_frame_read().frame

    # convert to gray scale of each frames
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Dilate the gray image to get rid of false positives
    delated = cv2.dilate(blur, None, iterations=2)

    # Morphological Transform, Dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    closing = cv2.morphologyEx(delated, cv2.MORPH_CLOSE, kernel)

    cars = car_cascade.detectMultiScale(closing, scaleFactor=1.13, minNeighbors=2, minSize=(50, 50), maxSize=(130, 130))

    for (x, y, w, h) in cars:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.putText(frame, "Car", (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        cv.imshow('frame', frame)

    cv.imshow('frame', frame)

# Clean up
me.streamoff()
me.land()
cv.destroyAllWindows()