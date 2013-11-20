# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import re

import common



def get_season_episode_rgx(season=r'[0-9]{1,2}', episode=r'[0-9]{2}'):
    return re.compile(
        r'(^|\W)(s{season:2>0}e{episode:2>0}|{season}x{episode:2>0})($|\W)'
            .format(season=season,episode=episode)
    )

def get_season_episode(query):
    for rgx in [r's([0-9]{2})e([0-9]{2})', r'([0-9])x([0-9]{2})']:
        m = re.search(rgx, query, re.I)
        if m:
            return map(int, m.groups())


def split_tv_show_query(query):
    try:
        s, e = get_season_episode(query)
        show = get_season_episode_rgx().sub('', query).strip()
    except:
        pass
    else:
        return show, s, e


def is_debrid_host(anchor):
    if isinstance(anchor, str):
        href = anchor
    elif isinstance(anchor, dict):
        href = anchor.get('url', '')
    else:
        # soup object ?
        try:
            href = anchor.get('href')
        except:
            return
    if href:
        return re.search(common.REAL_DEBRID_REGEX, href)
