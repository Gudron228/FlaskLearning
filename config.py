import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sdfjn2jh4b34h2k3jb2k4j2b'