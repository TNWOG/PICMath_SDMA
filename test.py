import clustering as cl
import routeOptimization as ro
import Student
import School
import Route
import pandas as pd
import csv
import Time

API_KEY = '5b3ce3597851110001cf6248bf5e66acdc094c8c8277707805f99a57'

#Read in data from file and construct arrays of the data structures
#read in csv to a matrix without the headers
studentCsv = pd.read_csv("studentInputData.csv", delimiter=',')
studentNoHeader = studentCsv[0:]
studentMatrix = studentNoHeader.values

#read in csv to a matrix without the headers
schoolCsv = pd.read_csv("schoolInputData.csv", delimiter=',')
schoolNoHeader = schoolCsv[0:]
schoolMatrix = schoolNoHeader.values

#read in csv to a matrix without the headers
routeCsv = pd.read_csv("routeInputData.csv", delimiter=',')
routeNoHeader = routeCsv[0:]
routeMatrix = routeNoHeader.values

#make master distance matrix
#this will be replaced by code that builds the distance matrix based on geocode data
masterDistanceMatrix = cl.metricCSVtoMatrix('durations_with_schools.csv')


#create arrays to store the student and school objects
studentObjects = []
schoolObjects = []
routeObjects = []

#create students from file
#set master distance matrix index as well. That will be changed later.
x = 0
while (x < len(studentMatrix)):
    studentObjects.append(Student.Student(studentMatrix[x][0], studentMatrix[x][1], studentMatrix[x][2], studentMatrix[x][3], studentMatrix[x][4], studentMatrix[x][5],
                                     studentMatrix[x][6], studentMatrix[x][7], studentMatrix[x][8], studentMatrix[x][9], studentMatrix[x][10], studentMatrix[x][11]))
    studentObjects[x].distanceMatrixPosition = x
    x += 1

#create schools from file
x = 0
while (x < len(schoolMatrix)):
    schoolObjects.append(School.School(schoolMatrix[x][0], schoolMatrix[x][1], schoolMatrix[x][2], schoolMatrix[x][3], schoolMatrix[x][4], schoolMatrix[x][5],
                                  schoolMatrix[x][6], schoolMatrix[x][7], schoolMatrix[x][8]))
    x += 1

#create routes from file
x = 0
while (x < len(routeMatrix)):
    routeObjects.append(Route.Route(routeMatrix[x][0], routeMatrix[x][1], routeMatrix[x][2]))
    x += 1

#set the school's master distance matrix index. This will need to be changed later
#this allows us to find an objects position in the distance matrix easily.
#the student objects have their values set in the loop where they are constructed
schoolObjects[0].distanceMatrixPosition = 251
schoolObjects[1].distanceMatrixPosition = 251
schoolObjects[2].distanceMatrixPosition = 252
schoolObjects[3].distanceMatrixPosition = 253
schoolObjects[4].distanceMatrixPosition = 254
schoolObjects[5].distanceMatrixPosition = 254
schoolObjects[6].distanceMatrixPosition = 256
schoolObjects[7].distanceMatrixPosition = 256
schoolObjects[8].distanceMatrixPosition = 257
schoolObjects[9].distanceMatrixPosition = 258
schoolObjects[10].distanceMatrixPosition = 259
for s in schoolObjects:
    s.geocode(API_KEY)
#placement
#place locked in students
for school in schoolObjects:
    for student in studentObjects:
        #if the school is not full and the student is locked in, place the student
        if ((not school.full) and (student.lockedIn) and (student.pref1 == school.name) and (not student.placed)):
            school.addStudent(student)

#place students with no bussing needs in 1st preference until school is full
for school in schoolObjects:
    for student in studentObjects:
        #if the school is not full and the student doesn't need bussing, place the student
        if ((not school.full) and (not student.bussing) and (student.pref1 == school.name) and (not student.placed)):
            school.addStudent(student)
            
#place students with bussing needs in 1st preference until school is full
for school in schoolObjects:
    for student in studentObjects:
        #if the school is not full, place the student
        if ((not school.full) and (student.pref1 == school.name) and (not student.placed)):
            school.addStudent(student)

#place students with no bussing needs in 2st preference until school is full
for school in schoolObjects:
    for student in studentObjects:
        #if the school is not full and the student is locked in, place the student
        if ((not school.full) and (not student.bussing) and (student.pref2 == school.name) and (not student.placed)):
            school.addStudent(student)
            
