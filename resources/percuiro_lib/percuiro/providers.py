# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import requests
from BeautifulSoup import BeautifulSoup

import util


downtr = dict(
    name='downtr.co',
    base_url='http://www.downtr.co',
    query_url='http://www.downtr.co/?do=search&subaction=search&story={query}',
    result_selector = [('div', {'class': 'result'}), ('div', {'class': 'name'}), ('a',)],
    result_title = lambda result: result.text,
    result_link = lambda result: result.get('href')
)


class Provider(object):
    def __init__(self, name, base_url, query_url, result_selector, 
            result_title, result_link):
        self.name = name
        self.base_url = base_url
        self.query_url = query_url
        self.result_selector = result_selector
        self.result_title = result_title
        self.result_link = result_link

    def _req_soup(self, url):
        req = requests.get(url)
        return BeautifulSoup(req.content)

    def search(self, query):
        url = self.query_url.format(query=query.replace(' ', '+'))
        soup = self._req_soup(url)
        results = None
        for selector in self.result_selector:
            if len(selector) == 1:
                tag = selector
                attr = {}
            else:
                tag, attr = selector
            print tag, attr, results
            if not results:
                results = soup.findAll(tag, attr)
            else:
                results = filter(
                    lambda result: result is not None,
                    map(
                        lambda result: result.find(tag, attr),
                        results))
        results = map(
            lambda result: dict(
                label=self.result_title(result),
                url=self.result_link(result)),
            results)
        next_page = self._get_next_page_url(soup)
        if next_page:
            results.append(dict(
                label='Next >>',
                url=next_page))
        return results

    def _get_next_page_url(self, soup):
        for a in soup.findAll('a'):
            if 'next' in a.text.lower() and a.get('href').startswith('http'):
                return a.get('href')

    def parse_result_page(self, url):
        soup = self._req_soup(url)
        return map(
            lambda link: dict(
                label=link.text or link.get('href'),
                url=link.get('href')),
            filter(
                lambda link: util.is_debrid_host(link),
                soup.findAll('a')))
        
