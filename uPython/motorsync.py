from machine import Pin, I2C, Timer
import utime
from hbridge import HBridge


class MotorSync():

    # Set up motor encoder interface
    motorEncoderCntR = 0
    motorEncoderCntTotalR = 0
    motorEncoderCntL = 0
    motorEncoderCntTotalL = 0

    # Current speed setting
    speed = 0

    # dFactor represents the coefficient for the amount that overall distance
    # corrections should be applied on one monitoring cycle. Values less than 1
    # will insure distance corrections are done slowly over multiple monitoring
    # cycles
    dFactor = 0.2

    def __init__(self, pin_num_pwm_l, pin_num_in1_l, pin_num_in2_l,  pin_num_pwm_r, pin_num_in1_r, pin_num_in2_r, pin_num_encoder_l, pin_num_encoder_r, freq=1000):
        # setup hbridge motor controller pin assignments
        self.motorLeft = HBridge(
            pin_num_pwm_l,  pin_num_in1_l, pin_num_in2_l, freq)
        self.motorRight = HBridge(
            pin_num_pwm_r,  pin_num_in1_r, pin_num_in2_r, freq)
        self.motorEncoderL = Pin(pin_num_encoder_l, Pin.IN)
        self.motorEncoderR = Pin(pin_num_encoder_r, Pin.IN)

    def run(self, speed):
        self.speed = speed
        self.motorEncoderR.irq(trigger=Pin.IRQ_FALLING,
                               handler=self.motorEncoderCallbackR)
        self.motorEncoderL.irq(trigger=Pin.IRQ_FALLING,
                               handler=self.motorEncoderCallbackL)

        self.statusTimer = Timer()
        self.statusTimer.init(freq=10, mode=Timer.PERIODIC,
                              callback=self.monitorRunStatus)
        if (self.speed > 0):
            self.motorLeft.forward(self.speed)
            self.motorRight.forward(self.speed)
        if (self.speed < 0):
            self.motorLeft.reverse(abs(self.speed))
            self.motorRight.reverse(abs(self.speed))
        if (self.speed == 0):
            self.stop()

    def stop(self):
        self.motorLeft.stop()
        self.motorRight.stop()
        self.statusTimer.deinit()
        self.motorEncoderR.irq(handler=None)
        self.motorEncoderL.irq(handler=None)

    def monitorRunStatus(self, timer):
        self.adjustLRSpeed()
        # print("updateStatus " + str(self.motorEncoderCntL) +
        #       " " + str(self.motorEncoderCntR))
        self.motorEncoderCntR = 0
        self.motorEncoderCntL = 0

    def adjustLRSpeed(self):
        # Checks the the distance moved on each Tick and
        # reduce the faster motor speed if needed
        speedL = self.speed
        speedR = self.speed
        print("* Adjust Speed: " + str(self.speed) +
              " speedL:" + str(speedL) + " speedR:" + str(speedR))
        if (self.motorEncoderCntR > 0 and self.motorEncoderCntL > 0 and self.motorEncoderCntTotalL > 0 and self.motorEncoderCntTotalR > 0):
            speedDiff = abs((self.motorEncoderCntL -
                             self.motorEncoderCntR) / ((self.motorEncoderCntR + self.motorEncoderCntL)/2))
            #  Distance difference is based on overall difference in distance divided by average delta distance
            distDiff = abs((self.motorEncoderCntTotalL -
                            self.motorEncoderCntTotalR) / ((self.motorEncoderCntR + self.motorEncoderCntL)/2))
            #  Set the difference to reduce faster motor speed based on if positive or negative speed
            # isPositiveSpeed = False
            # if (self.speed > 0):
            #     isPositiveSpeed = True
            speedDiff *= -1
            distDiff *= -1
            if (self.motorEncoderCntL < self.motorEncoderCntR):
                print("left diff :" + str(speedDiff) + " speedL:" + str(speedL))
                speedL += round(speedL * speedDiff)
            else:
                print("Right diff :" + str(speedDiff) + " speedR:" + str(speedR))
                speedR += round(speedR * speedDiff)
            # If speeds must be adjusted to compensate for over all distance
            # then do it gradually based on dFactor
            if (self.motorEncoderCntTotalL < self.motorEncoderCntTotalR):
                print("left comp :" + str(distDiff * self.dFactor) +
                      " speedL:" + str(speedL))
                speedL += round(speedL * distDiff * self.dFactor)
            else:
                print("right comp :" + str(distDiff * self.dFactor) +
                      " speedR:" + str(speedR))
                speedR += round(speedR * distDiff * self.dFactor)
        print("speedL:" + str(speedL) + " speedR:" + str(speedR) + " distL:" + str(self.motorEncoderCntTotalL) + " distR:" +
              str(self.motorEncoderCntTotalR) + " deltaL:" + str(self.motorEncoderCntL) + " deltaR:" + str(self.motorEncoderCntR))
        self.motorLeft.forward(speedL)
        self.motorRight.forward(speedR)

    def motorEncoderCallbackR(self, pin):
        self.motorEncoderCntR += 1
        self.motorEncoderCntTotalR += 1

    def motorEncoderCallbackL(self, pin):
        self.motorEncoderCntL += 1
        self.motorEncoderCntTotalL += 1
