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
    _state_on = GPIO.LOW
    _state_off = GPIO.HIGH
    _registered_outs = []

    def __init__(self, outports=[], inverted=True):
        """ Init GPIO interface """
        self.invertedLevels = inverted
        if not inverted: 
            self._state_on, self._state_off = self._state_off, self._state_on
        self._states = {self._state_on: 'ON', self._state_off: 'OFF'}

        GPIO.setmode(GPIO.BCM)  # BCM-numbering (GPIO 17) instead of pin (11)

        for port in outports:
            GPIO.setup(port, GPIO.OUT, initial=self._state_off)
            self._registered_outs.append(port)
            logger.debug('init GPIO {} as output'.format(port))
        time.sleep(0.5)

    def __del__(self):
        """ Clear GPIO interface """
        GPIO.cleanup()

    def toggle_output(self, port, value=-1):
        if port not in self._registered_outs:
            logger.warning('Cannot toggle unregistered GPIO {0}!'.format(port))
            return
        if value is -1:
            value = GPIO.input(port)
            logger.debug('toggle GPIO {0} from {1} to {2}'.format(port, self._states[value], self._states[not value]))
            value = not value
        elif self.invertedLevels:
            value = not value

        state = GPIO.HIGH if value > 0 else GPIO.LOW
        GPIO.output(port, state)
        logger.debug('set GPIO {0} to {1}'.format(port, self._states[state]))
        time.sleep(0.01)


# command line execution
if __name__ == '__main__':
    relay1 = 17                  # GPIO 17 / Pin 11 auf Ausgang setzen
    relay2 = 27                  # GPIO 27 / Pin 13 auf Ausgang setzen

    try:
        control = RelayControl([relay1, relay2])
        time.sleep(2.0)

        logger.debug('Testing invalid port...')
        control.toggle_output(4, True)

        logger.debug('Switching relais to ON...')
        control.toggle_output(relay1, True)
        control.toggle_output(relay2, True)
        time.sleep(2.0)

        logger.debug('Toggling relais...')
        control.toggle_output(relay1)
        time.sleep(2.0)
        control.toggle_output(relay2)
        time.sleep(2.0)

        logger.debug('Switching relais2 to OFF...')
        control.toggle_output(relay2, False)
        time.sleep(2.0)
        logger.debug('Switching relais2 to ON...')
        control.toggle_output(relay2, True)
        time.sleep(2.0)
    except KeyboardInterrupt:
        logger.debug('Key pressed - finishing now...')
    except:
        logger.error('Unknown error received. Reading aborted!')
