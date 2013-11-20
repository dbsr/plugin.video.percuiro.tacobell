# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import requests
from BeautifulSoup import BeautifulSoup

from providers import providers, QUERIES_TV, QUERIES_ALL, util



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

    def search_tv_show(self, show, season, episode):
        query = self.provider['query']
        qstring = '{0} s{1:0>2}e{2:0>2}'.format(show, season, episode)
        qmod = query['query_mods'].get('tv_show', lambda _: _)
        soup = self._req_soup(self.query_url, {
            query['query_parameter']: qmod(qstring)
        })
        mapping = self.get_mapping('items', soup)
        results = self.parse('items', mapping, qstring)
        return results

    def resolve(self, url):
        soup = self._req_soup(url)
        mapping = self.get_mapping('resolve', soup)
        return map(lambda x: self.parse('resolve', x), mapping)

    def parse(self, key, mapping, qstring):
        results = map(self.provider['soup'][key]['parser'], filter(lambda x: x, mapping))
        pfilter = self.provider['soup'][key].get('parser_filter')
        if pfilter:
            return filter(lambda x: pfilter(x, qstring), results)
        return results

    def get_mapping(self, key, soup):
        mapping = self.provider['soup'][key]['mapping']
        return mapping(soup)



provider_dict = dict((p['name'], Provider(p)) for p in providers)

def search(query_type, query):
    results = {}
    for name, provider in provider_dict.items():
        if query_type in provider.supported:
            if query_type is QUERIES_TV:
                pquery = util.split_tv_show_query(query)
                results[name] = provider.search_tv_show(*pquery)
    return results
