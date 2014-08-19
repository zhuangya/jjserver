# -*- coding: utf-8 -*-
import runserver
import settings

from flask.ext.testing import TestCase
from user.user_api import user_api
from utils.database import db

class baseTest(TestCase):
    def create_app(self):
        """
        
        Arguments:
        - `self`:
        """
        app = runserver.create_app()
        app.config['testing'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        return app

    def setUp(self):
        """
        
        Arguments:
        - `self`:
        """
        db.create_all()

    def tearDown(self):
        """
        
        Arguments:
        - `self`:
        """
        db.session.remove()
        db.drop_all()

    def succ_request(self, uri, data=None):
        """
        
        Arguments:
        - `uri`:
        - `data`:
        """
        if data:
            resp = self.client.post(uri, data=data)
        else:
            resp = self.client.get(uri)
        self.assertEqual(resp.status_code, 200)
        return resp, resp.json

