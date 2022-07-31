from unittest import TestCase
from fm_sim_code.client import MessageStream
import yaml


class TestMessageStream(TestCase):
    def setUp(self) -> None:
        with open("../examples/debug/trace_1.yaml", "r") as stream:
            print('yoo')
            try:
                x = yaml.safe_load(stream)
                print(x)
            except yaml.YAMLError as exc:
                print(exc)

        self.messageStream = MessageStream(x)


class TestInit(TestMessageStream):
    def test_initial(self):
        self.assertEqual(self.messageStream.cur_wait, 0)




