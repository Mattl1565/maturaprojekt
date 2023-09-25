from djitellopy import tello
import cv2
from time import sleep

# Connect to Tello
me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()

#enable mission pads
me.enable_mission_pads()
me.set_mission_pad_detection_direction(0)

me.takeoff()

print(me.get_mission_pad_id())

# me.go_xyz_speed_mid(-100, 0, 0, 50, 5)
# me.go_xyz_speed_mid(100, 0, 0, 50, 2)


while True:
    img = me.get_frame_read().frame
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if(me.get_mission_pad_id() == 2):
        me.land()
        break


    # if 'q' land
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break