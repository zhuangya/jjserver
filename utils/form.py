#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

def validate_form(param, request):
    """
    
    Arguments:
    - `param`:
    - `request`:
    """
    gb = globals()
    for pk in param.keys():
        pv = request.form.get(pk, None)
        
        mkey = 'massage_%s' % pk
        if gb.has_key(mkey):
            pv = gb[mkey](pv)
        if pv is None:
            if param[pk] is None:
                return -400, pk
        else:
            param[pk] = pv
    return 0, ''


def resp(code, msg, content=None):
    """
    
    Arguments:
    - `code`:
    - `msg`:
    """
    return json.dumps({'err': code,
                       'msg': msg,
                       'cnt': content});


def massage_cell(cell):
    """
    
    Arguments:
    - `cell`:
    """
    cell = cell and cell.replace('-', '') or ''
    return (len(cell) > 10) and cell[-11:] or None

def massage_password(pwd):
    """
    
    Arguments:
    - `cell`:
    """
    return (len(pwd) > 5) and pwd or None

