from L298 import L298
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import time
import gc
from dataLogger import DataLogger
import umemory

# Set up OLED display interface
WIDTH = 128
HEIGHT = 64
i2c = I2C(0)
# Uses I2C defaults for I2C0 SCL=Pin(GP9), SDA=Pin(GP8)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Set up motor encoder interface
gMotorEncoderCnt = 0
motorEncoder = Pin(10, Pin.IN)

#  Set globals
gDuration = 3
gFreq = 300
gCycle = 0

# Do manual garbage collects to manage CPU usage
gc.collect()
gc.disable()


def motorEncoderCallback(pin):
    global gMotorEncoderCnt
    gMotorEncoderCnt += 1


def setSpeed(speed, isForward=True):
    global gDuration
    global gCycle
    global gFreq
    global gMotorEncoderCnt

    oled.fill(0)
    oled.text("speed: {} ".format(speed), 5, 5)
    oled.text("forward: {}".format(isForward), 5, 15)
    oled.show()
    print("speed: {} isForward?: {} free:{} cycle:{}".format(
        speed, isForward, umemory.free(), gCycle))

    # Run for the sleepFor seconds
    motorEncoder.irq(trigger=machine.Pin.IRQ_FALLING,
                     handler=motorEncoderCallback)
    if isForward:
        my298.forward(speed)
    else:
        my298.reverse(speed)
    time.sleep(gDuration)
    # Reset motorEncoder and handler
    # Stop the irq handeler before doing anything else!
    motorEncoder.irq(handler=None)
    my298.stop()
    motorEncoder.init()
    #  Write out log and cleanup gc, and encoder counter
    dl.write(str(gCycle) + "\t" + str(speed) + "\t" + str(isForward) + "\t" +
             str(gMotorEncoderCnt) + "\t" + str(gDuration) + "\t" + str(gFreq) + "\tL298")
    gc.collect()
    gMotorEncoderCnt = 0
    # time.sleep(1)

# *********** Main code **************


my298 = L298(11, 12, 13, gFreq)
dl = DataLogger("cycle\tspeed\tisForward\tmotorEncoderCnt\tduration\tfreq\tmc")

while True:
    gCycle += 1
    setSpeed(0)
    setSpeed(100)
    setSpeed(80)
    setSpeed(60)
    setSpeed(40)
    setSpeed(20)
    setSpeed(10)
    setSpeed(5)
