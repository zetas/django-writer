"""
Django settings for Writerr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))

TEMPLATE_DEBUG = bool(os.environ.get('DEBUG', False))

ALLOWED_HOSTS = ['*']

SITE_ID = os.environ.get('SITE_ID', 3)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'classes',
    'papers',
    'main',
    'django.contrib.admin',
    'south',
    'raven.contrib.django.raven_compat',
    'django.contrib.sitemaps'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'Writerr.urls'

WSGI_APPLICATION = 'Writerr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

assert 'DB_ENGINE' in os.environ, 'Set DB_ENGINE in your environment!'
assert 'DB_NAME' in os.environ, 'Set DB_NAME in your environment!'
assert 'DB_USER' in os.environ, 'Set DB_USER in your environment!'
assert 'DB_PASSWORD' in os.environ, 'Set DB_PASSWORD in your environment!'
assert 'DB_HOST' in os.environ, 'Set DB_HOST in your environment!'

DATABASES = {
    'default': {
        'ENGINE': os.environ['DB_ENGINE'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.environ.get('STATIC_ROOT', '/var/www/writerr')

STATIC_URL = '/static/'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

LOGIN_REDIRECT_URL = '/papers/add/'
LOGIN_REDIRECT_URL_INSTRUCTORS = '/dashboard/'

LOGIN_URL = '/'
LOGOUT_URL = '/account/logout/'

AUTH_USER_MODEL = 'account.WUser'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.environ['APP_LOG'],
        },
        'prod_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.environ['APP_LOG']+'.prod',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'writerr.logs': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'writerr.prodlog': {
            'handlers': ['prod_file'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
}

#---------------------------------
# Email Settings
#---------------------------------
"""
All site email will come from this address unless otherwise specified.
"""
GLOBAL_EMAIL_FROM = os.environ.get('GLOBAL_EMAIL_FROM')

"""
Any site mail that needs to be sent to an administrator (i.e. "Contact Us")
will go to this address unless otherwise specified.
"""
GLOBAL_EMAIL_TO = os.environ.get('GLOBAL_EMAIL_TO')

CONTACT_EMAIL_SUBJECT = 'New Contact Request'
CONTACT_EMAIL_FROM = GLOBAL_EMAIL_FROM
CONTACT_EMAIL_TO = GLOBAL_EMAIL_TO
CONTACT_EMAIL_TEMPLATE = 'main.contact'


"""
These are the SMTP details for sending out mail.
"""
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')


#---------------------------------
# Stripe Settings
#---------------------------------

"""
The production stripe keys should be set via the environment
instead of being defined here. The keys you see in the second
parameter are the test keys which will be used as fallback
in the event the specified environment variables are empty.
"""
STRIPE_PUBLISHABLE = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_SECRET = os.environ.get("STRIPE_SECRET_KEY")

STRIPE_MONTHLY_COST = 5
STRIPE_YEARLY_COST = 50

#---------------------------------
# Misc App Settings
#---------------------------------

PDF_SAVE_LOCATION = STATIC_ROOT + '/pdfs/'

PDF_URL_BASE = STATIC_URL + 'pdfs/'

RAVEN_CONFIG = {
    'dsn': os.environ.get("RAVEN_DSN"),
}

#Change this to https:// when/if an SSL cert is applied
HTTP = os.environ.get('HTTP', 'https://')
