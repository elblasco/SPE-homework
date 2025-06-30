#!/usr/bin/env pyton3

import matplotlib.pyplot as plt
import csv

csv_reader = csv.reader(open('../output/delay.csv', mode ='r'))

time_percentage: list = []
lines: list = []

next(csv_reader)

for line in csv_reader:
    time_percentage.append(float(line[1]) / float(line[0]))
    lines.append(line[2].strip())

filtered_u1 = [time for time, line in zip(time_percentage, lines) if line == "U1"]
filtered_u2 = [time for time, line in zip(time_percentage, lines) if line == "U2"]

_, ax = plt.subplots(1, 3)
ax[0].hist(time_percentage, bins=20)
ax[1].hist(filtered_u1, bins=20)
ax[2].hist(filtered_u2, bins=20)

plt.show()