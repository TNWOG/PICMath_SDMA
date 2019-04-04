import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
import School
import Time
import Stop

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
        unRouted = []
        for s in self.students:
            if s not in route:
                unRouted.append(s)
        
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
        unRouted = []
        for s in self.schools:
            if s not in route:
                unRouted.append(s)
                
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
        self.busTimes = []

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
            if student.school not in newSchools:
                newSchools.append(student.school)
        self.schools = newSchools.copy()
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
    
    def plot(self, map):
        
        lat = []
        long = []
        markers = []
        colors = ['yellow', 'green', 'blue', 'red', 'magenta', 'crimson', 'cyan', 'orange', 'navy', 'wheat', 'silver', 'plum', 'black']
        ax = map.show_mpl(figsize=(8,6))
        for e in self.stopsInOrder:
            x, y = map.to_pixels(e.latitue,e.longitude)
            lat.append(x)
            long.append(y)
            if e in self.schools:
                ax.plot(x, y, 'x', color = colors[e.id], zorder=10, label = e.name, markersize = 20)
                ax.annotate(e.startTime, (x,y))
            elif e in self.students:
                ax.plot(x, y, '.', color = colors[e.placementId], zorder=10, markersize = 20, linewidth = 2)
                ax.annotate(e.busTime, (x,y))
        ax.plot(lat, long, 'b', linewidth = 2)
        ax.relim()
        ax.autoscale()
        ax.legend()
        plt.savefig(str(self.busNumber) + '.png')
        plt.draw()
        #plt.legend()
        #plt.show()

    def simplify(self):
        cullList = []
        ids = [x.id for x in self.stopsInOrder]
        idsNoDupes = deepcopy(list(set(ids)))
        for num in idsNoDupes:
            if ids.count(num)>1:
                dupes = [i for i, x in enumerate(self.stopsInOrder) if x.id == num]
                cullList.extend(dupes[1:])
        for index in sorted(cullList, reverse=True):
            del self.stopsInOrder[index]
            
            
