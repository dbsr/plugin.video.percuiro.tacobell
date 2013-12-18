# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os
import cPickle
import tempfile

from percuiro import get_providers


fixtures = {
    'downtr.co': dict(
        num_search_results=2,
        num_link_results=2),
    'filestube.com': dict(
        num_search_results=10,
        num_link_results=1),
    'theextopia.com': dict(
        num_search_results=4,
        num_link_results=14),
    'rapidlibrary.biz': dict(
        num_search_results=1,
        num_link_results=1)
}

plugin_path = os.path.join(tempfile.gettempdir(), '_percuiro_test')

providers = map(
    lambda provider: (
        provider,
        fixtures[provider.name],
        cPickle.load(open(os.path.join(os.path.dirname(os.path.realpath(
            __file__)), 'test_data/pickles/' + provider.name + '.pickle')))
    ),
    get_providers().values())


def test_search_results():
    for provider, fixture, pickle in providers:
        yield check_search_results, provider, fixture['num_search_results'], pickle['result_soup']


def test_link_results():
    for provider, fixture, pickle in providers:
        yield check_link_results, provider, fixture['num_link_results'], pickle['links_soup']


def check_search_results(provider, num_search_results, soup):
    results = provider._parse_results_page(soup, '')
    assert len(results) == num_search_results


def check_link_results(provider, num_link_results, soup):
    results = provider._parse_link_page(soup)
    assert len(results) == num_link_results
