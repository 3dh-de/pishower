#!/usr/bin/python
# coding=utf-8

import os, sys, time


class ThermometerDS18B20:
    """ Class to read temperature from 1wire DS18B20 sensors
    """

    def __init__(self):
        """ setup sensor connection """
        self.filename = '/sys/bus/w1/devices/28-05168033b0ff/w1_slave'

    def currentTemperature(self):
        """ return current sensor value in Celsius degrees """
        try:
            file = open(self.filename)
            filecontent = file.read()
            file.close()

            stringvalue = filecontent.split("\n")[1].split(" ")[9]
            temperature = float(stringvalue[2:]) / 1000
        except:
            pass
        return temperature


schleifenZaehler = 0
schleifenAnzahl = 20
schleifenPause = 1


print "Temperaturabfrage für ", schleifenAnzahl, \
      " Messungen alle ", schleifenPause, " Sekunden gestartet"

sensor = ThermometerDS18B20()

while True:
    messdaten = '{:6.2f}'.format(sensor.currentTemperature())
    print "Aktuelle Temperatur : ", messdaten, "°C\r"
    sys.stdout.flush()
    time.sleep(schleifenPause)
    schleifenZaehler = schleifenZaehler + 1

print "Temperaturabfrage beendet"
