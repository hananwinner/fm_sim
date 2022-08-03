import random
from queue import Queue
from random import randint
from collections import OrderedDict


class CacheBase(object):
    def __init__(self, cache_size):
        self.cache_size = cache_size

    def on_step(self, address_to_fetch):
        """
        Executes a step.
        Checking if address_to_fetch was in the cache.
        Doing custom logic of inserting/evicting the addresses in the cache.
        :param address_to_fetch: the address to fetch
        :return: True iff the address was in the cache
        """
        raise NotImplementedError("should implement in derived class")


class FifoCache(CacheBase):
    def __init__(self, cache_size):
        self._queue = Queue(maxsize=cache_size)
        self._set = set()
        super().__init__(cache_size)

    def _contains(self, address):
        return address in self._set

    def _evict(self):
        address = self._queue.get()  # removes first item
        self._set.remove(address)

    def _check_evict(self):
        if self._queue.full():
            self._evict()

    def _insert(self, address):
        self._queue.put(address)
        self._set.add(address)

    def on_step(self, address_to_fetch):
        """
        if not in cache:
            evicts the first-in if needed
            inserts
        """
        was_in_cache = self._contains(address_to_fetch)
        if not was_in_cache:
            self._check_evict()
            self._insert(address_to_fetch)

        return was_in_cache


class PrefetcherCache(CacheBase):
    def __init__(self, cache_size):
        self._cache = OrderedDict()
        self.cur_step = 0
        super().__init__(cache_size)

    def contains(self, address):
        return address in self._cache

    def _update_if_in_cache(self, address):
        return self._insert_or_update(address, update=True, insert=False)
        
    def _insert_if_not_in_cache(self, address):
        return self._insert_or_update(address, update=False, insert=True)

    def _insert_or_update(self, address, update=True, insert=True):
        insert_or_update_done = False
        if insert:
            if update:
                self._do_insert_or_update(address)
            else:  # dont update if already contains
                is_contains = self.contains(address)                
                if not is_contains:
                    self._do_insert_or_update(address)
                    insert_or_update_done = True                            
        else:
            if update:
                is_contains = self.contains(address)
                if is_contains:
                    self._do_insert_or_update(address)
                    insert_or_update_done = True
                    
        return insert_or_update_done

    def _do_insert_or_update(self, address):
        self._cache[address] = self.cur_step
        self._cache.move_to_end(address)

    def _evict(self):
        self._cache.popitem(last=False)

    def _check_evict(self):
        evicted = False
        _cur_size = len(self._cache)
        if _cur_size == self.cache_size:
            self._evict()
            evicted = True
            
        return evicted

    def on_step(self, address_to_fetch):
        """
        Checks if in cache.
        Update the currently fetched address if it was in the cache.
        Evicts if needed.
        Inserts new randmo address.
        """
        self.cur_step += 1
        in_cache = self.contains(address_to_fetch)

        self._update_if_in_cache(address_to_fetch)
        self._check_evict()
        
        # insert random address
        self._insert_new_random_address()

        return in_cache

    def _insert_new_random_address(self):
        inserted = False
        while not inserted:
            rand_address = randint(0, 4095)
            inserted = self._insert_if_not_in_cache(rand_address)

        return inserted


class BayesianMarkovCache(FifoCache):
    def __init__(self, cache_size):
        self._followers_dict = {}
        self._prev_address_fetched = None
        super().__init__(cache_size)

    def on_step(self, address_to_fetch):
        """
        Update the follower's metadata.
        make prediction and insert it to cache.
        """
        was_in_cache = self._contains(address_to_fetch)

        self._update_followers(address_to_fetch)

        prediction = self._predict_next_address(address_to_fetch)

        if prediction:
            if not self._contains(prediction):
                self._check_evict()
                self._insert(prediction)

        return was_in_cache

    def _update_followers(self, address_to_fetch):
        if self._prev_address_fetched:
            followers = self._followers_dict[self._prev_address_fetched]
            if address_to_fetch in followers:
                followers[address_to_fetch] += 1
            else:
                followers[address_to_fetch] = 1

        if address_to_fetch not in self._followers_dict:
            self._followers_dict[address_to_fetch] = {}

        self._prev_address_fetched = address_to_fetch

    def _predict_next_address(self, address):
        result = None
        if address in self._followers_dict:
            followers = self._followers_dict[address]
            if followers:
                item = max(followers, key=followers.get)
                result = item

        return result
