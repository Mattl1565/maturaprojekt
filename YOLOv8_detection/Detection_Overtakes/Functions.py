def track_id_in_list(track_id, carOrder):
    for car in carOrder:
        if car.getID() == track_id:
            return True
    return False