# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from providers import providers
from provider import Provider, PluginProvider


providers_dict = dict((provider['name'], provider) for provider in providers)


def get_providers():
    return dict((provider['name'], Provider(**provider))
                for provider in providers)


def get_plugin_providers(plugin, include_disabled=False):
    print include_disabled
    plugin_providers = sorted(
        map(
            lambda provider: PluginProvider(plugin, **provider),
            providers),
        key=lambda provider: provider.priority)
    if include_disabled:
        return plugin_providers
    for provider in plugin_providers:
        print provider, provider.status
    return filter(
        lambda provider: provider.status == 'enabled',
        plugin_providers)


def get_plugin_provider(plugin, provider):
    return PluginProvider(plugin, **providers_dict[provider])
