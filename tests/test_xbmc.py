# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os

from xbmcswift2.cli.app import PluginManager





def open_xbmc_plugin_url(url=None):
    _here = os.path.dirname(os.path.realpath(__file__))
    pm = PluginManager.load_plugin_from_addonxml(mode='ONCE', xml_path=os.path.join(_here, '..'))
    pm.url = url
    return pm.run()


def test_index_url():
    assert len(open_xbmc_plugin_url()) == 6


def test_provider_settings_url():
    url = 'plugin://plugin.video.percuiro.tacobell/provider-settings/filestube.com'
    assert len(open_xbmc_plugin_url(url)) == 2
