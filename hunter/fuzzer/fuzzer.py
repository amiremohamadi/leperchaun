from interface import Job
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

verbose_level = '0'


class FuzzerJob(Job):

    def __repr__(self):
        return 'fuzzer'

    def _run(self):
        return self._run_generator()

    def _run_generator(self):
        urls = defaultdict(list)

        for url in self.input:
            parsed = urlparse(url)
            url = '{}://{}{}'.format(parsed.scheme, parsed.netloc, parsed.path)
            # keep params in a dictionary so that we can call x8 once
            # with a word list instead of calling it multiple times for
            # each url
            for q in parse_qs(parsed.query):
                urls[url].append(q)

            # fuzzing
            for result in self.process('x8',
                                    '-v',
                                    verbose_level,
                                    '-O',
                                    'url',
                                    '-u',
                                    url,
                                    '-w',
                                    '/dev/stdin',
                                    stdin=(x for x in urls[url])):
                result = result.strip()
                if urlparse(result).query:
                    yield result
