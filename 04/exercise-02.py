#!/usr/bin/env python3
import math
import numpy as np
import matplotlib.pyplot as plt
from queue_mm1 import QueueServer, EventType


def post_stratify_departure(
    dep_elapsed: list, dep_queue_waiting: list, ro: float
) -> tuple[list, list, list]:
    lenght: int = max(dep_queue_waiting) + 1
    stratified: list = [[] for _ in range(lenght)]

    for inqueue, elapsed in zip(dep_queue_waiting, dep_elapsed):
        stratified[inqueue].append(elapsed)

    return_mean: list = []
    return_var: list = []
    return_pi: list = []
    for stratum in stratified:
        return_mean.append(np.average(stratum))
        return_var.append(np.var(stratum))
        return_pi.append(len(stratum) / len(dep_queue_waiting))
        # return_pi.append((1 - ro) * ro**i)

    return return_mean, return_var, return_pi


def stat_collect(s, time, event):
    if event != EventType.DEPARTURE:
        return []

    _, enqueue_time, enqueue_in_front = s.queue_peek()
    return [(time - enqueue_time, enqueue_in_front)]


def ex2(ro, sim_len, n_simulation, do_plot) -> tuple[float, float, float, float]:
    start = 0
    end = sim_len
    lam = 1  # arrivals
    mi = lam / ro  # departures

    full_departure_elapsed = []
    full_departure_queue_waiting = []

    for i in range(n_simulation):
        # print(f"Start simulation {i}")
        server: QueueServer = QueueServer(start, end, lam, mi)
        stats = server.simulate(stat_collect)
        dep_elapsed, dep_queue_waited = map(lambda x: list(x), zip(*stats))

        full_departure_elapsed += dep_elapsed
        full_departure_queue_waiting += dep_queue_waited

    naive_avg = np.average(full_departure_elapsed)
    naive_var = np.var(full_departure_elapsed)

    post_stratified_mean, post_stratified_var, post_stratified_pi = (
        post_stratify_departure(
            full_departure_elapsed, full_departure_queue_waiting, ro
        )
    )

    post_stratified_avg: float = float(
        np.average(post_stratified_mean, weights=post_stratified_pi)
    )
    post_stratified_var: float = float(
        np.average(post_stratified_var, weights=post_stratified_pi)
        / len(post_stratified_pi)
    )

    if do_plot:
        print(
            f"Expected {1 / (mi - lam)},   "
            + f"naïve {naive_avg} with var {naive_var},   "
            + f"post stratified {post_stratified_avg} with var {post_stratified_var}"
        )

        _, ax = plt.subplots(2, 2)

        ax[0][0].hist(
            full_departure_elapsed,
            label=f"Departure time",
            density=True,
            bins=50,
        )
        ax[0][1].hist(
            full_departure_queue_waiting,
            label=f"Waiting in queue when packet arrive",
            density=True,
            bins=10,
        )
        ax[1][0].plot(
            post_stratified_pi, label="Probabilities obtained with post-strat"
        )
        ax[1][0].plot(
            [(1 - ro) * ro**i for i in range(len(post_stratified_pi))],
            label="Theoretical probabilities",
        )
        ax[0][0].legend(loc="upper right")
        ax[0][1].legend(loc="upper right")
        ax[1][0].legend(loc="upper right")
        plt.show()

    return (
        naive_avg,
        naive_var,
        post_stratified_avg,
        post_stratified_var,
    )


def main():
    sim_time_len = 5000
    ro = 2 / 7  # lab/ mi
    n_simulation = 20

    lam = 1  # arrivals
    mi = lam / ro  # departures
    expected = 1 / (mi - lam)

    redo_n = 300

    diff_i = []
    naive_var_tot = []
    post_strat_var_tot = []
    for i in range(redo_n):
        (
            naive_avg,
            naive_var,
            post_strat_avg,
            post_strat_var,
        ) = ex2(ro, sim_time_len, n_simulation, False)
        print(
            f"Expected {expected},   "
            + f"naïve {naive_avg} with var {naive_var},   "
            + f"post stratified {post_strat_avg} with var {post_strat_var}"
        )

        diff_i.append(post_strat_var - naive_var)
        naive_var_tot.append(naive_var)
        post_strat_var_tot.append(post_strat_var)

    diff_avg = np.average(diff_i)
    diff_var = np.var(diff_i)
    eta = 1.96  # for confidence level 0.95
    diff_interval = eta * math.sqrt(diff_var / len(diff_i))
    print(
        "Difference average",
        diff_avg,
        "(mean of the two are",
        np.average(naive_var),
        np.average(post_strat_var_tot),
        ")",
        diff_interval,
    )

    _, ax = plt.subplots(2, 1)

    ax[0].plot(diff_i, label="Differences (post stratification var - naive var)")
    ax[0].plot(
        [diff_avg for i in range(len(diff_i))],
        label="Differences' mean",
    )
    ax[0].plot(
        [diff_avg - diff_interval for i in range(len(diff_i))],
        label="Lower Bound CI Mean",
    )
    ax[0].plot(
        [diff_avg + diff_interval for i in range(len(diff_i))],
        label="Upper Bound CI Mean",
    )
    ax[1].hist(diff_i)

    ax[1].legend(loc="lower right")
    plt.show()

    print("\nFinal graph")
    ex2(ro, sim_time_len, n_simulation, True)


if __name__ == "__main__":
    main()
