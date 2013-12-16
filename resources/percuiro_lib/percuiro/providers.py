# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import requests
from BeautifulSoup import BeautifulSoup

import util


downtr_co = dict(
    name='downtr_co',
    base_url='http://www.downtr.co',
    query_url='http://www.downtr.co/?do=search&subaction=search&story={query}',
    result_selector=[('div', {'class': 'result'}), ('div', {'class': 'name'}), ('a',)],
    result_title=lambda result: result.text,
    result_link=lambda result: result.get('href')
)

filestube_com = dict(
    name='filestube_com',
    base_url='http://www.filestube.com',
    query_url=('http://www.filestube.com/query.html?hosting=,23,99,15,24,13,'
               '22,27,25,8,28,2,40,11,46,47,51,55,59,60,64,65,67,68,70,71,81,'
               '87,92,97,102,104&q={query}'),
    result_selector=[('div', {'id': 'newresult'}), ('a',)],
    result_title=lambda result: result.text,
    result_link=lambda result: result.get('href'),
)

theextopia_com = dict(
    name='theextopia_com',
    base_url='http://www.theextopia.com',
    query_url='http://www.theextopia.com/?s={query}',
    result_selector=[('div', {'class': 'single'})],
    result_title=lambda result: result.find('div', {'class': 'title'}).text,
    result_link=lambda result: result.find('a', {'rel': 'bookmark'}).get('href')
)
