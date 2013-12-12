# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from xbmcswift2 import Module

from _exc import PercuiroException
from apis import query_tvdb
from _module import module


store = module.plugin.get_storage('browser', TTL=1440)


def search_tvshow(name):
    results = query_tvdb(name)
    return results

def add_tvshow(name, id):
    results = filter(lambda r: r['id'] == int(id), query_tvdb(name))
    if results:
        show = results[0]
        store[name] = show


def remove_tvshow(name):
    try:
        del store[name]
    except KeyError:
        pass


def get_tvshows():
    return store.values()


def get_tvshow(name):
    return store[name]


def get_season(name, season):
    return store[name]['seasons'][season - 1]
