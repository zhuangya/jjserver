import time
import hashlib

from utils.database import db
import settings
from utils import cell as cu

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cell = db.Column(db.String(16), index=True, unique=True)
    passsalt = db.Column(db.String(16))
    password = db.Column(db.String(64))
    create = db.Column(db.Integer)
    last_login = db.Column(db.Integer)

    login_retry = db.Column(db.Integer)

    def __init__(self, cell):
        """
        
        Arguments:
        - `self`:
        - `cell`:
        """
        self.cell = cell
        self.create = int(time.time())
        self.last_login = self.create
        self.login_retry = 0
        self.passsalt = cu.gen_voced()

    def gen_pwd(self, password):
        """
        
        Arguments:
        - `self`:
        - `password`:
        """
        return hashlib.sha224('%s%s' % (self.passsalt, password)).hexdigest()

    def reg(self, password):
        """
        
        Arguments:
        - `self`:
        - `password`:
        """
        self.password = self.gen_pwd(password)
        
    def login(self, password):
        now = int(time.time())
        self.last_login = now
        if (self.login_retry > 3) and ((now - 120) < self.last_login):
            return -4
        authed = (self.password == self.gen_pwd(password))
        rst = 0
        if authed:
            self.login_retry = 0
        else:
            rst = -1
            self.login_retry = self.login_retry + 1
        return rst


class vcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cell = db.Column(db.String(16), index=True, unique=True)
    vcode = db.Column(db.String(16))
    expire = db.Column(db.Integer)
    create = db.Column(db.Integer, index=True)
    sent = db.Column(db.Integer, index=True)

    def __init__(self, cell):
        """`
        
        Arguments:
        - `self`:
        - `cell`:
        - `vcode`:
        """
        self.cell = cell
        self.vcode = cu.gen_voced()
        self.create = int(time.time())
        self.expire = self.create + settings.VCODE_EXPIRE
        self.sent = 0

    @property
    def serialize(self):
        return {'cell': self.cell,
                'vcode': self.vcode,
                'create': self.create,
                'expire': self.expire}
        
    def expired(self):
        """
        
        Arguments:
        - `self`:
        """
        now = int(time.time())
        return (now - self.expire) > 0
        
    def renew(self):
        """
        
        Arguments:
        - `self`:
        """
        self.vcode = cu.gen_voced()
        self.create = int(time.time())
        self.expire = self.create + settings.VCODE_EXPIRE
        
    def verify(self, vcode):
        """
        
        Arguments:
        - `self`:
        - `vco`:
        """
        if self.expired():
            return -1
        if self.vcode != vcode:
            return -2
        return 0

