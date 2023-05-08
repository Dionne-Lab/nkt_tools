"""AI generated, untested module for control of Extend UV. Editting needed."""
import ctypes
import superk  # dummy import added to hide chatgpt mix up

# Below is original chatgpt import (wrong)
# Load the SuperK.dll library
# superk = ctypes.WinDLL("SuperK.dll")

# Define the module type number
MODULE_TYPE = 0x6B

class ExtendUV:
    def __init__(self, address):
        self.address = address

    def _read_register(self, register_address):
        """Reads the value of a register"""
        data = ctypes.c_uint16()
        result = superk.registerRead(MODULE_TYPE, self.address, register_address, ctypes.byref(data))
        if result != 0:
            raise Exception("Error reading register")
        return data.value

    def _write_register(self, register_address, value):
        """Writes a value to a register"""
        result = superk.registerWrite(MODULE_TYPE, self.address, register_address, ctypes.c_uint16(value))
        if result != 0:
            raise Exception("Error writing register")

    def set_wavelength(self, wavelength):
        """Sets the wavelength setpoint in 1/10 nm"""
        self._write_register(0x31, wavelength)

    def get_wavelength(self):
        """Returns the wavelength setpoint in 1/10 nm"""
        return self._read_register(0x31)

    def set_max_wavelength(self, wavelength):
        """Sets the maximum selectable wavelength in 1/10 nm"""
        self._write_register(0x32, wavelength)

    def get_max_wavelength(self):
        """Returns the maximum selectable wavelength in 1/10 nm"""
        return self._read_register(0x32)

    def set_min_wavelength(self, wavelength):
        """Sets the minimum selectable wavelength in 1/10 nm"""
        self._write_register(0x33, wavelength)

    def get_min_wavelength(self):
        """Returns the minimum selectable wavelength in 1/10 nm"""
        return self._read_register(0x33)

    def get_status_bits(self):
        """Returns the status bits"""
        return self._read_register(0x66)
