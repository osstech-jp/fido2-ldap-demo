#!/bin/sh
set -x

#FLASK_DEBUG=True

export FLASK_RUN_CERT=certs/${RP_HOST}/cert.pem
export FLASK_RUN_KEY=certs/${RP_HOST}/key.pem

exec uwsgi uwsgi.ini

