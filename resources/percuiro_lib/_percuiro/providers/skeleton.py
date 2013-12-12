# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import copy

from common import QUERIES_ALL, QUERIES_TV

'''
The base skeleton used by all providers

Lambda settings can chose from those extra arguments (if available):
    :param query: the query kwargs
    :param query_str: the parsed query string
To request an extra argument simply add the required argument to the
lambdas arguments, eg:
    lambda foo, query: blah

The lambdas in the comments describe:
    lambda soup (= type of argument(s)): mod_soup (= type lambda should return)

'''

_provider = {
    'name': None,
    'query': {
        'url': '',
        'query_parameter': 'q',
        'default_params': {},
        'supported': (QUERIES_TV),
        'query_mods': {
            'tv_show': lambda query: query,
            'global': lambda query: query
        }
    },
    'soup': {
        'items': {
            'mapping': None,
            'parser': {
                'label': None,
                'url': None
            },
            'parser_filter': None
        },
        'next_page': {
            'mapping': False,
            'parser': {
                'url': None
            }
        },
        'resolve': {
            'mapping': None,
            'parser': {
                'url': None
            }
        }
    }
}


def _update(update, src):
    for k, v in update.items():
        if isinstance(v, dict):
            _update(v, src[k])
        else:
            src[k] = v

def get_provider_skeleton(update_dct):
    skel = copy.deepcopy(_provider)
    _update(update_dct, skel)
    return skel
