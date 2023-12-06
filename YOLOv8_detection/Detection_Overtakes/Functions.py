def track_id_in_list(track_id, list):
    for car in list:
        if car.getID() == track_id:
            return True
    return False

def is_car_visible(car, track_ids):
    if car.getID() in track_ids:
        return True
    else:
        return False

def isSortedUp(list_cars):
    for i in range(len(list_cars) - 1):
        if list_cars[i].getY() > list_cars[i + 1].getY():
            if list_cars[i].getOvertaking() == True:
                return True
            list_cars[i].setOvertaking(True)
            return False
    return True

def isSortedDown(list_cars):
    for i in range(len(list_cars) - 1):
        if list_cars[i].getY() < list_cars[i + 1].getY():
            if list_cars[i].getOvertaking() == True:
                return True
            list_cars[i].setOvertaking(True)
            return False
    return True

def get_direction_from_Dict(track_id, CarDict):
    return CarDict[track_id].getDirectionString()

def get_direction(track_id, list_cars):
    for car in list_cars:
        if car.getID() == track_id:
            return car.getDirectionString()


def get_overtaking(track_id, CarDict):
    return CarDict[track_id].getOvertaking()

def get_id(track_id, CarDict):
    return CarDict[track_id].getID()

def check_if_passed_line(car, line_y):
    print("car.y[0]: " + str(car.y[0]))
    if car.y[0] > line_y:
        return True
    else:
        return False

