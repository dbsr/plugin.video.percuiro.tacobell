# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from providers import providers
from provider import Provider, PluginProvider
from plugin import plugin


def get_providers():
    return dict((provider['name'], Provider(**provider))
                for provider in providers)


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


def get_plugin_provider(plugin, provider):
    providers_dict = dict((provider['name'], provider) for provider in providers)
    return PluginProvider(plugin, **providers_dict[provider])
