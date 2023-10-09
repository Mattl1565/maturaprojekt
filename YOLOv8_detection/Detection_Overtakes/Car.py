class Car:
    def __init__(self, x, y, id, direction):
        self.x = x
        self.y = y
        self.id = id
        self.direction = direction

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getID(self):
        return self.id

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setID(self, id):
        self.id = id

    def setDirection(self, direction):
        self.direction = direction

    def getDirection(self, direction):
        self.direction = direction

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " id: " + str(self.id) + "direction: " + str(self.direction)