import os
import logging
from flask import Flask
from flask_cors import CORS

BASEDIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    FLASK_APP = 'app.py'
    SECRET_KEY = 'my_secret_key_mxUzRhivY5waFqt77ilzwyqYB0eTB40'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///' + os.path.join(BASEDIR, 'app.sqlite') + '?check_same_thread=False')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO = {
        'db_name': os.environ.get('MONGO_DB', 'samsung'),
        'host': os.environ.get('MONGO_HOST', '127.0.0.1'),
        'port': int(os.environ.get('MONGO_PORT', 27017)),
        'user': os.environ.get('MONGO_USER', 'root'),
        'pwd': os.environ.get('MONGO_PWD', 'root')
    }

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins=[
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5000",
    "http://localhost:8080",
    "http://localhost:5000",
])

logging.basicConfig(level=logging.WARNING,
                    filename=os.path.join(BASEDIR, 'app.log'),
                    format="%(asctime)s %(levelname)s %(message)s")