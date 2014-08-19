#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, request, session
from jinja2 import TemplateNotFound
import time
import json
from functools import wraps

import settings
from user import models as um
from user import controllers as uc
from utils import form as fu
from utils import cell as cu
from utils.database import db

user_api = Blueprint('user_api', __name__,
                     template_folder='templates')

def vcode_limit(f):
    """
    
    Arguments:
    - `f`:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        err = '验证码错误'
        param = {'cell': None,
                 'vcode': None}
        succ, msg = fu.validate_form(param, request)
        if succ < 0:
            return fu.resp(-500, msg)
        vc = uc.vcode_ctrl(param['cell'])
        succ, msg = vc.verify(param['vcode'])
        if succ < 0:
            return fu.resp(succ, msg)
        return f(*args, **kwargs)
    return decorated_function

@user_api.route('/view_code/<cell>', methods=['GET'])
def view_code(cell):
    """
    
    Arguments:
    - `cell`:
    """
    _v = uc.vcode_ctrl(cell)
    code = _v.exists() and _v.vr.serialize or {}
    return fu.resp(0, '', code)

@user_api.route('/vcode', methods=['POST'])
def vocode():
    """
    """
    param = {'cell': None}
    succ, msg = fu.validate_form(param, request)
    if succ < 0:
        return fu.resp(succ, '%s missing' % msg)

    vc = uc.vcode_ctrl(param['cell'])
    succ, msg = vc.create()
    return fu.resp(succ, msg)

@user_api.route('/reg', methods=['POST'])
@vcode_limit
def register():
    """
    """
    param = {'cell': None,
             'password': None,
             'passrep': None}
    succ, msg = fu.validate_form(param, request)
    if succ < 0:
        return fu.resp(succ, '%s missing' % msg)

    u = uc.user_ctrl(param['cell'])
    if u.exists():
        return fu.resp(-400, 'user_exists')
    if (param['password'] != param['passrep']):
        return fu.resp(-400, '两次密码不一致')

    #add new user
    _u = uc.user_ctrl(param['cell'])
    succ, msg = _u.register(param['password'])
    return fu.resp(succ, msg)

@user_api.route('/login', methods=['POST'])
def login():
    param = {'cell': None,
             'password': None}
    succ, msg = fu.validate_form(param, request)
    if succ < 0:
        return fu.resp(succ, '%s missing' % msg)

    _u = uc.user_ctrl(param['cell'])
    
    code, msg = _u.login(param['password'])
    #login succ, return real cont
    return fu.resp(code, msg)
    
@user_api.route('/rstpwd')
def reset_password():
    param = {'cell': None,
             'vcode': None,
             'password': None,
             'passrep': None}

    succ, msg = fu.validate_form(param, request)

    if succ < 0:
        return fu.resp(succ, '%s missing' % msg)

    _u = uc.user_ctrl(param['cell'])

    if not u.exists():
        return fu.resp(-400, 'user does not exist')
    if (param['password'] != param['passrep']):
        return fu.resp(-400, '两次密码不一致')

    code, msg = _u.reset_password(param['password'])

    return fs.resp(code, msg)


@user_api.route('/')
def show():
    cell = session.get('cell')
    return json.dumps(cell)

