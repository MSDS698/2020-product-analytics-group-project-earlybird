import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.urandom(24)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'week3.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@earlybird-testdb.cnbau0umxiny.us-west-2.rds.amazonaws.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True # flask-login uses sessions which require a secret Key



# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config(object):
#     SECRET_KEY=os.urandom(24)
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'week6.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = True # flask-login uses sessions which require a secret Key