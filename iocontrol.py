#!/usr/bin/python

import time
from pishowerutils import logger

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    logger.error('Error importing RPi.GPIO! Superuser privileges needed!')
    quit(-1)


class RelayControl:
    """ Easy GPIO control to toggle relais """
    invertedLevels = True

    def __init__(self, outports=[]):
        """ Init GPIO interface """
        GPIO.setmode(GPIO.BCM)  # BCM-numbering (GPIO 17) instead of pin (11)

        for port in outports:
            GPIO.setup(port, GPIO.OUT)
            logger.debug('init port #{}'.format(port))
        time.sleep(0.1)

        for port in outports:
            GPIO.output(port, GPIO.HIGH if self.invertedLevels == True else GPIO.LOW)
            logger.debug('set port #{} to LOW'.format(port))
            time.sleep(0.01)

    def __del__(self):
        """ Clear GPIO interface """
        GPIO.cleanup()

    def toggle_output(self, port, value=-1):
        if value is -1:
            value = GPIO.input(port)
            logger.debug('toggle port from "{}"'.format(value))
            value = not value
            logger.debug('toggle port to new "{}"'.format(value))
        elif self.invertedLevels:
            value = not value

        state = GPIO.HIGH if value > 0 else GPIO.LOW
        GPIO.output(port, state)
        logger.debug('toggle port #{0} to "{1}"'.format(port, state))
        time.sleep(0.01)


# command line execution
if __name__ == '__main__':
    relay1 = 17                  # GPIO 17 / Pin 11 auf Ausgang setzen
    relay2 = 27                  # GPIO 27 / Pin 13 auf Ausgang setzen

    try:
        control = RelayControl([relay1, relay2])
        time.sleep(2.0)
        control.toggle_output(relay1)
        time.sleep(2.0)
        control.toggle_output(relay2)
        time.sleep(2.0)
        control.toggle_output(relay2, False)
        time.sleep(2.0)
        control.toggle_output(relay2, True)
        time.sleep(2.0)
    except KeyboardInterrupt:
        logger.debug('Key pressed - finishing now...')
    except:
        logger.error('Unknown error received. Reading aborted!')
