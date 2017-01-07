#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PiShower project
    @copyright  Christian Daehn (c) 2006, http://3dh.de
    @license    MIT license
"""

import os
import sys
import unittest

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append("../")

from rfidreader import UsbRfidReader
from pishowerutils import logger


class TestRfidReader(unittest.TestCase):
    """ Control an USB RFID reader """
    reader = None

    def setUp(self):
        self.assertIsNotNone(logger,            'logger object is not initialized!')

        self.reader = None
        self.reader = UsbRfidReader()
        self.assertIsNotNone(self.reader,       'reader object cannot be initialized!')
        self.assertTrue(self.reader.is_open(), 'RFID reader cannot be opened!')

    def test_read(self):
        self.assertIsNotNone(self.reader,       'reader object cannot be initialized!')

        code = None
        try:
            logger.debug('reading code...')
            code = self.reader.readline()
        except:
            self.fail('error during reading code!')

    def test_reopen(self):
        self.assertIsNotNone(self.reader,       'reader object cannot be initialized!')

        self.reader.close()
        self.assertFalse(self.reader.is_open(), 'RFID reader cannot be closed!')

        self.reader.readline()
        self.assertTrue(self.reader.is_open(), 'RFID reader cannot be reopened!')

    def tearDown(self):
        if self.reader:
            self.reader.close()


# exec tests
if __name__ == "__main__":
    unittest.main()
