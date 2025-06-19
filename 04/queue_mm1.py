#!/usr/bin/env python3
from heapq import heappop, heappush
from typing import Deque, Callable, Self
from collections import deque
from enum import Enum
import numpy as np


class EventType(Enum):
    START = 0
    ARRIVAL = 1
    DEPARTURE = 2
    END = 3


class QueueServer:
    def __init__(self, start_time, end_time, lamb, mi):
        self.queue: Deque[(int, float, int)] = (
            deque()
        )  # arr[0] contains the pactet in processor
        self.next_id = 0
        self.lamb = lamb
        self.mi = mi

        self.events_heap = []
        heappush(self.events_heap, (start_time, EventType.START))
        heappush(self.events_heap, (end_time, EventType.END))

    def packet_arrival(self, curr_time: float):
        if not self.is_busy():
            self.__push_event_departure(curr_time)
        self.queue.append((self.next_id, curr_time, max(self.curr_load(), 0)))

    # return id of the packet and time it was inserted in queue/processor
    def packet_departure(self, curr_time: float) -> tuple[int, float, int]:
        finished = self.queue.popleft()
        if self.curr_load() > 0:
            self.__push_event_departure(curr_time)
        return finished

    def __push_event_departure(self, curr_time):
        schduled_departure: float = np.random.exponential(1 / self.mi) + curr_time
        heappush(self.events_heap, (schduled_departure, EventType.DEPARTURE))

    def __push_event_arrival(self, curr_time):
        schduled_departure: float = np.random.exponential(1 / self.lamb) + curr_time
        heappush(self.events_heap, (schduled_departure, EventType.ARRIVAL))

    def pop_next_event(self) -> tuple[float, EventType]:
        return heappop(self.events_heap)

    def empty_events(self) -> bool:
        return len(self.events_heap) <= 0

    # Queue len + process work
    def curr_load(self) -> int:
        return len(self.queue)

    def is_busy(self):
        return len(self.queue) > 0

    def queue_peek(self) -> tuple[int, float, int]:
        return self.queue[0]

    def simulate(self, collect_stats: Callable[[Self, float, EventType], any]) -> list:
        stats = []

        while not self.empty_events():
            curr_time, curr_event = self.pop_next_event()
            stats += collect_stats(self, curr_time, curr_event)

            match curr_event:
                case EventType.START:
                    self.__push_event_arrival(curr_time)
                case EventType.ARRIVAL:
                    self.__push_event_arrival(curr_time)
                    self.packet_arrival(curr_time)
                case EventType.DEPARTURE:
                    self.packet_departure(curr_time)
                case EventType.END:
                    break
        return stats
