#!/usr/bin/env python3

from enum import Enum
import heapq
import numpy as np
import matplotlib.pyplot as plt

class Event(Enum):
    START = 0
    ARRIVAL = 1
    DEPARTURE = 2
    END = 3

def generate_events(start_time, end_time, lamb) -> list:
    times: list = np.random.uniform(
        start_time,end_time, int(lamb * (end_time - start_time))
    )
    events: list = list(zip(times, [Event.ARRIVAL for _ in range(len(times))]))

    events.append((start_time, Event.START))
    events.append((end_time, Event.END))
    return events


def simulation(start_time, end_time, lamb, mi) -> (list, list):
    server_busy: bool = False
    packets: int = 0
    events_heap: list = generate_events(start_time, end_time, lamb)
    heapq.heapify(events_heap)
    packets_per_istant:list = []
    istants: list = []
    while len(events_heap) > 0:
        current_time, current_event = heapq.heappop(events_heap)
        #print(current_event)
        match current_event:
            case Event.START:
                print("Started")
            case Event.ARRIVAL:
                #packets += 1
                if not server_busy:
                    server_busy = True
                    schduled_departure = np.random.exponential(1/mi) + current_time
                    heapq.heappush(events_heap, (schduled_departure, Event.DEPARTURE))
                else:
                    packets += 1

            case Event.DEPARTURE:
                if packets > 0:
                    packets -= 1
#                    packets_per_istant[event_idx] = packets
                    # Schudeled departure for the nextr waiting packet
                    schduled_departure = np.random.exponential(1/mi) + current_time
                    heapq.heappush(events_heap, (schduled_departure, Event.DEPARTURE))
                else:
                    server_busy = False
            case Event.END:
                break
        packets_per_istant.append(packets + (1 if server_busy else 0))
        istants.append(current_time)
    return packets_per_istant, istants

def main():
    totali_pacchetti: list = []
    
    for _ in range(100):
        pacchetti, istanti = simulation(0, 1e4, 10, 2)
        totali_pacchetti += pacchetti
    #fig, ax = plt.subplots(1, 2)
    #ax[0].plot(istanti, pacchetti)
    d = np.diff(np.unique(totali_pacchetti)).min()
    left_of_first_bin = min(totali_pacchetti) - float(d)/2
    right_of_last_bin = max(totali_pacchetti) + float(d)/2
    plt.hist(totali_pacchetti, np.arange(left_of_first_bin, right_of_last_bin + d, d))
    plt.show()
    
if __name__=="__main__":
    main()
