from queue import Queue
from cache import CacheBase
from client import MessageStream
import logging


class LatencyMetadata(object):

    def __init__(self, address, latency) -> None:
        self.address = address
        self.latency = latency

    def __str__(self) -> str:
        return f'addr = {self.address}, latency =  {self.latency}'


class ServerSimulation(object):
    def __init__(self, instructions_provider: MessageStream, cache_provider: CacheBase):
        self._step = 1
        self._instructions_provider = instructions_provider
        self._cache_provider = cache_provider
        self._queue = Queue()
        self._resolved_latencies = []
        self._resolved_count = 0
        self._buffer = None

    def consume_from_client(self):
        while True:
            logging.debug(f"Step {self._step}")
            next_address = self._instructions_provider.get_next_message()
            logging.debug(f"Read {next_address}")

            # putting in the queue
            if next_address is not None and next_address != -1:
                logging.debug(f"Inserting {next_address} to Queue")
                self._queue.put(next_address)
                self._resolved_latencies.append(LatencyMetadata(next_address, 0))

            # latencies update
            for i in range(self._resolved_count, len(self._resolved_latencies)):
                self._resolved_latencies[i].latency += 1

            # processing the queue
            if not self._queue.empty():
                served_address = self._queue.get()
                logging.debug(f'Serving {served_address}')
                fetch_cost = 0
                if not self._cache_provider.on_step(served_address):
                    logging.debug(f"Cache Miss")
                    fetch_cost = 1
                self._buffer = served_address
                # logging.debug(f"Buffer {self._buffer}")
                cur_latency = self._resolved_latencies[self._resolved_count]
                cur_latency.latency += fetch_cost
                logging.debug(f'Resolved Address {cur_latency.address} Latency {cur_latency.latency}')
                self._resolved_count += 1

            if next_address == -1 and self._queue.empty():
                break
            self._step += 1

    def run(self):
        self.consume_from_client()
        self.print_summary()

    def print_summary(self):
        logging.info(f"Summary:")
        logging.info(f"Latencies:")
        for latency in self._resolved_latencies:
            logging.info(latency)