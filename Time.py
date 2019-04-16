#military time
class Time:

    #constructor
    def __init__(self, data):
        #set the time of day if given
        if (type(data) == str):
            split = data.index(':')
            self.hour = int(data[:split])
            self.minute = int(data[split+1:split+3])
            self.second = 0
        else:
            seconds = round(data)
            self.minute, self.second = divmod(seconds, 60)
            self.hour, self.minute = divmod(self.minute, 60)
            if (self.hour == 0):
                self.hour == 24
            

    #override print operator
    def __str__(self):
        if self.minute >= 10:
            return str(int(self.hour)) + ":" + str(int(self.minute))
        else:
            return str(int(self.hour)) + ":0" + str(int(self.minute))


#================Addition and subtraction=======================================
    #add another time object
    def __add__(self, other):
        #default value
        timeSum = Time(0)
        
        #adding another time object
        if (type(other) == Time):
            #seconds
            second = self.second + other.second
            if (second >= 60):
                second = second % 60
                carrySecond = 1
            else:
                carrySecond = 0

            #minutes
            minute = self.minute + other.minute + carrySecond
            if (minute >= 60):
                minute = minute % 60
                carryMinute = 1
            else:
                carryMinute = 0

            #hours
            hour = self.hour + other.hour + carryMinute
            if (hour >= 24):
                hour = hour % 24

            #assign
            timeSum.second = second
            timeSum.minute = minute
            timeSum.hour = hour
            return timeSum
        return timeSum

    #subract another time
    def __sub__(self, other):
        #default value
        timeDif = Time(0)
        
        #adding another time object
        if (type(other) == Time):
            #seconds
            second = self.second - other.second
            if (second < 0):
                second = 60 + second
                carrySecond = 1
            else:
                carrySecond = 0

            #minutes
            minute = self.minute - other.minute - carrySecond
            if (minute < 0):
                minute = 60 + minute
                carryMinute = 1
            else:
                carryMinute = 0

            #hours
            hour = self.hour - other.hour - carryMinute
            if (hour >= 24):
                hour = hour % 24

            #assign
            timeDif.second = int(second)
            timeDif.minute = int(minute)
            timeDif.hour = int(hour)
            return timeDif
        return timeDif


#========================boolean operators======================================
    #equality requires the hours, minutes, and seconds to match
    def __eq__(self, other):
        if (type(other) != 'Time'):
            return False
        if (self.hour == other.hour and self.minute == other.minute and self.second == other.second):
            return True
        else:
            return False
        
    def __ne__(self, other):
        if (type(other) != 'Time'):
            return True
        if (self.hour == other.hour and self.minute == other.minute and self.second == other.second):
            return False
        else:
            return True

    def __lt__(self, other):
        if (type(other) != 'Time'):
            return False
        if (self.hour < other.hour):
            return True
        elif (self.hour == other.hour and self.minute < other.minute):
            return True
        elif (self.hour == other.hour and self.minute == other.minute and self.second < other.second):
            return True
        else:
            return False
        
    def __gt__(self, other):
        if (type(other) != 'Time'):
            return False
        if (self.hour > other.hour):
            return True
        elif (self.hour == other.hour and self.minute > other.minute):
            return True
        elif (self.hour == other.hour and self.minute == other.minute and self.second > other.second):
            return True
        else:
            return False
        
    def __le__(self, other):
        return self == other or self < other
    
    def __ge__(self, other):
        return self == other or self > other


