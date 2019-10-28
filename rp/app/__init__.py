# -*- coding: utf-8 -*-

#import logging
#logging.basicConfig(level=logging.DEBUG)

from flask import Flask
from flask_ldapconn import LDAPConn

app = Flask(__name__)
app.config.from_pyfile('config.py')
ldap = LDAPConn(app)

from fido2.server import RelyingParty
rp = RelyingParty(app.config['FIDO2_RP'], 'Demo RP')

from . import views
from . import filters
from . import models
from . import cli
