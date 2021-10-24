import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = os.environ.get('DEBUG', False)
    LOG_DIR = os.path.join(basedir, 'logs')
    DATA_DIR = os.path.join(basedir, 'data')
