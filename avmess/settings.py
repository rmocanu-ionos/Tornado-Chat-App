import os


class DefaultConfig(object):
    debug = False
    db_host = 'localhost'
    db_port = 3306
    db_name = 'avmess'
    db_user = 'avmess'
    db_pass = 'avmess'

    port = 8889

    web_dir = os.environ.get('AVMESS_WEB_DIR')


class DevelopmentConfig(DefaultConfig):
    debug = True
    pass


class ProductionConfig(DefaultConfig):
    pass


ENV_TO_CONF = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}

CONF = ENV_TO_CONF[os.environ.get('AVMESS_ENV', 'dev')]

secret = 'fwg3g434r343t'
