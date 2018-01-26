# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from __future__ import division
import logging
import time
from pyftdi import i2c








class class_get_values(object):
    debug = 0

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG BH1750 {0} {1}, {2}".format(level, datetime.now(),
                                                     msg))

    #read data from sensor
    @classmethod
    def __init__(self, *args):
        DEVICE = 0x23  # Default device I2C address
        POWER_DOWN = 0x00  # No active state
        POWER_ON = 0x01  # Power on
        RESET = 0x07  # Reset data register value
        # Instanciate an I2C controller

        i2c = I2cController()

        # Configure the first interface (IF/1) of the FTDI device as an I2C master
        i2c.configure('ftdi://ftdi:2232h/1')

        # Get a port to an I2C slave device
        slave = i2c.get_port(0x21)

        # Send one byte, then receive one byte
        slave.exchange([0x04], 1)

        # Write a register to the I2C slave
        slave.write_to(0x06, b'\x00')

        # Read a register from the I2C slave
        slave.read_from(0x00, 1)



        # Start measurement at 4lx resolution. Time typically 16ms.
        CONTINUOUS_LOW_RES_MODE = 0x13
        # Start measurement at 1lx resolution. Time typically 120ms
        CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Start measurement at 0.5lx resolution. Time typically 120ms
        CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Start measurement at 0.5lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_LOW_RES_MODE = 0x23

        #bus = smbus.SMBus(0) # Rev 1 Pi uses 0
    #    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

        def convertToNumber(data):
            # Simple function to convert 2 bytes of data
            # into a decimal number
            return ((data[1] + (256 * data[0])) / 1.2)

        def readLight(addr=DEVICE):
            pass
        #    data = bus.readList(ONE_TIME_HIGH_RES_MODE_2,3)
            #data = bus.readU16BE(ONE_TIME_HIGH_RES_MODE_2)
            #print data

        readLight()
        """    for arg in args:
            try:
                maapidb.MaaPiDBConnection.insert_data(arg[0], readLight(),
                                                      arg[2], True)
            except:
                self._debug(1, "\tERROR reading values from dev: {0}".format(
                    arg[1]))
                maapidb.MaaPiDBConnection.insert_data(arg[0], 0, arg[2], False)
        """
