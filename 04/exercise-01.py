#!/usr/bin/env python3
from enum import Enum
from heapq import heapify, heappop, heappush
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import math


class EventType(Enum):
    START = 0
    ARRIVAL = 1
    DEPARTURE = 2
    END = 3


def generate_events(start_time, end_time, lamb) -> list:
    times: list = np.random.uniform(
        start_time, end_time, int(lamb * (end_time - start_time))
    )
    events: list = list(zip(times, [EventType.ARRIVAL for _ in range(len(times))]))

    events.append((start_time, EventType.START))
    events.append((end_time, EventType.END))
    return events


class QueueServerState:
    def __init__(self, start_time, end_time, lamb, mi):
        self.queue = deque([])  # arr[0] contains the pactet in processor
        self.next_id = 0
        self.lamb = lamb
        self.mi = mi

        self.events_heap = generate_events(start_time, end_time, lamb)
        heapify(self.events_heap)

    def packet_arrival(self, curr_time):
        if not self.is_busy():
            self.__push_event_departure(curr_time)
        self.queue.append((self.next_id, curr_time, max(self.curr_load(), 0)))

    # return id of the packet and time it was inserted in queue/processor
    def packet_departure(self, curr_time) -> (int, float, int):
        finished = self.queue.popleft()
        if self.curr_load() > 0:
            self.__push_event_departure(curr_time)
        return finished

    def __push_event_departure(self, curr_time):
        schduled_departure = np.random.exponential(1 / self.mi) + curr_time
        heappush(self.events_heap, (schduled_departure, EventType.DEPARTURE))

    def pop_next_event(self) -> (float, EventType):
        return heappop(self.events_heap)

    def empty_events(self) -> bool:
        return len(self.events_heap) <= 0

    # Queue len + process work
    def curr_load(self) -> int:
        return len(self.queue)

    def is_busy(self):
        return len(self.queue) > 0


def run_single_simulation(start_time, end_time, lamb, mi) -> (list, list, list, list):
    server = QueueServerState(start_time, end_time, lamb, mi)

    packets_per_istant: list = []
    istants: list = []
    departure_elapsed: list = []
    departure_queue_waited: list = []

    while not server.empty_events():
        curr_time, curr_event = server.pop_next_event()

        match curr_event:
            case EventType.START:
                pass  # NOP
            case EventType.ARRIVAL:
                server.packet_arrival(curr_time)
            case EventType.DEPARTURE:
                _, arrival_time, in_queue = server.packet_departure(curr_time)
                departure_elapsed.append(curr_time - arrival_time)
                departure_queue_waited.append(in_queue)
            case EventType.END:
                break

        packets_per_istant.append(server.curr_load())
        istants.append(curr_time)

    return packets_per_istant, istants, departure_elapsed, departure_queue_waited


def merge_with_avg(avg_p, avg_inst, curr_p, curr_inst) -> (list, list):
    assert len(avg_p) == len(avg_inst)
    tmp_pack = []
    tmp_inst = []
    i = j = old_avg = old_pack = 0
    while i < len(curr_p) and j < len(avg_p):
        t_i = curr_inst[i]
        t_j = avg_inst[j]

        if t_i < t_j:
            tmp_inst.append(curr_inst[i])
            tmp_pack.append(curr_p[i] + old_avg)
            old_pack = curr_p[i]
            i += 1
        elif t_i > t_j:
            tmp_inst.append(avg_inst[j])
            tmp_pack.append(avg_p[j] + old_pack)
            old_avg = avg_p[j]
            j += 1
        else:  # same instant
            tmp_inst.append(curr_inst[i])
            tmp_pack.append(curr_p[i] + avg_p[j])
            old_pack = curr_p[i]
            old_avg = avg_p[j]
            i += 1
            j += 1

    tmp_pack += curr_p[i:] + avg_p[j:]
    tmp_inst += curr_inst[i:] + avg_inst[j:]

    # assert all(tmp_inst[i] <= tmp_inst[i + 1] for i in range(len(tmp_inst) - 1))
    return tmp_pack, tmp_inst


def get_line(Xs, Ys):
    assert len(Xs) == len(Ys)
    lenght = len(Xs)
    weights = np.ones_like(Xs)
    weights[0] = 1000
    line = np.polyfit(Xs, Ys, 1, w=weights)

    # residual sum of squares
    ss_res = np.sum([(Ys[i] - (Xs[i] * line[0] + line[1])) ** 2 for i in range(lenght)])

    # total sum of squares
    ss_tmp_mean = np.mean(Ys)
    ss_tot = np.sum([(y - ss_tmp_mean) ** 2 for y in Ys])

    # r-squared
    r2 = 1 - (ss_res / ss_tot)
    return line


def unique_sum(totali_pacchetti, totali_pacchetti_durata, maxim):
    ret = [0 for i in range(maxim + 1)]
    for p, d in zip(totali_pacchetti, totali_pacchetti_durata):
        ret[p] += d

    return range(maxim + 1), ret


