class Car:
    def __init__(self, x, y, id):
        self.screenTime = 1
        self.y = []  # Initialize as an empty list
        self.x = x
        self.setY(y)  # Use setY method to add the initial y value
        self.id = id
        self.direction = 2

    def getX(self):
        return self.x

    def getY(self):
        return self.y[len(self.y) - 1]

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
        if len(self.y) > 5:
            self.y.pop(0)
        self.y.append(y)
        self.screenTime = self.screenTime + 1

    def setID(self, id):
        self.id = id

    def setDirection(self, direction):
        if(self.screenTime > 5):
            self.direction = direction
        else:
            self.direction = 2

    def getMeanY(self):
        non_none_values = [value for value in self.y if value is not None]
        if non_none_values:
            sumi = sum(non_none_values)
            return sumi / len(non_none_values)
        else:
            return 0

    def __str__(self):
        if(self.direction == 0):
            return "x: " + str(self.x) + " y: " + str(self.y) + " id: " + str(self.id) + " direction: " + "down"
        elif(self.direction == 1):
            return "x: " + str(self.x) + " y: " + str(self.y) + " id: " + str(self.id) + " direction: " + "up"
        else:
            return "x: " + str(self.x) + " y: " + str(self.y) + " id: " + str(self.id) + " direction: " + "unknown"