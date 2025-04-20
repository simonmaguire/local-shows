import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'shows.db')
     SECRET_KEY = os.environ.get('SECRET_KEY') or \
      'The quick brown fox jumps over the lazy dog'