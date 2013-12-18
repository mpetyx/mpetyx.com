"""
Django settings for website project.

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
SECRET_KEY = '8)w_b53)@iofviy-+uyn(==6e(g^jpp3o2db^8ss**u&ybr=q2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'museum',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SITE_ID = 1

INSTALLED_APPS += (
    'django.contrib.admin', # This must be configured
    'django.contrib.comments', # This must be configured
    # 'django.contrib.markup', # to render markdown
    # 'rest_framework', # django rest framework 2
    # 'taggit', # django-taggit
    # 'blogger.themes.default', # the base theme
    # 'blogger', # the app
    'museum',
    'easy_thumbnails',
    'djgeojson',
    'leaflet',
    # 'mapentity',
    'paperclip',
    'compressor',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'mapentity.context_processors.settings',
)

# this will attach BLOG_SETTINGS['info'] to HttpResponses
TEMPLATE_CONTEXT_PROCESSORS += (
    "django.contrib.auth.context_processors.auth",
    # "blogger.context_processors.blog_info",

)

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     },
#     # The fat backend is used to store big chunk of data (>1 Mo)
#     'fat': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

BLOG_SETTINGS = {
    'defaults': { # change the defaults of models and some constats for views
        'auto_publish': False,
        'auto_promote': False,
    },
    'info': { # attached to all responses so the information is available to the templates.
        'BLOG_TITLE': 'My Blog Name',
        'BLOG_SUBTITLE': 'Blog subname',
    }
}

MEDIA_URL = 'media/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
