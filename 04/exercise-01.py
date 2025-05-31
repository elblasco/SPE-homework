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


def get_line(xs: list[float], ys: list[float]):
    assert len(xs) == len(ys)
    lenght = len(xs)
    weights = np.ones_like(xs)
    weights[0] = 1000
    line = np.polyfit(xs, ys, 1, w=weights)

    # residual sum of squares
    ss_res: float = np.sum([(ys[i] - (xs[i] * line[0] + line[1])) ** 2 for i in range(lenght)])

    # total sum of squares
    ss_tmp_mean: float = float(np.average(ys))
    ss_tot: float = np.sum([(y - ss_tmp_mean) ** 2 for y in ys])

    # r-squared
    r2 = 1 - (ss_res / ss_tot)
    print("Value of r2 of line is", r2)
    return line


def unique_sum(totali_pacchetti, totali_pacchetti_durata, maxim):
    ret = [0 for _ in range(maxim + 1)]
    for p, d in zip(totali_pacchetti, totali_pacchetti_durata):
        ret[p] += d

    return range(maxim + 1), ret


def mean_time_weighted(n_packets: list, instants: list, start: float, end: float, initial_n_packet: int = 0):
    old_packet = initial_n_packet
    old_instant = start
    empirical_sum_n_packets = 0

    for packet, instant in zip(n_packets, instants):
        empirical_sum_n_packets += old_packet * (instant - old_instant)
        old_instant = instant
        old_packet = packet


    empirical_sum_n_packets += old_packet * (end - old_instant)
    
    return empirical_sum_n_packets / (end - start)

def plot_distribution_packets(ax1, ax2, start, end, n_packets, instants):
    totali_pacchetti = [0] + n_packets

    bin_max = max(totali_pacchetti)
    
    instants_mod = [start] + instants + [end]

    totali_pacchetti_durata = [
        instants_mod[i] - instants_mod[i - 1]
        for i in range(1, len(instants_mod))
    ]


    n_packet_in_queue, n_packet_in_queue_occur = unique_sum(
        totali_pacchetti, totali_pacchetti_durata, bin_max
    )
    empirical_log_n_packets = [np.log(c) for c in n_packet_in_queue_occur]
    # discard first because want to look at the exponential tail
    empirical_log_line = get_line(list(n_packet_in_queue), empirical_log_n_packets)

    linspace_n_packet_in_queue = np.linspace(0, bin_max, 100)
    
    ax1.fill_between(
        n_packet_in_queue, n_packet_in_queue_occur, alpha=0.2, color="orange"
    )
    ax1.plot(
        linspace_n_packet_in_queue,
        [
            math.e ** (empirical_log_line[1] + empirical_log_line[0] * x)
            for x in linspace_n_packet_in_queue
        ],
        label="Theoretical values",
    )
    ax1.plot(
        n_packet_in_queue,
        n_packet_in_queue_occur,
        label="Sorted unique numbers of packets",
    )
    ax1.legend(loc="upper right")

    ax2.plot(
        n_packet_in_queue,
        [
            empirical_log_line[1] + empirical_log_line[0] * c
            for c in range(len(n_packet_in_queue))
        ],
        label="Theoretical logarithm of packets in queue",
    )
    ax2.plot(
        n_packet_in_queue,
        empirical_log_n_packets,
        label="Empirical logarithm of packets in queue",
    )
    ax2.legend(loc="upper right")


def ex1(ro, sim_len, n_simulation):
    start = 0
    end = sim_len
    lam = 1  # arrivals
    mi = lam / ro  # departures
    
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

        mean_i = mean_time_weighted(n_packets, instants, start, end)
        mean_ith_simulation.append(float(mean_i))

        avg_packet, instant_avg = merge_with_avg(
            avg_packet, instant_avg, n_packets, instants
        )

    avg_packet = [a / n_simulation for a in avg_packet]

    print("Preparing graphs (may take some time)")
    _, ax = plt.subplots(2, 2)

    plot_distribution_packets(ax[0][0], ax[0][1], start, end, n_packets, instants)
    
    ax[1][0].plot(instants, n_packets, label="Packets [y] for each instant [x]")
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
        [grand_mean for _ in avg_packet],
        label="Empirical mean of packets",
    )
    ax[1][1].legend(loc="upper right")

    plt.show()


