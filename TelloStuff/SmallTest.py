from djitellopy import Tello

tello = Tello()

tello.connect()
print(tello.get_battery())
tello.takeoff()

tello.move_left(30)

tello.rotate_clockwise(90)
tello.move_forward(30)

tello.land()