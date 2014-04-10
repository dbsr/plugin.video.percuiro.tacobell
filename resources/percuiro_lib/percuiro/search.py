# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from plugin import plugin
from provider import PluginProvider
from providers import providers

def get_plugin_providers(plugin, include_disabled=False):
    plugin_providers = sorted(
        map(
            lambda provider: PluginProvider(plugin, **provider),
            providers),
        key=lambda provider: provider.priority)
    if include_disabled:
        return plugin_providers
    return filter(
        lambda provider: provider.status == 'enabled',
        plugin_providers)


def provider_search(query, min_results=2):
    results = []
    for provider in get_plugin_providers(plugin):
        presults = provider.search(query)
        results.extend(presults)
        if len(results) > 2:
            return results
