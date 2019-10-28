#!/bin/sh
set -x

ulimit -n 1024
USER=openldap
DEBUGLEVEL=stats

if [ ! -e "/var/lib/ldap/.initialized" ]; then
    sudo -u ${USER} slapadd -l /etc/ldap/init.ldif
    touch /var/lib/ldap/.initialized
fi

exec /usr/sbin/slapd -u ${USER} -f /etc/ldap/slapd.conf -d ${DEBUGLEVEL}

