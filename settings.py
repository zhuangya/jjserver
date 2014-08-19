import os

RUNDIR = os.path.dirname(os.path.realpath(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/rundata/tmp.db' % RUNDIR


VCODE_EXPIRE = 180
VCODE_FREN_LMT = 60


SESSION_SECRET_KEY = 'E^\xf9\\\xb1\x96\xf2\xc2`\xd9\x99pY\x85\xbc\x1bV\xa2{\x94\x01+\xdb#\xaaBp\x06Q\xd6\x16\x9d\x00Hu\xcf'


try:
    from local_settings import *
except:
    pass
