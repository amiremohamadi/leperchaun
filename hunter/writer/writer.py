from interface import Job
from cachetools import LRUCache
from urllib.parse import urlparse
import re
import os

pool_max_size = 10


def extract_domain(text):
    '''extract domain from a text line'''
    url = re.search("(?P<url>https?://[^\s\]]+)", text)
    if not url:
        return ''
    domain = urlparse(url.group('url')).netloc
    return domain


def str_to_generator(name):
    yield name


class FilePool(LRUCache):

    def popitem(self):
        _, fd = super().popitem()
        fd.close()


class WriterJob(Job):

    def __init__(self):
        super().__init__()
        self.pool = FilePool(maxsize=pool_max_size)

    def __repr__(self):
        return 'writer'

    def _run(self):
        rc = None

        name = extract_domain(self.input)
        fd = self.pool.get(name)
        if not fd:
            path = '{}/{}.txt'.format(self.dir, name)
            if not os.path.isfile(path):
                rc = name

            fd = open(path, 'a')
            self.pool[name] = fd

        fd.write('{}\n'.format(self.input))
        fd.flush()

        if rc:
            return str_to_generator(rc)
