#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PiShower project
    @copyright  Christian Daehn (c) 2006, http://3dh.de
    @license    MIT license
"""

import unittest
import os
import sys
import time
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append("../")

from pishowerutils import logger
import iocontroltimer as timer


# Control a IO control timer
class TestIOControlTimer(unittest.TestCase):
    control = None

    def setUp(self):
        self.control = timer.IOControlTimer(5)

    def test_start(self):
        self.assertIsNone(self.control._timer,      'timer is not empty after init!')

        self.control.start()
        self.assertIsNotNone(self.control._timer,   'timer is still empty after start!')

        self.control.stop()
        self.assertFalse(self.control.is_active(),  'timer is not stopped correctly!')
        self.assertFalse(self.control.is_finished(),'finished flag invalid after stop!')

        self.timeoutSeconds = 7
        self.control.reset()
        time.sleep(0.5)
        self.assertTrue(self.control.is_active(),   'timer is not resetted correctly!')
        self.assertFalse(self.control.is_finished(),'finished flag invalid after reset!')
        time.sleep(8.0)
        self.assertFalse(self.control.is_active(),  'invalid active state after timeout')
        self.assertTrue(self.control.is_finished(), 'invalid finished flag after timeout!')

    def test_handle_timeout(self):
        control2 = timer.IOControlTimer(8)

        event = control2.timeoutEvent
        logger.debug('restarting timer for event test...')
        control2.reset()
        time.sleep(0.5)
        logger.debug('restarted timer for event test')

        self.assertTrue(control2.is_active(), 'starting timer failed')
        self.assertFalse(event.wait(1.0), 'timeout event failed for too small timeout')
        self.assertTrue(event.wait(9.0), 'timeout event failed within timeout')
        self.assertTrue(event.is_set(), 'timeout event state is invalid')

    def tearDown(self):
        self.control = None


# exec tests
if __name__ == "__main__":
    unittest.main()
