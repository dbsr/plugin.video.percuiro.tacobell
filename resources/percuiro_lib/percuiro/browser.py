# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os

import requests
from BeautifulSoup import BeautifulSoup

import util


def _req_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content)

def _parse_links(soup):
    links = soup.findAll('a')
    real_debrid_links = filter(
        util.is_debrid_host,
        links)
    return map(
        lambda a: (
            a.text.encode('utf8') if a.text else os.path.basename(a.get('href')),
            a.get('href')
        ),
        real_debrid_links)


def open_url(url):
    soup = _req_soup(url)
    return _parse_links(soup)
