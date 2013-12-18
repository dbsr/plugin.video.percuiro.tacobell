# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import re
from types import FunctionType

import requests
from BeautifulSoup import BeautifulSoup

import util
import common


class Provider(object):
    def __init__(self, name, base_url, query_url, result_selector,
                 get_result_label, get_result_url, next_page_format=None, **kwargs):
        '''The Provider class is used by all provider definition to search
        and parse results.
        '''
        self.name = name
        self.base_url = base_url
        self.query_url = query_url
        self.result_selector = result_selector
        self.get_result_label = get_result_label
        self.get_result_url = get_result_url
        self.next_page_format = next_page_format

    def __repr__(self):
        return '<percuiro.Provider: ' + self.name + '>'

    def _req_soup(self, url):
        '''Returns souped result of the url request.

        Args:
            url (str): the url to request.

        Returns:
            A BeautifulSoup.BeautifulSoup object.
        '''
        if not url.startswith('http'):
            url = self.base_url + url
        req = requests.get(url)
        return BeautifulSoup(req.content)

    def _selector_chain(self, chain, soup):
        '''Sequentially iterates over soup / results using the selectors in
        the chain.

        Args:
            chain (list): list of selector tuples.
            soup (BeautifulSoup.BeautifulSoup): the soup to parse.

        Returns:
            the resulting soup objects remaining at end of chain.
        '''
        results = None
        for selector in chain:
            if len(selector) == 1:
                tag = selector
                attr = {}
            else:
                tag, attr = selector
            if not results:
                results = soup.findAll(tag, attr)
            else:
                results = filter(
                    lambda result: result is not None,
                    map(
                        lambda result: result.find(tag, attr),
                        results))
        return results

    def search(self, query):
        '''Queries the provider and parses the resulting html for links and
        optionally a link to the next page of the result set.

        Args:
            query (str): the search term(s).

        Returns:
            a list of result dictionaries.

        '''
        query = query.replace(' ', '+')
        try:
            url = self.query_url.format(query=query)
        except AttributeError:
            if isinstance(self.query_url, FunctionType):
                url = self.query_url(query)
            else:
                print 'invalid query_url'
                return []
        soup = self._req_soup(url)
        return self._parse_results_page(soup, url)

    def _parse_results_page(self, soup, url):
        results = []
        for soup_result in self._selector_chain(self.result_selector, soup):
            try:
                result = dict(
                    label=self.get_result_label(soup_result).encode('utf8'),
                    url=self.get_result_url(soup_result).encode('utf8'))
            except AttributeError as e:
                print e
                continue
            result_text = soup_result.text.encode('utf8')
            host_match = re.search(common.REAL_DEBRID_REGEX, result_text)
            if host_match:
                result['host'] = host_match.group(0)
            ext_match = re.search(common.FILE_EXTENSIONS_REGEX, result_text)
            if ext_match:
                result['ext'] = ext_match.group(0).strip('.')
            if util.is_valid_result(result):
                results.append(result)
        next_page = self._get_next_page_url(soup, url)
        if next_page:
            results.append(dict(
                label='Next >>',
                url=next_page))
        return results

    def _get_next_page_url(self, soup, url):
        '''Parses the soup of the result page and looks for a link pointing
        to the next page of the result set.

        Args:
            soup (BeautifulSoup.BeautifulSoup): The souped html result.
            url (str): the url for the current result soup

        Returns:
            the url of the next page or None if none found.
        '''
        if self.next_page_format:
            m = re.match(self.next_page_format, url)
            if m:
                next_page_num = str(int(m.group(1)) + 1)
            else:
                next_page_num = '2'
            is_next = lambda a: re.match(
                self.next_page_format.replace('([0-9]+)', next_page_num),
                a.get('href'))
        else:
            is_next = lambda a: 'next' in a.text.lower()

        for a in soup.findAll('a'):
            href = a.get('href', '')
            if href.startswith('/') or self.base_url in href:
                if is_next(a):
                    return href

    def get_link_page(self, url):
        '''Parses result page for playable url links.

        Args:
            url (str): the url to retrieve, soup, and look for supported
                       hoster urls in.

        Returns:
            a list of supported hoster_urls.
        '''
        soup = self._req_soup(url)
        return self._parse_link_page(soup)

    def _parse_link_page(self, soup):
        return map(
            lambda link: dict(
                label=util.label_from_link(link),
                url=link),
            filter(
                lambda url: util.is_debrid_host(url) and not re.search(
                    r'\.rar', url),
                set(re.findall(r'''http[\w.\-/:?=&_]+''', repr(soup)))))

    def parse_next_page(self, url):
        soup = self._req_soup(url)
        return self._parse_results_page(soup, url)


class PluginProvider(Provider):
    def __init__(self, plugin, thumbnail_url, *args, **kwargs):
        '''
        Subclassed to keep xbmc dependencies separated from main
        class for easier testing. The Pluginprovider class provides
        xbmc settings get and setters for the provider.

        Args:
            plugin: xbmcswift2.Plugin instance
        '''
        self.plugin = plugin
        self.thumbnail_url = thumbnail_url
        Provider.__init__(self, *args, **kwargs)
        if not self.priority:
            self.priority = 100
        if not self.status:
            self.status = 'enabled'

    @property
    def thumbnail(self):
        return util.get_provider_thumbnail(self.plugin.storage_path,
                                           self.thumbnail_url)

    def _provider_settings(self, key, value=None):
        settings = self.plugin.get_storage('provider_settings')
        if not settings.get(self.name):
            settings[self.name] = {}
        if value:
            settings[self.name][key] = value
        else:
            return settings[self.name].get(key)

    @property
    def priority(self):
        return self._provider_settings('priority')

    @priority.setter
    def priority(self, value):
        try:
            priority = int(value)
        except ValueError:
            raise ValueError('{0:!r} is not a valid priority value'.format(priority))
        if priority < 0 or priority > 100:
            raise ValueError('Priority value must be between 0 and 100')
        self._provider_settings('priority', priority)

    @property
    def status(self):
        return self._provider_settings('status')

    @status.setter
    def status(self, value):
        self._provider_settings('status', value)

    def toggle_status(self):
        self.status = 'enabled' if self.status == 'disabled' else 'disabled'
