#imports
import pandas as pd
import csv
from copy import deepcopy

#BEGIN CLUSTERING FUNCTIONS

#BEGIN HELPER FUNCTIONS

#read from .csv to matrix, removing first column and row
def metricCSVtoMatrix(filename):
    data = list(csv.reader(open(filename)))
    data.pop(0)
    for row in data:
        row.pop(0)
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    return data

#finds the student with the maximum total distance to all other students
#if two students have equal distance totals, the one with the lowest index wins
def findStartSeed(dataMatrix, studentsToCluster):
    numRow = len(dataMatrix)
    numCol = len(dataMatrix[0])
    maxStudent = studentsToCluster[0]
    maxValue = 0
    
    #traverse the matrix to find which row has the largest cumulative distance to all other students
    for potentialSeed in studentsToCluster:
        seedTotal = 0
        for student in studentsToCluster:
            seedTotal += dataMatrix[potentialSeed.distanceMatrixPosition][student.distanceMatrixPosition]
        if (seedTotal > maxValue):
            maxValue = seedTotal
            maxStudent = potentialSeed
    return maxStudent
    
#finds the next cluster seed based
def findNextSeed(dataMatrix, seeds, studentsToCluster):
    numRow = len(dataMatrix)
    numCol = len(dataMatrix[0])
    numSeeds = len(seeds)
    maxValue = 0
    maxStudent = studentsToCluster[0]

    #check each student as a potential next seed
    for potentialSeed in studentsToCluster:
        seedTotal = 0
        #find the total distance to all other seeds
        for seed in seeds:
            seedTotal += dataMatrix[potentialSeed.distanceMatrixPosition][seed.distanceMatrixPosition]
        if (seedTotal > maxValue):
            maxValue = seedTotal
            maxStudent = potentialSeed
    return maxStudent
    

#finds the next student for the specified cluster
def findNextStudent(dataMatrix, clusterMatrix, clusterNumber, studentsToCluster):
    minValue = 0
    minStudent = 0
    numStudents = len(dataMatrix)
    numStudentsInCluster = len(clusterMatrix[clusterNumber])

    #SET MINIMUM VALUE
    #create a list of students and remove all that have been placed
    unclusteredStudents = studentsToCluster.copy()
    for cluster in clusterMatrix:
        for student in cluster:
            if (unclusteredStudents.count(student) > 0):
                            unclusteredStudents.remove(student)
    #set the minimum total distance to the first student not in a cluster
    minStudent = deepcopy(unclusteredStudents[0])
    for x in range(len(clusterMatrix[clusterNumber])):
        minValue += dataMatrix[unclusteredStudents[0].distanceMatrixPosition][clusterMatrix[clusterNumber][x].distanceMatrixPosition]

    #FIND STUDENT WITH MINIMUM TOTAL DISTANCE
    for potentialNext in unclusteredStudents:
        total = 0
        for student in clusterMatrix[clusterNumber]:
            total += dataMatrix[potentialNext.distanceMatrixPosition][student.distanceMatrixPosition]
        if (total < minValue):
            minValue = total
            minStudent = potentialNext
    return minStudent



#END OF HELPER FUNCTIONS


#take in the master distance matrix, the number of clusters to make, and a list of student to break into those clusters
#returns a 2d array of student objects. Each array represents a cluster.
def calClusterMethod(dataMatrix, numClusters, studentsToCluster):
    clusteredStudents = 0
    numberOfStudents = len(studentsToCluster)
    #SEEDS
    #declare the seeds for the clusters and the cluster matrix
    seeds = []
    #find the first seed
    seed = deepcopy(findStartSeed(dataMatrix, studentsToCluster))
    studentsToCluster.remove(seed)
    seeds.append(seed)
    #find remaining seeds
    while (len(seeds) < numClusters):
        seed = deepcopy(findNextSeed(dataMatrix, seeds, studentsToCluster))
        studentsToCluster.remove(seed)
        seeds.append(seed)
    #CLUSTER
    #create empty 2d array that can be appended.
    #set the number of rows to the number of seeds
    clusters = seeds.copy()
    i = 0
    while (i < len(seeds)):
        clusters[i] = []
        #assign the first value in the cluster to the seed
        clusters[i].append(seeds[i])
        clusteredStudents += 1
        i += 1
    #add students to the clusters
    while (clusteredStudents < numberOfStudents):
        i = 0
        while (i < len(seeds) and clusteredStudents < numberOfStudents):
            clusters[i].append(findNextStudent(dataMatrix, clusters, i, studentsToCluster))
            clusteredStudents += 1
            i += 1    
    return clusters
    
    
#END OF CLUSTERING FUNCTIONS