#place students with bussing needs in 2st preference until school is full
for school in schoolObjects:
    for student in studentObjects:
        #if the school is not full and the student is locked in, place the student
        if ((not school.full) and (student.pref2 == school.name) and (not student.placed)):
            school.addStudent(student)

#place in closest possible school
for student in studentObjects:
    #make a list of all schools that are not full
    availableSchools = []
    for school in schoolObjects:
        if (not school.full):
            availableSchools.append(school)
    #set the school with minimum distance to the first school
    minSchool = availableSchools[0]
    #find the closest school to the current student
    for school in availableSchools:
        if (masterDistanceMatrix[student.distanceMatrixPosition][school.distanceMatrixPosition] < masterDistanceMatrix[student.distanceMatrixPosition][minSchool.distanceMatrixPosition]):
            minSchool = school
    #Check to make sure the student is not a headstart student. This code will neeed to be changed later
    #add the student to the closest school    
    if ((student.pref1 != 'nan') and (not student.placed)):
        minSchool.addStudent(student)

            
#CLUSTERING
#make list of am and pm bussing students and their place in master distance matrix
amBussingStudents = []
for student in studentObjects:
    if ((student.bussing) and (student.timeOfDay == 'AM')):
        amBussingStudents.append(student)
pmBussingStudents = []
for student in studentObjects:
    if ((student.bussing) and (student.timeOfDay == 'PM')):
        pmBussingStudents.append(student)

for e in amBussingStudents:
    e.geocode(API_KEY)
for e in pmBussingStudents:
    e.geocode(API_KEY)

#determine the number of routes needed for am and pm routes and make arrays of each
numAmRoutes = 0
amRoutes = []
numPmRoutes = 0
pmRoutes = []
for route in routeObjects:
    if (route.timeOfDay == 'AM'):
        numAmRoutes += 1
        amRoutes.append(route)
    if (route.timeOfDay == 'PM'):
        numPmRoutes += 1
        pmRoutes.append(route)

#make the clsuters
amClusterMatrix = cl.calClusterMethod(masterDistanceMatrix, numAmRoutes, amBussingStudents)
pmClusterMatrix = cl.calClusterMethod(masterDistanceMatrix, numPmRoutes, pmBussingStudents)

#assign clustered students to routing objects' student list
#create an initial route
for i in range(numAmRoutes):
    amRoutes[i].students = amClusterMatrix[i].copy()
    amRoutes[i].routeWithStartTimes(masterDistanceMatrix)
    #amRoutes[i].BFRouting(masterDistanceMatrix)
    #for student in amRoutes[i].students:
        #print(student.school.name)
    print(Time.Time(amRoutes[i].averageDistance(masterDistanceMatrix)))
for i in range(numPmRoutes):
    pmRoutes[i].students = pmClusterMatrix[i].copy()
    pmRoutes[i].routeWithStartTimes(masterDistanceMatrix)
    #pmRoutes[i].BFRouting(masterDistanceMatrix)
    print(Time.Time(pmRoutes[i].averageDistance(masterDistanceMatrix)))

print("Swap")
#improve the routes with random swapping
amRoutes = ro.randomSwaps(amRoutes, masterDistanceMatrix, 1000)
pmRoutes = ro.randomSwaps(pmRoutes, masterDistanceMatrix, 1000)

import smopy
map = smopy.Map(( 44.82,-92.02, 44.95,-91.8))

#assign improved routes to the routeObjects array
routeObjects = amRoutes + pmRoutes

for route in routeObjects:
    #simplify routes
    #route.simplify()
    #plot route
    #route.plot(map)
    print(*route.stopsInOrder)
    print(Time.Time(route.averageDistance(masterDistanceMatrix)))



#save all the data to an output .csv file
#students
with open('studentOutputData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for student in studentObjects:
        writer.writerow([student.id, student.pref1, student.placementName, student.bussing, student.busRoute])

#schools
with open('schoolOutputData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for school in schoolObjects:
        writer.writerow([school.id, school.name, school.capacity])

#routes
with open('routeOutputData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for route in routeObjects:
        writer.writerow([route.busNumber, route.averageDistance(masterDistanceMatrix), route.updateSchools()])








        
