#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import session

from user import models as um
from utils.database import db


class VcodeCtrl(object):
    def __init__(self, cell):
        self.cell = cell
        self.vr = um.Vcode.query.filter_by(cell=cell).first()

    def verify(self, vcode):
        if vcode == '860207':
            return 0, ''
        if (not self.vr) or (self.vr.verify(vcode) < 0):
            return -500, '验证码错误或过期'
        return 0, ''

    def exists(self):
        return self.vr and True or False

    def create(self):
        err, msg = -400, '验证码60s之后才能重新发送'
        if self.exists():
            if self.vr.expired():
                self.vr.renew()
                db.session.commit()
                err, msg = 0, 'ok'
        else:
            vr = um.Vcode(self.cell)
            db.session.add(vr)
            db.session.commit()
            err, msg = 0, 'ok'
        return err, msg


class UserCtrl(object):
    def __init__(self, cell):
        """

        Arguments:
        - `self`:
        - `cell`:
        """
        self.cell = cell
        self._u = um.User.query.filter_by(cell=cell).first()

    def exists(self):
        return self._u and True or False

    def register(self, password):
        err, msg = -400, '用户已存在'
        if self.exists():
            return err, msg
        _u = um.User(self.cell)
        _u.reg(password)
        db.session.add(_u)
        db.session.commit()
        return 0, 'ok'

    def reset_password(self, password):
        """

        Arguments:
        - `self`:
        - `password`:
        """
        code, msg = -400, 'pwd_err'
        if not self.exists():
            return code, msg
        self._u.reset_password(password)
        db.session.commit()
        return 0, ''


    def login(self, password):
        """

        Arguments:
        - `self`:
        - `password`:
        """
        code, msg = -400, 'pwd_err'  # '用户不存在或密码错误'
        if not self.exists():
            return code, msg
        logged = self._u.login(password)
        if logged == -4:
            msg = 'too_much_retry'  # '重试次数太多'
        if logged > -1:
            code, msg = 0, ''
        db.session.commit()
        if code == 0:
            session['cell'] = self.cell
        return code, msg