#===========BRUTEFORCE===============================
    #create smaller matrix from master distance matrix
    def GenerateMatrixFromMaster(self, cluster, masterMatrix):
        matrix = np.zeros((len(cluster),len(cluster)))
        for i in range(len(cluster)):
            for j in range(len(cluster)):
                matrix[i][j] = masterMatrix[cluster[i]][cluster[j]]
        return matrix
    #create smaller set of data from master array
    def GenerateDataFromMaster(self, cluster, fullData):
        return np.array([fullData[x] for x in cluster])
    
    def BFRouting(self, dataMatrix):
        indices = [x.distanceMatrixPosition for x in self.students]
        mat = self.GenerateMatrixFromMaster(indices, dataMatrix)
        data = list(zip([x.longitude for x in self.students], [x.latitue for x in self.students]))
        length, perm = self.TravellingSalesmanBF(mat, data, splits=2, FBProp=True, FBLoops=10)
        globalInd = [indices[x] for x in perm]
        schoolPerm, length = self.AddSchools(globalInd, dataMatrix, indices)
        self.stopsInOrder = []
        schoolInd = [x.distanceMatrixPosition for x in self.schools]
        for p in schoolPerm:
            if p in indices:
                self.stopsInOrder.append(self.students[indices.index(p)])
            elif p in schoolInd:
                self.stopsInOrder.append(self.schools[schoolInd.index(p)])
        
    def permutationDistances(self, a, l, r, M, minLen, minPerm, peekFor = None, peekBack = None): 
        #l = start, r = end
        if l==r: 
            curLength = 0
            #add the distances in the order of the permutation 
            for i in range(len(a)-1):
                #if the first element in array
                if i == 0:
                    #if peek is set
                    if peekFor is not None:
                        #add length of peek to array
                        curLength += M[peekFor][a[i]]
                if i == len(a)-2:
                    #if peek is set
                    if peekBack is not None:
                        #add length of peek to array
                        curLength += M[a[i+1]][peekBack]
                curLength += M[a[i]][a[i+1]]
            #if current minimum
            if curLength<minLen[0]:
                #clear reference arrays
                minLen.clear()
                minPerm.clear()
                #append new values
                minLen.append(curLength)
                minPerm.extend(a)
        else: 
            #recursively compute more permutations
            for i in range(l,r+1): 
                a[l], a[i] = a[i], a[l] 
                self.permutationDistances(a, l+1, r, M, minLen, minPerm, peekFor, peekBack) 
                a[l], a[i] = a[i], a[l]
            
    #bruteforce method for travelling salesman
    def TravellingSalesmanBF(self, M, data, splits = 1, peek = True, FBProp = False, FBLoops = 1):
        #generate indices of array
        #determines mean point
        mid = np.mean(data, axis=0)
        #get furthest from mean
        furthestPoint = np.linalg.norm(np.abs(data.copy()-mid),axis=1).argmax()
        #get all distances from furthest point
        dist = np.abs(data.copy()-np.array(data[furthestPoint]))
        #sort indexes according to distance from furthest point
        a = np.argsort(np.linalg.norm(dist,axis=1))
        #generate all possible permutations for indice list
        lengths = []
        print("Generating routes")
        #reshaping the array for n amount of splits
        final = []
        size = int(np.ceil(len(a)/splits))
        print(size, " size splits")
        k = 0
        while(size*k<len(a)):
            final.append(a[size*k:size+size*k])
            k+=1
        a = final
        #begin looping for number of loops
        for itr in range(FBLoops):
            minLens, perms = np.array([], dtype='int'), np.array([], dtype='int')
            #forward propagation
            for i in range(splits):
                #print(i)
                minLen = ([100000])
                minPerm = ([])
                #recursively determine permutation
                if peek:
                    if i == 0:
                        self.permutationDistances(a[i], 0, len(a[i])-1, M, minLen, minPerm)
                    else:
                        self.permutationDistances(a[i], 0, len(a[i])-1, M, minLen, minPerm, peekFor = a[i-1][len(a[i-1])-1]) 
                else:
                    self.permutationDistances(a[i], 0, len(a[i])-1, M, minLen, minPerm) 
                minLens = np.append(minLens, minLen)
                perms = np.append(perms, minPerm)
            #reshaping the array for n amount of splits
            final = []
            size = int(np.ceil(len(perms)/splits))
            k = 0
            while(size*k<len(perms)):
                final.append(perms[size*k:size+size*k])
                k+=1
            a = final
            #goes backwards if intended
            if(FBProp):
                minLens, perms = np.array([], dtype='int'), np.array([], dtype='int')
                for i in range(splits-1, -1, -1):
                    #print(i)
                    minLen = ([100000])
                    minPerm = ([])
                    #recursively determine permutation
                    if peek:
                        if i == splits-1:
                            minPerm = a[i]
                            curLength = 0
                            for j in range(len(a[i])-1):
                                curLength += M[a[i][j]][a[i][j+1]]
                            minLen = curLength
                        else:
                            self.permutationDistances(a[i], 0, len(a[i])-1, M, minLen, minPerm, peekBack = a[i+1][0]) 
                    else:
                        self.permutationDistances(a[i], 0, len(a[i])-1, M, minLen, minPerm) 
                    minLens = np.append(minLens, minLen)
                    perms = np.append(perms, minPerm)
                #reshaping the array for n amount of splits
                final = []
                size = int(np.ceil(len(perms)/splits))
                k = 0
                while(size*k<len(perms)):
                    beginInd = len(perms)-size-size*k
                    if beginInd<0:
                        beginInd = 0
                    final.append(perms[beginInd:len(perms)-size*k])
                    k+=1
                a = final.copy()
                a = np.array(final.copy())
                #convert back to 1-D array
                perms = a.flatten()
        #return length and indice array for minimal distance route.
        finalPerm = np.array([], dtype='int')
        for i in range(len(perms)):
            finalPerm = np.append(finalPerm, perms[i])
        return minLens.sum(), list(finalPerm)
    
    def AddSchools(self, perm, mat, indices):
        curSchools = [] 
        self.updateSchools()
        for p in range(len(perm)-1, -1, -1):
                for s in self.schools:
                    if self.students[indices.index(perm[p])].placementName == s.name and s not in [x[0] for x in curSchools]:
                        curSchools.append([s,p] )
        length = 0
        for c in curSchools:
            i = len(perm)
            minLen = 1000000000
            minPerm = []
            while i > c[1]:
                tempPerm = deepcopy(perm)
                tempPerm.insert(i, c[0].distanceMatrixPosition)
                curLen = 0
                for j in range(len(tempPerm)-1):
                    curLen += mat[tempPerm[j]][tempPerm[j+1]]
               
                if curLen < minLen :
                    minLen = curLen
                    minPerm = tempPerm
                i-= 1
            length = minLen
            perm = minPerm
        return perm, length
                    


