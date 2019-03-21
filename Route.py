class Route:
    #import Student

    #Private helper functions for route building
    #find the starting student
    def __greedyFindStart(self, dataMatrix):
        maxValue = 0
        maxStudent = self.students[0]
        
        #find student with largest disance to all other students
        for potentialRoot in self.students:
            total = 0
            for student in self.students:
                total += dataMatrix[potentialRoot.distanceMatrixPosition][student.distanceMatrixPosition]
            if (total > maxValue):
                maxValue = total
                maxStudent = potentialRoot
        return maxStudent
    
    #finds the student that is closest to the last routed student without overlapping
    def __greedyFindNext(self, dataMatrix, route):
        #make and array unrouted students 
        if len(list(set(self.students) - set(route))) == 0:
            print("AHHH")
        unRouted = list(set(self.students) - set(route))
        minStudent = unRouted[0]
        minValue = dataMatrix[route[len(route)-1].distanceMatrixPosition][unRouted[0].distanceMatrixPosition]
        #find the closest student out of all the unrouted students
        for student in unRouted:
            if (dataMatrix[route[len(route)-1].distanceMatrixPosition][student.distanceMatrixPosition] < minValue):
                minStudent = student
                minValue = dataMatrix[route[len(route)-1].distanceMatrixPosition][student.distanceMatrixPosition]
        return minStudent
                
        #finds the school that is closest to the last stop overlapping
    def __greedyFindNextSchool(self, dataMatrix, route):
        #make and array unrouted schools 
        unRouted = list(set(self.schools) - set(route))
        minSchool = unRouted[0]
        minValue = dataMatrix[route[len(route)-1].distanceMatrixPosition][unRouted[0].distanceMatrixPosition]
        #find the closest student out of all the unrouted students
        for school in unRouted:
            if (dataMatrix[route[len(route)-1].distanceMatrixPosition][school.distanceMatrixPosition] < minValue):
                minSchool = school
                minValue = dataMatrix[route[len(route)-1].distanceMatrixPosition][school.distanceMatrixPosition]
        return minSchool

    #find the index of the a student in the routes student array
    #this is necessary because the .index() function compares references to students, not actual students
    def __studentIndex(self, studentToFind):
        i = 0
        for student in self.students:
            if (student == studentToFind):
                return int(i)
            i += 1

    #find the index of the a school in the routes school array
    #this is necessary because the .index() function compares references to schools, not actual schools
    def __schoolIndex(self, studentToFind):
        i = 0
        for school in self.schools:
            if (school == schoolToFind):
                return int(i)
            i += 1

    #find the index of the a stop (school or student) in the routes stopsInOrder array
    #this is necessary because the .index() function compares references to stops, not actual objects
    def __stopIndex(self, stopToFind):
        i = 0
        for stop in self.stopsInOrder:
            if (stop == stopToFind):
                return int(i)
            i += 1
        return -1










    
    #public functions
    #constructor
    def __init__(self, busNumber, capacity, timeOfDay):
        #set by parameters in the constructor
        self.busNumber = busNumber
        self.capacity = capacity
        self.timeOfDay = timeOfDay
        #not set by parameters
        self.students = []
        self.schools = []
        self.stopsInOrder = []
        self.distanceMatrix = []

    #copy constructor
    def copy(self):
        newRoute = Route(self.busNumber, self.capacity, self.timeOfDay)
        newRoute.students = self.students.copy()
        newRoute.schools = self.schools.copy()
        newRoute.stopsInOrder = self.stopsInOrder.copy()
        newRoute.distanceMatrix = self.distanceMatrix.copy()
        return newRoute

    #updates a the list of what schools the route needs to stop at.
    #useful if the students on the route have changed 
    def updateSchools(self):
        newSchools = []
        for student in self.students:
            school = [student.school]
            newSchools = list(set(newSchools) | set(school))
        self.schools = newSchools
        return len(self.schools)

    #just adds the the students to the route and then the schools. There is no ordering
    def combineStudentsAndSchools(self):
        newRoute = []
        for student in self.students:
            newRoute.append(student)
        for school in self.schools:
            newRoute.append(school)
        self.stopsInOrder = newRoute

    #The greedy routing algorithm I described in class
    def greedyRouteSchoolsAtEnd(self, dataMatrix):
        #update the list of schools that need to be in route
        self.updateSchools()

        #assign the students objects to the route
        for student in self.students:
            student.busRoute = self.busNumber
        
        #an array of students that have been routed
        route = []
        
        #find the start student. 
        route.append(self.__greedyFindStart(dataMatrix))
        
        #add students to route
        while (len(route) < len(self.students)):
            route.append(self.__greedyFindNext(dataMatrix, route))
            
        #add schools to route
        while (len(route) < len(self.students) + len(self.schools)):
            route.append(self.__greedyFindNextSchool(dataMatrix, route))
            
        #store the route in the route object's stopsInOrder
        self.stopsInOrder = route

        
    #finds the average distance. 
    def averageDistance(self, dataMatrix):
        numStudents = len(self.students)
        cummulativeDistance = 0

        #find the length of the bus ride for every student
        for student in self.students:
            studentDistance = 0
            #find the index of the student and school
            studentIndex = self.__stopIndex(student)
            schoolIndex = self.__stopIndex(student.school)

            for i in range(studentIndex, schoolIndex - 1):
                studentDistance += dataMatrix[self.stopsInOrder[i].distanceMatrixPosition][self.stopsInOrder[i + 1].distanceMatrixPosition]
            #add the students time to the total
            cummulativeDistance += studentDistance
        averageDistance = cummulativeDistance / numStudents
        return averageDistance
        

    #finds the length of the route from start to finish
    def distance(self, dataMatrix):
        n = 0
        cummulativeDistance = 0
        numStops = len(self.stopsInOrder)
        while (n < numStops - 1):
            cummulativeDistance += dataMatrix[self.stopsInOrder[n].distanceMatrixPosition][self.stopsInOrder[n + 1].distanceMatrixPosition]
            n += 1
        return cummulativeDistance


    
