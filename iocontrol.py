#!/usr/bin/python

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print('Error importing RPi.GPIO! Superuser privileges needed!')

import time


class RelayControl:
    """ Easy GPIO control to toggle relais """
    invertedLevels = True

    def __init__(self, outports=[]):
        """ Init GPIO interface """
        GPIO.setmode(GPIO.BCM)  # BCM-numbering (GPIO 17) instead of pin (11)

        for port in outports:
            GPIO.setup(port, GPIO.OUT)
            print('init port #{}'.format(port))
        time.sleep(0.1)

        for port in outports:
            GPIO.output(port, GPIO.HIGH if self.invertedLevels == True else GPIO.LOW)
            print('set port #{} to LOW'.format(port))
            time.sleep(0.01)
        return

    def __del__(self):
        """ Clear GPIO interface """
        GPIO.cleanup()
        return

    def toggleOutput(self, port, value=-1):
        if value is -1:
            value = GPIO.input(port)
            print('toggle port from "{}"'.format(value))
            value = not value
            print('toggle port to new "{}"'.format(value))
        elif self.invertedLevels:
            value = not value

        state = GPIO.HIGH if value > 0 else GPIO.LOW
        GPIO.output(port, state)
        print('toggle port #{0} to "{1}"'.format(port, state))
        time.sleep(0.01)
        return


relay1 = 17                  # GPIO 17 / Pin 11 auf Ausgang setzen
relay2 = 27                  # GPIO 27 / Pin 13 auf Ausgang setzen

control = RelayControl([relay1, relay2])

try:
    time.sleep(2.0)
    control.toggleOutput(relay1)
    time.sleep(2.0)
    control.toggleOutput(relay2)
    time.sleep(2.0)
    control.toggleOutput(relay2, False)
    time.sleep(2.0)
    control.toggleOutput(relay2, True)
    time.sleep(2.0)
except KeyboardInterrupt:
    control = None
