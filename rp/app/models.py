# -*- coding: utf-8 -*-

import base64
import binascii
import ldap3
from fido2 import cbor

from flask_login import UserMixin

from fido2.ctap2 import AttestedCredentialData

from . import app
from . import ldap

class User(ldap.Entry, UserMixin):
    base_dn = 'ou=Users,dc=example,dc=com'
    object_classes = ['account', 'simpleSecurityObject']
    entry_rdn = ['uid']
    uid = ldap.Attribute('uid')
    description = ldap.Attribute('description')
    password = ldap.Attribute('userPassword')
    entryUUID = ldap.Attribute('entryUUID')

    @classmethod
    def get(self, uid):
        return User.query.filter('uid: {}'.format(uid)).first()

    @classmethod
    def get_by_entryUUID(self, entryUUID):
        return User.query.filter('entryUUID: {}'.format(entryUUID)).first()

    @property
    def credentials(self):
        query_filter = 'fido2UserID: {}'.format(self.entryUUID)
        return Credential.query.filter(query_filter).all()

    def get_id(self):
        return self.uid

    def add_credential(self, auth_data):
        credential_data = auth_data.credential_data
        credential = Credential(
            id = base64.urlsafe_b64encode(credential_data.credential_id).decode().strip('='),
            raw_id = credential_data.credential_id,
            aaguid = credential_data.aaguid,
            public_key = cbor.encode(credential_data.public_key),
            userid = self.entryUUID,
            counter = int(auth_data.counter),
        )
        attrs = credential.get_attributes_dict()
        changes = credential.get_entry_add_dict(attrs)
        res = credential.save()
        return res

    def delete_credential(self, credential_id):
        for credential in self.credentials:
            if credential.id == credential_id:
                res = credential.delete()
                return res
        return False

class Credential(ldap.Entry):
    base_dn = 'ou=Credentials,dc=example,dc=com'
    object_classes = ['fido2Credential']
    entry_rdn = ['fido2CredentialID']
    id = ldap.Attribute('fido2CredentialID')
    raw_id = ldap.Attribute('fido2RawID')
    public_key = ldap.Attribute('fido2PublicKey')
    counter = ldap.Attribute('fido2SignCount')
    userid = ldap.Attribute('fido2UserID')
    credential_name = ldap.Attribute('fido2CredentialName')
    aaguid = ldap.Attribute('fido2AAGUID')

    def to_credential_data(self):
        ret = AttestedCredentialData.create(self.aaguid,
                                            self.raw_id,
                                            cbor.decode(self.public_key))
        return ret

    @classmethod
    def get(self, id):
        return Credential.query.filter('id: {}'.format(id)).first()

    @property
    def user(self):
        query_filter = 'entryUUID: {}'.format(self.userid)
        return User.query.filter(query_filter).first()
