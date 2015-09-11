#!/usr/bin/env python

import serial

class Packet(object):
    desc = ""
    def __init__(self, bytes):
        self.header = bytes[0]
        self.data = bytes[1:-1]
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
        #line.append(c.encode('hex'))
        hexdata = [ch.encode("hex") for ch in self.data]
        return "{:12}|{}".format(self.desc, ":".join(hexdata))

class ResetPacket(Packet):
    desc = 'reset'

class BallDataPacket(Packet):
    desc = 'ball data'

class ButtonDataPacket(Packet):
    desc = 'button data'

    @classmethod
    def button_state_str(cls, byte):
        result = []
        byte = ord(byte)
        result.append('A' if byte & 0x01 else '-')
        result.append('B' if byte & 0x02 else '-')
        result.append('C' if byte & 0x04 else '-')
        result.append('D' if byte & 0x08 else '-')
        result.append('E' if byte & 0x10 else '-')
        result.append('F' if byte & 0x20 else '-')
        return "".join(result)


    def __str__(self):
        button_byte = self.data[1]
        return "{:12}| {}".format(self.desc, self.button_state_str(button_byte), button_byte.encode('hex'))

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
            line.append(c)
            if c == '\r':
                packet = Packet.create(line)
                print(packet)
                line = []
                break
finally:
    ser.close()             # close port
