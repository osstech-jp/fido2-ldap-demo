#!/bin/sh
set -x

#FLASK_DEBUG=True

CERT=certs/${RP_HOST}/cert.pem
KEY=certs/${RP_HOST}/key.pem

exec flask run --host 0.0.0.0 --cert=${CERT} --key=${KEY}

