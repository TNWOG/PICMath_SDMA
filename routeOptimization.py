import Route
import Time
import random
from copy import deepcopy

#ROUTE OPTIMIZATION FUCTIONS

#randomly swaps students and calls the greedyRouteSchoolsAtEnd routing algorithm
def randomSwaps(routeObjects, dataMatrix, numSwaps):
    
    
    #loop based on the number of swaps to check
    for x in range(numSwaps):
        #print(x)
        #copy the routeArray so that we don't make any unwanted changes
        routeArray = []
        for route in routeObjects:
            routeArray.append(route.copy())
        #pick to routes to randomly swap students
        #sample makes sure that the routes are not duplicated
        swapRoutes = random.sample(routeArray, 2)
        route1 = swapRoutes[0]
        route2 = swapRoutes[1]
        #route1oldTime = route1.averageDistance(dataMatrix)
        #route2oldTime = route2.averageDistance(dataMatrix)
        route1.generateRouteTimes(dataMatrix)
        route2.generateRouteTimes(dataMatrix)
        oldMetric1 = route1.mean
        oldMetric2 = route2.mean
        
        #pick a student from each route to swap
        route1student = deepcopy(route1.students[random.randint(0, len(route1.students)-1)])
        route2student = deepcopy(route2.students[random.randint(0, len(route2.students)-1)])
        #swap
        #remove students from their original list
        route1.students.remove(route1student)
        route2.students.remove(route2student)

        #add students to the other list
        route1.students.append(route2student)
        route2.students.append(route1student)
        #calculate routes and get the total distance of the routes after swapping
        route1.routeWithStartTimes(dataMatrix)
        route2.routeWithStartTimes(dataMatrix)
        #route1newTime = route1.averageDistance(dataMatrix)
        #route2newTime = route2.averageDistance(dataMatrix)
        route1.generateRouteTimes(dataMatrix)
        route2.generateRouteTimes(dataMatrix)
        newMetric1 = route1.mean
        newMetric2 = route2.mean

        #set the new routes if they are faster
        #if ((route1newTime < route1oldTime) and (route2newTime < route2oldTime)):
        if (newMetric1 < oldMetric1 and newMetric2 < oldMetric2):
            print("improve", newMetric1, oldMetric1, newMetric2, )
            routeObjects = deepcopy(routeArray)
    return routeObjects


#END OF ROUTE OPTIMIZATION FUNCTIONS

