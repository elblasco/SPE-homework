#!/usr/bin/env python3
from enum import Enum
from heapq import heapify, heappop, heappush
import numpy as np
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
        self.queue = []
        self.next_id = 0
        self.busy = False
        self.lamb = lamb
        self.mi = mi

        self.events_heap = generate_events(start_time, end_time, lamb)
        heapify(self.events_heap)

    def packet_arrival(self, curr_time):
        if self.busy:
            self.queue.append((self.next_id, curr_time))
        else:
            self.busy = True
            self.__push_event_departure(curr_time)

    # return tiem the packet was inserted in queue/processor
    def packet_departure(self, curr_time):
        if len(self.queue) > 0:
            self.queue.pop()
            # Schudeled departure for the nextr waiting packet
            self.__push_event_departure(curr_time)
        else:
            self.busy = False

    def __push_event_departure(self, curr_time):
        schduled_departure = np.random.exponential(1 / self.mi) + curr_time
        heappush(self.events_heap, (schduled_departure, EventType.DEPARTURE))

    def pop_next_event(self) -> (float, EventType):
        return heappop(self.events_heap)

    def empty_events(self) -> bool:
        return len(self.events_heap) <= 0

    # Queue len + process work
    def curr_load(self) -> int:
        return len(self.queue) + (1 if self.busy else 0)


def run_single_simulation(start_time, end_time, lamb, mi) -> (list, list):
    server = QueueServerState(start_time, end_time, lamb, mi)

    packets_per_istant: list = []
    istants: list = []

    while not server.empty_events():
        curr_time, curr_event = server.pop_next_event()

        match curr_event:
            case EventType.START:
                pass  # NOP
            case EventType.ARRIVAL:
                server.packet_arrival(curr_time)
            case EventType.DEPARTURE:
                server.packet_departure(curr_time)
            case EventType.END:
                break

        packets_per_istant.append(server.curr_load())
        istants.append(curr_time)

    return packets_per_istant, istants


def main():
    totali_pacchetti: list = []

    for i in range(1):
        print(f"Start simulation {i}")
        pacchetti, istanti = run_single_simulation(0, 1e4, 2, 4)
        totali_pacchetti += pacchetti

    print("Preparing graphs (may take some time)")
    # fig, ax = plt.subplots(1, 2)
    # ax[0].plot(istanti, pacchetti)

    bin_min = 0
    bin_max = max(totali_pacchetti)
    step_size = math.ceil((bin_max - bin_min) / 100)

    plt.hist(totali_pacchetti, np.arange(bin_min - 1 / 2, bin_max + 3 / 2, step_size))
    plt.show()


if __name__ == "__main__":
    main()
