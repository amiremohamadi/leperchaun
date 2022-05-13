from interface import Job


class NucleiJob(Job):

    def __repr__(self):
        return 'nuclei'

    def _run(self):
        url = self.input
        d1 = filter(
            lambda x: x != '',
            self.process('nuclei', '-c 10', '-nts', '-nc', '--silent', '-u', url))
        return d1
