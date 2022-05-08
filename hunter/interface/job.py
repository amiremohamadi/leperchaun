import subprocess
from abc import abstractmethod
from os import path
from inspect import getmodule


class Job:
    '''inherit and implement the class to create a job'''

    def __init__(self, input):
        if not isinstance(input, list):
            raise TypeError('job {} input is not type of list'.format(self))
        self.input = input
        self.pipe_to = None
        self.starter = False

        file = getmodule(self).__file__
        self.dir = path.dirname(path.realpath(file))

    def run(self):
        r = self._run()
        if not isinstance(r, list):
            raise TypeError('job {} output is not type of list'.format(self))
        return r

    def process(self, cmd, *args):
        '''run a subprocess in current "package" directory'''
        cmd = path.join(self.dir, cmd)
        cmd_with_args = '{} {}'.format(cmd, ' '.join(args))
        return subprocess.check_output(cmd_with_args,
                                       stderr=subprocess.STDOUT,
                                       shell=True)

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def _run(self):
        raise NotImplementedError
