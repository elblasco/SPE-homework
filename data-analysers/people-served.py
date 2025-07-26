#!/usr/bin/env pyton3

import csv
import math
import os

import matplotlib.pyplot as plt
import numpy as np

MOVING_AVG_SIZE = 30


def least_square(times: list, measurements: list, m: int):
    y: list = measurements
    x: list = times
    A: list = []

    for entry in x:
        A.append([entry ** i for i in range(m + 1)])

    AT = np.transpose(A)
    inv_mul = np.linalg.inv(np.matmul(AT, A))
    b: list = np.matmul(np.matmul(inv_mul, AT), y)

    return np.flip(b)

def norm_pdf(x, mu, var):
    return (1 / (math.sqrt(2 * math.pi * var))) * math.exp(- (((x - mu) ** 2) / (2 * var)))


def moving_average(x, w):
    cumsum_vec = np.cumsum(np.insert(x, 0, 0))
    return (cumsum_vec[w:] - cumsum_vec[:-w]) / w


def main():
    os.makedirs("./img/people-served", exist_ok=True)
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

    fig, ax = plt.subplots(1, 1)
    ax.plot(filtered_times, filtered_people, label="People served in 10 minutes")
    ax.legend(loc="upper right")
    ax.plot(filtered_times[int(math.ceil((MOVING_AVG_SIZE - 1) / 2)): -int((MOVING_AVG_SIZE - 1) / 2)],
            moving_average(filtered_people, MOVING_AVG_SIZE),
            label=f"Moving average (window {MOVING_AVG_SIZE})")
    ax.legend(loc="upper right")

    ax.set_xlabel("Snapshot time")
    ax.set_ylabel("People served")

    fig.set_size_inches(7, 5)
    fig.savefig("./img/people-served/people-served-plot.svg")

    fig, ax = plt.subplots(1, 1)

    ax.scatter(filtered_times, filtered_people, label='People served in 10 minutes', color='grey')
    ax.set_xlabel("Snapshot time")
    ax.set_ylabel("People served")

    for rank in range(1, 4):
        trend = least_square(filtered_times, filtered_people, rank)
        w = np.linspace(0, int(filtered_times[-1]), int(filtered_times[-1]))
        z = [np.polyval(trend, i) for i in w]
        ax.plot(w, z, label=f"lstsqr - {rank}")
        ax.legend(loc="upper right")

    fig.set_size_inches(9, 5)
    fig.savefig("./img/people-served/people-served-scatter.svg")

    fig, ax = plt.subplots(1, 1)
    avg = np.mean(filtered_people)
    var = np.var(filtered_people)

    max_v = max(filtered_people)
    min_v = min(filtered_people)
    xline = np.arange(min_v, max_v + 1)
    yline = [norm_pdf(x, avg, var) for x in xline]

    ax.hist(filtered_people, weights=filtered_time_diff, bins=80, label="People served in 10 minutes", density=True)
    ax.plot(xline, yline, color="orange" , label="Normal distribution")
    ax.axvline(x=avg, color='r', linestyle='dashed', label="Average people served")
    ax.legend(loc="upper right")
    ax.set_xlabel("People served")
    ax.set_ylabel("Normalised distribution")

    fig.set_size_inches(7, 5)
    fig.savefig("./img/people-served/people-served-hist.svg")

    print("Average (np)", avg, "with var", var, "and total over period", sum(filtered_people))


if __name__ == "__main__":
    main()
