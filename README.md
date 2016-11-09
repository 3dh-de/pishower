# pishower

Raspberry Pi based shower control for time based switching of showers or other devices by RFID / NFC cards, keys, time plans..

Originally this project was founded to control the access/usage of my Dojo's shower cabins to only allow paid members and to prevent fraud.

## Requirements

1x Raspberry Pi 1 or newer with Raspbian (Debian Jessie or newer) and Python 2.7 installed
2x TTL level converters (3.3V of GPIO pins to 5.0V to control I2C LCD and 5V relais)
1x SainSmart LCD 1602 / 2004 display module with HDxxx and I2C controller
1x 5V 1/2 channel relais 

## License

This software is free tu use following the terms of the MIT License (MIT):

Copyright (c) 2016 Christian Daehn, Germany, http://3dh.de

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
