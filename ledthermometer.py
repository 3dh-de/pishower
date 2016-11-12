#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import Adafruit_DHT
import max7219.led as led
from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT

# create matrix device
device = led.matrix(cascaded=4)
device.orientation(90)

# Parse command line parameters.
sensor_args = {'11': Adafruit_DHT.DHT11,
               '22': Adafruit_DHT.DHT22,
               '2302': Adafruit_DHT.AM2302}

sensor = sensor_args['11']
pin = 4

device.clear()


def fadeMessage(msg, seconds=2.5, f=TINY_FONT):
    """ display given message string by fading in and out the brightness """
    device.brightness(0)
    device.show_message(msg, font=f, always_scroll=False)
    print('intensity = 0, msg = {0}'.format(msg))

    for intensity in range(8):
        device.brightness(intensity)
        print('intensity = {0}'.format(intensity))
        time.sleep(0.150)

    time.sleep(3.05)

    for intensity in range(8):
        device.brightness(7 - intensity)
        print('intensity = {0}'.format(7 - intensity))
        time.sleep(0.150)

    return

while True:
    msg = u'{0}'.format(time.strftime('%H:%M'))
    fadeMessage(msg, 2.5, TINY_FONT)
    time.sleep(1.0)

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        msg = u'{0:0.0f}c {1:0.0f}%'.format(temperature, humidity)
        fadeMessage(msg, 2.5, TINY_FONT)
        time.sleep(1.0)
