from motorsync import MotorSync
import utime

motosync = MotorSync(20, 19, 18, 11, 12, 13, 10, 16)
motosync.run(50)
utime.sleep_ms(3000)
motosync.stop()
