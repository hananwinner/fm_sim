class MessageStreamElement(object):
    def __init__(self, address, wait):
        self.address = address
        self.wait = wait


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

    def get_next_message(self):
        result = -1
        if self.state == self.STATE_ELEMENT:
                cur_elem = self.stream_elements[self.cur_elem_index]
                result = cur_elem.address
                wait = cur_elem.wait
                if wait > 0:
                    self.state = self.STATE_WAIT
                    self.cur_wait = wait
                else:
                    self.cur_elem_index += 1
                    if self.cur_elem_index > len(self.stream_elements):
                        self.state = self.STATE_DONE
                    else:
                        self.state = self.STATE_ELEMENT
        elif self.state == self.STATE_WAIT:
            result = None
            self.cur_wait -= 1
            if self.cur_wait == 0:
                self.cur_elem_index += 1
                if self.cur_elem_index > len(self.stream_elements):
                    self.state = self.STATE_DONE
                else:
                    self.state = self.STATE_ELEMENT

        return result













class Client(object):
    def get(self):
        """
        Get the Current message.
        If the client is in wait time after the previous message,
        :return:
        :rtype:
        """

