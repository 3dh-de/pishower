#!/usr/bin/python

import time
import sys
import threading
import logging
import unittest
import sys
sys.path.append('../')

import iocontroltimer as timer

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d.%m. %H:%M:%S')

logger = logging.getLogger()


# Control a IO control timer
class TestIOControlTimer(unittest.TestCase):
    control = None
   
    def setUp(self):
        self.control = timer.IOControlTimer()
        logger.debug('timer init for {} seconds'.format(self.control.timeoutSeconds))

    def test_start(self):
        self.assertEqual(self.control.timer,        None, 'timer is not empty after init!')

        self.control.start()

        self.assertNotEqual(self.control.timer,     None, 'timer is still empty after start!')

    def test_stop(self):
        self.assertNotEqual(self.control.timer,     None, 'timer is not initialized after start!')

        self.control.stop()

        self.assertEqual(self.control.isActive(),   False, 'timer is not stopped correctly!')
        self.assertEqual(self.control.finished,     False, 'finished flag invalid after stop!')
        self.assertEqual(self.control.isFinished(), False, 'finished flag invalid after stop!')

    def test_reset(self):
        self.timeoutSeconds = 60
        self.control.reset()
        self.assertEqual(self.control.isActive(),   True, 'timer is not resetted correctly!')

    def test_isActive(self):
        self.assertEqual(self.control.isActive(),   True, 'timer state is invalid!')

    def test_isFinished(self):
        self.assertEqual(self.control.isFinished(), False, 'finished flag invalid after reset!')

    def test_handleTimeout(self):
        pass

    def tearDown(self):
        self.control = None


# exec tests
if __name__ == "__main__": 
    unittest.main()
