from interface import Job


class NucleiJob(Job):

    def __repr__(self):
        return 'nuclei'

    def _run(self):
        url = self.input
        d1 = filter(
            lambda x: x != '',
            self.process('nuclei', '-nts', '-nc', '--silent', '-u', url, '-t',
                         '{}/templates/open-redirect.yaml'.format(self.dir)))
        return d1
