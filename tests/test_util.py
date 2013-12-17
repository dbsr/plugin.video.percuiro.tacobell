# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from percuiro.util import (is_debrid_host, label_from_link, query_in_label,
                           get_website_logo)


def test_is_debrid_host():
    debrid_host = 'http://rapidgator.net/file/b9ab1a38f5e9fb691ecf2920d7cb7dca'
    not_debrid_host = 'http://www.google.com/?q=foo'
    assert is_debrid_host(debrid_host)
    assert not is_debrid_host(not_debrid_host)


def test_label_from_link():
    link = 'http://rapidgator.net/file/b9ab1a38f5e9fb691ecf2920d7cb7dca'
    label = label_from_link(link) 
    assert label == 'RAPIDGATOR.NET       b9ab1a38f5e9fb691ecf2920d7cb7dca'


def test_query_in_label():
    query = 'Happy Endings S01E03'
    in_label = 'Happy.Endings.S01E03.HDTV.XviD.LOL'
    not_in_label = 'Breaking_Bad_S04E2_720p_HDTV.x264'
    assert query_in_label(query, in_label)
    assert not query_in_label(query, not_in_label)
