class CarData:
    def __init__(self, car_ids):
        self.car_data = {car_id: {'meanLast5': []} for car_id in car_ids}

    def update_mean_last_5(self, car_id, y_coordinate):
        if len(self.car_data[car_id]['meanLast5']) < 5:
            self.car_data[car_id]['meanLast5'].append(y_coordinate)
        else:
            self.car_data[car_id]['meanLast5'].pop(0)
            self.car_data[car_id]['meanLast5'].append(y_coordinate)

    def get_mean_last_5(self, car_id):
        return sum(self.car_data[car_id]['meanLast5']) / len(self.car_data[car_id]['meanLast5'])
