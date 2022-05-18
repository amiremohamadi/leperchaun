# should be imported before any imports
import grequests

from interface import Job
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as BS
import re


class Type:

    def __init__(self, content):
        self.content = content


class JS(Type):
    pass


class ATag(Type):
    pass


class Input(Type):
    pass


class Json(Type):
    pass



class FallparamsJob(Job):
    '''only works with direct pipe (leads to a better performance)'''

    def __repr__(self):
        return 'fallparams'

    def _run(self):
        return self._run_generator()

    def _run_generator(self):
        urls = self.input
        # TODO: remove protocol part
        reqs = (grequests.get('http://{}'.format(url)) for url in urls)

        for resp in grequests.imap(reqs, size=20):
            for param in self.extract_params(resp.url, resp.content):
                yield param

    def extract_params(self, url, content):
        tokens = self.tokenize(url, content)
        for token in tokens:
            if isinstance(token, JS):
                for var in self.extract_js_variables(token.content):
                    yield var
            elif isinstance(token, Json):
                try:
                    j = json.loads(token.content)
                    for key in j:
                        yield key
                except:
                    # TODO: logging
                    continue
            elif isinstance(token, ATag):
                yield token.content

    def tokenize(self, url, content):
        # cleanup query params
        url = urljoin(url, urlparse(url).path)

        if url.endswith('.js'):
            return [JS(content)]
        if url.endswith('.json'):
            return [Json(content)]

        tokens = []
        soup = BS(content, 'html.parser')

        # hrefs from a tags
        for a in soup.find_all('a'):
            if href := a.get('href'):
                if href != '#':
                    tokens.append(ATag(href))

        # scripts
        for script in soup.find_all('script'):
            tokens.append(JS(script.text))

        # inputs

        return tokens

    def extract_js_variables(self, js_content):
        matches = re.findall('(var|let|const)\\s+(\\w+)\\s+=\\s+', js_content)
        return [var for (_, var) in matches]
