#define the school class

class School:

    def __init__(self, id, name, capacity, address, city, state, zipCode, timeOfDay, startTime):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.timeOfDay = timeOfDay
        self.startTime = startTime
        #set variables not set in by parameters to dummy data to show that it is unset
        self.full = False
        self.longitude = -1
        self.latitue = -1
        self.studentList = []
        self.distanceMatrixPosition = -1

    def addStudent(self, student):
        if (self.full):
            return False
        self.studentList.append(student)
        student.timeOfDay = self.timeOfDay
        student.placed = True
        student.placementName = self.name
        student.placementId = self.id
        student.school = self
        if (len(self.studentList) >= self.capacity):
            self.full = True
        return True
        
        
