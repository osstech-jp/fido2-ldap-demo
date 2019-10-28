FROM debian:buster-slim
RUN apt-get update -qq &&\
 DEBIAN_FRONTEND=noninteractive \
 apt-get install -y slapd ldap-utils procps sudo

RUN rm -rf /etc/ldap/slapd.d && \
    rm -rf /var/lib/ldap/*

COPY slapd.conf /etc/ldap/
COPY fido2.schema /etc/ldap/schema/
RUN chown openldap.openldap /etc/ldap/slapd.conf
RUN chmod 400 /etc/ldap/slapd.conf
COPY run.sh /
COPY init.ldif /etc/ldap/

EXPOSE 389
CMD ["/run.sh"]
