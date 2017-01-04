#!/usr/bin/python

import os
import sys
import unittest

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append("../")

from rfidreader import UsbRfidReader
from pishowerutils import logger

# Control a IO control timer
class TestRfidReader(unittest.TestCase):
    reader = None

    def setUp(self):
        self.assertIsNotNone(logger,            'logger object is not initialized!')

        self.reader = None
        self.reader = UsbRfidReader()
        self.assertIsNotNone(self.reader,       'reader object cannot be initialized!')
        self.assertTrue(self.reader.isOpen(),   'RFID reader cannot be opened!')

    def test_read(self):
        self.assertIsNotNone(self.reader,       'reader object cannot be initialized!')

        code = None
        try:
            logger.debug('reading code...')
            code = self.reader.readCode()
        except:
            self.fail('error during reading code!')

    def test_reopen(self):
        self.assertIsNotNone(self.reader,       'reader object cannot be initialized!')

        self.reader.close()
        self.assertFalse(self.reader.isOpen(),  'RFID reader cannot be closed!')

        self.reader.readCode()
        self.assertTrue(self.reader.isOpen(),   'RFID reader cannot be reopened!')

    def tearDown(self):
        if self.reader:
            self.reader.close()


# exec tests
if __name__ == "__main__":
    unittest.main()
