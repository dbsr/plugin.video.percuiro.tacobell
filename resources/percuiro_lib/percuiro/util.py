# -*- coding: utf-8 -*-
# dydrmntion@gmail.com


import os
import commands
import re
import subprocess
from urlparse import urlparse
import urllib

from common import REAL_DEBRID_REGEX, PROVIDERS_THUMBNAIL_PATH, FILTER_EXTENSIONS

def clipboard_paste():
    ret = ''
    try:
        prc = subprocess.Popen(['xclip', '-o'], stdout=subprocess.PIPE)
        paste_buffer = prc.stdout.read()
    except IOError:
        pass
    else:
        if re.match(r'https?://[^\s]+\.[a-z]+', paste_buffer, re.I):
            ret = paste_buffer
    return ret


def is_debrid_host(href):
    return re.search(REAL_DEBRID_REGEX, href) is not None


def label_from_link(link):
    purl = urlparse(link)
    return '{0:<20} {1}'.format(purl.netloc.upper(), os.path.basename(link))


def query_in_label(query, label):
    query_split = query.split()
    matches = filter(
        lambda split: re.search(split, label, re.I),
        query_split)
    return len(matches) == len(query_split)


def get_provider_thumbnail(plugin_profile_path, url):
    ext = url.split('.')[-1]
    provider_thumbnails_path = os.path.join(plugin_profile_path, PROVIDERS_THUMBNAIL_PATH)
    if not os.path.isdir(provider_thumbnails_path):
        os.mkdir(provider_thumbnails_path)
    destination = os.path.join(
        provider_thumbnails_path, 
        '{0}.{1}'.format(str(hash(url)), ext).strip('-'))
    if not os.path.exists(destination):
        try: 
            urllib.urlretrieve(url, destination)
        except IOError as e:
            print 'Error retrieving provider thumbnail: {0} -> {1}.'.format(
                url, destination)
            return
    return destination


def is_valid_result(result):
    if len(result) < 2:
        return False
    if result.get('ext', '').strip('.') in FILTER_EXTENSIONS:
        return False
    if result.get('host') and not is_debrid_host(result['host']):
        return False
    if re.search(r'\.?(?:rar|zip)', str(result)):
        return False
    return True
