
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '../resources/percuiro_lib'))
import cPickle

from percuiro import get_active_providers


fixtures = dict(
    downtr_co=dict(
        num_search_results=2,
        num_link_results=2),
    filestube_com=dict(
        num_search_results=10,
        num_link_results=1),
    theextopia_com=dict(
        num_search_results=4,
        num_link_results=1))

providers = []
for provider in get_active_providers().values():
    providers.append((
        provider, 
        fixtures[provider.name], 
        cPickle.load(open(os.path.join(os.path.dirname(os.path.realpath(
            __file__)), 'pickles/' + provider.name + '.pickle')))))


def test_search_results():
    for provider, fixture, pickle in providers:
        yield check_search_results, provider, fixture['num_search_results'], pickle['result_soup']


def test_search_results():
    for provider, fixture, pickle in providers:
        yield check_link_results, provider, fixture['num_link_results'], pickle['links_soup']



def check_search_results(provider, num_search_results, soup):
    results = provider._parse_search_results(soup)
    assert len(results) == num_search_results


def check_link_results(provider, num_link_results, soup):
    results = provider._parse_link_page(soup)
    print '\n' + provider.name
    print results
    assert len(results) == num_link_results
