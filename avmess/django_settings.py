from avmess.settings import CONF

DEBUG = CONF.debug
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CONF.db_name,
        'USER': CONF.db_user,
        'PASSWORD': CONF.db_pass,
        'HOST': CONF.db_host,
        'PORT': CONF.db_port,
    }
}


INSTALLED_APPS = ('avmess',)

TIME_ZONE = 'UTC'
USE_TZ = False
SECRET_KEY = 'daskfhoapikfhsiu-0r9oq309r23r-09ijonfjask;dln'