#========================Route that accounts for start times=========================
#this algorithm starts with the last school in the route, build the route from the
#back to the front, and then flip the route. This algorithm takes into account start
#times


    def routeWithStartTimes(self, dataMatrix):
        #declare/define variables
        #the window of time that we can arrive before school starts
        window = Time.Time("0:15")
        #the array of Stop objects
        route = []
        #the array of Student and School objects that are encapsulated into Stops in the route array
        objectsInRoute = []

        #assign the students objects to the route
        for student in self.students:
            student.busRoute = self.busNumber

        #define school related variables
        #set the list of schools on the route to all the student's schools
        self.updateSchools()
        #order the schools based on start times from latest to earliest
        schools = self.schools.copy()
        schools.sort(reverse=True)
        #create a 2d array where the first subarray is all the students that attend the first school in schools array
        studentsInSchools = []
        for school in schools:
            schoolArray = []
            for student in self.students:
                if (student.school == school):
                    schoolArray.append(student)
            studentsInSchools.append(schoolArray)

        #loop for adding students in between schools on route
        for i in range(len(schools)-1):
            #add the first school to the route with the visit time set to the start time
            if (i == 0):
                route.append(Stop.Stop(schools[0], schools[0].startTime))
                objectsInRoute.append(schools[0])
                #print(schools[0])
            #for all other schools, add the school to the route and set the visit time to the time it takes to drive to there
            else:
                visitTime = route[len(route)-1].time - Time.Time(dataMatrix[route[len(route)-1].element.distanceMatrixPosition][schools[i].distanceMatrixPosition])
                route.append(Stop.Stop(schools[i], visitTime))
                objectsInRoute.append(schools[i])
                #print(schools[i])
            
            #the next loop find the as many students that will fit between school i and i+1
            #students are chosen from all unrouted students that attend schools in the route so far
            proceed = True
            infiniteLoopCheck = 0
            while (proceed and infiniteLoopCheck < 10):                                   
                potentialStudents = []
                #find all unrouted students that attend schools that have been added to the route
                for j in range(i+1):
                    #go through every student that attends the selected school
                    for student in studentsInSchools[j]:
                        #print(student, student.school)
                        #add to list of potentially routable students if they are not yet routed
                        if student not in objectsInRoute:
                            potentialStudents.append(student)
                #find the student with the minimum additional time between the end of the route and the next school to be added
                minStudent = potentialStudents[0]
                minValue = dataMatrix[route[len(route)-1].element.distanceMatrixPosition][potentialStudents[0].distanceMatrixPosition] + dataMatrix[potentialStudents[0].distanceMatrixPosition][schools[i+1].distanceMatrixPosition]
                for student in potentialStudents:
                    if (dataMatrix[route[len(route)-1].element.distanceMatrixPosition][student.distanceMatrixPosition] + dataMatrix[student.distanceMatrixPosition][schools[i+1].distanceMatrixPosition] < minValue):
                        minStudent = student
                        minValue = dataMatrix[route[len(route)-1].element.distanceMatrixPosition][student.distanceMatrixPosition] + dataMatrix[student.distanceMatrixPosition][schools[i+1].distanceMatrixPosition]

                #check to see if this student can be added to the route
                endOfRouteVisitTime = route[len(route)-1].time
                schoolStartTime = schools[i+1].startTime
                travelTime = Time.Time(minValue)
                if (endOfRouteVisitTime - travelTime > schoolStartTime - window):
                    visitTime = endOfRouteVisitTime - Time.Time(dataMatrix[route[len(route)-1].element.distanceMatrixPosition][minStudent.distanceMatrixPosition])
                    route.append(Stop.Stop(minStudent, visitTime))
                    objectsInRoute.append(minStudent)
                    #print(minStudent)
                #check to see if the time from the end of the route to the next school will fall in between the drop off window
                #recalculate the stop time for the end of the route because a student may have been added in the last if statement
                endOfRouteVisitTime = route[len(route)-1].time
                timeToNextSchool = endOfRouteVisitTime - Time.Time(dataMatrix[route[len(route)-1].element.distanceMatrixPosition][schools[i+1].distanceMatrixPosition])
                if (endOfRouteVisitTime - timeToNextSchool < schoolStartTime):
                    proceed = False
                else:
                    infiniteLoopCheck += 1
        
        #add the last school, but check if the last school is also the first
        if (len(schools) == 1):
            route.append(Stop.Stop(schools[0], schools[0].time))
            objectsInRoute.append(schools[0])
        else:
            endOfRouteVisitTime = route[len(route)-1].time
            visitTime = endOfRouteVisitTime - Time.Time(dataMatrix[route[len(route)-1].element.distanceMatrixPosition][schools[len(schools)-1].distanceMatrixPosition])
            route.append(Stop.Stop(schools[len(schools)-1], visitTime))
            objectsInRoute.append(schools[len(schools)-1])
        
        #loop until all student have been added to the route
        while (len(route) < len(self.schools) + len(self.students)):
            
            #find all the unrouted students
            potentialStudents = []
            for student in self.students:
                #add to list of potentially routable students if they are not yet routed
                if student not in objectsInRoute:
                    potentialStudents.append(student)
                        
            #find the unrouted student that is closest to the end of the route
            minStudent = potentialStudents[0]
            minValue = dataMatrix[route[len(route)-1].element.distanceMatrixPosition][potentialStudents[0].distanceMatrixPosition]
            for student in potentialStudents:
                if (dataMatrix[route[len(route)-1].element.distanceMatrixPosition][student.distanceMatrixPosition]):
                    minStudent = student
                    minValue = dataMatrix[route[len(route)-1].element.distanceMatrixPosition][student.distanceMatrixPosition]
                    
            #add the student to the route
            endOfRouteVisitTime = route[len(route)-1].time
            visitTime = endOfRouteVisitTime - Time.Time(dataMatrix[route[len(route)-1].element.distanceMatrixPosition][minStudent.distanceMatrixPosition])
            route.append(Stop.Stop(minStudent, visitTime))
            objectsInRoute.append(minStudent)
            #print(minStudent)

        #flip the route
        objectsInRoute = objectsInRoute[::-1]
        #add final route to the route's object
        self.stopsInOrder = objectsInRoute.copy()
        
    def generateRouteTimes(self, distMatrix):
        lastStop = self.stopsInOrder[-1]
        curTime = lastStop.startTime
        idx = self.stopsInOrder.index(lastStop)
        self.busTimes.insert(0,curTime)
        while idx > 0:
            duration = distMatrix[self.stopsInOrder[idx-1].distanceMatrixPosition][self.stopsInOrder[idx].distanceMatrixPosition]
            durationTime = Time.Time(duration)
            curTime = curTime-durationTime
            if self.stopsInOrder[idx-1] in self.schools:
                print(curTime, self.stopsInOrder[idx-1].startTime)
                if curTime>self.stopsInOrder[idx-1].startTime:
                    print("reset")
                    curTime = self.stopsInOrder[idx-1].startTime
            self.busTimes.insert(0,curTime)
            idx -= 1






            
    
    








