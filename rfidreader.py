#!/usr/bin/env python3

from evdev import InputDevice, categorize, ecodes
from pishowerutils import logger


class UsbRfidReader:
    """ Class for reading out RFID transponders via USB HID readers """

    __inputDevice = None
    __deviceOpenRetries = 0
    __minCodeLength = 8
    __scancodes = {
        # Scancode: ASCIICode
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5',
        7: u'6', 8: u'7', 9: u'8', 10: u'9', 11: u'0', 12: u'-', 13: u'=',
        14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[',
        27: u']', 28: u'CRLF', 29: u'LCTRL', 30: u'A', 31: u'S', 32: u'D',
        33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X',
        46: u'C', 47: u'V', 48: u'B', 49: u'N', 50: u'M', 51: u',', 52: u'.',
        53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }

    def __init__(self, inputEvent='/dev/input/event0', minCodeLength=8):
        """ Init the input device object """
        self.__minCodeLength = minCodeLength
        self.__inputDevicePath = inputEvent
        self.open()

    def __del__(self):
        """ Destroy class and handle for input device """
        self.close()

    def open(self):
        """ Open the input device object for reading """
        try:
            self.close()
            self.__inputDevice = InputDevice(self.__inputDevicePath)
            self.__deviceOpenRetries = 0
            time.sleep(1.0)     # prevent timing issues
            logger.debug('Opened RFID reader device \'{0}\''.format(self.__inputDevicePath))
        except:
            if self.__deviceOpenRetries < 1:
                logger.error('Unable to open USB RFID reader \'{0}\'!'.format(self.__inputDevicePath))
            self.__inputDevice = None
            self.__deviceOpenRetries += 1

    def close(self):
        """ Close the input device and wait 1 second """
        try:
            if self.__inputDevice is None:
                return
            self.__inputDevice.close()
            self.__inputDevice = None
            time.sleep(1.0)     # prevent timing issues
        except:
            logger.warning('Error while closing RFID input device!')
        else:
            logger.debug('RFID input device closed')

    def readCode(self):
        """ Try reading a code from the input device and return it as string """
        if self.__inputDevice is None:
            self.open()
            if self.__inputDevice is None:
                return None
        code = ''
        try:
            while True:
                event = self.__inputDevice.read_one()
                if event is None and code == '':
                    # There are blank events in between characters, so we don't want
                    # to break if we've started reading them
                    break  # start a new read.
                if event is None or event.type != ecodes.EV_KEY:
                    continue
                data = categorize(event)
                # catch only keyup, and not Enter
                if data.keystate == 0 and data.scancode != 42:
                    if data.scancode == 28:
                        # looking return key to be pressed
                        if len(code) < self.__minCodeLength:
                            logger.warn('ignoring to small code: {0}'.format(code))
                            break
                        else:
                            logger.debug('code read: \'{0}\''.format(code))
                            return code
                    else:
                        code += self.__scancodes[data.scancode]
        except:
            logger.error('Parsing input stream failed!')
            self.close()
        return None


# command line execution
if __name__ == '__main__':
    import time
    import sys

    rfidReader = UsbRfidReader('/dev/input/event2', 10)
    while True:
        try:
            code = rfidReader.readCode()
            if code is not None:
                logger.debug('found a code: \'{0}\''.format(code))
            time.sleep(0.5)
        except KeyboardInterrupt:
            logger.debug('Key pressed - finishing now...')
            sys.exit(0)
        except:
            logger.error('Unknown error received. Reading aborted!')
            time.sleep(2)