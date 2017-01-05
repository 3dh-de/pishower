#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
from pishowerutils import logger

try:
    scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(scriptPath)
    sys.path.append("./hd44780")
    import lcddriver
except RuntimeError:
    logger.error('Error importing hd44780 lcddriver!')
    quit(-1)


class LcdControl:
    """ Easy output to HD44780 based LCD displays """
    __outputDevice = None
    __deviceOpenRetries = 0

    def __init__(self):
        """ Init display interface """
        self.open()

    def __del__(self):
        """ Clear display interface """
        self.close()

    def open(self):
        """ Open connection to LCD display """
        try:
            self.__outputDevice = lcddriver.lcd()
            if self.__outputDevice is None:
                raise RuntimeWarning
            self.__outputDevice.lcd_clear()
            time.sleep(1.0)  # prevent timing issues
        except:
            if self.__deviceOpenRetries < 1:
                logger.error('Unable to open HD44780 LCD display!')
            self.__outputDevice = None
            self.__deviceOpenRetries += 1

    def close(self):
        """ Close the input device and wait 1 second """
        try:
            if self.__outputDevice is not None:
                del self.__outputDevice
                self.__outputDevice = None
                logger.debug('lcd device closed')
                time.sleep(1.0)  # prevent timing issues
        except:
            logger.warning('Error while closing lcd device!')

    def is_open(self):
        """ Returns True, if connection to LCD device is open """
        return self.__outputDevice is not None

    def backlight(self, on=True):
        """ Switch LCD backlight on/off """
        try:
            if self.__outputDevice is not None:
                self.__outputDevice.lcd_backlight('ON' if on else 'OFF')
        except:
            logger.error('Switching display backlight failed!')
            self.close()

    def clear(self):
        """ Clears all text from LCD """
        try:
            if self.__outputDevice is not None:
                self.__outputDevice.lcd_clear()
        except:
            logger.error('Clearing lcd display failed!')
            self.close()

    def show(self, text, line=1):
        """ Displays given text on LCD at given line (1..n) """
        try:
            if self.__outputDevice is None:
                self.open()
            if self.__outputDevice is not None:
                self.__outputDevice.lcd_display_string(text, line)
        except:
            logger.error('Showing text on lcd failed!')
            self.close()


# command line execution
if __name__ == '__main__':
    try:
        display = LcdControl()

        display.backlight(False)
        time.sleep(2.0)
        display.backlight()

        display.close()
        display.show('Restart OK', 1)
        time.sleep(2.0)

        display.show('Duschzeit   5min', 1)
        display.show('>>> Pruefe Karte', 2)
        time.sleep(2.0)

        display.show('>>> Karte OK <<<', 2)
        time.sleep(2.0)
    except KeyboardInterrupt:
        logger.debug('Key pressed - finishing now...')
    except:
        logger.error('Unknown error received. Test aborted!')
