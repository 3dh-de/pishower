#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, time
from temperaturesensor import TemperatureSensor


class DS18B20(TemperatureSensor):
    """ Class to read temperature from 1wire DS18B20 sensors """
    __lastCelsius = None
    __sensors = []
    currentSensor = None

    def __init__(self, sensorId=""):
        """ Check for 1wire drivers and setup sensor connection """
        self.__updateSensors()
        if sensorId is not "" and sensorId in self.__sensors:
            self.currentSensor = sensorId
        else:
            self.currentSensor = self.__sensors[0]

    def __teardown__(self):
        return

    def __updateSensors(self):
        """ Check for 1wire drivers and read available sensors """
        try:
            # open 1-wire slaves list to read sensor ids
            file = open('/sys/devices/w1_bus_master1/w1_master_slaves')
            w1_slaves = file.read().splitlines()
            file.close()
            self.__sensors = w1_slaves
            if w1_slaves[0] is None:
                print("warning: no sensors found!")
            else:
                for s in w1_slaves:
                    print("sensor found:  {}".format(s))
        except:
            print("error: unable to read 1-wire device list!")
            pass

    def availableSensors(self):
        """ Update available sensors and return their ids """
        self.__updateSensors()
        return self.__sensors

    def currentCelsius(self):
        # type: () -> float
        """ Return current sensor value in Celsius degrees """
        temperature = None
        try:
            file = open('/sys/bus/w1/devices/{0}/w1_slave'
                        .format(self.currentSensor))
            filecontent = file.read()
            file.close()

            if filecontent:
                stringvalue = filecontent.split("\n")[1].split(" ")[9]
                temperature = float(stringvalue[2:]) / 1000
                if temperature:
                    self.__lastCelsius = temperature
                    return float(temperature)
        except:
            # failed reading sensor
            pass
        if temperature is None:
            return -0.0
        return float(temperature)

    def currentFahrenheit(self):
        # type: () -> float
        """ Return current sensor value in Fahrenheit degrees """
        temperature = self.currentCelsius()
        return float(temperature) * 9.0/5.0 + 32.0


schleifenZaehler = 0
schleifenAnzahl = 20
schleifenPause = 1

sensor = DS18B20()

print("sensors found: ", sensor.availableSensors())

print("Temperaturabfrage für ", schleifenAnzahl, \
      " Messungen alle ", schleifenPause, " Sekunden gestartet")

while True:
    print("Aktuelle Temperatur : {0}  {1}\r" \
            .format(sensor.currentCelsiusStr(), sensor.currentFahrenheitStr()))
    sys.stdout.flush()
    time.sleep(schleifenPause)
    schleifenZaehler = schleifenZaehler + 1

print("Temperaturabfrage beendet")
