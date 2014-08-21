#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from functools import wraps

from flask import Blueprint, request, session

from user import controllers as uc
from user import models as um
from utils import form as fu


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
            return fu.resp(-500, 'invalid ' + msg)
        vc = uc.VcodeCtrl(param['cell'])
        succ, msg = vc.verify(param['vcode'])
        if succ < 0:
            return fu.resp(succ, msg)
        return f(*args, **kwargs)

    return decorated_function


def tgtcell_operatable(f):
    """检查参数中的``tgtcell`` 在当前登录用户的联系人列表中，且是合法用户。
    如果不满足条件，返回 -403 错误

    Arguments:
    - `f`:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        err = ''
        cell = session.get('cell', None)
        if not cell:
            return fu.resp(-401, '请先登录')
        param = {'tgtcell': None}
        succ, msg = fu.validate_form(param, request)
        if succ < 0:
            return fu.resp(-500, msg)

        if cell == param['tgtcell']:
            return fu.resp(-500, '无法查找自己')

        # if it's a user
        if not um.User.query.filter_by(cell=param['tgtcell']).first():
            return fu.resp(-404, '好友未找到')

        # if it's a contact
        if not um.Contact.query.filter_by(cell=cell,
                                          tgtcell=param['tgtcell']).first():
            return fu.resp(-403, '未添加通讯录')

        return f(*args, **kwargs)

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cell = session.get('cell', None)
        if not cell:
            return fu.resp(-401, '请先登录')
        return f(*args, **kwargs)

    return decorated_function


@user_api.route('/view_code/<cell>', methods=['GET'])
def view_code(cell):
    """

    Arguments:
    - `cell`:
    """
    _v = uc.VcodeCtrl(cell)
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

    vc = uc.VcodeCtrl(param['cell'])
    succ, msg = vc.create()
    return fu.resp(succ, msg)


@user_api.route('/reg', methods=['POST'])
@vcode_limit
def register():
    """
    """
    param = {'cell': None,
             'password': None}
    succ, msg = fu.validate_form(param, request)
    if succ < 0:
        return fu.resp(succ, '%s missing' % msg)

    u = uc.UserCtrl(param['cell'])
    if u.exists():
        return fu.resp(-400, 'user_exists')

    # add new user
    _u = uc.UserCtrl(param['cell'])
    succ, msg = _u.register(param['password'])
    return fu.resp(succ, msg)


@user_api.route('/login', methods=['POST'])
def login():
    param = {'cell': None,
             'password': None}
    succ, msg = fu.validate_form(param, request)
    if succ < 0:
        return fu.resp(succ, '%s missing' % msg)

    _u = uc.UserCtrl(param['cell'])

    code, msg = _u.login(param['password'])
    # login succ, return real cont
    return fu.resp(code, msg)
    
@user_api.route('/rstpwd', methods=['POST'])
@vcode_limit
def reset_password():
    param = {'cell': None,
             'vcode': None,
             'password': None}

    succ, msg = fu.validate_form(param, request)

    if succ < 0:
        return fu.resp(succ, '%s missing' % msg)

    _u = uc.UserCtrl(param['cell'])

    if not _u.exists():
        return fu.resp(-400, 'user does not exist')

    code, msg = _u.reset_password(param['password'])

    return fu.resp(code, msg)


@user_api.route('/')
def show():
    cell = session.get('cell')
    return json.dumps(cell)
