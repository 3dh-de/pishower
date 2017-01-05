#!/usr/bin/python

import unittest
import os
import sys
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
        logger.debug('timer init for {} seconds'.format(self.control.timeoutSeconds))

    def test_start(self):
        self.assertEqual(self.control._timer,        None, 'timer is not empty after init!')

        self.control.start()

        self.assertNotEqual(self.control._timer,     None, 'timer is still empty after start!')

    def test_stop(self):
        self.assertNotEqual(self.control._timer,     None, 'timer is not initialized after start!')

        self.control.stop()

        self.assertEqual(self.control.is_active(), False, 'timer is not stopped correctly!')
        self.assertEqual(self.control.is_finished(), False, 'finished flag invalid after stop!')

    def test_reset(self):
        self.timeoutSeconds = 7
        self.control.reset()
        self.assertEqual(self.control.is_active(), True, 'timer is not resetted correctly!')

    def test_is_active(self):
        self.assertEqual(self.control.is_active(), True, 'timer state is invalid!')

    def test_is_finished(self):
        self.assertEqual(self.control.is_finished(), False, 'finished flag invalid after reset!')

    def test_handle_timeout(self):
        event = self.control.timeoutEvent
        self.control.start()
        self.assertTrue(self.control.is_active(), 'starting timer failed')
        self.assertFalse(event.wait(1.0), 'timeout event failed for too small timeout')
        self.assertTrue(event.wait(9.0), 'timeout event failed within timeout')
        self.assertTrue(event.is_set(), 'timeout event state is invalid')

    def tearDown(self):
        self.control = None


# exec tests
if __name__ == "__main__":
    unittest.main()
