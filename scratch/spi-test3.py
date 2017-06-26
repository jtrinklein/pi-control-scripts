#!/usr/bin/env python

import time
import pigpio

SPI_FLAGS=0b100000000
#SPI_FLAGS=0b0000000

pi = pigpio.pi()

if not pi.connected:
   exit(0)

dp = pi.spi_open(0, 976000, SPI_FLAGS) # MCP4251

start = time.time()

count = 0

for v in range(256):

    count += 5

    pi.spi_xfer(dp, [0x00, v])

    print (v, v)

    time.sleep(0.1)

stop = time.time()

diff = stop - start

print("{} SPI xfers in {:.2f} seconds ({}/s)".format(count, diff, int(count/diff)))

pi.spi_close(dp)
pi.stop()
