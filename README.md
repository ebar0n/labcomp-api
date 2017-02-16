# LABCOMP App

[![Build Status](https://travis-ci.org/UNETDevStudents/labcomp-api.svg?branch=master)](https://travis-ci.org/UNETDevStudents/labcomp-api)

## Requirements

### Install and configure Docker

1. Install docker. [Docker](https://docker.github.io/engine/installation/)

1. Intall docker-compose. [Compose](https://docs.docker.com/compose/install/)

### Set Var Environment

1. Copy to `env.example` into `.env`

        cp env.example .env

1. Edit values in `.env`

        nano .env

1. Config domain

        echo "127.0.1.1 dev.labcomp.com" | sudo tee -a /etc/hosts > /dev/null

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

### Django Internationalization

1. Execute this command to runs over the entire source tree of the current directory and pulls out all strings marked for translation.

        docker-compose run --rm django python manage.py makemessages --no-location -l es

1. Edit file public/locale/es/LC_MESSAGES/django.po and add a translation.

        msgid "Hello world"
        msgstr "Hola mundo"

1. Compiles .po files to .mo files for use with builtin gettext support.

        docker-compose run --rm django python manage.py compilemessages

### Run the project for Production

1. Build

        docker-compose -f docker-compose-production.yml build

1. Initialize

        docker-compose -f docker-compose-production.yml up -d mysql
        docker-compose -f docker-compose-production.yml run --rm django python manage.py migrate --noinput
        docker-compose -f docker-compose-production.yml run --rm django python manage.py collectstatic --noinput
        docker-compose -f docker-compose-production.yml run --rm django python manage.py compilemessages

1. Run Django server

        docker-compose -f docker-compose-production.yml up -d

1. Visit API [api.labcomp.edwarbaron.me/](http://api.labcomp.edwarbaron.me/)

### Automatic deploy using `fabric`

1. On Linux

        pip install fabric
        ~/.local/bin/fab deploy_dev

1. On macOS

        pip install --user fabric
        ~/Library/Python/2.7/bin/fab deploy_dev

1. Other taks

    1. fab deploy_dev
    1. fab deploy_production
    1. fab test
    1. fab update_local_db
