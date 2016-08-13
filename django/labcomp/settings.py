import environ

root = environ.Path(__file__) - 2
env = environ.Env()

BASE_DIR = root()
public_root = root.path('public/')

DEBUG = env.bool('DEBUG')
SECRET_KEY = env('SECRET_KEY')

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# CSRF_COOKIE_DOMAIN = env('COOKIE_DOMAIN')
# SESSION_COOKIE_DOMAIN = env('COOKIE_DOMAIN')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

ADMIN_MAIL = env('ADMIN_MAIL')
ADMINS = (
    (env('ADMIN_NAME'), ADMIN_MAIL),
)
MANAGERS = ADMINS
ADMIN_FOR = MANAGERS

EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DATABASES = {
    # 'default': env.db('DATABASE_URL')
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'local',
    }
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

INSTALLED_APPS = (
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_python3_ldap',
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'sorl.thumbnail',
    'import_export',

    # apps
    'lab_accounts',
    'lab_rooms',
    'lab_subjects',
    'lab_reservations',

    'utils',
    'scripts',
)

DEBUG_TOOLBAR = env.bool('DEBUG_TOOLBAR')
if DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES

    INSTALLED_APPS = (
        'debug_toolbar',
    ) + INSTALLED_APPS

    def custom_show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
        'JQUERY_URL': '/static/js/vendor/jquery-1.11.3.min.js',
    }

# SSL
if env.bool('SSL'):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Celery
TEST = env.bool('TEST')
if TEST:
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

BROKER_URL = env('BROKER_URL')
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': env('CACHE'),
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_KEY = 'public_key_labcomp'

TIME_ZONE = 'America/Caracas'

LANGUAGE_CODE = 'es'
USE_I18N = True
USE_L10N = True
USE_TZ = False

ROOT_URLCONF = 'labcomp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [public_root('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'labcomp.wsgi.application'

locale_root = root.path('locale/')

LOCALE_PATHS = (locale_root(),)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_DIRS = (public_root('static'),)
STATIC_ROOT = public_root('staticfiles')
STATIC_URL = env('STATIC_URL')
MEDIA_ROOT = public_root('media')
MEDIA_URL = env('MEDIA_URL')

AUTH_USER_MODEL = 'lab_accounts.User'

AUTHENTICATION_BACKENDS = (
    # Django
    'django.contrib.auth.backends.ModelBackend',
    'django_python3_ldap.auth.LDAPBackend',
)

# Config DRF
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

# LDAP
# The URL of the LDAP server.
LDAP_AUTH_URL = env('LDAP_AUTH_URL')

# Initiate TLS on connection.
LDAP_AUTH_USE_TLS = False

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = 'ou=people,dc=example,dc=com'

# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = 'inetOrgPerson'

# User model fields mapped to the LDAP
# attributes that represent them.
LDAP_AUTH_USER_FIELDS = {
    'username': 'uid',
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

# A tuple of django model fields used to uniquely identify a user.
LDAP_AUTH_USER_LOOKUP_FIELDS = ('username',)

# Path to a callable that takes a dict of {model_field_name: value},
# returning a dict of clean model data.
# Use this to customize how data loaded from LDAP is saved to the User model.
LDAP_AUTH_CLEAN_USER_DATA = 'django_python3_ldap.utils.clean_user_data'

# Path to a callable that takes a user model and a dict of {ldap_field_name: [value]},
# and saves any additional user relationships based on the LDAP data.
# Use this to customize how data loaded from LDAP is saved to User model relations.
# For customizing non-related User model fields, use LDAP_AUTH_CLEAN_USER_DATA.
LDAP_AUTH_SYNC_USER_RELATIONS = 'django_python3_ldap.utils.sync_user_relations'

# Path to a callable that takes a dict of {ldap_field_name: value},
# returning a list of [ldap_search_filter]. The search filters will then be AND'd
# together when creating the final search filter.
LDAP_AUTH_FORMAT_SEARCH_FILTERS = 'django_python3_ldap.utils.format_search_filters'

# Path to a callable that takes a dict of {model_field_name: value}, and returns
# a string of the username to bind to the LDAP server.
# Use this to support different types of LDAP server.
LDAP_AUTH_FORMAT_USERNAME = 'django_python3_ldap.utils.format_username_openldap'
# LDAP_AUTH_FORMAT_USERNAME = 'django_python3_ldap.utils.format_username_active_directory'

# Sets the login domain for Active Directory users.
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = 'labcom.com'

# The LDAP username and password of a user for authenticating the `ldap_sync_users`
# management command. Set to None if you allow anonymous queries.
LDAP_AUTH_CONNECTION_USERNAME = None
LDAP_AUTH_CONNECTION_PASSWORD = None


# Django Jet
JET_DEFAULT_THEME = 'light-violet'
JET_SIDE_MENU_COMPACT = True
