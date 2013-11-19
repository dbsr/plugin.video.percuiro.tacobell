# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from BeautifulSoup import BeautifulSoup

from tv_series4you import tv_series4you


def test_query_mod_tv_show():
    qfilter = tv_series4you['query']['query_mods']['tv_show']
    query_str = 'reno 911 s01e11'
    assert qfilter(query_str) == 'reno 911'
    query_str = 'reno 911 1x11'
    assert qfilter(query_str) == 'reno 911'
    query_str = 'weird show 900x900'
    assert qfilter(query_str) == query_str


def test_items_mapping():
    mapping = tv_series4you['soup']['items']['mapping']
    html = BeautifulSoup('''
        <a href="http://rapidgator.net/foo">blah</a>
        <a href="http://ikea.rox/">1</a>''')
    assert len(mapping(html)) == 1


def test_items_parser_filter():
    pfilter = tv_series4you['soup']['items']['parser_filter']
    result = BeautifulSoup('''
        <a href="http://rapidgator.net/ss293">reno 911 s02e11</a>''')
    assert pfilter(result, 'reno 911 s02e11')
    assert not pfilter(result, 'reno 911 s01e01')
