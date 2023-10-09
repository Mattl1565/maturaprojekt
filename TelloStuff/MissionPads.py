from turtle import right

from djitellopy import tello
import cv2
from time import sleep

# Connect to Tello
me = tello.Tello()
me.connect()
print("Batteriestand: ")
print(me.get_battery())

me.streamon()

#enable mission pads
me.enable_mission_pads()
me.set_mission_pad_detection_direction(0)

#me.takeoff()

print("Mission-Pad-ID: ")
print(me.get_mission_pad_id())

me.takeoff()
me.move_down(20)
me.move_left(50)


print("Mission-Pad-ID: ")
print(me.get_mission_pad_id())

me.land()

# me.go_xyz_speed_mid(-100, 0, 0, 50, 5)
# me.go_xyz_speed_mid(100, 0, 0, 50, 2)


#while True:
#    img = me.get_frame_read().frame
#    cv2.imshow("Image", img)
#    cv2.waitKey(1)

#    if(me.get_mission_pad_id() == 3):
#        me.move_right(50)
#        break



#    # if 'q' land
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        me.land()
#        break