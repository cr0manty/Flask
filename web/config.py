class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1@localhost/flask'
    SECRET_KEY = 'my secret code is pisun'
    SECURITY_PASSWORD_SALT = 'salt-key'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'