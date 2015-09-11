#!/usr/bin/env python

import serial

class Packet(object):
    desc = ""
    def __init__(self, bytes):
        self.header = bytes[0]
        #assert(self.header in orb_packet_types.keys())

    @classmethod
    def create(cls, bytes):
        header = bytes[0]
        if header == 'R':
            result = ResetPacket(bytes)
        elif header == 'D':
            result =  BallDataPacket(bytes)            
        elif header == 'K':
            result = ButtonDataPacket(bytes)
        elif header == 'E':
            result = ErrorPacket(bytes)
        elif header == 'N':
            result = NullRegionPacket(bytes)
        elif header == '!':
            result = InformationPacket(bytes)
        else:
            result = UnknownPacket(bytes)
        return result

    def __str__(self):
        return self.desc

class ResetPacket(Packet):
    desc = 'reset'

class BallDataPacket(Packet):
    desc = 'ball data'

class ButtonDataPacket(Packet):
    desc = 'button data'

class ErrorPacket(Packet):
    desc = 'error'

class NullRegionPacket(Packet):
    desc = 'null region'

class InformationPacket(Packet):
    desc = 'information'

class UnknownPacket(Packet):
    desc = 'unknown'

ser = serial.Serial("/dev/cu.usbserial-AJ03ACPV", baudrate=9600, parity='N', stopbits=1)  
try:
    line = []
    while True:
        for c in ser.read():
                 #line.append(c.encode('hex'))
            line.append(c)
            if c == '\r':
                packet = Packet.create(line)
                print(packet)
                line = []
                break
finally:
    ser.close()             # close port
