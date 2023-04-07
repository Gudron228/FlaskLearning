import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sdfjn2jh4b34h2k3jb2k4j2b'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'mysql+pymysql://root:vovik2003@localhost/socialnetwork'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
