class Car:
    def __init__(self, x, y, id):
        self.screenTime = 1
        self.y = y
        self.x = x
        self.old_y = 0
        self.old_x = 0
        self.id = id
        self.direction = 2
        self.overtaking = False
        self.screenTime = 0
        self.busted = False
        self.speeding = False
        self.speed = 0
        self.time_old = 0
        self.time_currently = 0
        self.speed_values = []

    def getScreenTime(self):
        return self.screenTime

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getID(self):
        return self.id

    def getDirection(self):
        return self.direction

    def getDirectionString(self):
        if(self.direction == 0):
            return "down"
        elif(self.direction == 1):
            return "up"
        else:
            return "unknown"

    def getOvertaking(self):
        return self.overtaking

    def getBusted(self):
        return self.busted

    def getSpeed(self):
        return self.speed

    def getOldX(self):
        return self.old_x

    def getOldY(self):
        return self.old_y
    def setTime(self, time):
        self.time_old = self.time_currently
        self.time_currently = time
    def setScreenTime(self, screenTime):
        self.screenTime = screenTime

    def setOvertaking(self, overtaking):
        self.overtaking = overtaking

    def setX(self, x):
        self.x = x

    def setY(self, y, mpp):
        self.old_y = self.y
        self.y = y
        self.screenTime += 1
        if self.screenTime > 2:
            speed = (((self.y[0] - self.old_y[0]) * mpp) / (self.time_currently - self.time_old) * 3.6)
            speed = round(speed, 1)
            self.speed_values.append(speed)

            if len(self.speed_values) > 5:
                self.speed_values = self.speed_values[-5:]

            mean_speed = sum(self.speed_values) / len(self.speed_values)

            # Update self.speed with the rounded speed value
            self.speed = round(mean_speed, 1)

    def setOldX(self, old_x):
        self.old_x = old_x

    def setOldY(self, old_y):
        self.old_y = old_y

    def setID(self, id):
        self.id = id

    def setDirection(self, direction):
        self.direction = direction

    def setBusted(self, busted):
        self.busted = busted

    def setSpeed(self, speed):
        self.speed = speed

    def __str__(self):
        if(self.direction == 0):
            return "x: " + str(self.x) + " y: " + str(self.getY()) + " id: " + str(self.id) + " direction: " + "down"
        elif(self.direction == 1):
            return "x: " + str(self.x) + " y: " + str(self.getY()) + " id: " + str(self.id) + " direction: " + "up"
        else:
            return "x: " + str(self.x) + " y: " + str(self.getY()) + " id: " + str(self.id) + " direction: " + "unknown"