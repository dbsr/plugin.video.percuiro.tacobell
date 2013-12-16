# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import util
from providers import downtr_co, filestube_com, theextopia_com
from provider import Provider


def get_active_providers():
    return dict((p['name'], Provider(**p)) for p in [
        downtr_co,
        filestube_com,
        theextopia_com
    ])
