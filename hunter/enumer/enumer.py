from interface import Job


class EnumerJob(Job):

    def __repr__(self):
        return 'enumer'

    def _run(self):
        return [
            result.decode() for i in self.input
            for result in self.process('assetfinder', i).strip().split(b'\n')
        ]
