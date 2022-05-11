from interface import Job


class HttpxJob(Job):
    '''only accepts generator as input'''

    # TODO: find a way to check input/outputs in modules

    def __repr__(self):
        return 'httpx'

    def _run(self):
        url = self.input

        d1 = self.process('httpx',
                          '-silent',
                          '-fc',
                          '404,403,401,500',
                          stdin=self.input)
        return d1
