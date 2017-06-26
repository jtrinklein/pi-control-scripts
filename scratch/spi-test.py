#!/usr/bin/python

import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1953000

# Split an integer input into a two byte array to send via SPI
def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb, lsb])

write_pot(0xFF)
# Repeatedly switch a MCP4151 digital pot off then on
while True:
    
    raw_input('1. turn on?')
    write_pot(0x00)
    raw_input('2. turn off?')
    write_pot(0x1FF)
    
