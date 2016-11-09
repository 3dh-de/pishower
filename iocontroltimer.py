#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
import threading
import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d.%m. %H:%M:%S')

logger = logging.getLogger()


# Control a IO control timer
class IOControlTimer:
    timeoutSeconds = 420    # 7min
    finished       = False
    timer          = None
   
    def __init__(self,seconds=420):
        self.timeoutSeconds = seconds
        self.finished       = False
        logger.debug('timer init for {} seconds'.format(seconds))

    def start(self):
        if self.timer is not None:
            if self.timer.isActive():
                logger.warning('timer is already running! cancelling timer to start new one.')
            self.stop()
                
        self.timer = threading.Timer(self.timeoutSeconds, self._handleTimeout)
        self.timer.start()

        logger.info('timer started')

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        
        self.finished = False
        logger.info('timer stopped')

    def reset(self):
        self.stop()
        self.start()

    def isActive(self):
        return self.timer is not None and self.timer.isActive()

    def isFinished(self):
        return self.finished

    def _handleTimeout(self):
        self.finished = True
        logger.debug('timeout reached!')

# Control IO ports to activate/deactivate devices
class IOControl:
    pass


controlTimer = IOControlTimer(5)
controlTimer.start()


while True:
    if controlTimer.isFinished():
        sys.exit(0)

    time.sleep(0.1)

