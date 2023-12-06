class Car:
    def __init__(self, x, y, id):
        self.screenTime = 1
        self.y = y
        self.x = x
        self.id = id
        self.direction = 2
        self.overtaking = False
        self.screenTime = 0
        self.busted = False

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
    def setScreenTime(self, screenTime):
        self.screenTime = screenTime

    def setOvertaking(self, overtaking):
        self.overtaking = overtaking

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y
        self.screenTime += 1

    def setID(self, id):
        self.id = id

    def setDirection(self, direction):
        self.direction = direction

    def setBusted(self, busted):
        self.busted = busted
    def __str__(self):
        if(self.direction == 0):
            return "x: " + str(self.x) + " y: " + str(self.getY()) + " id: " + str(self.id) + " direction: " + "down"
        elif(self.direction == 1):
            return "x: " + str(self.x) + " y: " + str(self.getY()) + " id: " + str(self.id) + " direction: " + "up"
        else:
            return "x: " + str(self.x) + " y: " + str(self.getY()) + " id: " + str(self.id) + " direction: " + "unknown"