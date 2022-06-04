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
        reqs = (grequests.get(url) for url in urls)

        for resp in grequests.imap(reqs, size=20):
            for param in self.extract_params(resp.url, resp.content):
                if not param:
                    continue
                yield param

    def extract_params(self, url, content):
        parsed = urlparse(url)
        host = '{}://{}'.format(parsed.scheme, parsed.netloc)
        tokens = self.tokenize(url, content)
        for token in tokens:
            if isinstance(token, JS):
                for var in self.extract_js_variables(token.content):
                    yield '{}?{}=0'.format(url, var)
            elif isinstance(token, Json):
                try:
                    for (k, v) in json.loads(token.content).items():
                        yield '{}?{}={}'.format(url, k, v)
                except:
                    # TODO: logging
                    continue
            elif isinstance(token, ATag):
                href = token.content
                if not href.startswith('http') and host not in href:
                    if href.startswith('.'):
                        href = '{}/{}'.format(url.rstrip('/'),
                                              href.lstrip('/'))
                    else:
                        href = '{}/{}'.format(host.rstrip('/'),
                                              href.lstrip('/'))
                yield href
            elif isinstance(token, Input):
                yield '{}?{}=0'.format(url, token.content)

    def tokenize(self, url, content):
        # cleanup query params
        url = urljoin(url, urlparse(url).path)

        if url.endswith('.js'):
            return [JS(content)]
        if url.endswith('.json'):
            return [Json(content)]

        tokens = []
        soup = BS(content, 'html.parser', from_encoding='iso-8859-1')

        # hrefs from a tags
        for a in soup.find_all('a'):
            if href := a.get('href'):
                if href == '#':
                    continue
                if href.startswith('javascript'):
                    continue
                tokens.append(ATag(href))

        # scripts
        for script in soup.find_all('script'):
            if script.content is None:
                continue
            tokens.append(JS(script.content))

        # inputs
        for i in soup.find_all('input'):
            if name := i.get('name'):
                tokens.append(Input(name))
            if id := i.get('id'):
                tokens.append(Input(id))

        return tokens

    def extract_js_variables(self, js_content):
        matches = re.findall(b'(var|let|const)\\s+(\\w+)\\s+=\\s+', js_content)
        return [var for (_, var) in matches]
