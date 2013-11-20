# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import re

from skeleton import get_provider_skeleton


filestube = get_provider_skeleton({
    'name': 'filestube',
    'query': {
        'url': 'http://www.filestube.com/query.html',
        'default_params': {
            'hosting': ('23,99,15,24,13,22,27,25,8,28,2,40,11,46,47,51,55,59,'
                        '60,64,65,67,68,70,71,81,87,92,97,102,104')
        }
    },
    'soup': {
        'items': {
            'mapping': lambda soup: soup.findAll('div', {'id': 'newresult'}),
            'parser': lambda soup: {
                'label': '[{0}] {1}'.format(
                    soup.findNext('b', {'style': re.compile(r'.*943100.*')}).text,
                    soup.findNext('a').text),
                'url': soup.findNext('a').get('href'),
                'resolved': False
            }
        },
        'resolve': {
            'mapping': lambda soup: soup.find('pre'),
            'parser': {
                'url': lambda soup: soup.get('href')
            }
        }
    }
})
