#!/usr/bin/python

import os
import sys
import unittest
import time

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append("../")
sys.path.append("../hd44780")

from lcdcontrol import LcdControl
from pishowerutils import logger

# Control an I2C HD44780 LCD
class TestLcdControl(unittest.TestCase):
    display = None

    def setUp(self):
        self.assertIsNotNone(logger,            'logger object is not initialized!')

        self.display = None
        self.display = LcdControl()
        self.assertIsNotNone(self.display,      'display object cannot be initialized!')
        self.assertTrue(self.display.isOpen(),  'RFID display cannot be opened!')

    def test_show(self):
        self.assertIsNotNone(self.display,      'display object cannot be initialized!')

        try:
            logger.debug('displaying text...')
            self.display.clear()

            self.display.show('Hello World! #1', 1)
            self.display.show('Hello World! #2', 2)

            self.display.backlight(False)
            time.sleep(1)
            self.display.backlight()
        except:
            self.fail('error during showing text!')

    def test_reopen(self):
        self.assertIsNotNone(self.display,      'display object cannot be initialized!')

        self.display.close()
        self.assertFalse(self.display.isOpen(), 'display cannot be closed!')

        self.display.show('Reopened!', 2)
        self.assertTrue(self.display.isOpen(),  'display cannot be reopened!')

    def tearDown(self):
        if self.display:
            self.display.close()


# exec tests
if __name__ == "__main__":
    unittest.main()
