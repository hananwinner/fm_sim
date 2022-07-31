from queue import Queue
from cache import CacheBase


class ServerSimulation(object):
    def __init__(self, instructions_provider, cache_provider: CacheBase):
        self._step = -1
        self._instructions_provider = instructions_provider
        self._cache_provider = cache_provider
        self._queue = Queue()
        self._resolved_latencies = []
        self._resolved_count = 0
        self._buffer = None

    def consume_from_client(self):
        self._step += 1

        while True:
            next_address = self._instructions_provider.get_next_message()

            # latencies update
            for i in self._resolved_latencies[self._resolved_count:]:
                self._resolved_latencies[i] += 1

            # putting in the queue
            if next_address and next_address != -1:
                self._queue.put(next_address)
                self._latencies.append()

            # processing the queue
            if not self._queue.empty():
                served_address = self._queue.get()
                fetch_cost = 1
                if not self._cache_provider.contains(served_address):
                    self._cache_provider.insert(served_address)
                    fetch_cost = 2
                self._buffer = served_address
                self._resolved_latencies[self._resolved_count] += fetch_cost
                self._resolved_count += 1

            if next_address == -1 and self._queue.empty():
                break

    def run(self):
        self.consume_from_client()
        self.print_summary()

    def print_summary(self):
        pass








