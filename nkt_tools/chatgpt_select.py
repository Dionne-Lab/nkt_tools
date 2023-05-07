"""AI generated, untested module for control of Select. Editting needed."""
import nkt

class SuperKSelect:
    def __init__(self, portname, module_address):
        self.portname = portname
        self.module_address = module_address

    def registerRead(self, register_address):
        return nkt.registerRead(self.portname, self.module_address, register_address, -1)

    def registerReadAscii(self, register_address):
        return nkt.registerReadAscii(self.portname, self.module_address, register_address, -1)

    def registerWrite(self, register_address, value):
        return nkt.registerWrite(self.portname, self.module_address, register_address, -1, value)

    def readMonitor1(self):
        return self.registerRead(0x10)

    def readMonitor2(self):
        return self.registerRead(0x11)

    def setMonitor1Gain(self, gain):
        self.registerWrite(0x32, gain)

    def setMonitor2Gain(self, gain):
        self.registerWrite(0x33, gain)

    def setRfSwitch(self, value):
        self.registerWrite(0x34, value)

    def setMonitorSwitch(self, value):
        self.registerWrite(0x35, value)

    def getCrystal1MinWavelength(self):
        return self.registerRead(0x90)

    def getCrystal1MaxWavelength(self):
        return self.registerRead(0x91)

    def getCrystal2MinWavelength(self):
        return self.registerRead(0xA0)

    def getCrystal2MaxWavelength(self):
        return self.registerRead(0xA1)
