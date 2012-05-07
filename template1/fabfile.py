import os
from fabric import utils
from fabric.api import env, require, run
from fabric.contrib.project import rsync_project
from fabric.operations import sudo

RSYNC_EXCLUDE = [
    '*.db',
    '*.pyc',
    '*.sqlite3',
    '.git*',
    'bin*',
    'env/*',
    'media/*',
    'tests/*',
    'whoosh_index',
    'static/sass',
    '.sass-cache',
    'DS_Store',
    'pylintrc',
    'config.rb',
    'fabfile.py',

    # Production (prevent delete)
    'apache2/*',
    'http/production.conf',
    'http/production.py',
    'settings/production.py',
]

env.python_version = 'python2.7'
env.project = '{{ project_name }}'
env.local_root_path = os.path.abspath(os.path.dirname(__file__))


def _paths():
    env.project_path = os.path.join(env.root, env.project)
    env.project_root_path = os.path.join(env.project_path, env.project)

    # Manage file
    env.manage_file = os.path.join(env.project_path, 'manage.py')

    # Http paths
    env.static_path = os.path.join(env.root, '%s_static' % env.project)
    env.http_path = os.path.join(env.project_root_path, 'http')
    env.http_conf = os.path.join(env.http_path, '%s.conf' % env.environment)
    env.apache2_path = os.path.join(env.project_path, 'apache2', 'conf')
    env.apache2_conf = os.path.join(env.apache2_path, '%s.conf' % env.project)
    env.wsgi_file = os.path.join(env.http_path, '%s.py' % env.project)

    # Virtualenv paths
    env.virtualenv_root = os.path.join(env.project_path, 'env')
    env.virtualenv_activate = os.path.join(env.virtualenv_root, 'bin',
        'activate')

    # Requirements path
    env.requirements = os.path.join(env.project_root_path,
        'requirements', '%s.txt' % env.environment)

    # Crons path
    env.crons_path = os.path.join(env.project_root_path, 'cron')


def staging():
    """
    Use staging environment on remote host.
    """
    env.environment = 'staging'
    env.python_version = 'python2.6'

    # Remote settings
    env.user = 'username'
    env.hosts = ['192.168..0.0', ]

    # Paths
    env.root = os.path.join('/home', 'username', 'webapps')
    _paths()


def production():
    """
    Use production environment on remote host.
    """
    env.environment = 'production'
    env.python_version = 'python2.7'

    # Remote settings
    env.hosts = ['108.59.11.109', ]
    env.user = 'username'

    # Paths
    env.root = os.path.join('/home', 'username', 'webapps')
    _paths()


def create_virtualenv():
    """
    Setup virtualenv on remote host.
    """
    require('virtualenv_root', provided_by=('staging', 'production'))

    run(('virtualenv --clear --no-site-packages --distribute '
        '--python=%(python_version)s %(virtualenv_root)s' % env))


def deploy():
    """
    Send the code to the remote host.
    """
    require('project_root_path', provided_by=('staging', 'production'))

    # Copy the project
    rsync_project(
        remote_dir=env.root,
        local_dir=env.local_root_path,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts='--omit-dir-times',
    )

    # Make apache2 dir (for Webfaction)
    run('mkdir -p %s' % env.apache2_path)
    # Remove symbolic link if exists
    run('rm -f %s' % env.apache2_conf)
    # Create a symbolic link to http conf
    run('ln -s %s %s' % (env.http_conf, env.apache2_conf))


def update_requirements():
    """
    Update Python dependencies on remote host.
    """
    require('virtualenv_activate', provided_by=('staging', 'production'))

    command = ('source %(virtualenv_activate)s; '
        'pip install -E %(virtualenv_root)s '
        '-r %(_requirements)s; deactivate')

    run(command % {
        'virtualenv_activate': env.virtualenv_activate,
        'virtualenv_root': env.virtualenv_root,
        '_requirements': env.requirements,
    })


def syncdb():
    """
    Execute syncdb on remote host.
    """
    require('virtualenv_activate', provided_by=('staging', 'production'))

    run(('source %(virtualenv_activate)s; python %(manage_file)s '
        ' syncdb --settings=settings.%(environment)s') % env)


def migrate(apps):
    """
    Execute South on remote host, to update the database structure.
    """
    require('manage_file', provided_by=('staging', 'production'))

    commands = [('python %(manage_file)s migrate %(app)s '
            '--settings=settings.%(environment)s') % {
        'manage_file': env.manage_file,
        'app': app,
        'environment': env.environment,
    } for app in apps.split()]

    run('source %(virtualenv_activate)s; %(commands)s; deactivate' % {
        'virtualenv_activate': env.virtualenv_activate,
        'commands': ';'.join(commands),
    })


def http_restart():
    """
    Restart the HTTP server on remote server.
    """
    require('environment', provided_by=('staging', 'production'))

    if env.environment == 'staging':
        sudo('/sbin/service httpd restart')
    else:
        run(os.path.join(env.project_path, 'apache2/bin/restart'))


def database_restart():
    """
    Restart the database server on remote server.
    """
    require('environment', provided_by=('staging', 'production'))

    if env.environment == 'staging':
        sudo('/sbin/service mysqld restart')
    else:
        utils.abort('Not yet implemented in production')


def collect_static():
    """
    Collect all static files from Django apps and copy them into the public
    static folder.
    """
    require('project_root_path', provided_by=('staging', 'production'))

    run(('source %(virtualenv_activate)s; '
            'python %(manage_file)s collectstatic %(settings_condition)s --clear; '
            'python %(manage_file)s compress %(settings_condition)s; '
            'deactivate') % {
        'virtualenv_activate': env.virtualenv_activate,
        'manage_file': env.manage_file,
        'settings_condition': '--settings=settings.%s' % env.environment,
    })


def rebuild_index():
    """
    Rebuild all indexes used by Haystack in search.
    """
    require('project_root_path', provided_by=('staging', 'production'))

    run('%s' % os.path.join(env.crons_path, 'rebuild_index.sh'))


def update_index():
    """
    Update all indexes used by Haystack in search.
    """
    require('project_root_path', provided_by=('staging', 'production'))

    run('%s' % os.path.join(env.crons_path, 'update_index.sh'))


def bootstrap():
    """
    Initialize remote host environment.
    """
    require('root', provided_by=('staging', 'production'))

    # Create virtualenv to wrap the environment
    create_virtualenv()
    # Send the project to the remote host
    deploy()
    # Install dependencies on the virtualenv
    update_requirements()
    # Create the database
    syncdb()
    # Restart http server
    http_restart()
