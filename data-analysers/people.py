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
    people.append(int(line[1]))
    lines.append(line[2].strip())

# for time, n, line in zip(times, people, lines):
filtered: list = [
    zip(*[(totals, times) for totals, times, line in zip(people, times, lines) if line == "All lines"]),
    zip(*[(filtered_U1, times_U1) for filtered_U1, times_U1, line in zip(people, times, lines) if line == "U1"]),
    zip(*[(filtered_U2, times_U2) for filtered_U2, times_U2, line in zip(people, times, lines) if line == "U2"]),
    zip(*[(filtered_U3, times_U3) for filtered_U3, times_U3, line in zip(people, times, lines) if line == "U3"]),
    zip(*[(filtered_U4, times_U4) for filtered_U4, times_U4, line in zip(people, times, lines) if line == "U4"]),
    zip(*[(filtered_U6, times_U6) for filtered_U6, times_U6, line in zip(people, times, lines) if line == "U6"]),
]
names = [
    "General People",
    "People U1",
    "People U2",
    "People U3",
    "People U4",
    "People U6",
]

fig, ax = plt.subplots(2, 6)
fig.set_size_inches(30, 15)

for el in range(6):
    # single_people_fig, single_people_ax = plt.subplots(1, 1)
    # single_people_fig.set_size_inches(20, 15)

    x, time = filtered[el]

    ax[0][el].hist(x, bins=40, label=names[el])
    ax[1][el].plot(time, x, label='Evolution of' + names[el])
    ax[0][el].legend(loc="upper right")
    ax[1][el].legend(loc="upper right")
    print(names[el])

fig.savefig("./img/people/people.svg")
# plt.show()
