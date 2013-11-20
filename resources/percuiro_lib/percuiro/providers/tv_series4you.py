# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os

from skeleton import get_provider_skeleton, QUERIES_TV
from util import get_season_episode_rgx, get_season_episode, is_debrid_host


tv_series4you = get_provider_skeleton({
    'name': 'tv_series4you',
    'query': {
        'url': 'http://tv-series4you.blogspot.nl/search',
        'supported': (QUERIES_TV,),
        'query_mods': {
            'tv_show': lambda query_str: get_season_episode_rgx().sub(
                '', query_str).strip()
        }
    },
    'soup': {
        'items': {
            'mapping': lambda soup: filter(is_debrid_host, soup.findAll('a')),
            'parser': lambda result: {
                'label': os.path.basename(result.text),
                'url': result['href'],
                'resolved': True
            },
            'parser_filter': lambda item, qstring: (
                get_season_episode(qstring) == get_season_episode(item['label'])
            )
        }
    }
})
