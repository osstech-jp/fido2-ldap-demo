# -*- coding: utf-8 -*-

import os

TEMPLATES_AUTO_RELOAD = True
SECRET_KEY = 'secret'

LDAP_SERVER = os.environ.get("LDAP_SERVER", 'localhost')
LDAP_PORT = 389
LDAP_USE_TLS = False
LDAP_BINDDN = 'cn=Manager,dc=example,dc=com'
LDAP_SECRET = 'secret'

FIDO2_RP = os.environ.get("RP_HOST", "localhost")
FIDO2_ATTESTATION="none"
#FIDO2_ATTESTATION="direct"
FIDO2_USER_VERIFICATION="discouraged"
#FIDO2_USER_VERIFICATION="preferred"
