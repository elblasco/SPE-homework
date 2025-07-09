#!/usr/bin/env pyton3

import csv

# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt

csv_reader = csv.reader(open('../output/people.csv', mode='r'))

# time_instant: list = []
# people: list = []
times: list = []
lines: list = []
people: list = []

next(csv_reader)

for line in csv_reader:
    times.append(float(line[0]))
    people.append(float(line[1]))
    lines.append(line[2].strip())

# totals = []
# times = []
# filtered_U1 = []
# times_U1 = []
# filtered_U2 = []
# times_U2 = []
# filtered_U3 = []
# times_U3 = []
# filtered_U4 = []
# times_U4 = []
# filtered_U6 = []
# times_U6 = []
#
# for time, n, line in zip(times, people, lines):
totals, times = zip(*[(p, t) for p, t, line in zip(people, times, lines) if line == "All lines"])
filtered_U1, times_U1 = zip(*[(p, t) for p, t, line in zip(people, times, lines) if line == "U1"])
filtered_U2, times_U2 = zip(*[(p, t) for p, t, line in zip(people, times, lines) if line == "U2"])
filtered_U3, times_U3 = zip(*[(p, t) for p, t, line in zip(people, times, lines) if line == "U3"])
filtered_U4, times_U4 = zip(*[(p, t) for p, t, line in zip(people, times, lines) if line == "U4"])
filtered_U6, times_U6 = zip(*[(p, t) for p, t, line in zip(people, times, lines) if line == "U6"])

_, ax = plt.subplots(2, 6)

ax[0][0].hist(totals, bins=20)
ax[0][1].hist(filtered_U1, bins=20)
ax[0][2].hist(filtered_U2, bins=20)
ax[0][3].hist(filtered_U3, bins=20)
ax[0][4].hist(filtered_U4, bins=20)
ax[0][5].hist(filtered_U6, bins=20)
ax[1][0].plot(times, totals, label='Total')
ax[1][1].plot(times_U1, filtered_U1, label='Line U1')
ax[1][2].plot(times_U2, filtered_U2, label='Line U2')
ax[1][3].plot(times_U3, filtered_U3, label='Line U3')
ax[1][4].plot(times_U4, filtered_U4, label='Line U4')
ax[1][5].plot(times_U6, filtered_U6, label='Line U6')

plt.show()
