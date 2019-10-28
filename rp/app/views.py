# -*- coding: utf-8 -*-

import pprint
pp = pprint.PrettyPrinter(indent=2)
from uuid import UUID

from . import app
from . import rp

from .models import User
from .models import Credential

from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import abort

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import LoginManager

from fido2 import cbor
from fido2.server import Fido2Server
from fido2.server import ATTESTATION
from fido2.client import ClientData
from fido2.ctap2 import AttestationObject
from fido2.ctap2 import AuthenticatorData

server = Fido2Server(rp, attestation=app.config['RP_ATTESTATION'])

login_manager = LoginManager()
login_manager.login_view =  "index"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return User.get(username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login_with_password', methods=['POST'])
def login_with_password():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username:
        abort(401)
    if not password:
        abort(401)
    user = User.get(username)
    if not user:
        abort(401)
    res = user.authenticate(password)
    if res:
        login_user(user)
    else:
        abort(401)
    return redirect('/home')

@app.route('/home')
@login_required
def home():
    return render_template('home.html', credentials=current_user.credentials)

@app.route('/register/options', methods=['POST'])
@login_required
def register_options():
    app.logger.debug('/register/response')
    if 'resident_key' in request.json:
        resident_key = request.json['resident_key']
    else:
        regident_key = False
    credentials = []
    user_verification = app.config.get('RP_USER_VERIFICATION', "discouraged")
    user_id = UUID(current_user.entryUUID).bytes
    registration_data, state = server.register_begin({
        'id': user_id,
        'name': current_user.uid,
        'displayName': current_user.description,
        'icon': 'https://example.com/'
    }, credentials, user_verification=user_verification,
    resident_key=resident_key)
    session['state'] = state
    app.logger.debug('registration_data:\n%s', pp.pformat(registration_data))
    app.logger.debug('state:\n%s', pp.pformat(state))
    return cbor.encode(registration_data)

@app.route('/register/response', methods=['POST'])
@login_required
def register_response():
    app.logger.debug('/register/response')
    state = session['state']
    data = cbor.decode(request.get_data())
    client_data = ClientData(data['clientDataJSON'])
    att_obj = AttestationObject(data['attestationObject'])
    app.logger.debug('clientData:\n%s', pp.pformat(client_data))
    app.logger.debug('attestationObject:\n%s', pp.pformat(att_obj))
    auth_data = server.register_complete(state, client_data, att_obj)
    app.logger.debug('credential_data:\n%s',
                     pp.pformat(auth_data.credential_data))
    username = current_user.get_id()
    res = current_user.add_credential(auth_data)
    if not res:
        app.logger.error('Registration failed.')
        abort(500)
    app.logger.info('Registration succeeded.')
    return cbor.encode({'status': 'OK'})

@app.route('/remove_credential', methods=['POST'])
@login_required
def remove_authenticator():
    if 'credential_id' not in request.json:
        abort(400)
    credential_id = request.json['credential_id']
    res = current_user.delete_credential(credential_id)
    if res:
        return "OK"
    else:
        abort(400)

@app.route('/assertion/options', methods=['POST'])
def assertion_options():
    app.logger.debug("/assertion/options")
    if 'username' in request.json:
        username = request.json['username']
        user = User.get(username)
        if not user:
            abort(404)
        credential_data = [credential.to_credential_data() for credential in user.credentials]
        user_verification = app.config.get('RP_USER_VERIFICATION', "discouraged")
        auth_data, state = server.authenticate_begin(credential_data,
                                                     user_verification=user_verification)
        session['state'] = state
    else:
        # using regident key
        auth_data, state = server.authenticate_begin([])
        session['state'] = state
    app.logger.debug('auth_data:\n%s', pp.pformat(auth_data))
    app.logger.debug('state:\n%s', pp.pformat(state))
    return cbor.encode(auth_data)

@app.route('/assertion/response', methods=['POST'])
def assertion_response():
    app.logger.debug("/assertion/response")
    data = cbor.decode(request.get_data())
    app.logger.debug('post_data:\n%s', pp.pformat(data))
    credential_id = data['id']
    raw_id = data['rawId']
    client_data = ClientData(data['clientDataJSON'])
    app.logger.debug('client_data:\n%s', pp.pformat(client_data))
    auth_data = AuthenticatorData(data['authenticatorData'])
    app.logger.debug('auth_data:\n%s', pp.pformat(auth_data))
    signature = data['signature']
    credential = Credential.get(credential_id)
    if not credential:
        abort(404)
    credential_data = credential.to_credential_data()
    server.authenticate_complete(
        session.pop('state'),
        [credential_data],
        raw_id,
        client_data,
        auth_data,
        signature
    )
    # Checking signCount
    if auth_data.counter > credential.counter:
        # TODO: flask_ldapconn is not allow to store integer value
        credential.counter = str(auth_data.counter)
        credential.save()
    else:
        app.logger.warn('wrong counter: stored counter=%d but %d asserted',
                        credential.counter, auth_data.counter)
        abort(404)
    user = credential.user
    if not user:
        abort(404)
    login_user(user)
    return cbor.encode({'status': 'OK'})
