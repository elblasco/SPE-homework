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
    for i in range(lenght):
        return_mean.append(np.average(stratified[i]))
        return_var.append(np.var(stratified[i]))
        # ro * (1 - ro) ** i
        return_pi.append(len(stratified[i]) / len(dep_elapsed))

    return return_mean, return_var, return_pi


def stat_collect(s, time, event):
    if event != EventType.DEPARTURE:
        return []

    _, enqueue_time, enqueue_in_front = s.queue_peek()
    return [(time - enqueue_time, enqueue_in_front)]


def ex2(ro, sim_len, n_simulation):
    start = 0
    end = sim_len
    lam = 1  # arrivals
    mi = lam / ro  # departures

    full_departure_elapsed = []
    full_departure_queue_waiting = []

    for i in range(n_simulation):
        print(f"Start simulation {i}")
        server: QueueServer = QueueServer(start, end, lam, mi)
        stats = server.simulate(stat_collect)
        dep_elapsed, dep_queue_waited = map(lambda x: list(x), zip(*stats))

        full_departure_elapsed += dep_elapsed
        full_departure_queue_waiting += dep_queue_waited

    naive_avg = np.average(full_departure_elapsed)
    naive_var = np.var(full_departure_elapsed)
    eta = 1.96  # for confidence level 0.95
    naive_interval = eta * math.sqrt(naive_var / len(full_departure_elapsed))
    print(f"Naïve Avg {naive_avg} +- {naive_interval}, expected {1 / (mi - lam)}")

    post_stratified_mean, post_stratified_var, post_stratified_pi = (
        post_stratify_departure(
            full_departure_elapsed, full_departure_queue_waiting, ro
        )
    )

    post_stratified_avg: float = float(np.average(
        post_stratified_mean, weights=post_stratified_pi
    ))
    post_stratified_var: float = float(np.average(
        post_stratified_var, weights=list(map(lambda x: x * x, post_stratified_pi))
    ))

    post_stratified_interval = eta * math.sqrt(
        post_stratified_var / len(full_departure_elapsed)
    )
    print(
        f"Post stratified Avg {post_stratified_avg} +- {post_stratified_interval}, expected {1 / (mi - lam)}"
    )

    _, ax = plt.subplots(1, 3)

    ax[0].hist(
        full_departure_elapsed,
        label=f"Departure time over {n_simulation} simuls",
        density=True,
    )
    ax[1].hist(
        full_departure_queue_waiting,
        label=f"Waiting time in {n_simulation} simuls",
        density=True,
    )
    ax[2].plot(post_stratified_pi, label="Probabilities obtained with post-strat")
    ax[2].plot(
        [ro ** i * (1 - ro) for i in range(len(post_stratified_pi))],
        label="Theoretical probabilities",
    )
    ax[0].legend(loc="upper right")
    ax[1].legend(loc="upper right")
    ax[2].legend(loc="upper right")
    plt.show()


def main():
    sim_time_len = 5000
    ro = 2 / 7  # lab/ mi
    n_simulation = 30
    ex2(ro, sim_time_len, n_simulation)


if __name__ == "__main__":
    main()
