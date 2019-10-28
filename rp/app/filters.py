# -*- coding: utf-8 -*-

import binascii

from . import app

@app.template_filter('hexlify')
def hexlify(b):
    return binascii.hexlify(b).decode()
