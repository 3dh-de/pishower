#!/usr/bin/python

import time
import threading
import logging

# set up logging to file - see previous section for more details
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d.%m. %H:%M:%S')

logger = logging.getLogger()


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
        if self._timer is not None:
            if self._timer.is_alive():
                logger.warning('timer is already running!'
                               ' cancelling timer to start new one.')
            self.stop()

        self._timer = threading.Timer(self.timeoutSeconds, self._handleTimeout)
        self._timer.start()

        logger.info('timer started')

    def stop(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer.join()
            self._timer = None

        self._finished = False
        logger.info('timer stopped')

    def reset(self):
        self.stop()
        self.start()
        logger.info('timer resetted')

    def isActive(self):
        return self._timer is not None and self._timer.is_alive()

    def isFinished(self):
        return self._finished

    def _handleTimeout(self):
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
        if controlTimer.isFinished():
            sys.exit(0)

        time.sleep(0.1)

