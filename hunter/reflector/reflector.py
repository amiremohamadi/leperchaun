from interface import Job


class ReflectorJob(Job):

    def __repr__(self):
        return 'reflector'

    def _run(self):
        return filter(
            lambda x: len(x) > 0,
            self.process('Gxss',
                         stdin=filter(lambda x: x.startswith('http'),
                                      self.input)))
