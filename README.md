# Demo RP Server

## run

~~~
$ docker-compose up --build
~~~

You can access to https://localhost/

If you want to use another hostname.
You need to set `RP_HOST` environment value that is also used for FIDO2 `rp.origin`

docker-compose.yml:

~~~
-       RP_HOST: 'localhost'
+       RP_HOST: 'HOSTNAME'
~~~

and put SSL certificates:

- rp/certs/*HOSTNAME*/cert.pem
- rp/certs/*HOSTNAME*/key.pem

## ldapsearch

~~~
$ docker-compose exec ldap ldapsearch -x -b "dc=example,dc=com"
~~~

## CLI

~~~
$ docker-compose exec rp flask
Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  cred_delete
  cred_show
  routes       Show the routes for the app.
  run          Run a development server.
  shell        Run a shell in the app context.
  user_add
  user_auth
  user_delete
  user_list
  user_show
~~~

* add user

~~~
$ docker-compose exec rp flask user_add username password
~~~
