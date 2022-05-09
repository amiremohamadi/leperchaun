from interface import Job
from itertools import chain
import re


def extract_url(text):
    '''extract url from string'''
    url = re.search("(?P<url>https?://[^\s\]]+)", text)
    if not url:
        return ''
    return url.group('url')


def filter_static_files(url):
    if len(url) < 4:
        return False
    if url[:-4] in [
            '.jpg', '.jpeg', '.gif', '.css', '.tif', '.tiff', '.png', '.ttf',
            '.woff', '.woff2', '.ico', '.pdf', '.svg'
    ]:
        return False
    return True


class FlinksJob(Job):

    def __repr__(self):
        return 'flinks'

    def _run(self):
        url = self.input
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        d1 = self.process('gospider', '-s', url, '--sitemap')
        d1 = map(extract_url, d1)
        d1 = filter(filter_static_files, d1)
        d1 = map(lambda x: url + ' -> ' + x, d1)
        return d1
