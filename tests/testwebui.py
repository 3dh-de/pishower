#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PiShower project
    @copyright  Christian Daehn (c) 2006, http://3dh.de
    @license    MIT license
"""

import os
import flaskr
import unittest
import tempfile

class WebUITestCase(unittest.TestCase):
    """ Basic unit test for web user interface in webui.py """

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data
