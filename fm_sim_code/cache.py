import random
from queue import Queue
from random import randint


class CacheBase(object):
    def __init__(self, cache_size):
        self.cache_size = cache_size

    def insert(self, address):
        raise NotImplementedError("should implement in derived class")

    def contains(self, address):
        raise NotImplementedError("should implement in derived class")


class FifoCache(CacheBase):
    def __init__(self, cache_size):
        self._queue = Queue(maxsize=cache_size)
        self._set = set()
        super.__init__(cache_size)

    def contains(self, address):
        return address in self._set

    def insert(self, address):
        if not self.contains(address):
            if self._queue.full():
                self._queue.get()
            self._queue.put(address)
            self._set.add(address)


class PrefetcherCache(CacheBase):
    def __init__(self, cache_size):
        self._used_queue = Queue(maxsize=cache_size)
        self._used_set = set()
        self._set = set()
        super.__init__(cache_size)

    def do_step(self):
        new_address = randint(0, 4095)
        self.insert(new_address)

    def contains(self, address):
        self._used_set.insert(address)
        return address in self._set

    def insert(self, address):
        if not self.contains(address):
            if self._queue.full():
                self._queue.get()
            self._queue.put(address)
            self._set.add(address)
