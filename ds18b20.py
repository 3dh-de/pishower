#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from temperaturesensor import TemperatureSensor
from pishowerutils import logger


class DS18B20(TemperatureSensor):
    """ Class to read temperature from 1wire DS18B20 sensors """
    __lastCelsius = None
    __sensors = []
    currentSensor = None

    def __init__(self, sensorId=''):
        """ Check for 1wire drivers and setup sensor connection """
        TemperatureSensor.__init__(self)
        self.__update_sensors()
        if sensorId is not '' and sensorId in self.__sensors:
            self.currentSensor = sensorId
        else:
            self.currentSensor = self.__sensors[0]

    def __update_sensors(self):
        """ Check for 1wire drivers and read available sensors """
        try:
            # open 1-wire slaves list to read sensor ids
            file = open('/sys/devices/w1_bus_master1/w1_master_slaves')
            w1_slaves = file.read().splitlines()
            file.close()
            self.__sensors = w1_slaves
            if w1_slaves[0] is None:
                logger.warning('no 1-wire sensors found!')
            else:
                for s in w1_slaves:
                    logger.debug('sensor found:  {}'.format(s))
        except:
            logger.error('Unable to read 1-wire device list!')

    def available_sensors(self):
        """ Update available sensors and return their ids """
        self.__update_sensors()
        return self.__sensors

    def current_celsius(self):
        # type: () -> float
        """ Return current sensor value in Celsius degrees """
        temperature = None
        try:
            file = open('/sys/bus/w1/devices/{0}/w1_slave'
                        .format(self.currentSensor))
            filecontent = file.read()
            file.close()

            if filecontent:
                stringvalue = filecontent.split('\n')[1].split(' ')[9]
                temperature = float(stringvalue[2:]) / 1000
                if temperature:
                    self.__lastCelsius = temperature
                    return float(temperature)
        except:
            pass  # failed reading sensor
        return float(temperature) if temperature is not None else -0.0

    def current_fahrenheit(self):
        # type: () -> float
        """ Return current sensor value in Fahrenheit degrees """
        temperature = self.current_celsius()
        return float(temperature) * 9.0/5.0 + 32.0


# command line execution
if __name__ == '__main__':
    sensor = DS18B20()

    logger.debug('sensors found: {0}'.format(sensor.available_sensors()))

    while True:
        try:
            logger.debug('Temperature : {0}  {1}\r' \
                         .format(sensor.current_celsius_str(), sensor.current_fahrenheit_str()))
            sys.stdout.flush()
            time.sleep(2.0)
        except KeyboardInterrupt:
            logger.debug('Key pressed - finishing now...')
            break
        except:
            logger.error('Unknown error received. Reading aborted!')
            break
