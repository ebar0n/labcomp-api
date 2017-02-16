import os

from fabric.api import cd, env, hosts, local, sudo

LOCAL = any(['deploy_dev' in task for task in env.tasks])

if LOCAL:
    from fabric.api import local as run
    HOME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
else:
    from fabric.api import run
    HOME_DIRECTORY = '/root/labcomp-api'
    env.user = 'root'
    env.password = os.environ.get('PASSWORD', None)
    if not env.password:
        env.key_filename = '~/.ssh/id_rsa.pub'


if any(['update_local_db' in task for task in env.tasks]) or any(['remote_db_backup' in task for task in env.tasks]):
    from fabric.contrib.files import exists
    from fabric.operations import get
    HOME_DIRECTORY_LOCAL = os.path.dirname(os.path.abspath(__file__))
    env.db_name = 'labcomp'
    env.db_user = 'labcomp'

def pull(branch='master'):
    """
    Pull repostory by branch

    Args:
        branch: Name branch

    Example:
        $ fab pull:branch='master'
    """
    with cd(HOME_DIRECTORY):
        run('git checkout .')
        run('git fetch --all')
        run('git checkout {}'.format(branch))
        run('git pull origin {}'.format(branch))


def build(branch='master', yml=''):
    """
    Build by branch

    Args:
        branch: Name branch
        container: Name container
        yml: File docker-compose.yml

    Example:
        $ fab build:branch='master'
    """
    if not LOCAL:
        pull(branch=branch)
    with cd(HOME_DIRECTORY):
        run('docker-compose {} build'.format(yml))


def load(branch='master', yml=''):
    """
    Load by branch

    Args:
        branch: Name branch
        yml: File docker-compose.yml

    Example:
        $ fab load

        Perform deployment
        $ fab load:branch='master',yml=''
    """
    build(branch=branch, yml=yml)
    with cd(HOME_DIRECTORY):
        commands = [
            'django python manage.py migrate --noinput',
            'django python manage.py collectstatic --noinput',
            'django python manage.py compilemessages',
        ]
        run('docker-compose up -d mysql')
        for command in commands:
            run('docker-compose run --rm {}'.format(command))


def deploy(branch='master', yml=''):
    """
    Deploy by branch

    Args:
        branch: Name branch
        yml: File docker-compose.yml

    Example:
        $ fab deploy

        Perform deployment
        $ fab deploy:branch='master',yml=''
    """
    with cd(HOME_DIRECTORY):
        run('docker-compose {} down'.format(yml))
    load(branch=branch, yml=yml)
    with cd(HOME_DIRECTORY):
        run('docker-compose {} up -d'.format(yml))


def deploy_dev():
    """
    Deploy project

    Example:
        $ fab deploy_dev
    """
    deploy()


@hosts('labcomp.edwarbaron.me')
def deploy_production(branch='master'):
    """
    Deploy project by branch

    Args:
        branch: Name branch

    Example:
        $ fab nginx:branch='master'
    """
    deploy(branch=branch, yml='-f docker-compose-production.yml')


def test(sleep=0, debug=''):
    """
    Test by branch

    Example:
        $ fab test
    """
    with cd(HOME_DIRECTORY):
        local('docker-compose up -d mysql && sleep {}'.format(sleep))
        local('docker-compose run --rm django python manage.py check')
        local(
            'docker-compose run --rm -e TEST=true django py.test {}'.format(
                debug
            )
        )


@hosts('labcomp.edwarbaron.me')
def free_m():
    """
    To display memory ram of the server.

    """
    run('free -m')


@hosts('labcomp.edwarbaron.me')
def enable_swap():
    """
    To enable swap on a server.

    """
    free_m()
    run('dd if=/dev/zero of=/swapfile bs=1024 count=1024k')
    run('mkswap /swapfile')
    run('swapon /swapfile')
    run('swapon -s')
    run('echo 10 | sudo tee /proc/sys/vm/swappiness')
    run(('if grep -Fxq "/swapfile       none    swap    sw      0       0 " /etc/fstab > /dev/null;'
         'then echo ya tiene la linea; else echo "/swapfile       none    swap    sw      0       0 "'
         ' >> /etc/fstab; fi'))
    run('echo vm.swappiness = 10 | sudo tee -a /etc/sysctl.conf')
    run('chown root:root /swapfile')
    run('chmod 0600 /swapfile')
    free_m()


@hosts('labcomp.edwarbaron.me')
def remote_db_backup():
    """To generate db backup."""
    with cd(HOME_DIRECTORY):
        fname = '%(db_name)s-mysqlql-production.backup' % env
        if exists(fname):
            run('rm "%s"' % fname)

        run(
            'docker exec -t trip180voluntarybackend_mysql_1 pg_dump -Fc %(db_name)s '
             '-U %(db_user)s -f %(db_name)s-mysqlql-production.backup' % env
        )
        run('docker cp trip180voluntarybackend_mysql_1:/{} {}'.format(
            fname, fname
        ))
        get(HOME_DIRECTORY + '/' + fname, HOME_DIRECTORY_LOCAL + '/' + fname)
        run('rm "%s"' % fname)


def drop_create_schema(yml=''):
    local(
        'docker-compose {} run --rm django /bin/bash -c '
        '"echo \'DROP SCHEMA PUBLIC CASCADE; CREATE SCHEMA PUBLIC;\' | '
        'python manage.py dbshell"'.format(yml)
    )

@hosts('labcomp.edwarbaron.me')
def update_local_db(yml=''):
    """To generate db backup, and update local db"""
    drop_create_schema()
    remote_db_backup()
    fname = '%(db_name)s-mysqlql-production.backup' % env
    local('docker cp {} trip180voluntarybackend_mysql_1:/{}'.format(fname, fname))
    try:
        local(
            'docker exec -t trip180voluntarybackend_mysql_1 pg_restore -U %(db_user)s '
            '-d %(db_name)s -F c -c %(db_name)s-mysqlql-production.backup' % env
        )
    except:
        pass
    local('docker-compose {} run --rm django python manage.py migrate'.format(yml))
    local('rm "%s"' % fname)
