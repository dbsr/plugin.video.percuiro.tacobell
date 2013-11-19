# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import requests
from BeautifulSoup import BeautifulSoup

from providers import providers


class Provider(object):
    def __init__(self, provider):
        self.name = provider['name']
        self.query_url = provider['query']['url']
        self.supported = provider['query']['supported']
        self.provider = provider

    def _req_soup(self, url, params=None):
        if not params:
            params = {}
        params.update(self.provider['query']['default_params'])
        if not url.startswith('http'):
            url = os.path.dirname(self.query_url) + url
        req = requests.get(url, params=params)
        print req.url
        return BeautifulSoup(req.content)

    def search_tv_show(self, show, episode, title):
        query = self.provider['query']
        qstring = '{} s{:0>2}e{:0>2}'.format(show, episode, title)
        qmod = query['query_mods'].get('tv_show', lambda _: _)
        soup = self._req_soup(self.query_url, {
            query['query_parameter']: qmod(qstring)
        })
        mapping = self.get_mapping('items', soup)
        print len(mapping)
        results = self.parse('items', mapping, qstring)
        return results

    def resolve(self, url)

    def parse(self, key, mapping, qstring):
        results = map(self.provider['soup'][key]['parser'], filter(lambda x: x, mapping))
        pfilter = self.provider['soup'][key].get('parser_filter')
        if pfilter:
            return filter(lambda x: pfilter(x, qstring), results)
        return results

    def get_mapping(self, key, soup):
        mapping = self.provider['soup'][key]['mapping']
        return mapping(soup)


def get_providers():
    return dict((p.name, Provider(p)) for p in providers)
