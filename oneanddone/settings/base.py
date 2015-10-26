"""
Django settings for oneanddone project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import socket
import urllib

from django.core.urlresolvers import reverse_lazy
from django.utils.functional import lazy
from django.utils.safestring import mark_safe

import dj_database_url
from decouple import Csv, config
from django_sha2 import get_password_hashers


_dirname = os.path.dirname
ROOT = _dirname(_dirname(_dirname(os.path.abspath(__file__))))


def path(*args):
    return os.path.join(ROOT, *args)


# Environment-dependent settings. These are loaded from environment
# variables.

DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

DEV = config('DEV', default=DEBUG, cast=bool)

TEMPLATE_DEBUG = config('DEBUG', default=DEBUG, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

HMAC_KEYS = {
    '2015-04-30': config('DJANGO_HMAC_KEY'),
}

SECRET_KEY = config('DJANGO_SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=dj_database_url.parse
    )
}

ROOT_URLCONF = 'oneanddone.urls'

WSGI_APPLICATION = 'oneanddone.wsgi.application'

# Django Settings
##############################################################################

INSTALLED_APPS = [
    'oneanddone.base',
    'oneanddone.tasks',
    'oneanddone.users',

    # Third-party apps, patches, fixes
    'commonware.response.cookies',
    'django_ace',
    'django_browserid',
    'django_jinja',
    'django_nose',
    'pipeline',
    'rest_framework',
    'rest_framework.authtoken',
    'tower',
    'session_csrf',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_csrf.CsrfMiddleware',  # Must be after auth middleware.
    'django.contrib.messages.middleware.MessageMiddleware',
    'commonware.middleware.FrameOptionsHeader',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'oneanddone.base.middleware.TimezoneMiddleware',
    'oneanddone.base.middleware.ClosedTaskNotificationMiddleware',
)

CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'session_csrf.context_processor',
    'django.contrib.messages.context_processors.messages',
    'oneanddone.base.context_processors.i18n',
    'oneanddone.base.context_processors.globals',
)

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '',
            'match_regex': r'^(?!(admin|registration)/).*\.(html|jinja)$',
            'context_processors': CONTEXT_PROCESSORS,
            'extensions': [
                'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                'jinja2.ext.with_',
                'jinja2.ext.i18n',
                'jinja2.ext.autoescape',
                'django_jinja.builtins.extensions.CsrfExtension',
                'django_jinja.builtins.extensions.CacheExtension',
                'django_jinja.builtins.extensions.TimezoneExtension',
                'django_jinja.builtins.extensions.UrlsExtension',
                'django_jinja.builtins.extensions.StaticFilesExtension',
                'django_jinja.builtins.extensions.DjangoFiltersExtension',
                'pipeline.templatetags.ext.PipelineExtension',
            ],
            'globals': {
                'browserid_info': 'django_browserid.helpers.browserid_info',
            }
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': CONTEXT_PROCESSORS
        }
    },
]

AUTHENTICATION_BACKENDS = [
    'django_browserid.auth.BrowserIDBackend',
    'django.contrib.auth.backends.ModelBackend',
]

PIPELINE_COMPILERS = (
    'pipeline.compilers.es6.ES6Compiler',
)

PIPELINE_YUGLIFY_BINARY = path('node_modules/.bin/yuglify')
PIPELINE_BABEL_BINARY = path('node_modules/.bin/babel')
PIPELINE_BABEL_ARGUMENTS = '--modules ignore'

PIPELINE_DISABLE_WRAPPER = True
PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/style.css',
            'css/font-awesome.css',
        ),
        'output_filename': 'css/base.min.css',
    },
    'admin': {
        'source_filenames': (
            'css/admin.css',
        ),
        'output_filename': 'css/admin.min.css',
    },
    'admin_project': {
        'source_filenames': (
            'css/admin_project.css',
        ),
        'output_filename': 'css/admin_project.min.css',
    },
    'locale_project': {
        'source_filenames': (
            'css/locale_project.css',
        ),
        'output_filename': 'css/locale_project.min.css',
    },
    'locales': {
        'source_filenames': (
            'css/locales.css',
        ),
        'output_filename': 'css/locales.min.css',
    },
    'project': {
        'source_filenames': (
            'css/project.css',
        ),
        'output_filename': 'css/project.min.css',
    },
    'translate': {
        'source_filenames': (
            'css/translate.css',
        ),
        'output_filename': 'css/translate.min.css',
    },
    'user': {
        'source_filenames': (
            'css/user.css',
        ),
        'output_filename': 'css/user.min.css',
    },
    'users': {
        'source_filenames': (
            'css/users.css',
        ),
        'output_filename': 'css/users.min.css',
    },
}

PIPELINE_JS = {
    'admin_project': {
        'source_filenames': (
            'js/admin_project.js',
        ),
        'output_filename': 'js/admin_project.min.js',
    },
    'main': {
        'source_filenames': (
            'js/main.js',
            'js/jquery.timeago.js',
        ),
        'output_filename': 'js/main.min.js',
    },
    'locale_project': {
        'source_filenames': (
            'js/locale_project.js',
        ),
        'output_filename': 'js/locale_project.min.js',
    },
    'project': {
        'source_filenames': (
            'js/project.js',
        ),
        'output_filename': 'js/project.min.js',
    },
    'translate': {
        'source_filenames': (
            'browserid/api.js',
            'js/translate.js',
        ),
        'output_filename': 'js/translate.min.js',
    },
    'user': {
        'source_filenames': (
            'js/user.js',
        ),
        'output_filename': 'js/user.min.js',
    },
    'search': {
        'source_filenames': (
            'js/search.js',
        ),
        'output_filename': 'js/search.min.js',
    },
}

# Sessions
#
# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

# Auth
# The first hasher in this list will be used for new passwords.
# Any other hasher in the list can be used for existing passwords.
# Playdoh ships with Bcrypt+HMAC by default because it's the most secure.
# To use bcrypt, fill in a secret HMAC key in your local settings.
BASE_PASSWORD_HASHERS = (
    'django_sha2.hashers.BcryptHMACCombinedPasswordVerifier',
    'django_sha2.hashers.SHA512PasswordHasher',
    'django_sha2.hashers.SHA256PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

PASSWORD_HASHERS = get_password_hashers(BASE_PASSWORD_HASHERS, HMAC_KEYS)

# Email

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
SERVER_EMAIL = config('OUTBOUND_EMAIL_ADDRESS', default='root@localhost')

# Postmark Email addon
POSTMARK_API_KEY = config('POSTMARK_API_TOKEN', default='inavlid-key')
POSTMARK_SENDER = SERVER_EMAIL
POSTMARK_TEST_MODE = False
POSTMARK_TRACK_OPENS = False

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')

TIME_ZONE = config('DJANGO_TIME_ZONE', default='America/New_York')

USE_I18N = config('USE_I18N', default=True, cast=bool)

USE_L10N = config('USE_L10N', default=True, cast=bool)

USE_TZ = config('USE_TZ', default=True, cast=bool)

# Gettext text domain
TEXT_DOMAIN = 'messages'
STANDALONE_DOMAINS = [TEXT_DOMAIN, 'javascript']
TOWER_KEYWORDS = {'_lazy': None}
TOWER_ADD_HEADERS = True

# Accepted locales
PROD_LANGUAGES = ('de', 'en-US', 'es', 'fr',)

DEV_LANGUAGES = PROD_LANGUAGES


def lazy_lang_url_map():
    from django.conf import settings
    langs = settings.DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return dict([(i.lower(), i) for i in langs])

LANGUAGE_URL_MAP = lazy(lazy_lang_url_map, dict)()


# Override Django's built-in with our native names
def lazy_langs():
    from django.conf import settings
    from product_details import product_details
    langs = DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return dict([(lang.lower(), product_details.languages[lang]['native'])
                 for lang in langs if lang in product_details.languages])

LANGUAGES = lazy(lazy_langs, dict)()

STATIC_ROOT = config('STATIC_ROOT', default=path('static'))
STATIC_URL = config('STATIC_URL', default='/static/')

MEDIA_ROOT = config('MEDIA_ROOT', default=path('media'))
MEDIA_URL = config('MEDIA_URL', default='/media/')

STATICFILES_STORAGE = 'oneanddone.base.storage.GzipManifestPipelineStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)

# Django-CSP
CSP_DEFAULT_SRC = (
    "'self'",
)
CSP_FONT_SRC = (
    "'self'",
    'http://*.mozilla.net',
    'https://*.mozilla.net'
)
CSP_IMG_SRC = (
    "'self'",
    'http://*.mozilla.net',
    'https://*.mozilla.net',
)
CSP_SCRIPT_SRC = (
    "'self'",
    'http://www.mozilla.org',
    'https://www.mozilla.org',
    'http://*.mozilla.net',
    'https://*.mozilla.net',
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'http://www.mozilla.org',
    'https://www.mozilla.org',
    'http://*.mozilla.net',
    'https://*.mozilla.net',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SESSION_COOKIE_SECURE = not DEBUG

# Third-party Library Settings
##############################################################################

# Testing configuration.
NOSE_ARGS = ['--logging-clear-handlers', '--logging-filter=-factory,-south,-django.db']

# Should robots.txt deny everything or disallow a calculated list of URLs we
# don't want to be crawled?  Default is false, disallow everything.
# Also see http://www.google.com/support/webmasters/bin/answer.py?answer=93710
ENGAGE_ROBOTS = True

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        ('oneanddone/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('oneanddone/**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
        ('templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
    ],
}

# Error Reporting
##############################################################################

# Recipients of traceback emails and other notifications.
ADMINS = (
    ('One and Done Admin', config('DJANGO_ADMIN_EMAIL', default='')),
)
MANAGERS = ADMINS


# Authentication settings.
BROWSERID_VERIFY_CLASS = 'oneanddone.users.views.Verify'
LOGIN_URL = reverse_lazy('users.login')
LOGIN_REDIRECT_URL = reverse_lazy('base.home')
LOGIN_REDIRECT_URL_FAILURE = reverse_lazy('users.login')
LOGOUT_REDIRECT_URL = reverse_lazy('base.home')

BROWSERID_AUDIENCES = config('BROWSERID_AUDIENCE',
                             default='http://localhost:8000, http://127.0.0.1:8000',
                             cast=Csv())

# Paths that don't require a locale code in the URL.
SUPPORTED_NONLOCALES = ['media', 'static', 'admin', 'api', 'browserid']

# Celery

# True says to simulate background tasks without actually using celeryd.
# Good for local development in case celeryd is not running.
CELERY_ALWAYS_EAGER = True

BROKER_CONNECTION_TIMEOUT = 0.1
CELERY_RESULT_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Time in seconds before celery.exceptions.SoftTimeLimitExceeded is raised.
# The task can catch that and recover but should exit ASAP.
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 10


# Permissions for the REST api
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# For absolute urls
try:
    DOMAIN = socket.gethostname()
except socket.error:
    DOMAIN = 'localhost'
PROTOCOL = "http://"
PORT = 80


# Lazy-load request args since they depend on certain settings.
def _request_args():
    from django.contrib.staticfiles import finders
    from tower import ugettext_lazy as _lazy

    site_logo = open(finders.find('img/qa-logo.png'), 'rb').read().encode('base64')
    logo_uri = urllib.quote('data:image/png;base64,{image}'.format(image=site_logo), safe=',:;/')
    return {
        'privacyPolicy': 'https://www.mozilla.org/privacy/websites/',
        'siteName': _lazy(u'One and Done'),
        'termsOfService': 'https://www.mozilla.org/about/legal/',
        'siteLogo': mark_safe(logo_uri),
        'backgroundColor': '#E0DDD4',
    }
BROWSERID_REQUEST_ARGS = lazy(_request_args, dict)()

# Project-specific Settings
##############################################################################
# Number of days that a one-time task attempt can be open before it expires
TASK_ATTEMPT_EXPIRATION_DURATION = 30

# The minimum duration for a complete task attempt, in seconds, to
# be considered valid
MIN_DURATION_FOR_COMPLETED_ATTEMPTS = 120

# Whitelisted tags allowed to be used in task instructions.
INSTRUCTIONS_ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'dl',
    'dt',
    'em',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'i',
    'img',
    'li',
    'ol',
    'p',
    'strong',
    'ul',
]

# Whitelisted attributes allowed to be used in task instruction tags.
INSTRUCTIONS_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['src', 'alt', 'title'],
}

# Google Analytics ID
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')
