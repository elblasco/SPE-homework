#!/usr/bin/env pyton3

import csv

# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt

csv_reader = csv.reader(open('../output/people_served.csv', mode='r'))

# time_instant: list = []
# people: list = []
times: list = []
lines: list = []
people: list = []

next(csv_reader)

for line in csv_reader:
    times.append(float(line[0]))
    people.append(int(line[1]))

filtered_times, filtered_time_diff, filtered_people = list(
    zip(*[(times[i], times[i] - times[i - 1], people[i]) for i in range(1, len(times))]))

fig, ax = plt.subplots(1, 2)
fig.set_size_inches(40, 15)

ax[0].hist(filtered_people, weights=filtered_time_diff, bins=40, label="People served")
ax[0].legend(loc="upper right")
ax[1].plot(filtered_times, filtered_people, label="People served")
ax[1].legend(loc="upper right")

print(sum(filtered_people))

fig.savefig("./img/people-served/people-served.svg")
