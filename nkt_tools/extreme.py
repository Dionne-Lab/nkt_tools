"""Python module to control NKT Extreme and Fianium Lasers."""
import NKTP_DLL as nkt


class Extreme:
    status_messages = {
        0: 'Emission on',
        1: 'Interlock relays off',
        2: 'Interlock supply voltage low (possible short circuit)',
        3: 'Interlock loop open',
        4: 'Output Control signal low',
        5: 'Supply voltage low',
        6: 'Inlet temperature out of range',
        7: 'Clock battery low voltage',
        8: '-',
        9: '-',
        10: '-',
        11: '-',
        12: '-',
        13: 'CRC error on startup (possible module address conflict)',
        14: 'Log error code present',
        15: 'System error code present'
        }
    
    def __init__(self, portname=None):
        print('init class')

        self.portname = None  #: COM port for laser. Auto found if not given.
        self.module_address = 15  #: module address = 15 for Extreme/Fianium
        self.system_type = None

        if portname:  # Allow user to init specific NKT Laser on portname
            self.portname = portname

        else:
            # Open available ports
            nkt.openPorts(nkt.getAllPorts(), 1, 1)

            # Get open NKT ports
            portlist = nkt.getOpenPorts().split(',')
            extreme_found = False
            for portName in portlist:

                # get binary devList of connected nkt devices
                result, devList = nkt.deviceGetAllTypes(portName)
                # Get byte at location 15 (device address for extreme/fianium)
                device_type = devList[self.module_address]

                # Double check device_type matches extreme/fianium laser
                if hex(device_type) == '0x60':  # 96 == 0x60 in hex
                    if extreme_found:  # If extreme found on other port, error
                        err_msg = ('''Multiple NKT Lasers found on computer.
                        COM port 1 = %s
                        COM port 2 = %s
                        Please initialize Extreme class with designated \
                        portname to avoid conflict'''
                                   % (self.portname, portName))

                        raise RuntimeError(err_msg)

                    else:  # If first laser found,
                        extreme_found = True
                        self.portname = portName
                        self.device_type = device_type

        # Close all ports
        closeResult = nkt.closePorts('')
        if extreme_found:
            print('NKT Extreme/Fianium Found:')
            print('Comport: ', self.portname, 'Device type: ',
                  "0x%0.2X" % device_type, 'at address:', self.module_address)
            # Determine whether system is Extreme or Fianium
            register_address = 0x6B
            _, type_index = nkt.registerReadU8(self.portname, 
                                               self.module_address,
                                               register_address, -1)

            if not type_index:  # Errors should default to Extreme
                type_index = 0 
            type_list = ["SuperK Extreme", "SuperK Fianium"]
            self.system_type = type_list[type_index]
        else:
            print('No Extreme/Fianium Laser Found')


    def emission(self, state):
        """
        Change emission state of laser to on/off

        Uses nktp_dll to write to register 0x30.

        Parameters:
        state: bool
            True turns laser on, false turns emission off
        """
        register_address = 0x30
        if state is True:
            nkt.registerWriteU8(self.portname, self.module_address,
                                register_address, 0x03, -1)
        elif state is False:
            nkt.registerWriteU8(self.portname, self.module_address,
                                register_address, 0x00, -1)

    def interlock_status(self):
        register_address = 0x32
        result, reading = nkt.registerRead(self.portname, self.module_address,
                                           register_address, -1)

        LSB = reading[0]  # What manual calls first byte
        MSB = reading[1]  # What manual calls second byte
        # Interlock status message based on manual
        output_options = ['Interlock off (interlock circuit open)',
                          'Front panel interlock/key switch off',
                          'Door switch open',
                          'External module interlock',
                          'Application interlock',
                          'Internal module interlock',
                          'Interlock power failure',
                          'Interlock disabled by light source']
        if LSB == 0:
            reason = output_options[MSB]
            print('Interlocked: %s' % reason)

        elif LSB == 1:
            print('Waiting for interlock reset')

        elif LSB == 2:
            print('Interlock is OK')

    def get_status(self):
        register_address = 0x66
        result, byte = nkt.registerReadU16(self.portname, self.module_address,
                                           register_address, -1)
        print(nkt.RegisterResultTypes(result))
        bits = bin(byte)
        for index, bit in enumerate(reversed(bits)):
            if bit == 'b':
                break
            elif bit == '1':
                print(Extreme.status_messages[index])
                
        return(bits)

if __name__ == "__main__":
    laser = Extreme()
    laser.get_status()
    laser.interlock_status()
    print(laser.system_type)