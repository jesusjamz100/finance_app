from os import environ

class BaseConfig(object):
    ''' Basic configuration of the app '''

    # main configuration
    SECRET_KEY = 'finance.123456'
    DEBUG = False
    SECURITY_PASSWORD_SALT = 'my_precious_two'

    # email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = environ.get('APP_MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('APP_MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///financeapp.db'