from djitellopy import Tello

tello = Tello()

tello.connect()
print(tello.get_battery())
tello.takeoff()

tello.move_up(20)
tello.move_forward(10)

while tello.get_battery() > 30:
    print(tello.get_battery())

tello.move_back(10)
tello.move_down(20)
tello.land()
