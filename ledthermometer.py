#!/usr/bin/python

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


def fadeMessage(msg, seconds=2.5, f=TINY_FONT):
    """ display given message string by fading in and out the brightness """
    device.brightness(0)
    device.show_message(msg, font=f, always_scroll=False)

    for intensity in range(8):
        device.brightness(intensity)
        time.sleep(0.050)
    time.sleep(2.50)

    for intensity in range(8):
        device.brightness(7 - intensity)
        time.sleep(0.050)
    return

try:
    device.clear()

    while True:
        msg = u'{0}'.format(time.strftime('%H:%M'))
        fadeMessage(msg, 2.5, TINY_FONT)
        time.sleep(0.5)

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            msg = u'{0:0.0f}c {1:0.0f}%'.format(temperature, humidity)
            fadeMessage(msg, 2.5, TINY_FONT)
            time.sleep(0.5)

# Abbruch durch Taste Strg-C
except KeyboardInterrupt:
    device.clear()
