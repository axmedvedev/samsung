import os
import logging
from flask import Flask
from flask_cors import CORS

BASEDIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    FLASK_APP = 'app.py'
    SECRET_KEY = 'my_secret_key_mxUzRhivY5waFqt77ilzwyqYB0eTB40'

    MONGO_ENDPOINT = os.environ.get('MONGO_ENDPOINT', 'mongodb://127.0.0.1:27017')

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins=[
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5000",
    "http://localhost:8080",
    "http://localhost:5000",
])

logging.basicConfig(level=logging.WARNING,
                    filename=os.path.join(BASEDIR, '/logs/app.log'),
                    format="%(asctime)s %(levelname)s %(message)s")