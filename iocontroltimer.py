#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
from pishowerutils import logger


class IOControlTimer:
    """ Timer to exec I/O actions after x seconds """
    timeoutSeconds = 420    # 7min
    _finished = False
    _timer = None

    def __init__(self, seconds=420):
        self.timeoutSeconds = seconds
        self._finished = False
        logger.debug('timer init for {} seconds'.format(seconds))

    def __del__(self):
        self.stop()

    def start(self):
        """ Starts the timer thread to execute _handle_timeout() """
        if self._timer is not None:
            if self._timer.is_alive():
                logger.warning('timer is already running!'
                               ' cancelling timer to start new one.')
            self.stop()

        self._timer = threading.Timer(self.timeoutSeconds, self._handle_timeout)
        self._timer.start()

        logger.info('timer started')

    def stop(self):
        """ Stop the timer thread """
        if self._timer is not None:
            self._timer.cancel()
            self._timer.join()
            self._timer = None

        self._finished = False
        logger.info('timer stopped')

    def reset(self):
        """ Stops and starts the timer thread """
        self.stop()
        self.start()
        logger.info('timer resetted')

    def is_active(self):
        """ Returns True, if timer thread is running """
        return self._timer is not None and self._timer.is_alive()

    def is_finished(self):
        """ Returns True, if timer was executed successfully """
        return self._finished

    def _handle_timeout(self):
        """ Worker method to execute commands on timeout """
        self._finished = True
        logger.debug('timeout reached!')


# Control IO ports to activate/deactivate devices
class IOControl:
    pass


# simple demo code for script execution
if __name__ == "__main__":
    import sys

    controlTimer = IOControlTimer(5)
    controlTimer.start()

    while True:
        if controlTimer.is_finished():
            sys.exit(0)

        time.sleep(0.1)
