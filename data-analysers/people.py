#!/usr/bin/env pyton3

import matplotlib.pyplot as plt
import csv

csv_reader = csv.reader(open('../output/people.csv', mode ='r'))

# time_instant: list = []
# people: list = []
times: list = []
stations: dict = []
people: list = []

next(csv_reader)

for line in csv_reader:
    times.append(float(line[0]))
    people.append(float(line[1]))
    stations.append(line[2].strip())

totals, times = zip(*[(p, t) for p, t,  station in zip(people, times,  stations) if station == "All lines"])


print(len(totals))

_, ax = plt.subplots(1, 2)

ax[0].hist(totals, bins=20)
ax[1].plot(times, totals)
plt.show()