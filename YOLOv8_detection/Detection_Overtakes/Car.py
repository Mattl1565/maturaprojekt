class Car:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

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

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " id: " + str(self.id)