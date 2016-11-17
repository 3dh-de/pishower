# pishower

Raspberry Pi based shower control for time based switching of showers or other devices by RFID / NFC cards, keys, time plans..

Originally this project was founded to control the access/usage of my Dojo's shower cabins to only allow paid members and to prevent fraud.

## Requirements

1x Raspberry Pi 1 or newer with Raspbian (Debian Jessie or newer) and Python 2.7 installed  
2x 3V3 to 5V TTL level converters (3.3V of GPIO pins to 5.0V to control I2C LCD and 5V relais)  
1x SainSmart LCD 1602 / 2004 display module with HDxxx and I2C controller  
1x 5V TTL 1/2 channel relais  
1x DHT11 / DHT22 temperature sensor
1x Max 7219 LED matrix panel

## Wiring

### LED Matrix Panel

Max 7219 controlled array of 8x8 red LED panels

| LED-Panel | RPi Pin | Function  |
|:---------:|:-------:|-----------|
|VCC        | 2/4     | 5V+       | 
|GND        | 20/25   | GND       |
|DIN        | 19      | SPI MOSI / GPIO 10 |
|CS         | 24      | SPI CS0 / GPIO 8 |
|CLK        | 23      | SPI CLK / GPIO 11 |

### LCD 1602 I2C Display

SainSmart IIC/I2C/TWI 1602 Serial LCD Module, white on blue backlight, 16x2 chars

Due to 5VDC TTL level of the I2C module a 3.3V to 5V level changer is needed to connect it with the RPi's GPIOs.

| LCD I2C | 5V-to-3V3 changer | RPi Pin | Function |
|:-------:|:-----------------:|:-------:|----------|
|VCC      | HV (5V)           | 2/4     | 5V+      | 
|GND      | GND               | 6/9/14  | GND      |
|SDA      | TXO <--> TXI      | 3       | I2C1 SDA / GPIO 2 |
|SCL      | TXO <--> TXI      | 5       | I2C1 SCL / GPIO 3 |

### 5V Relay

1 or 2 channel 5V TTL relay for 230V

Due to 5VDC TTL level of the relay module a 3.3V to 5V level changer is needed to connect it with the RPi's GPIOs.

| Relay | 5V-to-3V3 changer | RPi Pin | Function |
|:-----:|:-----------------:|:-------:|----------|
|VCC    | HV (5V)           | 2/4     | 5V+      | 
|GND    | GND               | 6/9/14  | GND      |
|IN1    | TXO <--> TXI      | 11      | GPIO 17  |
|IN2    | TXO <--> TXI      | 13      | GPIO 27  |

### Temperature sensor DHTxx

DHT11 or DHT22 5V temperature and humidity sensor for indoor use.

| LED-Panel | RPi Pin  | Function  |
|:---------:|:--------:|-----------|
|VCC        | 2/4      | 5V+       | 
|GND        | 14/20/25 | GND       |
|DATA       | 7        | GPIO 4    |

Needed libs: ...


## License

This software is free tu use following the terms of the MIT License (MIT):

Copyright (c) 2016 Christian Daehn, Germany, http://3dh.de

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
