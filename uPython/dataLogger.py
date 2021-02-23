# A simple data logging application
# When the class is initiated,
# a logging file is created as D<seconds>.txt and
# a header line written based on a tab set of file names
# Writes out a tab delimited log line starting with <seconds><tab><data>

import time


class DataLogger():
    logFile = "D"

    def __init__(self, fields):
        self.logFile += str(time.time()) + ".txt"
        with open(self.logFile, "a") as logger:
            logger.write("epoch_sec\t" + fields + "\n")

    def write(self, data):
        with open(self.logFile, "a") as logger:
            logger.write(str(time.time()) + "\t" + data + "\n")
