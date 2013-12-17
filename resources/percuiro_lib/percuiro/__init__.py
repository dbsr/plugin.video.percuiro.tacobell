# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os

import util
from providers import providers
from provider import Provider, PluginProvider


def get_providers():
    return dict((provider['name'], Provider(**provider))
        for provider in providers)


def get_plugin_providers(plugin):
    return sorted(
        map(
            lambda provider: PluginProvider(plugin, **provider),
            providers)
        key=lambda provider: provider.priority)


def get_plugin_provider(plugin, provider):
    provider = filter(
        lambda provider: provider['name'] == provider,
        providers)
    if provider:
        return PluginProvider(plugin, **provider[0])
