#import clustering as cl
import routeOptimization as ro
import Student
import School
import Route
import pandas as pd
import numpy as np
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

#make master distance matrix
#this will be replaced by code that builds the distance matrix based on geocode data
masterDistanceMatrix = cl.metricCSVtoMatrix('durations_with_schools.csv')



#create arrays to store the student and school objects
studentObjects = []
schoolObjects = []

#create students from file
#set master distance matrix index as well. That will be changed later.
#create schools from file
x = 0
while (x < len(schoolMatrix)):
    schoolObjects.append(School.School(schoolMatrix[x][0], schoolMatrix[x][1], schoolMatrix[x][2], schoolMatrix[x][3], schoolMatrix[x][4], schoolMatrix[x][5],
                                  schoolMatrix[x][6], schoolMatrix[x][7], schoolMatrix[x][8]))
    x += 1

x = 0
while (x < len(studentMatrix)):
    studentObjects.append(Student.Student(studentMatrix[x][0], studentMatrix[x][1], studentMatrix[x][2], studentMatrix[x][3], studentMatrix[x][4], studentMatrix[x][5],
                                     studentMatrix[x][6], studentMatrix[x][7], studentMatrix[x][8], studentMatrix[x][9], studentMatrix[x][10], studentMatrix[x][11]))
    studentObjects[x].distanceMatrixPosition = x
    if not np.isnan(studentMatrix[x][13]):
        studentObjects[x].originalRoute = studentMatrix[x][13]
        studentObjects[x].originalPickup= Time.Time(studentMatrix[x][12])
        stuSchool = [i for i in schoolObjects if i.name == studentMatrix[x][14]]
        print(studentMatrix[x][14], [i.name for i in schoolObjects])
        if len(stuSchool)>0:
            studentObjects[x].school = stuSchool[0]
            studentObjects[x].placementId = stuSchool[0].id
            studentObjects[x].placementName = stuSchool[0].name
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
busRouteNums = np.unique([x.originalRoute for x in studentObjects if x.originalRoute>=0])
routes = []
for i in busRouteNums:
    newRoute = Route.Route(i, float('inf'), 'N/A')
    newRoute.students.extend([x for x in studentObjects if x.originalRoute == i])
    newRoute.updateSchools()
    newRoute.combineStudentsAndSchools()
    print(newRoute.stopsInOrder)
    routes.append(newRoute)
'''
#save all the data to an output .csv file
#students
with open('studentOutputData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['id', 'pref1', 'pref2', 'pref3', 'pref4', 'pref5', 'lockedIn', 'address', 'city', 'state', 'zipCode', 'bussing', 'placementName', 'timeOfDay'])
    for student in studentObjects:
        writer.writerow([student.id, student.pref1,student.pref2,student.pref3,student.pref4,student.pref5,student.lockedIn, student.address, student.city, student.state, student.zipCode,  student.bussing, student.placementName, student.timeOfDay])
'''
