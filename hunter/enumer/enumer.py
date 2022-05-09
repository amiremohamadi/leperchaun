from interface import Job
from itertools import chain


class EnumerJob(Job):

    def __repr__(self):
        return 'enumer'

    def _run(self):
        print('enumer ' + self.input)
        d1 = self.process('assetfinder', self.input)
        # TODO: subfinder
        # return chain(d1, d2)
        return d1

    def validate(self, sub):
        domain = self.input
        if domain in sub and '@' not in sub:
            return True
        return False
