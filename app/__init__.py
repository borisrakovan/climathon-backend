import os
from flask import Flask
from flask_cors import CORS

from app.config import Config
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(Config)

CORS(app)


def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


mkdir(app.config["LOG_DIR"])
mkdir(app.config["DATA_DIR"])

if not app.debug:
    # logging to file
    log_dir = app.config['LOG_DIR']

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'climathon-backend.log'),
        maxBytes=10240,
        backupCount=10
    )

    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )

    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('API META startup')

from app import routes

print("\nAPI READY.")
