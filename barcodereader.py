#!/usr/bin/env python

from evdev import *
import signal, sys
from pishowerutils import logger


class UsbRfidReader:
    """ Class for reading out RFID transponders via USB HID readers """

    __inputDevice = None
    __scancode = {
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
    
    def __init__(self, inputEvent='/dev/input/event0'):
        try:
            self.__inputDevice = InputDevice(inputEvent)
        except:    
            logger.error("Unable to open USB RFID reader '{0}'!".format(inputEvent))
            pass

    def readCode(self):
        """ Try reading a code from the input device and return it as string """
        if self.__inputDevice is None:
            logger.error("No USB RFID reader found!")
            return None
            
        code = ''
        while True:
            event = dev.read_one()
            if event is None and code == '':
                # There are blank events in between characters, so we don't want
                # to break if we've started reading them
                break # start a new read. 
            try:
                if event is not None:
                    if event.type == ecodes.EV_KEY:
                        data = categorize(event)
                    # catch only keyup, and not Enter   
                    if data.keystate == 0 and data.scancode != 42:
                        if data.scancode == 28:
                            # looking return key to be pressed
                            logger.debug("code read: '{0}'".format(code))
                            return code
                        else:
                            code += self.__scancodes[data.scancode]
            except AttributeError:
                logger.error("Parsing input stream failed!")
                break
            except:
                logger.error("Code reading failed!")
                break
        return None


# command line execution
if __name__ == "__main__":
    import time

    rfidReader = UsbRfidReader('/dev/input/event2')
    while True:
        try:
            code = rfidReader.readCode()
            if code is not None:
                logger.debug("result: '{0}'".format(code))
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
        except:
            logger.error("Reading aborted!")
            break
