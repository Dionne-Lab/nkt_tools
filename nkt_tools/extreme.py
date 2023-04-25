"""Python module to control NKT Extreme and Fianium Lasers."""
import NKTP_DLL as nkt


class Extreme:
    def __init__(self, portname=None):
        print('init class')

        self.portname = ''  #: COM port for laser. Auto found if not given.
        self.module_address = 15  #: module address = 15 for Extreme/Fianium

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

        # Close all ports
        closeResult = nkt.closePorts('')
        print('NKT Extreme/Fianium Found:')
        print('Comport: ', self.portname, 'Device type: ',
              "0x%0.2X" % device_type, 'at address:', self.module_address)


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
        result = nkt.registerRead(self.portname, self.module_address,
                                  register_address, -1)
        print(result)
        #TODO Get MSB/LSB from result
        MSB = 1  # What manual calls second byte
        LSB = 0  # What manual calls first byte
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
            print('Interlocked')
            reason = output_options[MSB]
            print(reason)

        elif LSB == 1:
            print('Waiting for interlock reset')

        elif LSB == 2:
            print('Interlock is OK')



def find_modules():
    print('Find modules on all existing and accessible ports - Might take a few seconds to complete.....')
    if (nkt.getLegacyBusScanning()):
        print('Scanning following ports in legacy mode:', nkt.getAllPorts())
    else:
        print('Scanning following ports in normal mode:', nkt.getAllPorts())

    # Use the openPorts function with Auto & Live settings. This will scan and detect modules
    # on all ports returned by the getAllPorts function.
    # Please note that a port being in use by another application, will show up in this list but will
    # not show any devices due to this port being inaccessible.
    print(nkt.openPorts(nkt.getAllPorts(), 1, 1))

    # All ports returned by the getOpenPorts function has modules (ports with no modules will automatically be closed)
    print('Following ports has modules:', nkt.getOpenPorts())

    # Traverse the getOpenPorts list and retrieve found modules via the deviceGetAllTypes function
    portlist = nkt.getOpenPorts().split(',')
    for portName in portlist:
        result, devList = nkt.deviceGetAllTypes(portName)
        for devId in range(0, len(devList)):
            if (devList[devId] != 0):
                print('Comport:', portName, 'Device type:', "0x%0.2X" % devList[devId], 'at address:', devId)

    # Close all ports
    closeResult = nkt.closePorts('')
    print('Close result: ', nkt.PortResultTypes(closeResult))
