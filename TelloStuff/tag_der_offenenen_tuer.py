from djitellopy import Tello

tello = Tello()

tello.connect()
print(tello.get_battery())
tello.takeoff()

tello.move_up(200)
tello.move_forward(100)

while tello.get_battery() > 20:
    print(tello.get_battery())

tello.move_back(100)
tello.move_down(200)
#tello.move_forward(30)

tello.land()