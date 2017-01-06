#!/usr/bin/python

import time
from threading import Thread
from rfidreader import UsbRfidReader
from iocontroltimer import IOControlTimer
from iocontrol import RelayControl
from lcdcontrol import LcdControl
from pishowerutils import logger


class PiShowerMain(Thread):
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
    __running = False

    def __init__(self, shower_id=1, shower_seconds=420):
        """ Init card reader, display and I/O controls """
        Thread.__init__(self)
        try:
            if shower_seconds < 60:
                logger.error('invalid shower time given! time must be > 60s')
                raise AttributeError()
            self.shower_id = shower_id
            self.shower_time = shower_seconds
            self._cardReader = UsbRfidReader()
            self._showerTimer = IOControlTimer(self.shower_time)
            self._relays = RelayControl([self._gpio_cold_water, self._gpio_warm_water])
            self._display = LcdControl()
            self.__running = False
            time.sleep(1.0)
            logger.debug('shower control ready')
        except Exception as error:
            logger.error('Error during init of main control! {0}'.format(error))

    def __del__(self):
        """ Close all devices and stop timers """
        try:
            self.stop()
        except Exception as error:
            logger.error('Error in destructor of main control! {0}'.format(error))

    def start(self):
        """ Init timers, reader and display user message """
        self.__running = True
        Thread.start(self)
        try:
            logger.debug('starting shower control...')
            time.sleep(1.0)
        except Exception as error:
            logger.error('Error during starting main control! {0}'.format(error))

    def stop(self):
        """ Close all valves (relays), stop timers and display warning """
        try:
            logger.warning('stopping and locking shower control...')
            self.__running = False

            if self._showerTimer:
                self._showerTimer.stop()
            if self._relays:
                self._relays.toggle_output(self._gpio_cold_water, False)
                self._relays.toggle_output(self._gpio_warm_water, False)
            if self._display:
                self.show_message_error()
        except Exception as error:
            logger.error('Error during stopping main control! {0}'.format(error))

    def run(self):
        """ Handle card reader events and logic for shower control """
        if self._cardReader is None:
            logger.error('No card reader available! Aborting!')
            self.stop()
            return
        if self._relays is None:
            logger.error('No I/O control for relays available! Aborting!')
            self.stop()
            return

        try:
            logger.debug('running main control loop...')
            self.show_message_ready()
            shower_active = False

            while self.__running:
                if shower_active:
                    minutes_left = 0  # TODO
                    if self._showerTimer:
                        if not self._showerTimer.is_finished():
                            self.show_message_processing(minutes_left)
                        else:
                            shower_active = False
                            self.show_message_stop()
                            if self._relays:
                                self._relays.toggle_output(self._gpio_cold_water, False)
                                self._relays.toggle_output(self._gpio_warm_water, False)
                            time.sleep(30.0)
                            self.show_message_ready()
                    else:
                        shower_active = False
                        self.show_message_ready()
                else:
                    code = self._cardReader.readline()

                if code is not None:
                    logger.debug('found a code: \'{0}\''.format(code))
                    self.show_message_processing(self.shower_time//60)
                    if self._relays:
                        self._relays.toggle_output(self._gpio_cold_water, True)
                        self._relays.toggle_output(self._gpio_warm_water, True)
                    if self._showerTimer:
                        self._showerTimer.start()
                        shower_active = True
                    time.sleep(30.0)
                else:
                    time.sleep(0.2)

            logger.debug('stopping main control loop...')
        except Exception as error:
            logger.error('Error in main control loop! {0}'.format(error))

    def show_message_ready(self):
        if self._display:
            self._display.show('Dusche {0}    FREI'.format(self.shower_id), 1)
            self._display.show('>>> Karte ?? <<<', 2)

    def show_message_processing(self, shower_time):
        if self._display:
            self._display.show('Duschzeit {0:3d}min'.format(shower_time), 1)
            self._display.show('>>> Karte OK <<<', 2)

    def show_message_error(self):
        if self._display:
            self._display.show('Dusche {0}     AUS'.format(self.shower_id), 1)
            self._display.show('>>> STOERUNG <<<', 2)

    def show_message_stop(self):
        if self._display:
            self._display.show('Dusche {0}  BELEGT'.format(self.shower_id), 1)
            self._display.show('>>> GESPERRT <<<', 2)


# exec tests
if __name__ == "__main__":
    try:
        main = PiShowerMain(1, 60)
        main.start()

        while main.is_alive():
            time.sleep(0.2)

    except KeyboardInterrupt:
        logger.debug('Key pressed - finishing now...')
    except Exception as error:
        logger.error('Error in main control! {0}'.format(error))
    finally:
        main.stop()

