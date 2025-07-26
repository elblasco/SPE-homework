#!/usr/bin/env pyton3

import csv
import math
import os

import matplotlib.pyplot as plt
import numpy as np

MOVING_AVG_SIZE = 50

def least_square(timing: list, measurements: list, m: int):
    y: list = measurements
    x: list = timing
    A: list = []

    for entry in x:
        A.append([entry ** i for i in range(m + 1)])

    AT: list = np.transpose(A)
    inv_mul = np.linalg.inv(np.matmul(AT, A))
    b: list = np.matmul(np.matmul(inv_mul, AT), y)

    return np.flip(b)

def norm_pdf(x, mu, var):
    return (1 / (math.sqrt(2 * math.pi * var))) * math.exp(- (((x - mu) ** 2) / (2 * var)))

def moving_average(x, w):
    cumsum_vec = np.cumsum(np.insert(x, 0, 0))
    return (cumsum_vec[w:] - cumsum_vec[:-w]) / w

def main():
    os.makedirs("./img/people", exist_ok=True)
    csv_reader = csv.reader(open('../output/people.csv', mode='r'))

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
        "People waiting",
        "People waiting on U1",
        "People waiting on U2",
        "People waiting on U3",
        "People waiting on U4",
        "People waiting on U6",
    ]

    for el in range(6):
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(10, 4)

        xs, time = filtered[el]
        avg = np.mean(xs)

        ax.hist(xs, bins=80, label=names[el], density=True)
        ax.axvline(x=avg, color='r', linestyle='dashed', label="Mean of people waiting")
        ax.set_xlabel("People")
        ax.set_ylabel("Normalised distribution")
        ax.legend(loc="upper right")
        fig.savefig(f"./img/people/people-{names[el]}-histo.svg")

        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(10, 4)

        ax.plot([0.0] + list(time), [0.0] + list(xs), label='Evolution of ' + names[el])
        ax.plot([0.0] + list(time[int(math.ceil((MOVING_AVG_SIZE - 1) / 2)): -int((MOVING_AVG_SIZE - 1) / 2)]),
                [0.0] + list(moving_average(xs, MOVING_AVG_SIZE)),
                label=f"Moving average (window {MOVING_AVG_SIZE})")
        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("People")
        ax.legend(loc="lower right")
        fig.savefig(f"./img/people/people-{names[el]}-plot.svg")

        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(10, 4)

        ax.scatter(time, xs, label='People waiting', color='grey')
        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("People waiting")

        for rank in range(1, 4):
            trend = least_square(time, xs, rank)
            w = np.linspace(0, int(times[-1]), int(times[-1]))
            z = [np.polyval(trend, i) for i in w]
            ax.plot(w, z, label=f"lstsqr - {rank}")
            ax.legend(loc="upper right")
        fig.savefig(f"./img/people/people-{names[el]}-scatter.svg")

        print(names[el],"has average", avg)

if __name__=="__main__":
    main()