from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import framebuf
import utime
from hbridge import HBridge

# Set up motor driver
PWM_FREQUENCY = 1000
motorLeft = HBridge(20, 19, 18, PWM_FREQUENCY)
motorRight = HBridge(11, 12, 13, PWM_FREQUENCY)


# Set up motor encoder interface
motorEncoderCntR = 0
motorEncoderCntTotalR = 0
motorEncoderR = Pin(10, Pin.IN)
motorEncoderCntL = 0
motorEncoderCntTotalL = 0
motorEncoderL = Pin(16, Pin.IN)

baseSpeed = 0
# Amount of compensation to apply to motor speed to re-align distance totals
# we don't want to adjust too much in a single monitoring cycle
dFactor = 0.2


def motorEncoderCallbackR(pin):
    global motorEncoderCntR
    global motorEncoderCntTotalR
    motorEncoderCntR += 1
    motorEncoderCntTotalR += 1


def motorEncoderCallbackL(pin):
    global motorEncoderCntL
    global motorEncoderCntTotalL
    motorEncoderCntL += 1
    motorEncoderCntTotalL += 1


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


def adjustLRSpeed():
    # Checks the the distance moved on each mover and
    # adjust faster one down if moved further tan the slower
    global motorLeft
    global motorRight
    speedL = baseSpeed
    speedR = baseSpeed
    if (motorEncoderCntR > 0 and motorEncoderCntL > 0 and motorEncoderCntTotalL > 0 and motorEncoderCntTotalR > 0):
        speedDiff = abs(motorEncoderCntL - motorEncoderCntR) / motorEncoderCntR
        #  Distance difference is based on overall difference in distance divided by average delta distance
        distDiff = abs(motorEncoderCntTotalL -
                       motorEncoderCntTotalR) / ((motorEncoderCntR + motorEncoderCntL)/2)
        # print(" Diff:" + str(speedDiff))
        # if (speedDiff > 0.001):
        # print(" Comp:" + str(speedCompensation))
        if (motorEncoderCntL > motorEncoderCntR):
            speedL -= round(speedL * speedDiff)
            print("left diff :" + str(speedDiff))
        else:
            speedR -= round(speedR * speedDiff)
            print("Right diff :" + str(speedDiff))
        # if (distDiff > 0.001):
            # If speeds must be adjusted to compensate for over all distance
            # then do it gradually
        if (motorEncoderCntTotalL > motorEncoderCntTotalR):
            speedL -= round(speedL * distDiff * dFactor)
            print("left comp :" + str(distDiff * dFactor))
        else:
            speedR -= round(speedR * distDiff * dFactor)
            print("right comp :" + str(distDiff * dFactor))
    print("speedL:" + str(speedL) + " speedR:" + str(speedR) + " distL:" + str(motorEncoderCntTotalL) + " distR:" +
          str(motorEncoderCntTotalR) + " deltaL:" + str(motorEncoderCntL) + " deltaR:" + str(motorEncoderCntR))
    motorLeft.forward(speedL)
    motorRight.forward(speedR)


def updateStatus(timer):
    global motorEncoderCntR
    global motorEncoderCntL

    oled.fill(0)
    oled.text("R:" + str(motorEncoderCntR) +
              " " + str(motorEncoderCntTotalR), 5, 5)
    oled.text("L:" + str(motorEncoderCntL) +
              " " + str(motorEncoderCntTotalL), 5, 15)
    adjustLRSpeed()
    motorEncoderCntR = 0
    motorEncoderCntL = 0
    oled.show()
    # print("motorEncoderCnt:",motorEncoderCnt)


def setSpeed():
    global baseSpeed
    motorRight.forward(baseSpeed)
    motorLeft.forward(baseSpeed)


statusTimer.init(freq=10, mode=Timer.PERIODIC, callback=updateStatus)
baseSpeed = 50
setSpeed()
utime.sleep_ms(10000)

# The following lines will stop the timer and motorEncoder irq from running in the background
# Run from REPL when you want the routine to stop running
baseSpeed = 0
setSpeed()
statusTimer.deinit()
motorEncoderR.irq(handler=None)
motorEncoderL.irq(handler=None)
