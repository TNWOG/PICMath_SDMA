
# coding: utf-8

# In[1]:


#import dependencies
API_KEY = '5b3ce3597851110001cf6248bf5e66acdc094c8c8277707805f99a57'
import pandas as pd
import numpy as np


# <h1>Generating Data</h1>

# In[2]:


#saves matrix as a CSV file
def distMatrixToCsv(M, filename, labels):
    data = pd.DataFrame(M, columns = labels)
    data.index = labels
    data.to_csv(filename, sep=",")


# In[23]:


#initialize ors client
import openrouteservice
import time
client = openrouteservice.Client(key=API_KEY) # Specify your personal API key
#get 2018 Lat Long data
latLong = pd.read_csv("SDMA_Student_LatLongGen.csv")
allData = list(zip(latLong['Longitude'], latLong['Latitude']))
#get school data from file
#get ids
ids = np.array(latLong['student ID'], dtype='int')
#initialize big array
masterDistMatrix = np.zeros((len(allData),len(allData)))
masterDuraMatrix = np.zeros((len(allData),len(allData)))
#generate 50x50 matrices and add to master matrix
#iterate over a 5x5 "grid"
for i in range(5):
    for j in range(5):
        #generate a distance and a duration matrix for a "driving-car" given the points
        matrix = client.distance_matrix(allData, profile="driving-car", metrics=("duration","distance"), sources=list(np.arange(50*i, 50*i+50)), destinations=list(np.arange(50*j,50*j+50)))
        #add generated matrix to master
        masterDistMatrix[50*i:50*i+50, 50*j:50*j+50] = np.array(matrix['distances'])
        masterDuraMatrix[50*i:50*i+50, 50*j:50*j+50] = np.array(matrix['durations'])
        #space processes so that api is happy
        time.sleep(1)
#generate outlier matrices
for i in range(5):
    #generate a distance and a duration matrix for a "driving-car" given the points
    matrix = client.distance_matrix(allData, profile="driving-car", metrics=("duration","distance"), sources=list(np.arange(50*i, 50*i+50)), destinations=[250])
    #add generated matrix to master
    masterDistMatrix[50*i:50*i+50, 250:251] = np.array(matrix['distances'])
    masterDuraMatrix[50*i:50*i+50, 250:251] = np.array(matrix['durations'])
    time.sleep(1)
for j in range(5):
    #generate a distance and a duration matrix for a "driving-car" given the points
    matrix = client.distance_matrix(allData, profile="driving-car", metrics=("duration","distance"), sources=[250], destinations=list(np.arange(50*j,50*j+50)))
    #add generated matrix to master
    masterDistMatrix[250:251, 50*j:50*j+50] = np.array(matrix['distances'])
    masterDuraMatrix[250:251, 50*j:50*j+50] = np.array(matrix['durations'])
    #space processes so that api is happy
    time.sleep(1)


# In[24]:


distMatrixToCsv(masterDistMatrix, 'distances.csv', ids)
distMatrixToCsv(masterDuraMatrix, 'durations.csv', ids)


# In[8]:


#initialize ors client
import openrouteservice
import time
client = openrouteservice.Client(key=API_KEY) # Specify your personal API key
#get 2018 Lat Long data
latLong = pd.read_csv("SDMA_Student_LatLongGen - student&School.csv")
allData = list(zip(latLong['Longitude'], latLong['Latitude']))
#get school data from file
#get ids
ids = np.array(latLong['student ID / school Name'])
#initialize big array
masterDistMatrix = np.zeros((len(allData),len(allData)))
masterDuraMatrix = np.zeros((len(allData),len(allData)))
#generate 50x50 matrices and add to master matrix
#iterate over a 5x5 "grid"
for i in range(5):
    for j in range(5):
        #generate a distance and a duration matrix for a "driving-car" given the points
        matrix = client.distance_matrix(allData, profile="driving-car", metrics=("duration","distance"), sources=list(np.arange(50*i, 50*i+50)), destinations=list(np.arange(50*j,50*j+50)))
        #add generated matrix to master
        masterDistMatrix[50*i:50*i+50, 50*j:50*j+50] = np.array(matrix['distances'])
        masterDuraMatrix[50*i:50*i+50, 50*j:50*j+50] = np.array(matrix['durations'])
        #space processes so that api is happy
        time.sleep(1)
#generate outlier matrices
for i in range(5):
    #generate a distance and a duration matrix for a "driving-car" given the points
    matrix = client.distance_matrix(allData, profile="driving-car", metrics=("duration","distance"), sources=list(np.arange(50*i, 50*i+50)), destinations=list(np.arange(250,260)))
    #add generated matrix to master
    masterDistMatrix[50*i:50*i+50, 250:260] = np.array(matrix['distances'])
    masterDuraMatrix[50*i:50*i+50, 250:260] = np.array(matrix['durations'])
    time.sleep(1)
for j in range(5):
    #generate a distance and a duration matrix for a "driving-car" given the points
    matrix = client.distance_matrix(allData, profile="driving-car", metrics=("duration","distance"), sources=list(np.arange(250,260)), destinations=list(np.arange(50*j,50*j+50)))
    #add generated matrix to master
    masterDistMatrix[250:260, 50*j:50*j+50] = np.array(matrix['distances'])
    masterDuraMatrix[250:260, 50*j:50*j+50] = np.array(matrix['durations'])
    #space processes so that api is happy
    time.sleep(1)
matrix = client.distance_matrix(allData, profile="driving-car", metrics=("duration","distance"), sources=list(np.arange(250,260)), destinations=list(np.arange(250,260)))
masterDistMatrix[250:260, 250:260] = np.array(matrix['distances'])
masterDuraMatrix[250:260, 250:260] = np.array(matrix['durations'])


# In[9]:


distMatrixToCsv(masterDistMatrix, 'distances_with_schools.csv', ids)
distMatrixToCsv(masterDuraMatrix, 'durations_with_schools.csv', ids)


# <h1>Read Data</h1>

# In[8]:


dist = pd.read_csv("distances.csv", delimiter=",", index_col=0)
dist.head()


# In[9]:


dura = pd.read_csv("durations.csv", delimiter=",", index_col=0)
dura.head()


# In[7]:


print(dura['1003'].loc[1001])

