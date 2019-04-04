class Stop:

    def __init__(self, element, time):
        self.element = element
        self.time = time

    def __str__(self):
        return str(self.element) + " " + str(self.time) + ","
