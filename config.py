'''
--> RENAME AS config.py
'''
# -*- coding: utf-8 -*-
# available languages
LANGUAGES = {
    'en': 'English',
    'de': 'German',
    'ko': 'Korean'
}
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'


# TOCKEN
SECURITY_PASSWORD_SALT = 'my_precious_two'

# DEGUB
DEBUG = True
# WTForms

SECRET_KEY = 'real_secret_key' #WTF Form require secret key -> TO BE CHANGES PLZ

# Flask-Bcrypt
BCRYPT_LOG_ROUNDS = 12 # Configuration for the Flask-Bcrypt extension

# DATABASE Connection
SQLALCHEMY_DATABASE_URI = 'postgresql://gboard:gboard@localhost/gboard'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# Mail
MAIL_FROM_EMAIL = 'noreplay@lupon.ch' # For use in application emails
MAIL_DEFAULT_SENDER = 'noreplay@lupon.ch'
# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'florian.rindlisbacher@gmail.com'
MAIL_PASSWORD = 'xxxxxxxxxxxx'