def ex1(ro, sim_len, n_simulation):
    start = 0
    end = sim_len
    lam = 1  # arrivals
    mi = lam / ro  # departures

    totali_pacchetti: list = []
    totali_pacchetti_durata: list = []
    avg_packet: list = []
    instant_avg: list = []
    n_packets: list = []
    instants: list = []

    # Start simulation
    for sim in range(n_simulation):
        print(f"Start simulation {sim}")
        n_packets, instants, _, _ = run_single_simulation(start, end, lam, mi)

        avg_packet, instant_avg = merge_with_avg(
            avg_packet, instant_avg, n_packets, instants
        )

        instants_mod = [start] + instants + [end]
        totali_pacchetti += [0] + n_packets
        totali_pacchetti_durata += [
            instants_mod[i] - instants_mod[i - 1] for i in range(1, len(instants_mod))
        ]
    avg_packet = [a / n_simulation for a in avg_packet]

    print("Preparing graphs (may take some time)")
    _, ax = plt.subplots(2, 3)
    bin_min = 0
    bin_max = max(totali_pacchetti)

    n_packet_in_queue, n_packet_in_queue_occur = unique_sum(
        totali_pacchetti, totali_pacchetti_durata, bin_max
    )
    empirical_log_n_packets = [np.log(c) for c in n_packet_in_queue_occur]
    # discard first because want to look at the exponential tail
    empirical_log_line = get_line(n_packet_in_queue, empirical_log_n_packets)

    linspace_n_packet_in_queue = np.linspace(0, bin_max, 100)

    ax[0][0].fill_between(
        n_packet_in_queue, n_packet_in_queue_occur, alpha=0.2, color="orange"
    )
    ax[0][0].plot(
        linspace_n_packet_in_queue,
        [
            math.e ** (empirical_log_line[1] + empirical_log_line[0] * x)
            for x in linspace_n_packet_in_queue
        ],
        label="Theoretical values",
    )
    ax[0][0].plot(
        n_packet_in_queue,
        n_packet_in_queue_occur,
        label="Sorted unique numbers of packets",
    )
    ax[0][0].legend(loc="upper right")

    ax[0][1].plot(
        n_packet_in_queue,
        [
            empirical_log_line[1] + empirical_log_line[0] * c
            for c in range(len(n_packet_in_queue))
        ],
        label="Theoretical logarithm of packets in queue",
    )
    ax[0][1].plot(
        n_packet_in_queue,
        empirical_log_n_packets,
        label="Empirical logarithm of packets in queue",
    )
    ax[0][1].legend(loc="upper right")

    ax[0][2].plot(instants, n_packets, label="Packets [y] for each instant [x]")
    ax[0][2].legend(loc="upper right")

    step_size = math.ceil((bin_max - bin_min) / 100)

    ax[1][0].hist(
        totali_pacchetti,
        np.arange(bin_min - 1 / 2, bin_max + 3 / 2, step_size),
        label="Number of istants with [x] packets in the queue",
    )
    ax[1][0].legend(loc="upper right")

    ax[1][1].plot(instant_avg, avg_packet, label="Average Packet per instant")

    old_packet = 0
    old_instant = 0
    empirical_sum_n_packets = 0
    for packet, instant in zip(avg_packet, instant_avg):
        empirical_sum_n_packets += old_packet * (instant - old_instant)
        old_instant = instant
        old_packet = packet
    empirical_mean_n_packets = empirical_sum_n_packets / (end - start)

    theoretical_mean_n_packets = ro / (1 - ro)
    print(
        "Theoretical mean:",
        theoretical_mean_n_packets,
        "and empirical mean",
        empirical_mean_n_packets,
    )
    ax[1][1].plot(
        instant_avg,
        [theoretical_mean_n_packets for _ in avg_packet],
        label="Theoretical mean of packets",
    )
    ax[1][1].plot(
        instant_avg,
        [empirical_mean_n_packets for _ in avg_packet],
        label="Empirical mean of packets",
    )
    ax[1][1].legend(loc="upper right")

    plt.show()


def post_stratify_departure(
    dep_elapsed: list, dep_queue_waiting: list, ro: float
) -> (list, list, list):
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

    return (return_mean, return_var, return_pi)


def ex2(ro, sim_len, n_simulation):
    start = 0
    end = sim_len
    lam = 1  # arrivals
    mi = lam / ro  # departures

    full_departure_elapsed = []
    full_departure_queue_waiting = []

    for i in range(n_simulation):
        print(f"Start simulation {i}")
        _, _, dep_elapsed, dep_queue_waited = run_single_simulation(start, end, lam, mi)

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

    post_stratified_avg: float = np.average(
        post_stratified_mean, weights=post_stratified_pi
    )
    post_stratified_var: float = np.average(
        post_stratified_var, weights=list(map(lambda x: x * x, post_stratified_pi))
    )

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
        [ro**i * (1 - ro) for i in range(len(post_stratified_pi))],
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

    # ex1(ro, sim_time_len, n_simulation)
    ex2(ro, sim_time_len, n_simulation)


if __name__ == "__main__":
    main()
