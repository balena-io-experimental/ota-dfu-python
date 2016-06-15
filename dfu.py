#!/usr/bin/env python

#------------------------------------------------------------------------------
# DFU Server for Nordic nRF51 based systems.
# Conforms to nRF51_SDK 11.0 BLE_DFU requirements.
#------------------------------------------------------------------------------
import sys
import optparse
import time

from unpacker import Unpacker
from bleServer import BleServer

#------------------------------------------------------------------------------
# Entry point
#------------------------------------------------------------------------------
def main():

    print "DFU Server start"

    try:
        parser = optparse.OptionParser(usage='%prog -f <hex_file> -a <dfu_target_address>\n\nExample:\n\tdfu.py -f application.hex -f application.dat -a cd:e3:4a:47:1c:e4',
                                       version='0.5')

        parser.add_option('-a', '--address',
                  action='store',
                  dest="address",
                  type="string",
                  default=None,
                  help='DFU target address.'
                  )

        parser.add_option('-f', '--file',
                  action='store',
                  dest="hexfile",
                  type="string",
                  default=None,
                  help='hex file to be uploaded.'
                  )

        parser.add_option('-d', '--dat',
                  action='store',
                  dest="datfile",
                  type="string",
                  default=None,
                  help='dat file to be uploaded.'
                  )

        parser.add_option('-z', '--zip',
                  action='store',
                  dest="zipfile",
                  type="string",
                  default=None,
                  help='zip file to be used.'
                  )

        options, args = parser.parse_args()

    except Exception, e:
        print e
        print "For help use --help"
        sys.exit(2)

    try:

        ''' Validate input parameters '''

        if not options.address:
            parser.print_help()
            exit(2)

        unpacker = None
        hexfile  = None
        datfile  = None

        if options.zipfile != None:

            if (options.hexfile != None) or (options.datfile != None):
                print "Conflicting input directives"
                exit(2)

            unpacker = Unpacker()
            hexfile, datfile = unpacker.unpack_zipfile(options.zipfile)

        else:
            if (not options.hexfile) or (not options.datfile):
                parser.print_help()
                exit(2)

            if not os.path.isfile(options.hexfile):
                print "Error: Hex file doesn't exist"
                exit(2)

            if not os.path.isfile(options.datfile):
                print "Error: DAT file doesn't exist"
                exit(2)

            hexfile = options.hexfile
            datfile = options.datfile


        ''' Start of Device Firmware Update processing '''

        bleServer = BleServer(options.address.upper(), hexfile, datfile)

        # Initialize inputs
        bleServer.input_setup()

        # Connect to peer device.
        bleServer.scan_and_connect()

        # Place into bootloader mode
        bleServer.dfu_bootloader()

        # Wait to receive the disconnect event from peripheral device.
        time.sleep(1)

        # Connect to peer device.
        bleServer.scan_and_connect()

        # Transmit the hex image to peer device.
        bleServer.dfu_send_image()

        # Wait to receive the disconnect event from peripheral device.
        time.sleep(1)

        # Disconnect from peer device if not done already and clean up.
        bleServer.disconnect()

    except Exception, e:
        print e
        pass

    except:
        pass

    # If Unpacker for zipfile used then delete Unpacker
    if unpacker != None:
        unpacker.delete()

    print "DFU Server done"

#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------
if __name__ == '__main__':

    # Do not litter the world with broken .pyc files.
    sys.dont_write_bytecode = True

    main()
