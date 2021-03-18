from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import framebuf

# Set up motor encoder interface
motorEncoderCntR = 0
motorEncoderR = Pin(10, Pin.IN)
motorEncoderCntL = 0
motorEncoderL = Pin(16, Pin.IN)


def motorEncoderCallbackR(pin):
    global motorEncoderCntR
    motorEncoderCntR = motorEncoderCntR+1


def motorEncoderCallbackL(pin):
    global motorEncoderCntL
    motorEncoderCntL = motorEncoderCntL+1


motorEncoderR.irq(trigger=machine.Pin.IRQ_FALLING,
                  handler=motorEncoderCallbackR)

motorEncoderL.irq(trigger=machine.Pin.IRQ_FALLING,
                  handler=motorEncoderCallbackL)

# Set up OLED display interface
WIDTH = 128
HEIGHT = 64
i2c = I2C(0)
# Uses I2C defaults for I2C0 SCL=Pin(GP9), SDA=Pin(GP8)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)


statusTimer = Timer()


def updateStatus(timer):
    global motorEncoderCntR
    global motorEncoderCntL

    oled.fill(0)
    oled.text("Right:" + str(motorEncoderCntR), 5, 5)
    oled.text("Left:" + str(motorEncoderCntL), 5, 15)
    motorEncoderCntR = 0
    motorEncoderCntL = 0
    oled.show()
    # print("motorEncoderCnt:",motorEncoderCnt)


statusTimer.init(freq=1, mode=Timer.PERIODIC, callback=updateStatus)

# The following lines will stop the timer and motorEncoder irq from running in the background
# Run from REPL when you want the routine to stop running
# statusTimer.deinit()
# motorEncoder.irq(handler=None)
