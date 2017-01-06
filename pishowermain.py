#!/usr/bin/python

import time
from rfidreader import UsbRfidReader
from iocontroltimer import IOControlTimer
from iocontrol import RelayControl
from lcdcontrol import LcdControl
from pishowerutils import logger


class PiShowerMain:
    """
    Main control of PiShower system

    Controls the I/O devices and logic to switch the
    magnet valves for the shower cabin water.

    There are separate valves for cold (GPIO 17, blue cable)
    and warm (GPIO 27, yellow cable) water, switched by relays
    connected to GPIO 17+27.

    An I2C LCD 16x2 display shows the current state and
    messages for the user.

    By an attached USB Mifare RFID/NFC reader the users
    authenticate and start the shower for a predefined time.
    After the time is expired, all valves are closed by an
    timeout event.
    """
    shower_time = 420
    shower_id = 1
    _gpio_cold_water = 17
    _gpio_warm_water = 27
    _cardReader = None
    _showerTimer = None
    _relays = None
    _display = None

    def __init__(self, shower_id=1, shower_seconds=420):
        """ Init card reader, display and I/O controls """
        try:
            self._cardReader = UsbRfidReader()
            self._showerTimer = IOControlTimer(self.shower_time)
            self._relays = RelayControl([self._gpio_cold_water, self._gpio_warm_water])
            self._display = LcdControl()
            time.sleep(1.0)
            logger.debug('shower control ready')
        except:
            logger.error('Error during init of main control!')

    def __del__(self):
        """ Close all devices and stop timers """
        try:
            self.stop()
        except:
            logger.error('Error in destructor of main control!')

    def start(self):
        """ Init timers, reader and display user message """
        try:
            logger.debug('starting shower control...')
            if self._display:
                self._display.show(' Dusche {0} FREI '.format(self.shower_id), 1)
                self._display.show('>>> Karte ? <<<', 2)
        except:
            logger.error('error during starting main control')

    def stop(self):
        """ Close all valves (relays), stop timers and display warning """
        try:
            logger.warning('stopping and locking shower control...')
            if self._showerTimer:
                self._showerTimer.stop()
            if self._relays:
                self._relays.toggle_output(self._gpio_cold_water, False)
                self._relays.toggle_output(self._gpio_warm_water, False)
            if self._display:
                self._display.show('Dusche gesperrt!', 1)
                self._display.show('>>> STOERUNG <<<', 2)
        except:
            logger.error('error during stopping main control')

    def is_active(self):
        """ Returns true, while main control thread is running """
        return False


# exec tests
if __name__ == "__main__":
    try:
        main = PiShowerMain()
        main.start()

        while main.is_active():
            time.sleep(0.2)

        time.sleep(3.0)

        main.stop()
    except:
        logger.error('error in main control')
        quit(-1)
