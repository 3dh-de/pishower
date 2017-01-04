#!/usr/bin/env python3

import glob
import time
from evdev import InputDevice, categorize, ecodes
from pishowerutils import logger


class UsbRfidReader:
    """
    Class for reading out RFID transponders via USB HID readers

    Opens USB HID devices like simple RFID readers for EM4100 and
    Mifare NFC transponders and reads the received transponder
    serial number.

    Supported are Linux systems and any card/code readers registered
    as HID devices under /dev/input/event[0..n].

    WARNING:
    File read permissions to the devices are needed - check your
    user's groups! (e.g. for membership of group 'input')
    """

    __inputDevice = None
    __inputDevicePath = ''
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

    def __init__(self, devicePath='', minCodeLength=8):
        """
        Init the input device object

        Parameter 'devicePath' for input event device like
        '/dev/input/event0' is optional. If empty all available
        input devices are tried.
        """
        self.__minCodeLength = minCodeLength
        self.__inputDevicePath = devicePath
        self.open()

    def __del__(self):
        """ Destroy class and handle for input device """
        self.close()

    def open(self):
        """
        Open an input event device for reading

        Tries to open the device path given to the constructor
        or search for all available input event devices.
        """
        devicePaths = []
        if len(self.__inputDevicePath):
            devicePaths = ["{0}".format(self.__inputDevicePath)]
        else:
            devicePaths = glob.glob('/dev/input/event*')  # search all available devices
        for path in devicePaths:
            try:
                self.close()
                self.__inputDevice = InputDevice(path)
                self.__deviceOpenRetries = 0
                self.__inputDevicePath = path
                logger.debug('Opened RFID reader device \'{0}\''.format(path))
                time.sleep(1.0)  # prevent timing issues
                return
            except:
                if self.__deviceOpenRetries < 1:
                    logger.error('Unable to open USB RFID reader \'{0}\'!'.format(path))
                self.__inputDevice = None
                self.__deviceOpenRetries += 1

    def close(self):
        """ Close the input device and wait 1 second """
        try:
            if self.__inputDevice is not None:
                self.__inputDevice.close()
                self.__inputDevice = None
                logger.debug('RFID input device closed')
                time.sleep(1.0)  # prevent timing issues
        except:
            logger.warning('Error while closing RFID input device!')

    def isOpen(self):
        """ Returns True, if connection to RFID reader is open """
        return self.__inputDevice is not None

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
                            logger.warning('ignoring to small code: {0}'.format(code))
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
    rfidReader = UsbRfidReader('/dev/input/event2', 10)
    while True:
        try:
            code = rfidReader.readCode()
            if code is not None:
                logger.debug('found a code: \'{0}\''.format(code))
            time.sleep(0.5)
        except KeyboardInterrupt:
            logger.debug('Key pressed - finishing now...')
            break
        except:
            logger.error('Unknown error received. Reading aborted!')
            break
