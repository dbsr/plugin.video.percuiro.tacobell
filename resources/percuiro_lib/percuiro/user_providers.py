# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import sys
import os
import re
from types import FunctionType


class PercuiroUserProvidersException(Exception):
    pass


def get_user_providers(user_providers_fpath):
    user_providers_module = import_user_providers(user_providers_fpath)
    user_providers = validate_user_providers_module(user_providers_module)
    for provider in user_providers:
        validate_provider(provider)
    return user_providers


def import_user_providers(user_providers_fpath):
    if not os.path.exists(user_providers_fpath):
        raise PercuiroUserProvidersException(
            '{0!r} does not exist on filesystem'.format(user_providers_fpath))

    fname = os.path.basename(user_providers_fpath)
    fpath = os.path.dirname(user_providers_fpath)
    sys.path.append(fpath)
    try:
        user_providers = __import__(fname.rstrip('.py'))
    except ImportError as e:
        raise PercuiroUserProvidersException('Could not import `{0}`: {1!r}'.format(
            user_providers_fpath, e.message))
    finally:
        sys.path.remove(fpath)
    return user_providers


def validate_user_providers_module(user_providers_module):
    try:
        user_providers = getattr(user_providers_module, 'my_providers')
    except AttributeError:
        raise PercuiroUserProvidersException(
            'Required variable `my_providers` not found in user_providers module.')

    if not isinstance(user_providers, tuple):
        raise PercuiroUserProvidersException(
            'user_providers variable should be a `tuple`, `{0}` found.'.format(
                type(user_providers)))
    return user_providers


def validate_provider(provider):
    is_function = lambda x: isinstance(x, FunctionType)
    is_url = lambda x: isinstance(x, str) and re.match(r'/|http', x)
    validators = [
        (
            'name',
            lambda x: isinstance(x, str)
        ), (
            'base_url',
            is_url
        ), (
            'query_url',
            lambda x: (is_url(x) and '{query}' in x or is_function(x) or
                       isinstance(x, tuple) and len(x) == 2)
        ), (
            'result_selector',
            lambda x: isinstance(x, list) and len(x) > 0
        ), (
            'get_result_label',
            lambda x: is_function(x)
        ), (
            'next_page_format',
            lambda x: re.search(r'\(\[0-9\]\+\)', x)
        ), (
            'thumbnail_url',
            lambda x: is_url(x) and re.search(r'\.(?:png|jpg)', x)
        )
    ]
    for k, v in validators:
        val = provider.get(k)
        if not val:
            if k not in ['next_page_format', 'thumbnail_url']:
                raise PercuiroUserProvidersException(
                    '{0} provider validation key error: {1!r} not in dictionary'.format(
                        provider.get('name', 'UNKNOWN_NAME'), k))
            else:
                continue
        if not v(val):
            raise PercuiroUserProvidersException(
                '{0} provider validation invalid value error: {1}, {2}'.format(
                    provider.get('name', 'UNKNOWN_NAME'), k, val))
    return True
