Steps to install Labcomp Site Development Environment [![Build Status](https://travis-ci.com/ebar0n/labcomp.svg?token=DY8zmJsbUNWWXjfwiUs8&branch=master)](https://travis-ci.com/ebar0n/labcomp)
========================================================

### Install and configure docker
0. Install and configure Docker

    0. docker [Docker](https://www.docker.com)

    0. docker-machine [install-machine](https://docs.docker.com/machine/) and [install-virtualbox](https://www.virtualbox.org/wiki/Downloads) *optional in linux* 

    0. docker-compose [install](https://docs.docker.com/compose/install/)

0. Set Var Environment

    * Copy to `env.example` into `django/.env`
    * Edit values in `doango/.env`

### Run the project for development
0. Only in docker-machine

    0. Pre-Build

            labcomp$ docker-machine create --driver virtualbox --virtualbox-memory 1024 --virtualbox-cpu-count 2 labcomp
            labcomp$ docker-machine start labcomp
            labcomp$ eval "$(docker-machine env labcomp)"
            labcomp$ docker-machine ip labcomp
            192.168.99.100
            labcomp$ echo "192.168.99.100 dev.labcomp.com" | sudo tee -a /etc/hosts > /dev/null
            # Or use 127.0.0.1 if you do *not use docker-machine*

0. Build

        labcomp$ docker-compose build

0. Run Django server

        labcomp$ docker-compose up -d

0. Initialize Database

        labcomp$ docker-compose run --rm djangoo python manage.py migrate

0. Visit [http://dev.labcomp.com:8000/](http://dev.labcomp.com:8000/)