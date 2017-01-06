# pishower

Raspberry Pi based shower control for time based switching of showers or other devices by RFID / NFC cards, keys, time plans..

Originally this project was founded to control the access/usage of my Dojo's shower cabins to only allow paid members and to prevent fraud.

A german blog entry to this project and its aims can be found in my blog [[http://3dh.de]].

## License

All documents in this repository are free for private and commercial use, licensed under the MIT License - see LICENSE.md.

## Requirements

1x Raspberry Pi 1 or newer with Raspbian (Debian Jessie or newer) and Python 2.7 installed  
2x 3V3 to 5V TTL level converters (3.3V of GPIO pins to 5.0V to control I2C LCD and 5V relais)  
1x SainSmart LCD 1602 / 2004 display module with HDxxx and I2C controller  
1x 5V TTL 1/2 channel relais  
1x DHT11 / DHT22 temperature sensor
1x Max 7219 LED matrix panel
1x USB RFID Mifare 13.56 MHz reader

## Wiring

### LED Matrix Panel

![Max7219 8x8 LED](/doc/max7219_8x8_panel.jpg)!

Max 7219 controlled array of 8x8 red LED panels

| LED-Panel | RPi Pin | Function  |
|:---------:|:-------:|-----------|
|VCC        | 2/4     | 5V+       | 
|GND        | 20/25   | GND       |
|DIN        | 19      | SPI MOSI / GPIO 10 |
|CS         | 24      | SPI CS0 / GPIO 8 |
|CLK        | 23      | SPI CLK / GPIO 11 |

### LCD 1602 I2C Display

![LCD 1602 HD44780](/doc/lcd_hd44780_i2c.jpg)!

SainSmart IIC/I2C/TWI 1602 Serial LCD Module with HD44780 controller, white on blue backlight, 16x2 chars

Due to 5VDC TTL level of the I2C module a 3.3V to 5V level changer is needed to connect it with the RPi's GPIOs.

| LCD I2C | 5V-to-3V3 changer | RPi Pin | Function |
|:-------:|:-----------------:|:-------:|----------|
|VCC      | HV (5V)           | 2/4     | 5V+      | 
|GND      | GND               | 6/9/14  | GND      |
|SDA      | TXO <--> TXI      | 3       | I2C1 SDA / GPIO 2 |
|SCL      | TXO <--> TXI      | 5       | I2C1 SCL / GPIO 3 |

### 5V Relay

![relay ttl](/doc/relay_5v_ttl.jpg)!

1 or 2 channel 5V TTL relay for 230V

Due to 5VDC TTL level of the relay module a 3.3V to 5V level changer is needed to connect it with the RPi's GPIOs.

| Relay | 5V-to-3V3 changer | RPi Pin | Function |
|:-----:|:-----------------:|:-------:|----------|
|VCC    | HV (5V)           | 2/4     | 5V+      | 
|GND    | GND               | 6/9/14  | GND      |
|IN1    | TXO <--> TXI      | 11      | GPIO 17  |
|IN2    | TXO <--> TXI      | 13      | GPIO 27  |

### Temperature sensor DHTxx

![dht11](/doc/dht11.jpg)!

DHT11 or DHT22 5V temperature and humidity sensor for indoor use.

| LED-Panel | RPi Pin  | Function  |
|:---------:|:--------:|-----------|
|VCC        | 2/4      | 5V+       | 
|GND        | 14/20/25 | GND       |
|DATA       | 7        | GPIO 4    |

Needed libs: ...

### Temperature sensor DS18B20

![ds18b20](/doc/ds18b20.jpg)!

DS18B20 3.3V temperature sensor for indoor and outdoor use.

| LED-Panel | RPi Pin  | Function  |
|:---------:|:--------:|-----------|
|VCC        | 1        | 3.3V+     | 
|GND        | 14/20/25 | GND       |
|DATA       | 7        | GPIO 4    |

Needed libs: ...

#### USB RFID reader

![usb rfid reader](/doc/rfid_hid_usb_reader.jpg)!

USB RFID reader for Mifare and ISO 14443A, working as USB HID device

*Warning:* Needs at minimum a power level of 4.90 VDC contantly, otherwise reader will disconnect and reconnect (with annoying beep sounds) infrequently!
