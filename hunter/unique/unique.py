from interface import Job
from cachetools import LRUCache

maxsize = 2000


class UniqueJob(Job):

    def __init__(self):
        super().__init__()
        self.cache = LRUCache(maxsize=maxsize)

    def __repr__(self):
        return 'unique'

    def _run(self):

        def _generator(input):
            if not self.cache.get(input):
                self.cache[input] = True
                yield input

        return _generator(self.input)
