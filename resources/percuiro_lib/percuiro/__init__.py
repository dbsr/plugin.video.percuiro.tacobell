# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from providers import providers
from provider import Provider, PluginProvider


providers_dict = dict((provider['name'], provider) for provider in providers)
print providers_dict


def get_providers():
    return dict((provider['name'], Provider(**provider))
                for provider in providers)


def get_plugin_providers(plugin):
    return sorted(
        map(
            lambda provider: PluginProvider(plugin, **provider),
            providers),
        key=lambda provider: provider.priority)


def get_plugin_provider(plugin, provider):
    return PluginProvider(plugin, **providers_dict[provider])
