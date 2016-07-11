# LABCOMP App

## Requirements

0. Install and configure Docker

    0. Install docker. [Docker](https://www.docker.com)

    0. Install docker-machine and virtualbox. [Machine](https://docs.docker.com/machine/), [Virtualbox](https://www.virtualbox.org/wiki/Downloads) `optional in linux`

    0. Intall docker-compose. [Compose](https://docs.docker.com/compose/install/)

0. Set Var Environment

    * Copy to `env.example` into `.env`

            cp env.example .env

    * Edit values in `.env`

            nano .env

### Run the project DEV

0. Only in docker-machine

    0. Pre-Build

            docker-machine create --driver virtualbox --virtualbox-memory 10240 --virtualbox-cpu-count 2 labcomp
            docker-machine start labcomp
            eval "$(docker-machine env labcomp)"
            docker-machine ip labcomp
            192.168.99.100
            echo "192.168.99.100 dev.labcomp.com" | sudo tee -a /etc/hosts > /dev/null
0. Not use docker-machine

        echo "127.0.0.1 dev.labcomp.com" | sudo tee -a /etc/hosts > /dev/null

0. Enable cache for Dev

    0. Install

            docker pull ebar0n/proxy-cache

            docker run --name proxy-cache -d --restart=always \
              --publish 3128:3128 --publish 3141:3141 --publish 3142:3142 \
              --volume ~/data/proxy-cache/squid/:/var/spool/squid3 \
              --volume ~/data/proxy-cache/devpi:/var/.devpi/server \
              --volume ~/data/proxy-cache/aptcacherng:/var/cache/apt-cacher-ng \
              ebar0n/proxy-cache

    0. Using

            docker start proxy-cache

    0. Check cache container IP == "172.17.0.2"

            docker inspect proxy-cache | grep '"IPAddress":'

0. Build containers

          docker-compose build

## FrontEnd

...

## BackEnd

0. Start container DB

        docker-compose up -d mysql

0. Apply migrations

        docker-compose run --rm django python manage.py migrate

0. Run Django Project

        docker-compose up -d

0. Open project on browser

        http://dev.labcomp.com:8000

### Django Admin

0. Create superuser (Execute command and follow the steps)

        docker-compose run --rm django python manage.py createsuperuser

0. Access to django admin

        http://dev.labcomp.com:8000/admin/

### Run tests to code

0. Exit instantly on first error or failed test

        docker-compose run --rm -e TEST=true django py.test -x accounts/tests.py

0. Activate the Python Debugger

        docker-compose run --rm -e TEST=true django py.test --pdb accounts/tests.py

0. Run all the tests

        docker-compose run --rm -e TEST=true django py.test

### Run tests to style

0. Run tests isort

        docker-compose run --rm django isort -c -rc -df

0. Run tests flake8

        docker-compose run --rm django flake8

#### Run all test

        ./test-all.sh

### Django Internationalization

* Add import and use the function _ to mark the text to translate

        from django.utils.translation import ugettext as _
        hello = _('Hello world')

*  Execute this command to runs over the entire source tree of the current directory and pulls out all strings marked for translation.

        docker-compose run --rm django python manage.py makemessages -l es

*  Edit file django/locale/es/LC_MESSAGES/django.po and add a translation.

        #: module/file.py:12
        msgid "Hello world"
        msgstr "Hola mundo"

*  Compiles .po files to .mo files for use with builtin gettext support.

        docker-compose run --rm django python manage.py compilemessages
