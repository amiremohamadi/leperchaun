from abc import abstractmethod
from os import path
from inspect import getmodule


class Job:
    '''inherit and implement the class to create a job'''

    def __init__(self, input):
        if not isinstance(input, list):
            raise TypeError('job {} input is not type of list'.format(self))
        self.input = input

        file = getmodule(self).__file__
        self.dir = path.dirname(path.realpath(file))

    def run(self):
        r = self._run()
        if not isinstance(r, list):
            raise TypeError('job {} output is not type of list'.format(self))
        return r

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def _run(self):
        raise NotImplementedError
