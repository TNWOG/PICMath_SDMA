import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Time


data = pd.read_csv("baseRouteStudentInfo_generated.csv")
durations = np.array(data['duration'].values)
baseBusTimes = []
for d in durations:
    if not pd.isnull(d):
        t = Time.Time(d)
        baseBusTimes.append((t.hour*60+t.minute)*60)
baseBusTimes = np.array(baseBusTimes)
data = pd.read_csv("routeStudentInfo.csv")
durations = np.array(data['duration'].values)
routeBusTimes = []
busTimes2 = []
busTimes = []
for d in durations:
    if not pd.isnull(d):
        if d == "NEXT":
            routeBusTimes.append(busTimes2)
            busTimes2 = []
        else:
            t = Time.Time(d)
            busTimes.append((t.hour*60+t.minute)*60)
            busTimes2.append((t.hour*60+t.minute)*60)
    
busTimes = np.array(busTimes)
f, ax = plt.subplots()
ax.set_ylabel('duration of ride (seconds)')
ax.boxplot([baseBusTimes, busTimes], labels=['Original', 'Algorithm'], widths=0.7, meanline=True, showmeans=True)
plt.savefig('boxplot.png')

f, ax = plt.subplots()
ax.set_ylabel('duration of ride (seconds)')
ax.set_xlabel('route number')
ax.boxplot(routeBusTimes, widths=0.7, meanline=True, showmeans=True)
plt.savefig('routeBoxplot.png')



data = pd.read_csv("studentOutputData.csv")
num1 = 0
denom1 = 0
num2 = 0
denom2 = 0
schools = np.unique(data['placementName'].dropna().values)
placementProbs = np.zeros((len(schools),2))
for index, row in data.iterrows():
    if not pd.isnull(row['pref1']):
        placementProbs[np.where(schools==row['pref1']),1]+= 1
        denom1 += 1
        if row['pref1']==row['placementName']:
            placementProbs[np.where(schools==row['pref1']),0]+= 1
            num1 += 1
plt.figure(figsize=(30,3))
plt.title("Probability of First Preferences")
plt.bar(schools, placementProbs[:,0]/placementProbs[:,1])
plt.savefig('algplace1.png')
schools = np.unique(data['placementName'].dropna().values)
print(np.sum(placementProbs[:,0]), np.sum(placementProbs[:,1]))
algPlace1 = np.sum(placementProbs[:,0])/np.sum(placementProbs[:,1])
placementProbs = np.zeros((len(schools),2))
for index, row in data.iterrows():
    if not pd.isnull(row['pref1']):
        denom2 += 1
        placementProbs[np.where(schools==row['pref2']),1]+= 1
        if row['pref2']==row['placementName'] and row['pref1']!=row['placementName']:
            num2 += 1
            placementProbs[np.where(schools==row['pref2']),0]+= 1
plt.figure(figsize=(30,3))
plt.title("Probability of Second Preferences")
plt.bar(schools, placementProbs[:,0]/placementProbs[:,1])
plt.savefig('algplace2.png')
algPlace2 = np.sum(placementProbs[:,0])/np.sum(placementProbs[:,1])
data = pd.read_csv('studentInputData.csv')
placementProbs = np.zeros((len(schools),2))
for index, row in data.iterrows():
    placementProbs[np.where(schools==row['preference1']),1]+= 1
    if row['preference1']==row['base placement']:
        placementProbs[np.where(schools==row['preference1']),0]+= 1
plt.figure(figsize=(30,3))
plt.title("Probability of First Preferences")
plt.bar(schools, placementProbs[:,0]/placementProbs[:,1])
plt.savefig('origplace1.png')
origPlace1 = np.sum(placementProbs[:,0])/np.sum(placementProbs[:,1])
placementProbs = np.zeros((len(schools),2))
for index, row in data.iterrows():
    placementProbs[np.where(schools==row['preference2']),1]+= 1
    if row['preference2']==row['base placement'] and row['preference1']!=row['base placement']:
        placementProbs[np.where(schools==row['preference2']),0]+= 1
plt.figure(figsize=(30,3))
plt.title("Probability of Second Preferences")
plt.bar(schools, placementProbs[:,0]/placementProbs[:,1])
plt.savefig('origplace2.png')
origPlace2 = np.sum(placementProbs[:,0])/np.sum(placementProbs[:,1])


plt.figure(figsize=(5,3))
plt.title("Probability of First Preferences")
plt.bar(["orignal", "algorithm"], [origPlace1, algPlace1])
plt.ylim(0,1)
plt.savefig('place1')

plt.figure(figsize=(5,3))
plt.title("Probability of First or Second Preferences")
plt.bar(["orignal", "algorithm"], [origPlace1+origPlace2, algPlace1+algPlace2])
plt.ylim(0,1)
plt.savefig('place2')
