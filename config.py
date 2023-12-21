#config file

import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_APP = 'app.py'
    SECRET_KEY = 'my_secret_key_mxUzRhivY5waFqt77ilzwyqYB0eTB40'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///' + os.path.join(BASEDIR, 'app.sqlite') + '?check_same_thread=False')
    SQLALCHEMY_TRACK_MODIFICATIONS = False