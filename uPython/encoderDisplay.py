from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import framebuf

# Set up motor encoder interface
motorEncoderCnt = 0
motorEncoder = Pin(10, Pin.IN)


def motorEncoderCallback(pin):
    global motorEncoderCnt
    motorEncoderCnt = motorEncoderCnt+1


motorEncoder.irq(trigger=machine.Pin.IRQ_FALLING, handler=motorEncoderCallback)

# Set up OLED display interface
WIDTH = 128
HEIGHT = 64
i2c = I2C(0)
# Uses I2C defaults for I2C0 SCL=Pin(GP9), SDA=Pin(GP8)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)


statusTimer = Timer()


def updateStatus(timer):
    global motorEncoderCnt

    oled.fill(0)
    oled.text("Pulses:" + str(motorEncoderCnt), 5, 5)
    motorEncoderCnt = 0
    oled.show()
    # print("motorEncoderCnt:",motorEncoderCnt)


statusTimer.init(freq=1, mode=Timer.PERIODIC, callback=updateStatus)

# The following lines will stop the timer and motorEncoder irq from running in the background
# Run from REPL when you want the routine to stop running
# statusTimer.deinit()
# motorEncoder.irq(handler=None)
