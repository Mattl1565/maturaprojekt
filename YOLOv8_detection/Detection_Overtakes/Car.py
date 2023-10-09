class Car:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.direction = 2

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

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setID(self, id):
        self.id = id

    def setDirection(self, direction):
        self.direction = direction



    def __str__(self):
        if(self.direction == 0):
            return "x: " + str(self.x) + " y: " + str(self.y) + " id: " + str(self.id) + " direction: " + "down"
        elif(self.direction == 1):
            return "x: " + str(self.x) + " y: " + str(self.y) + " id: " + str(self.id) + " direction: " + "up"
        else:
            return "x: " + str(self.x) + " y: " + str(self.y) + " id: " + str(self.id) + " direction: " + "unknown"