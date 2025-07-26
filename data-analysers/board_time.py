#!/usr/bin/env pyton3

import csv
import os

import matplotlib.pyplot as plt
import numpy as np

QUANTILES = [0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999]

os.makedirs("./img/board_time", exist_ok=True)
csv_reader = csv.reader(open('../output/board_time.csv', mode='r'))

arrival_times_h: list = []
time_to_board_min: list = []
lines: list = []
n_people: list = []

next(csv_reader)

for line in csv_reader:
    arrival_times_h.append(float(line[0]) / 24.0)
    lines.append(line[2].strip())
    time_to_board_min.append(float(line[3]))
    n_people.append(float(line[4]))

filtered: list = [
    (time_to_board_min, arrival_times_h, n_people),
    zip(*[(time_to_board, arrival, n_p) for time_to_board, arrival, line, n_p in zip(time_to_board_min, arrival_times_h, lines, n_people) if
          line == "U1"]),
    zip(*[(time_to_board, arrival, n_p) for time_to_board, arrival, line, n_p in zip(time_to_board_min, arrival_times_h, lines, n_people) if
          line == "U2"]),
    zip(*[(time_to_board, arrival, n_p) for time_to_board, arrival, line, n_p in zip(time_to_board_min, arrival_times_h, lines, n_people) if
          line == "U3"]),
    zip(*[(time_to_board, arrival, n_p) for time_to_board, arrival, line, n_p in zip(time_to_board_min, arrival_times_h, lines, n_people) if
          line == "U4"]),
    zip(*[(time_to_board, arrival, n_p) for time_to_board, arrival, line, n_p in zip(time_to_board_min, arrival_times_h, lines, n_people) if
          line == "U6"]),
]

names = [
    "Time to board",
    "Board time U1",
    "Board time U2",
    "Board time U3",
    "Board time U4",
    "Board time U6",
]

fig, ax = plt.subplots(3, 4)
fig.set_size_inches(20, 15)

for el in range(6):
    single_hist, single_hist_ax = plt.subplots(1, 1)
    single_hist.set_size_inches(8, 4)

    single_plot, single_plot_ax = plt.subplots(1, 1)
    single_plot.set_size_inches(8, 4)

    i = el % 3
    j = int(el / 3) * 2

    print("Processing", names[el])
    times_to_board, arrival_times, n_people = filtered[el]

    mean = np.average(times_to_board, weights=n_people)
    quantiles = np.quantile(times_to_board, QUANTILES, weights=n_people, method="inverted_cdf")

    # General image
    ax[i][j].hist(times_to_board, weights=n_people, bins=80, label=names[el], density=True)
    ax[i][j].axvline(x=mean, color='red', linestyle='dashed', label="Mean")
    ax[i][j].axvline(x=quantiles[0], color='green', linestyle='dashed', label=f"{QUANTILES[0]} quantile")
    ax[i][j].axvline(x=quantiles[1], color='purple', linestyle='dashed', label=f"{QUANTILES[1]} quantile")
    ax[i][j].axvline(x=quantiles[2], color='orange', linestyle='dashed', label=f"{QUANTILES[2]} quantile")
    ax[i][j].set_xlabel("Time (minutes)")
    ax[i][j].set_ylabel("Normalized distribution")
    ax[i][j + 1].plot(arrival_times, times_to_board, label=names[el])
    ax[i][j + 1].set_xlabel("Time since simulation start (days)")
    ax[i][j + 1].set_ylabel("Time to board (minute)")

    # Single image
    single_hist_ax.hist(times_to_board, weights=n_people, bins=80, label=names[el], density=True)
    single_hist_ax.axvline(x=mean, color='red', linestyle='dashed', label="Mean")
    single_hist_ax.axvline(x=quantiles[0], color='green', linestyle='dashed', label=f"{QUANTILES[0]} quantile")
    single_hist_ax.axvline(x=quantiles[1], color='purple', linestyle='dashed', label=f"{QUANTILES[1]} quantile")
    single_hist_ax.axvline(x=quantiles[2], color='orange', linestyle='dashed', label=f"{QUANTILES[2]} quantile")
    single_hist_ax.set_xlabel("Time (minutes)")
    single_hist_ax.set_ylabel("Normalized distribution")
    single_plot_ax.plot(arrival_times, times_to_board, label=names[el])
    single_plot_ax.set_xlabel("Time since simulation start (days)")
    single_plot_ax.set_ylabel("Time to board (minute)")


    ax[i][j + 1].axhline(y=mean, color='r', linestyle='dashed', label="Mean (minutes)")
    single_plot_ax.axhline(y=mean, color='r', linestyle='dashed', label="Mean (minutes)")

    ax[i][j].legend(loc="upper right")
    ax[i][j + 1].legend(loc="upper right")
    single_hist_ax.legend(loc="upper right")
    single_plot_ax.legend(loc="upper right")

    single_hist.savefig(f"./img/board_time/time-{names[el]}.svg")
    single_plot.savefig(f"./img/board_time/evolution-{names[el]}.svg")

    print(names[el], "mean", mean, "quantiles of", QUANTILES, "are", quantiles)

fig.savefig('./img/board_time/board_time.png')
