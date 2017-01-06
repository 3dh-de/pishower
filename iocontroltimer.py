#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
from pishowerutils import logger


class IOControlTimer:
    """
    Timer to exec I/O actions after x seconds

    After start() a timer runs for the given seconds and executes
    _handle_timeout() at the scheduled time. Then the event
    'timeoutEvent' is set and the state is set to finished -
    checkable by is__finished().

    While the timer is running is_active() returns True and
    the timer can be stopped by stop() or restart().
    """
    timeoutSeconds = 420                # timeout in 7min after start
    timeoutEvent = threading.Event()    # event object to signal the timeout
    _finished = False
    _timer = None

    def __init__(self, seconds=420):
        """ Init the timer """
        self.timeoutSeconds = seconds
        self._finished = False
        logger.debug('timer init for {} seconds'.format(seconds))

    def __del__(self):
        """ Ensure the timer is stopped """
        self.stop()

    def start(self):
        """ Starts the timer thread to execute _handle_timeout() and trigger the timeoutEvent """
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
        if self._timer:
            if self._timer.is_alive():
                self._timer.cancel()
                self._timer.join()
                logger.debug('cancelled timer')
            self._timer = None
        if self.timeoutEvent.is_set():
            self.timeoutEvent.clear()

        self._finished = False
        logger.info('timer stopped')

    def reset(self):
        """ Stops and starts the timer thread """
        self.stop()
        self.start()
        logger.info('timer resetted')

    def is_active(self):
        """ Returns True, if timer thread is running """
        return self._timer and self._timer.is_alive()

    def is_finished(self):
        """ Returns True, if timer was executed successfully """
        return self._finished

    def _handle_timeout(self):
        """ Worker method to set the timeoutEvent and execute commands on timeout """
        self.timeoutEvent.set()
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

    event = controlTimer.timeoutEvent

    while True:
        if event.wait(0.1):
            sys.exit(0)
