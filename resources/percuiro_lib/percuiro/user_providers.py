# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import sys
import os


class PercuiroUserProvidersException(Exception):
    pass


def import_user_providers(my_providers_fpath):
    if not os.path.exists(my_providers_fpath):
        raise PercuiroUserProvidersException(
            '{!r} does not exist on filesystem'.format(my_providers_fpath))

    fname = os.path.basename(my_providers_fpath)
    fpath = os.path.dirname(my_providers_fpath)
    sys.path.append(fpath)
    user_providers = __import__(fname.rstrip('.py'))
    sys.path.remove(fpath)
    return user_providers


def validate_user_providers_module(user_providers_module):
    try:
        user_providers = getattr(user_providers_module, 'my_providers')
    except AttributeError:
        raise PercuiroUserProvidersException(
            'Required variable `my_providers` not found in my_providers module.')

    if not isinstance(user_providers, tuple):
        raise PercuiroUserProvidersException(
            'my_providers variable should be a `tuple`, `{}` found.'.format(
                type(user_providers)))
    return True
