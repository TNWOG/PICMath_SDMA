#find index of the root student
def findRoot(dataMatrix):
    numRow = len(dataMatrix)
    numCol = len(dataMatrix[0])
    minValue = 0
    minIndex = 0
    
    #set minimum to first row
    i = 0
    while(i < numCol):
        minValue += dataMatrix[0][i]
        i += 1
    #traverse the matrix to find which row has the shortest cumulative distance to all other students
    i = 0
    while(i < numRow):
        j = 0
        rowTotal = 0
        while(j < numCol):
            rowTotal += dataMatrix[i][j]
            j += 1
        if(rowTotal < minValue):
            minValue = rowTotal
            minIndex = i
        i += 1
    return minIndex

#find the index of the student that is the furthest from the root
def furthestFromRoot(rootRow):
    furthest = rootRow.index(max(rootRow))
    return furthest

#finds the student that is closest to the last routed student without overlapping
def findNext(routedStudents, dataMatrix):
    #make and array of the distance from the last student in the route to all the students
    distances = dataMatrix[routedStudents[len(routedStudents)-1]]
    #set all the routed students' distances to the max of the array
    for student in routedStudents:
        distances[student] = max(distances)
    #find the student that is closest to the last student in the route
    nextStudent = distances.index(min(distances))
    return nextStudent

#builds a route in the form of an array
def spanningTree(dataMatrix):
    #an array of indexes of students that have been routed
    routedStudents = []
    #find the root student. It is and integer that represents the student at that row and column
    root = findRoot(dataMatrix)
    #find starting point of route.
    start = furthestFromRoot(dataMatrix[root])
    routedStudents.append(start)
    #build route
    n = 0
    while(n < (len(dataMatrix) - 1)):
        nextStudent = findNext(routedStudents, dataMatrix)
        routedStudents.append(nextStudent)
        n += 1
    return routedStudents



    
    
    
