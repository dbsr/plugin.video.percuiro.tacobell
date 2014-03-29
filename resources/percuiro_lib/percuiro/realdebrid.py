# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import requests

from plugin import plugin


def get_cookies(force=False):
    realdebrid_storage = plugin.get_storage('realdebrid')
    cookies = realdebrid_storage.get('cookies')
    if not cookies or force:
        username = plugin.get_setting('real_debrid_username')
        password = plugin.get_setting('real_debrid_password')
        req = requests.get('http://real-debrid.com/ajax/login.php', 
            params={
                'user':username,
                'pass':password})
        cookies = req.cookies
        realdebrid_storage['cookies'] = cookies
    return cookies


def unrestrict_url(url):
    cookies = get_cookies()
    req = requests.get(
        'http://real-debrid.com/ajax/unrestrict.php',
        params=dict(
            link=url),
        cookies=cookies)
    resp = req.json()
    print resp
    if resp['error']:
        pass
    else:
        return resp['main_link']
