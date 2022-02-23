# -*- coding: utf-8 -*-

# Creation DT 2018 04 23
# Last update DT 2018 05 03

import logging
import base64
import pickle
import serial
import socket
#---------------------------------------------------------------------------#

# Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

TARGET_IP = '10.48.159.255'
TARGET_PORT = 3261


def send_udp(data):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.sendto(data, (TARGET_IP, TARGET_PORT))
        udp_socket.close()
    except Exception as error:
            log.debug('Connection failed to final destination')
            log.debug(str(error))

def get_modbus_data_serial():
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )

    serial_data=ser.readline()
    serial_data = serial_data.rstrip()
    if len(serial_data) > 0:
        get_modbus_data_serial.counter += 1
        # log.debug('packet n ' + str(get_modbus_data_serial.counter) + ', Bytes: ' + str(len(serial_data)))
        decoded_data = base64.b64decode(serial_data)
        depickeled_data = pickle.loads(decoded_data)
        send_udp(depickeled_data)
    ser.close()


get_modbus_data_serial.counter = 0


def receiving_loop():
    log.debug('Modbus Loop')
    while(1):
        try:
            get_modbus_data_serial()
        except Exception as error:
            log.debug('Error while updating modbus values')
            log.debug(str(error))

if __name__ == '__main__':
    receiving_loop()

