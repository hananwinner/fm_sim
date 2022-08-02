import logging
import logging.config
import pandas as pd
# logging.config.fileConfig('logging.config')


class MessageStream(object):
    STATE_ELEMENT = "element"
    STATE_WAIT = "wait"
    STATE_DONE = "done"

    def __init__(self, stream_elements):
        self.stream_elements = stream_elements
        self.cur_elem_index = 0
        self.cur_wait = 0
        if self.stream_elements:
            self.state = self.STATE_ELEMENT
        else:
            self.state = self.STATE_DONE
        self.rate = 0
        self.top_addresses = []


        # TODO
        # _list = [x["address"] for x in stream_elements]
        # s = pd.Series(_list)
        # mean = s.mean()
        # _top = [x for x in _list if x > mean + 3]

    def get_next_message(self):
        result = -1
        if self.state == self.STATE_ELEMENT:
                cur_elem = self.stream_elements[self.cur_elem_index]
                result = cur_elem["address"]
                wait = cur_elem["wait"]
                if wait > 0:
                    self.state = self.STATE_WAIT
                    self.cur_wait = wait
                else:
                    self.cur_elem_index += 1
                    if self.cur_elem_index == len(self.stream_elements):
                        self.state = self.STATE_DONE
                    else:
                        self.state = self.STATE_ELEMENT
        elif self.state == self.STATE_WAIT:
            result = None
            self.cur_wait -= 1
            if self.cur_wait == 0:
                self.cur_elem_index += 1
                if self.cur_elem_index == len(self.stream_elements):
                    self.state = self.STATE_DONE
                else:
                    self.state = self.STATE_ELEMENT

        return result
