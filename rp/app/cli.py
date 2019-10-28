# -*- coding: utf-8 -*-

import click

from . import app
from . import ldap
from .models import User
from .models import Credential

import cbor2

@app.cli.command("user_list")
def user_list():
    users = User.query.all()
    for user in users:
        print(user.uid)

@app.cli.command("user_add")
@click.argument("username")
@click.argument("password")
def user_add(username, password):
    user = User(uid=username, password=password)
    res = user.save()
    print(res)

@app.cli.command("user_delete")
@click.argument("username")
def user_delete(username):
    user = User.get(username)
    if not user:
        print("user not found")
        return
    creds = user.credentials
    for cred in creds:
        res = cred.delete()
        if res:
            print("cred deleted:", cred.id)
    res = user.delete()
    if res:
        print("user deleted:", user.dn)

@app.cli.command("user_auth")
@click.argument("username")
@click.argument("password")
def user_auth(username, password):
    user = User.get(username)
    if not user:
        print("user not found")
        return
    res = user.authenticate(password)
    print(res)

@app.cli.command("user_show")
@click.argument("username")
def user_show(username):
    user = User.get(username)
    print("DN:", user.dn)
    print("uid:", user.uid)
    print("entryUUID:", user.entryUUID)
    credentials = user.credentials
    print("credentials: ")
    for cred in credentials:
        print(" ", cred.id)

@app.cli.command("cred_show")
@click.argument("credential_id")
def cred_show(credential_id):
    cred = Credential.get(credential_id)
    if not cred:
        print("Credential not found")
        exit(0)

    print("credential_id: ", cred.id)
    print("user_id: ", cred.userid)
    print("counter: ", cred.counter)
    print("public_key: ", cbor2.loads(cred.public_key))
    user = cred.user
    if not user:
        print("Credential user not found")
        exit(0)
    print("user: ", user.dn)

@app.cli.command("cred_delete")
@click.argument("credential_id")
def cred_delete(credential_id):
    cred = Credential.get(credential_id)
    if not cred:
        print("Credential not found")
        exit(0)
    res = cred.delete()
    print(res)
