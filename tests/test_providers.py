# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os
import cPickle

from percuiro import get_providers

providers = []


def setup_module():
    providers.extend(map(
        lambda provider: (
            _get_soup(provider), provider),
        get_providers().values()))


def _get_soup(provider):
    name = provider.name
    pickle_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_data/pickles/{0}.pickle'.format(name))
    if not os.path.isfile(pickle_path):
        query_url = provider._create_query_url(provider.test_data['query'])
        search_result_soup = provider._req_soup(query_url)
        with open(pickle_path, 'w') as f:
            cPickle.dump(search_result_soup, f)
    with open(pickle_path) as f:
        return cPickle.load(f)


def test_providers():
    for soup, provider in providers:
        yield (
            check_search_results,
            provider,
            soup,
            provider.test_data['num_search_results'],
            provider.test_data['first_link_url'])


def check_search_results(provider, soup, num_search_results, first_link_url):
    results = provider._parse_results_page(soup, '')
    print provider.name, len(results)
    assert len(results) == num_search_results
    print results[0]['url']
    assert results[0]['url'] == first_link_url
