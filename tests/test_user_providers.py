# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os

from nose.tools import raises
from percuiro.user_providers import (
    import_user_providers, validate_user_providers_module,
    PercuiroUserProvidersException)


class MockMyProvidersModule(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_import_my_providers():
    user_providers_fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'test_data/my_providers.py')
    user_providers = import_user_providers(user_providers_fpath)
    assert user_providers

    @raises(PercuiroUserProvidersException)
    def test_does_not_exist():
        import_user_providers('/__if_this_exists_itd_be_weird/lol.py')
    test_does_not_exist()

    @raises(PercuiroUserProvidersException)
    def test_could_not_import():
        import_user_providers(user_providers_fpath.replace('.py', '.foo'))
    test_could_not_import()


def test_validate_user_profiles():
    my_providers = MockMyProvidersModule()

    @raises(PercuiroUserProvidersException)
    def my_providers_not_exists():
        validate_user_providers_module(my_providers)
    my_providers_not_exists()

    my_providers.my_providers = 1

    @raises(PercuiroUserProvidersException)
    def my_providers_no_tuple():
        validate_user_providers_module(my_providers)
    my_providers_no_tuple()

    my_providers.my_providers = tuple()
    assert validate_user_providers_module(my_providers)
