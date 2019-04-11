import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Time


data = pd.read_csv("baseRouteStudentInfo.csv")
durations = np.array(data['duration'].values)
baseBusTimes = []
for d in durations:
    if not pd.isnull(d):
        t = Time.Time(d)
        baseBusTimes.append((t.hour*60+t.minute)*60)
baseBusTimes = np.array(baseBusTimes)
data = pd.read_csv("routeStudentInfo.csv")
durations = np.array(data['duration'].values)
busTimes = []
for d in durations:
    if not pd.isnull(d):
        t = Time.Time(d)
        busTimes.append((t.hour*60+t.minute)*60)
busTimes = np.array(busTimes)
f, ax = plt.subplots()
ax.set_ylabel('duration of ride (seconds)')
ax.boxplot([baseBusTimes, busTimes], labels=['Original', 'Algorithm'], widths=0.7)
