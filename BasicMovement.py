from djitellopy import tello
from time import sleep

# Connect to Tello
me = tello.Tello()
me.connect()
print(me.get_battery())

# Takeoff
me.takeoff()
me.send_rc_control(0, -60, 0, 0)
sleep(2)
me.send_rc_control(0, 0, 0, 0)
me.land()

