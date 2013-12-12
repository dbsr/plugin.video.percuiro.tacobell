# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import util
from providers import downtr
from provider import Provider


def get_active_providers():
    return dict((p['name'], Provider(**p)) for p in [
        downtr
    ])
