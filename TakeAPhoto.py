from djitellopy import Tello
import cv2
import time

tello = Tello()
tello.connect()
tello.streamon()

count = 0
vidcap = cv2.VideoCapture(tello.get_udp_video_address())

success, image = vidcap.read()

while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
    success, image = vidcap.read()
    print('Read a new frame: ', success)
    cv2.imwrite("Resources/Images/frame%d.jpg" % count, image) # save frame as JPEG file
    count = count + 5

tello.streamoff()
tello.end()