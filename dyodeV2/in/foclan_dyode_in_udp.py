# -*- coding: utf-8 -*-

# Creation DT 2018 04 23
# Last update DT 2018 05 03

import sys
import logging
import base64
import pickle
import struct
import serial

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import protocol, reactor
#---------------------------------------------------------------------------#

# Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

PORT_NUMBER = 3261

def modbus_send_serial(data):
    modbus_data = pickle.dumps(data)
    data_length = len(modbus_data)
    encoded_data = base64.b64encode(modbus_data)
    data_size = sys.getsizeof(encoded_data)
    # log.debug('Data size : %s' % data_size)

    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5
        )

    ser.write(encoded_data)
    ser.write('\n')
    # log.debug('written ' + str(len(encoded_data) + 1) + ' Bytes on serial')

class DyodeProtocol(DatagramProtocol):
    def sendReply(self, data, address):
        # log.debug('send reply')
        reply_content = data[0:4] + struct.pack('>H', 6) + data[6:12]
        # log.debug("send: " + " ".join([hex(ord(x)) for x in reply_content]))
        self.transport.write(reply_content, address)

    def datagramReceived(self, data, address):
        # log.debug('Received message')
        # log.debug("Received: " + " ".join([hex(ord(x)) for x in data]))
        # log.debug('function code')
        # log.debug(ord(data[7]))
        # log.debug('address')
        # log.debug(ord(data[9]))
        # log.debug(ord(data[10]))
        modbus_send_serial(data)
        self.sendReply(data, address)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

if __name__ == '__main__':
    log.debug('address')
    reactor.listenUDP(PORT_NUMBER, DyodeProtocol())
    reactor.run()
