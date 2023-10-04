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