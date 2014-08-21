#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Flask

from user.user_api import user_api
from utils.database import db

import settings


def create_app():
    """
    """
    app = Flask(__name__)
    app.register_blueprint(user_api,
                           url_prefix='/user')

    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI

    db.app = app
    db.init_app(app)

    app.secret_key = settings.SESSION_SECRET_KEY
    return app


if __name__ == '__main__':
    app = create_app()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'initdb':
            db.create_all()
    else:
        app.run(host='0.0.0.0', port=8000, debug=True)
