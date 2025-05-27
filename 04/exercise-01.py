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


def ex1(ro, sim_len, n_simulation):
    start = 0
    end = sim_len
    lam = 1  # departures
    mi = lam / ro  # arrivals

    totali_pacchetti: list = []
    avg_packet: list = []
    instant_avg: list = []
    n_packets:list = []
    instants:list = []
    
    for sim in range(n_simulation):
        print(f"Start simulation {sim}")
        n_packets, instants, _, _ = run_single_simulation(start, end, lam, mi)

        #assert len(avg_packet) == len(instant_avg)
        tmp_pack = []
        tmp_inst = []
        i = j = old_avg = old_pack = 0
        while i < len(n_packets) and j < len(avg_packet):
            t_i = instants[i]
            t_j = instant_avg[j]

            if t_i < t_j:
                tmp_inst.append(instants[i])
                tmp_pack.append(n_packets[i] + old_avg)
                old_pack = n_packets[i]
                i += 1
            elif t_i > t_j:
                tmp_inst.append(instant_avg[j])
                tmp_pack.append(avg_packet[j] + old_pack)
                old_avg = avg_packet[j]
                j += 1
            else:  # same instant
                tmp_inst.append(instants[i])
                tmp_pack.append(n_packets[i] + avg_packet[j])
                old_pack = n_packets[i]
                old_avg = avg_packet[j]
                i += 1
                j += 1

        tmp_inst.extend(instants[i:])
        tmp_pack.extend(n_packets[i:])
        tmp_inst.extend(instant_avg[j:])
        tmp_pack.extend(avg_packet[j:])

        avg_packet = tmp_pack
        instant_avg = tmp_inst

        totali_pacchetti += n_packets

    avg_packet = [a / n_simulation for a in avg_packet]

    print("Preparing graphs (may take some time)")
    _, ax = plt.subplots(2, 3)

    bin_min = 0
    bin_max = max(totali_pacchetti)

    n_packet_in_queue, n_packet_in_queue_occur = np.unique(totali_pacchetti, return_counts=True)
    empirical_derivative_n_packets = [np.log(c) for c in n_packet_in_queue_occur]
    empirical_derivative_slope = (
        empirical_derivative_n_packets[int(len(empirical_derivative_n_packets) / 2)] - empirical_derivative_n_packets[1]) / (n_packet_in_queue[int(len(n_packet_in_queue) / 2)] - n_packet_in_queue[1])
    linspace_n_packet_in_queue = np.linspace(1, bin_max, 100)
    theoretical_n_packet_values = [n_packet_in_queue_occur[1] * math.e ** (empirical_derivative_slope * (x - 1)) for x in linspace_n_packet_in_queue]
    
    ax[0][0].plot(n_packet_in_queue, n_packet_in_queue_occur, label="Sorted unique numbers of packets")
    ax[0][0].plot(linspace_n_packet_in_queue, theoretical_n_packet_values, label="Theoretical values")
    ax[0][0].legend()
    
    ax[0][1].plot(n_packet_in_queue[1:], empirical_derivative_n_packets[1:], label="Empirical derivative of packets in queue")
    ax[0][1].plot(
        n_packet_in_queue[1:],
        [empirical_derivative_n_packets[1] + empirical_derivative_slope * c for c in range(len(n_packet_in_queue) - 1)],
        label="Theoretical derivative of packets in queue"
        )
    ax[0][1].legend()
    
    ax[0][2].plot(instants, n_packets, label="Packets [y] for each instant [x]")
    ax[0][2].legend()

    step_size = math.ceil((bin_max - bin_min) / 100)

    ax[1][0].hist(
        totali_pacchetti, np.arange(bin_min - 1 / 2, bin_max + 3 / 2, step_size), label="Number of istants with [x] packets in the queue"
    )
    ax[1][0].legend()

    ax[1][1].plot(instant_avg, avg_packet, label="Average Packet per instant")
    empirical_mean_n_packets = np.average(avg_packet[int(len(avg_packet) / 4) :])
    theoretical_mean_n_packets = ro / (1 - ro)
    print(theoretical_mean_n_packets, empirical_mean_n_packets)
    ax[1][1].plot(instant_avg, [theoretical_mean_n_packets for _ in avg_packet], label="Theoretical mean of packets")
    ax[1][1].plot(instant_avg, [empirical_mean_n_packets for _ in avg_packet], label="Empirical mean of packets")
    ax[1][1].legend()
    
    plt.show()

    
def post_stratify_departure(dep_elapsed: list, dep_queue_waiting: list, ro: float) -> (list, list, list):
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
        return_pi.append(len(stratified[i]) / len(dep_elapsed))
        print(i, return_pi[i], len(stratified[i]), dep_queue_waiting.count(i), len(dep_elapsed))

    return (return_mean, return_var, return_pi) 

def ex2(ro, sim_len, n_simulation):
    start = 0
    end = sim_len
    lam = 1  # departures
    mi = lam / ro  # arrivals

    full_dep_elapsed = []
    full_dep_queue_waiting = []

    for i in range(n_simulation):
        print(f"Start simulation {i}")
        _, _, dep_elapsed, dep_queue_waited = run_single_simulation(start, end, lam, mi)

        full_dep_elapsed.extend(dep_elapsed)
        full_dep_queue_waiting.extend(dep_queue_waited)

    naive_avg = np.average(full_dep_elapsed)

    naive_vari = np.var(full_dep_elapsed)
    eta = 1.96  # for confidence level 0.95
    naive_diff = eta * math.sqrt(naive_vari / len(full_dep_elapsed))
    print(f"Naïve Avg {naive_avg} +- {naive_diff}, expected {1 / (mi - lam)}")

    post_strat_mean, post_strat_var, post_stratified_pi = post_stratify_departure(
        full_dep_elapsed, full_dep_queue_waiting, ro
    )

    post_stratified_avg: float = np.average(post_strat_mean, weights=post_stratified_pi)
    post_stratified_var: float = np.average(post_strat_var, weights=list(map(lambda x: x*x, post_stratified_pi)))

    post_stratified_diff = eta * math.sqrt(post_stratified_var / len(full_dep_elapsed))
    print(f"Post stratified Avg {post_stratified_avg} +- {post_stratified_diff}, expected {1 / (mi - lam)}")
    
    _, ax = plt.subplots(2, 2)

    ax[0][0].hist(full_dep_elapsed)
    ax[0][1].hist(full_dep_queue_waiting)
    ax[1][0].hist(full_dep_queue_waiting)
    ax[1][1].plot(post_stratified_pi)    
    ax[1][1].plot([ro*((1 - ro)**i) for i in range(len(post_stratified_pi))])
    plt.show()


def main():
    sim_time_len = 100000
    ro = 1 / (2)  # lab/ mi
    n_simulation = 5
    
    ex1(ro, sim_time_len, n_simulation)


if __name__ == "__main__":
    main()
