#Define the student class
import openrouteservice
import numpy as np
import pandas as pd
import Time

class Student:

    def __init__(self, id, pref1, pref2, pref3, pref4, pref5, lockedIn, address, city, state, zipCode, bussing):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.pref1 = str(pref1)
        self.pref2 = str(pref2)
        self.pref3 = str(pref3)
        self.pref4 = str(pref4)
        self.pref5 = str(pref5)
        #will need to be changed to something more universal
        if (bussing == 'x'):
            self.bussing = True
        else:
            self.bussing = False
        #will need to be changed to something more universal
        if (lockedIn == 'X'):
            self.lockedIn = True
        else:
            self.lockedIn = False
            
        #set variables not set in by parameters to dummy data to show that it is unset
        self.timeOfDay = ""
        self.placed = False
        self.placementName = ""
        self.placementId = -1
        self.school = None
        self.busTime = Time.Time(0)
        self.busRoute = -1
        self.longitude = -1
        self.latitue = -1
        self.distanceMatrixPosition = -1
        self.originalRoute = -1
        self.originalPickup = -1


    def __eq__(self, other):
        if (self.id == other.id):
            return True
        return False

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return str(self.id)


    def geocode(self, API_KEY):
        data = pd.read_csv("SDMA_Student_LatLongGen - student&School.csv")
        studentRow = data.loc[data['student ID / school Name'] == str(int(self.id))]
        self.longitude = studentRow['Longitude'].values[0]
        self.latitue = studentRow['Latitude'].values[0]
        
        '''
        import time
        client = openrouteservice.Client(key=API_KEY)
        queryText = str(str(self.address) + ", " + str(self.city) + ", " + str(self.state) + " " + str(int(self.zipCode)))
        query = openrouteservice.geocode.pelias_autocomplete(client, queryText)
        if query['features']:
            features = query['features'][0]
            coordinates = features['geometry']['coordinates']
            print(coordinates)
            self.longitude = coordinates[0]
            self.latitude = coordinates[1]
        else:
            print("FAIL", queryText)
        time.sleep(0.5)
        '''

