#define the school class
import pandas as pd
import Time
class School:

    def __init__(self, id, name, capacity, address, city, state, zipCode, timeOfDay, startTime, endTime):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.timeOfDay = timeOfDay
        self.startTime = Time.Time(startTime)
        self.endTime = Time.Time(endTime)
        #set variables not set in by parameters to dummy data to show that it is unset
        self.full = False
        self.longitude = -1
        self.latitue = -1
        self.studentList = []
        self.distanceMatrixPosition = -1

    def __eq__(self, other):
        if (self.id == other.id):
            return True
        return False
    
    #overloading less than and greater than for sorting based on start times
    def __lt__(self, other):
        return self.startTime < other.startTime

    def __gt__(self, other):
        return self.startTime > other.startTime

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.name + ' ' + str(self.startTime)

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
    def geocode(self, API_KEY):
        data = pd.read_csv("SDMA_Student_LatLongGen - student&School.csv")
        studentRow = data.iloc[self.distanceMatrixPosition]
        self.longitude = studentRow['Longitude']
        self.latitue = studentRow['Latitude']
        
