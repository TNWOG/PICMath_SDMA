class Time:

    #constructor
    def __init__(self, text):
        if ('a' in text or 'A' in text):
            self.timeOfDay = 'AM'
        else:
            self.timeOfDay = 'PM'
        split = text.index(':')
        self.hour = int(text[:split])
        self.minute = int(text[split+1:split+3])

    #override print operator
    def __str__(self):
        return str(self.hour) + ":" + str(self.minute) + self.timeOfDay




testy = Time("8:05 p.m")
print(testy)
