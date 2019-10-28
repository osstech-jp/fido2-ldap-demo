# -*- coding: utf-8 -*-

import os

TEMPLATES_AUTO_RELOAD = True
SECRET_KEY = 'secret'

LDAP_SERVER = os.environ.get("LDAP_SERVER", 'localhost')
LDAP_PORT = 389
LDAP_USE_TLS = False
LDAP_BINDDN = 'cn=Manager,dc=example,dc=com'
LDAP_SECRET = 'secret'

RP_LOGLEVEL = os.environ.get("RP_LOGLEVEL", "INFO")
RP_HOST = os.environ.get("RP_HOST", "localhost")
RP_NAME = os.environ.get("RP_NAME", "Demo RP")
RP_ATTESTATION="none"
#RP_ATTESTATION="direct"
RP_USER_VERIFICATION="discouraged"
#RP_USER_VERIFICATION="preferred"
