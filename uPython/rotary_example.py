
# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
#
# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import framebuf

import time
from rotary_irq import RotaryIRQ

# Set up OLED display interface
WIDTH = 128
HEIGHT = 64
i2c = I2C(0)
# Uses I2C defaults for I2C0 SCL=Pin(GP9), SDA=Pin(GP8)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

r = RotaryIRQ(pin_num_clk=15,
              pin_num_dt=14,
              min_val=0,
              max_val=20,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

val_old = r.value()
while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        # print('result =', val_new)
        oled.fill(0)
        oled.text("Encoder:" + str(val_new), 5, 5)
        oled.show()

    time.sleep_ms(50)
