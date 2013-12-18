#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import sys
import cPickle

import requests
from BeautifulSoup import BeautifulSoup

def soup_it(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    return soup


if __name__ == '__main__':
    search_url = sys.argv[1]
    links_url = sys.argv[2]
    name = sys.argv[3] + '.pickle'
    cPickle.dump(
        dict(
            result_soup=soup_it(search_url),
            links_soup=soup_it(links_url)),
        open(name, 'w'))
    print 'saving pickle => ' + name
