# -*- coding: utf-8 -*-

import logging
from flask import Flask
from flask_ldapconn import LDAPConn

app = Flask(__name__)
app.config.from_pyfile('config.py')
logging.basicConfig(level=app.config['RP_LOGLEVEL'])

ldap = LDAPConn(app)
from fido2.server import RelyingParty
rp = RelyingParty(app.config['RP_HOST'], app.config['RP_NAME'])

from . import views
from . import filters
from . import models
from . import cli
