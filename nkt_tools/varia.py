"""Python module to control NKT Varia."""
import NKTP_DLL as nkt


class Varia:
    def __init__(self):
        print('init')
        self.portname = 'COM27'
        self.module_address = 17  # This apparently varies for Varia

    def monitor_input(self):
        register_address = 0x13
        result = nkt.registerRead(self.portname, self.module_address,
                                  register_address, -1)
        print(result)
        output_power = 'not yet implemented'

        return output_power

    def nd_setpoint(self, value):
        register_address = 0x32
        value = int(value/10)  # convert percent to permille
        nkt.registerWrite(self.portname, self.module_address,
                          register_address, value, -1)

    def swp_setpoint(self, value):
        register_address = 0x33
        value = int(value/10)  # convert nm to 1/10 nm
        nkt.registerWrite(self.portname, self.module_address,
                          register_address, value, -1)

    def lwp_setpoint(self, value):
        register_address = 0x34
        value = int(value/10)  # convert nm to 1/10 nm
        nkt.registerWrite(self.portname, self.module_address,
                          register_address, value, -1)

    def get_status(self):
        register_address = 0x66
        result = nkt.registerRead(self.portname, self.module_address,
                                  register_address, -1)
        print(result)
