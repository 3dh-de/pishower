#!/usr/bin/python
# -*- coding: utf-8 -*-

import typing
from abc import ABCMeta, abstractmethod


class TemperatureSensor:
    """ Generic class for temperature sensors """
    __metaclass__ = ABCMeta

    def __init__(self):
        return

    @abstractmethod
    def current_celsius(self):
        # type: () -> float:
        """ Read sensor and return value in Celsius degrees """
        return 0.0

    @abstractmethod
    def current_fahrenheit(self):
        # type: () -> float:
        """ Read sensor and return value in Fahrenheit degrees """
        return 0.0

    def currentHumidity(self):
        # type: () -> float:
        """ Read relative humidity in percent """
        return 0.0

    def current_celsius_str(self):
        """ Return string value with Celsius degrees """
        temperature = self.current_celsius()
        if temperature is None:
            return ''
        return '{:2.2f} °C'.format(float(temperature))

    def current_fahrenheit_str(self):
        """ Return string value with Fahrenheit degrees """
        temperature = self.current_fahrenheit()
        if temperature is None:
            return ''
        return '{:3.2f} °F'.format(float(self.current_fahrenheit()))