def test_batch_means(lam: float, mi: float):
    server: QueueServer = QueueServer(0, 100_000, lam, mi)
    stats = server.simulate(lambda s, time, event: [(
        s.curr_load() + (1 if event == EventType.ARRIVAL else 0) - (1 if event == EventType.DEPARTURE else 0),
        time)])
    n_packets, instants = map(lambda x: list(x), zip(*stats))
    batch_num = len(n_packets)/100
    splitted_n_packets = np.array_split(n_packets, batch_num)
    mean_ith_batch = [np.average(batch) for batch in splitted_n_packets]
    grand_mean = np.average(mean_ith_batch)
    variance_estimator = 1/(batch_num - 1) * sum((mean_i - grand_mean) ** 2 for mean_i in mean_ith_batch)
    eta = 1.96  # for confidence level 0.95
    ci_grand_mean = eta * math.sqrt(variance_estimator / batch_num)
    print(
        "Batch Means method empirical mean",
        grand_mean,
        "+-",
        ci_grand_mean,
        "(with var",
        variance_estimator,
        ")"
    )
    _, ax = plt.subplots(1, 2)
    ax[0][0].hist(mean_ith_batch)
    plt.show()


# batch_time_size < (end - start) 
def time_based_overlapping_batch_mean(n_packets: list, instants: list, batch_time_size: int, batch_number: int, start: int, end: int) -> list:
    mean_ith_batch: list = []
    step_size = (end - start - batch_time_size) / (batch_number - 1)
    window_start = window_end = 0
    old_n_packet = 0
    
    for batch in range(batch_number):
        batch_start: int = start + (step_size * batch)
        batch_end: int = batch_start + batch_time_size
        while instants[window_start] < batch_start:
            old_n_packet = n_packets[window_start]
            window_start += 1

        window_end = max(window_start, window_end)

        while instants[window_end] < batch_end:
            window_end += 1
        
        mean_ith_batch.append(mean_time_weighted(n_packets[window_start:window_end], instants[window_start:window_end], batch_start, batch_end, initial_n_packet = old_n_packet))
        
    return mean_ith_batch

    
def test_overlapping_batch_means(lam: float, mi: float, sim_time_len: float):
    simulation_end = sim_time_len
    simulation_start = 0
    server: QueueServer = QueueServer(simulation_start, simulation_end, lam, mi)
    packets_and_instants = server.simulate(lambda s, time, event: [(
        s.curr_load() + (1 if event == EventType.ARRIVAL else 0) - (1 if event == EventType.DEPARTURE else 0),
        time)])
    n_packets, instants = map(lambda x: list(x), zip(*packets_and_instants))

    mean_ith_batch = time_based_overlapping_batch_mean(n_packets, instants, 1_000, 10_001, simulation_start, simulation_end)
    
    grand_mean = np.average(mean_ith_batch)
    variance_estimator = 1/(len(mean_ith_batch) - 1) * sum((mean_i - grand_mean) ** 2 for mean_i in mean_ith_batch)
    eta = 1.96  # for confidence level 0.95
    ci_grand_mean = eta * math.sqrt(variance_estimator / len(mean_ith_batch))

    expected_grand_mean = mean_time_weighted(n_packets, instants, simulation_start, simulation_end)
    
    print(
        "Batch Overlapping Means method, expected mean",
        expected_grand_mean,
        "empirical mean",
        grand_mean,
        "+-",
        ci_grand_mean,
        "(with var",
        variance_estimator,
        ")"
    )
    
    _, ax = plt.subplots(2, 2)

    plot_distribution_packets(ax[0][0], ax[0][1], simulation_start, simulation_end, n_packets, instants)

    ax[1][0].hist(mean_ith_batch, bins = 80)
    
    plt.show()
    
def main():
    sim_time_len = 50_000
    ro = 1 / 2  # lab/ mi
    n_simulation = 10

    test_overlapping_batch_means(1, 1/ro, sim_time_len * n_simulation)
    ex1(ro, sim_time_len, n_simulation)


if __name__ == "__main__":
    main()
    
