# LABCOMP App

## Requirements

1. Install and configure Docker

    1. Install docker. [Docker](https://www.docker.com)

    1. Install docker-machine and virtualbox. [Machine](https://docs.docker.com/machine/), [Virtualbox](https://www.virtualbox.org/wiki/Downloads) `optional in linux`

    1. Intall docker-compose. [Compose](https://docs.docker.com/compose/install/)

1. Set Var Environment

    * Copy to `env.example` into `.env`

            cp env.example .env

    * Edit values in `.env`

            nano .env

### Run the project DEV

1. Only in docker-machine

    1. Pre-Build

            docker-machine create --driver virtualbox --virtualbox-memory 10240 --virtualbox-cpu-count 2 labcomp
            docker-machine start labcomp
            eval "$(docker-machine env labcomp)"
            docker-machine ip labcomp
            192.168.99.100
            echo "192.168.99.100 dev.labcomp.com" | sudo tee -a /etc/hosts > /dev/null
1. Not use docker-machine

        echo "127.0.1.1 dev.labcomp.com" | sudo tee -a /etc/hosts > /dev/null

1. Enable cache for Dev

    1. Install

            docker pull ebar0n/proxy-cache

            docker run --name proxy-cache -d --restart=always \
              --publish 3128:3128 --publish 3141:3141 --publish 3142:3142 \
              --volume ~/data/proxy-cache/squid/:/var/spool/squid3 \
              --volume ~/data/proxy-cache/devpi:/var/.devpi/server \
              --volume ~/data/proxy-cache/aptcacherng:/var/cache/apt-cacher-ng \
              ebar0n/proxy-cache

    1. Using

            docker start proxy-cache

    1. Check cache container IP == "172.17.1.2"

            docker inspect proxy-cache | grep '"IPAddress":'

1. Build containers

          docker-compose build

## FrontEnd

...

## BackEnd

1. Start container DB

        docker-compose up -d mysql

1. Apply migrations

        docker-compose run --rm django python manage.py migrate

1. Run Django Project

        docker-compose up -d

1. Open project on browser

        http://dev.labcomp.com:8000

### Django Admin

1. Create superuser (Execute command and follow the steps)

        docker-compose run --rm django python manage.py createsuperuser

1. Access to django admin

        http://dev.labcomp.com:8000/admin/

### Run tests to code

1. Exit instantly on first error or failed test

        docker-compose run --rm -e TEST=true django py.test -x accounts/tests.py

1. Activate the Python Debugger

        docker-compose run --rm -e TEST=true django py.test --pdb accounts/tests.py

1. Run all the tests

        docker-compose run --rm -e TEST=true django py.test

### Run tests to style

1. Run tests isort

        docker-compose run --rm django isort -c -rc -df

1. Run tests flake8

        docker-compose run --rm django flake8

#### Run all test

        ./test-all.sh

### Django Internationalization

1. Add import and use the function _ to mark the text to translate

        from django.utils.translation import ugettext as _
        hello = _('Hello world')

1. Execute this command to runs over the entire source tree of the current directory and pulls out all strings marked for translation.

        docker-compose run --rm django python manage.py makemessages --no-location -l es

1. Edit file django/locale/es/LC_MESSAGES/django.po and add a translation.

        #: module/file.py:12
        msgid "Hello world"
        msgstr "Hola mundo"

1. Compiles .po files to .mo files for use with builtin gettext support.

        docker-compose run --rm django python manage.py compilemessages
