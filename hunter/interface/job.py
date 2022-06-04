import subprocess
import select
from types import GeneratorType
from itertools import tee
from time import time
from abc import abstractmethod
from os import path
from inspect import getmodule

time_limit = 10  # seconds


class Job:
    '''inherit and implement the class to create a job'''

    def __init__(self):
        self.input = None
        self.ctx = {}
        self.pipes = []
        self.starter = False
        self.direct = False

        # in order to kill proccesses at teardown
        self.active_process = set()

        file = getmodule(self).__file__
        self.dir = path.dirname(path.realpath(file))

    def run(self):
        rgen = self._run()
        if rgen is None:
            return

        if self.direct:
            self.pipe(rgen)
            return

        for r in rgen:
            if not self.validate(r):
                continue
            self.pipe(r)

    def pipe(self, input):
        if isinstance(input, GeneratorType):
            if len(self.pipes) == 2:
                g1, g2 = tee(input)

                p1 = self.pipes[0]
                p2 = self.pipes[1]

                p1.input = g1
                p2.input = g2
                p1.run()
                p2.run()

        for p in self.pipes:
            p.input = input
            p.run()

    def process(self, cmd, *args, stdin=None):
        '''run a subprocess in current "package" directory'''
        cmd = path.join(self.dir, cmd)
        cmd_with_args = [cmd, *args]

        poller = select.poll()
        proc = subprocess.Popen(cmd_with_args,
                                stdin=subprocess.PIPE if stdin else None,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE)

        if stdin:
            # TODO: handle when it's not byte input
            stdin = ('\n'.join(stdin)).encode()
            proc.stdin.write(stdin)
            proc.stdin.close()

        poller.register(proc.stdout, select.POLLIN)
        self.active_process.add(proc)

        # the idea is to limit processes on a time_limit
        # in some cases maybe a process hangs then we can
        # handle the situation.
        # TODO: log in case of time limit
        # TODO: retry mechanism
        t = time()
        while (time() - t) < time_limit:
            if poller.poll(0):
                output = proc.stdout.readline()
                if output == b'' and proc.poll() is not None:
                    break
                else:
                    yield output.decode().strip()
                    t = time()
        # clean up
        proc.kill()
        self.active_process.remove(proc)

    def teardown(self):
        for proc in self.active_process:
            proc.kill()
        for pipe in self.pipes:
            pipe.teardown()

    @abstractmethod
    def validate(self, input):
        '''return True to be included otherwise False'''
        return True

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def _run(self):
        raise NotImplementedError
