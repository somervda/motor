from hbridge import HBridge
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import utime
import gc
from dataLogger import DataLogger
import umemory

DURATION = 3
PWM_FREQUENCY = 1000

# Set up OLED display interface
WIDTH = 128
HEIGHT = 64
i2c = I2C(0)
# Uses I2C defaults for I2C0 SCL=Pin(GP9), SDA=Pin(GP8)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Set up motor encoder interface
motorEncoder = Pin(10, Pin.IN)


# Varabled used in function that are not updated, so don't need to be global
cycle = 0

#  Set globals (Updated within functions)
gMotorEncoderCnt = 0

# Do manual garbage collects to manage CPU usage
gc.collect()
gc.disable()


def motorEncoderCallback(pin):
    global gMotorEncoderCnt
    gMotorEncoderCnt += 1


def setSpeed(speed, isForward=True):
    global gMotorEncoderCnt

    oled.fill(0)
    oled.text("speed: {} ".format(speed), 5, 5)
    oled.text("forward: {}".format(isForward), 5, 15)
    oled.show()
    print("speed: {} isForward?: {} free:{} cycle:{}".format(
        speed, isForward, umemory.free(), cycle))

    # Run for the sleepFor seconds
    motorEncoder.irq(trigger=Pin.IRQ_FALLING,
                     handler=motorEncoderCallback)
    if isForward:
        my298.forward(speed)
    else:
        my298.reverse(speed)
    utime.sleep(DURATION)
    # Reset motorEncoder and handler
    # Stop the irq handler before doing anything else!
    motorEncoder.irq(handler=None)
    my298.stop()
    motorEncoder.init()
    #  Write out log and cleanup gc, and reset encoder counter
    dl.write(str(cycle) + "\t" + str(speed) + "\t" + str(isForward) + "\t" +
             str(gMotorEncoderCnt) + "\t" + str(DURATION) + "\t" + str(PWM_FREQUENCY) + "\tL298")
    gc.collect()
    gMotorEncoderCnt = 0
    # time.sleep(1)

# *********** Main code **************


my298 = HBridge(11, 12, 13, PWM_FREQUENCY)
dl = DataLogger("cycle\tspeed\tisForward\tmotorEncoderCnt\tduration\tfreq\tmc")

setSpeed(70, False)
utime.sleep_ms(3000)
my298.stop()
# while True:
#     cycle += 1
#     setSpeed(70, False)
# setSpeed(100)
# setSpeed(80)
# setSpeed(60)
# setSpeed(40)
# setSpeed(20)
# setSpeed(10)
# setSpeed(5)
