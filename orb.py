#!/usr/bin/env python

import serial

ser = serial.Serial("/dev/cu.usbserial-AJ03ACPV", baudrate=9600, parity='N', stopbits=1)  
print(ser)
#ser.write("?\r")      # write a string
try:
    line = []
    while True:
        for c in ser.read():
            if ord(c) > 128:
                c = chr(ord(c) - 128)
                #line.append(c.encode('hex'))
                line.append(c)
            else:
                line.append(c)
            if c == '\r':
                print(line)
                line = []
                break
finally:
    ser.close()             # close port