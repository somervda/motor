from L298 import L298
import time

from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import framebuf
import gc
from dataLogger import DataLogger
import _thread
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

statusTimer = Timer()

gSpeed = 0
gIsForward = True
gDuration = 0
gFreq = 300
gCycle = 0

# Do manual garbage collects to manage CPU usage
gc.collect()
gc.disable()


def motorEncoderCallback(pin):
    global gMotorEncoderCnt
    gMotorEncoderCnt += 1


def stopMoving(timer):
    # Reset motorEncoder and handler
    motorEncoder.irq(handler=None)
    my298.stop()
    motorEncoder.init()
    print("stopMoving")
    global gMotorEncoderCnt
    global gDuration
    global gSpeed
    global gIsForward
    global gFreq
    #motorEncoder.irq(trigger=None, handler=None)
    dl.write(str(gCycle) + "\t" + str(gSpeed) + "\t" + str(gIsForward) + "\t" +
             str(gMotorEncoderCnt) + "\t" + str(gDuration) + "\t" + str(gFreq) + "\tL298")
    gc.collect()
    gMotorEncoderCnt = 0


def setSpeed(speed, isForward=True):
    global gDuration
    global gSpeed
    global gIsForward
    global gCycle
    gDuration = 3
    gSpeed = speed
    gIsForward = isForward
    oled.fill(0)
    oled.text("speed: {} ".format(speed), 5, 5)
    oled.text("forward: {}".format(isForward), 5, 15)
    oled.show()
    print("speed: {} isForward?: {} free:{} cycle:{}".format(
        speed, isForward, umemory.free(), gCycle))

    statusTimer.init(freq=1/gDuration, mode=Timer.ONE_SHOT,
                     callback=stopMoving)
    # Run for the sleepFor seconds
    motorEncoder.irq(trigger=machine.Pin.IRQ_FALLING,
                     handler=motorEncoderCallback)
    if isForward:
        my298.forward(speed)
    else:
        my298.reverse(speed)
    # time.sleep(sleepFor)

    #  Reset the motor encoder cnt
#     motorEncoderCnt = 0


my298 = L298(11, 12, 13, gFreq)
dl = DataLogger("cycle\tspeed\tisForward\tmotorEncoderCnt\tduration\tfreq\tmc")

while True:
    gCycle += 1
    my298.stop()
    oled.fill(0)
    oled.text("Stopped!", 5, 5)
    oled.show()
    time.sleep(3)
    # setSpeed(20)
    setSpeed(100)
    time.sleep(5)
    setSpeed(80)
    time.sleep(5)
    setSpeed(60)
    time.sleep(5)
    setSpeed(40)
    time.sleep(5)
    setSpeed(20)
    time.sleep(5)
    setSpeed(10)
    time.sleep(5)
    setSpeed(5)
    time.sleep(5)
