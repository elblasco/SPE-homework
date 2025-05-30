#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math
from queue_mm1 import QueueServer, EventType


def merge_with_avg(avg_p, avg_inst, curr_p, curr_inst) -> tuple[list, list]:
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


def get_line(Xs: list[float], Ys: list[float]):
    assert len(Xs) == len(Ys)
    lenght = len(Xs)
    weights = np.ones_like(Xs)
    weights[0] = 1000
    line = np.polyfit(Xs, Ys, 1, w=weights)

    # residual sum of squares
    ss_res: float = np.sum([(Ys[i] - (Xs[i] * line[0] + line[1])) ** 2 for i in range(lenght)])

    # total sum of squares
    ss_tmp_mean: float = float(np.average(Ys))
    ss_tot: float = np.sum([(y - ss_tmp_mean) ** 2 for y in Ys])

    # r-squared
    r2 = 1 - (ss_res / ss_tot)
    print("Value of r2 of line is", r2)
    return line


def unique_sum(totali_pacchetti, totali_pacchetti_durata, maxim):
    ret = [0 for _ in range(maxim + 1)]
    for p, d in zip(totali_pacchetti, totali_pacchetti_durata):
        ret[p] += d

    return range(maxim + 1), ret


def mean_time_weighted(n_packets: list, instants: list, duration: float):
    old_packet = 0
    old_instant = 0
    empirical_sum_n_packets = 0

    for packet, instant in zip(n_packets, instants):
        empirical_sum_n_packets += old_packet * (instant - old_instant)
        old_instant = instant
        old_packet = packet

    return empirical_sum_n_packets / duration


def ex1(ro, sim_len, n_simulation):
    start = 0
    end = sim_len
    lam = 1  # arrivals
    mi = lam / ro  # departures

    totali_pacchetti: list = []
    totali_pacchetti_durata: list = []
    mean_ith_simulation: list = []
    avg_packet: list = []
    instant_avg: list = []
    n_packets: list = []
    instants: list = []

    # Start simulation
    for sim in range(n_simulation):
        print(f"Start simulation {sim}")
        server: QueueServer = QueueServer(start, end, lam, mi)
        stats = server.simulate(lambda s, time, event: [(
            s.curr_load() + (1 if event == EventType.ARRIVAL else 0) - (1 if event == EventType.DEPARTURE else 0),
            time)])
        n_packets, instants = map(lambda x: list(x), zip(*stats))

        mean_i = mean_time_weighted(n_packets, instants, end - start)
        mean_ith_simulation.append(float(mean_i))

        avg_packet, instant_avg = merge_with_avg(
            avg_packet, instant_avg, n_packets, instants
        )

    instants_mod = [start] + instants + [end]
    totali_pacchetti += [0] + n_packets
    totali_pacchetti_durata += [
        instants_mod[i] - instants_mod[i - 1]
        for i in range(1, len(instants_mod))

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
    empirical_log_line = get_line(list(n_packet_in_queue), empirical_log_n_packets)

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

    theoretical_mean_n_packets = ro / (1 - ro)
    grand_mean: float = float(np.average(mean_ith_simulation))

    varian = 1 / (n_simulation - 1) * sum((mean_i - grand_mean) ** 2 for mean_i in mean_ith_simulation)
    eta = 1.96  # for confidence level 0.95
    ci_grand_mean = eta * math.sqrt(varian / n_simulation)

    print(
        "Theoretical mean:",
        theoretical_mean_n_packets,
        "and empirical mean",
        grand_mean,
        "+-",
        ci_grand_mean,
        "(with var",
        varian,
        ")"
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


def main():
    sim_time_len = 50000
    ro = 100 / 101  # lab/ mi
    n_simulation = 30

    ex1(ro, sim_time_len, n_simulation)


if __name__ == "__main__":
    main()
