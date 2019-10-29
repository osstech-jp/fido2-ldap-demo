# Demo RP Server

## run

~~~
$ docker-compose up --build
~~~

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
