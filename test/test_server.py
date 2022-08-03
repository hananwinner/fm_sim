import logging
import sys
import os
print(f'current directory: {os.getcwd()}')
sys.path.insert(0, "/home/hanan/dev/fm_sim/fm_sim_code")
from unittest import TestCase
from cache import FifoCache, PrefetcherCache, BayesianMarkovCache
from client import MessageStream
from server import ServerSimulation
import yaml
import log_utils


class TestServerSimulation(TestCase):
    def read_trace(self, num):
        with open(f"../examples/traces/trace_{num}.yaml", "r") as stream:
            try:
                trace = yaml.safe_load(stream)
                # print(x)
            except yaml.YAMLError as exc:
                print(exc)
        return trace

    def test_run_all(self):
        for i in range(1,10):
            print(f'reading trace {i}')
            trace = self.read_trace(i)
            for cache_size in [8,
                               64,
                               512
                               ]:
                for cache_type in [
                    FifoCache,
                    PrefetcherCache,
                    BayesianMarkovCache
                ]:
                    self._run_test_case(i, trace, cache_type, cache_size)

    def _run_test_case(self, i, trace, cache_type, cache_size):
        print(f'started test {i} on {cache_type.__name__} cache size {cache_size}')
        log_utils.configure_log(f'trace_{i}_{cache_type.__name__}_{cache_size}')
        cache = cache_type(cache_size)
        message_stream = MessageStream(trace)
        server = ServerSimulation(message_stream, cache)
        server.run()
        # logging.getLogger().handlers[0].flush()
        print('finished test')

    def test_run_trace1_fifo_8(self):
        i = 1
        print(f'reading trace {i}')
        trace = self.read_trace(i)
        print(f'finished reading trace {i}')
        self._run_test_case(i, trace, FifoCache, 8)

    def test_interactive(self):
        i = input('Please specify trace number (1-9): ')
        i = int(i)
        cache_type_num = input('Please specify cache type (1-Fifo, 2-Prefetch, 3-Markov): ')
        cache_type_num = int(cache_type_num)
        cache_type = FifoCache
        if cache_type_num == 2:
            cache_type = PrefetcherCache
        elif cache_type_num == 3:
            cache_type = BayesianMarkovCache

        cache_size = input('Please specify cache size (8, 64, 512): ')
        cache_size = int(cache_size)

        print(f'reading trace {i}')
        trace = self.read_trace(i)
        print(f'finished reading trace {i}')
        self._run_test_case(i, trace, cache_type, cache_size)
