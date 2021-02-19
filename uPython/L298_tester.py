from L298 import L298
import time

from machine import I2C
from ssd1306 import SSD1306_I2C
import framebuf
# Set up OLED display interface
WIDTH = 128
HEIGHT = 64
i2c = I2C(0)
# Uses I2C defaults for I2C0 SCL=Pin(GP9), SDA=Pin(GP8)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)


def setSpeed(speed, forward=True):
    oled.fill(0)
    oled.text("speed: {} ".format(speed), 5, 5)
    oled.text("forward: {}".format(forward), 5, 15)
    oled.show()
    print("speed: {} forward: {}".format(speed, forward))
    if forward:
        my298.forward(speed)
    else:
        my298.reverse(speed)
    time.sleep(3)


my298 = L298(11, 12, 13)

while True:
    setSpeed(0)
    setSpeed(25)
    setSpeed(50)
    setSpeed(75)
    setSpeed(100)
    setSpeed(0)
    setSpeed(25, forward=False)
    setSpeed(50, forward=False)
    setSpeed(75, forward=False)
    setSpeed(100, forward=False)
    my298.stop()
    oled.fill(0)
    oled.text("Stopped!", 5, 5)
    oled.show()
    time.sleep(5)
