from interface import Job


class EnumerJob(Job):

    def __repr__(self):
        return 'enumer'

    def _run(self):
        d1 = [
            sub for i in self.input for sub in self.process(
                'assetfinder', i).decode().strip().split('\n')
            if self.check(sub, i)
        ]
        d2 = [
            sub for i in self.input for sub in self.process(
                'subfinder', '-silent', '-d', i).decode().strip().split('\n')
            if self.check(sub, i)
        ]
        # eliminate duplicates
        d = list(set(d1).union(set(d2)))
        return d

    def check(self, sub, domain):
        if domain in sub and '@' not in sub:
            return True
        return False
