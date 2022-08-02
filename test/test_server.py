import sys
sys.path.append("../fm_sim_code")
import logging
logging.config.fileConfig('logging.config')
from unittest import TestCase
from fm_sim_code.cache import FifoCache
from fm_sim_code.client import MessageStream
from fm_sim_code.server import ServerSimulation
import yaml


class TestServerSimulation(TestCase):
    def setUp(self) -> None:
        with open("../examples/debug/trace_1.yaml", "r") as stream:
            print('yoo')
            try:
                x = yaml.safe_load(stream)
                print(x)
            except yaml.YAMLError as exc:
                print(exc)
        self._trace1 = x

    def test_run(self):
        cache = FifoCache(3)
        message_steram = MessageStream(self._trace1)
        server = ServerSimulation(message_steram, cache)
        server.run()

