import cv2
from djitellopy import tello
from time import sleep
import numpy as np
import KeyPressModule as kp

############# Parameters ##############
fSpeed = 117/10  # Forward Speed in cm/s (15cm/s)
aSpeed = 360/10  # Angular Speed Degrees/s (50d/s)
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval
########################################

x, y = 300, 500
a = 0
yaw = 0
points = [(0, 0), (0, 0)]

kp.init()

me = tello.Tello()
me.connect()
print(me.get_battery())


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aSpeed = 50
    d = 0
    global yaw, a, x, y
    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = +aSpeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = -aSpeed
        yaw += aInterval

    if kp.getKey("q"):
        me.land()
    if kp.getKey("e"):
        me.takeoff()

    sleep(interval)
    a += yaw
    x += int(d * np.cos(np.radians(a)))
    y += int(d * np.sin(np.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500)/100},{(points[-1][1] - 500)/100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)


while True:
    if me.get_battery() < 5:
        me.land()
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    points.append([vals[4], vals[5]])
    img = np.zeros((1000, 1000, 3), np.uint8)
    drawPoints(img, points)
    cv2.imshow("Output", img)
