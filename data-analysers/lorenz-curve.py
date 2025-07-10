#!/usr/bin/env pyton3

import csv

# noinspection PyUnresolvedReferences
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
import numpy as np

csv_reader = csv.reader(open('../output/board_time.csv', mode='r'))

TIME_TO_BOARD = 0
LORENZ = 1
NAME = 2

filtered: dict = {
    "All": ([], [], "General Board Time (minutes)"),
    "U1": ([], [], "Board Time U1 (minutes)"),
    "U2": ([], [], "Board Time U2 (minutes)"),
    "U3": ([], [], "Board Time U3 (minutes))"),
    "U4": ([], [], "Board Time U4 (minutes))"),
    "U6": ([], [], "Board Time U6 (minutes))"),
}

next(csv_reader)

csv_entries = []

for line in csv_reader:
    time_to_board_min = float(line[3])
    line = line[2].strip()

    csv_entries.append((time_to_board_min, line))

sorted(csv_entries, key=lambda x: x[TIME_TO_BOARD])

for time_to_board_min, line in csv_entries:
    filtered["All"][TIME_TO_BOARD].append(time_to_board_min)
    filtered[line][TIME_TO_BOARD].append(time_to_board_min)

for key in filtered.keys():
    sums = 0
    times = filtered[key][TIME_TO_BOARD]
    n = len(times)
    m = np.mean(times)
    mad = 0
    for xi in times:
        sums += xi
        mad += abs(xi - m)
        filtered[key][LORENZ].append(sums / (n * m))
    mad = mad / n
    gap = mad / (2 * m)

    # Code for the `Gini coefficient` we used the approximate version
    # since it is so much faster and still quite accurate
    # sums = 0
    # for xi in times:
    #     for xj in times:
    #         sums += abs(xi - xj)
    # gini = sums / (n * (n - 1) * 2 * m)
    approx_gini = gap * (1.5 - 0.5 * gap)

    print(filtered[key][NAME], "has a gap of", gap, "[Gini approx from Lorenz", approx_gini, "]")

fig, ax = plt.subplots(2, 3)
fig.set_size_inches(20, 15)

for idx, value in enumerate(filtered.values()):
    single_lorenz_fig, single_lorenz_ax = plt.subplots(1, 1)
    single_lorenz_fig.set_size_inches(20, 15)
    name = value[NAME]
    li = value[LORENZ]

    n = len(li)
    x = [i / n for i in range(n)]

    ax[int(idx / 3)][idx % 3].plot(x, li, label=name)
    ax[int(idx / 3)][idx % 3].legend(loc="upper right")
    single_lorenz_ax.plot(x, li, label=name)
    single_lorenz_ax.legend(loc="upper right")
    single_lorenz_fig.savefig(f"lorenz-{idx}.svg")

fig.savefig('lorenz-tot.svg')
