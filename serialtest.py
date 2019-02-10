#!/usr/bin/env python
# coding: UTF-8
import serial
from time import sleep
import sys
import binascii

#ser = serial.Serial('COM4', 115200, timeout=5)#Windows
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=None)#Ubuntu
#sudo python user.py -p /dev/ttyUSB0
#sudo screen /dev/ttyUSB0 115200
#sudo cat /dev/ttyUSB0 |od -tx1 -v
#A5 4A 0F 10832399
#A5 4A 1D 10832413
#OPENBCI_PACKET_SIZE 33 #Packet Size

str_bytes = bytes(b'v')
ser.write(str_bytes)
sleep(1)
str_bytes = bytes(b'b')
ser.write(str_bytes)
raw_data = ser.read(33)
data_list = [d for d in raw_data]
try:
    start = data_list.index(b'\xa0')
except:
    print(ValueError)
"""
while 1:
    try:
        d = ser.read(33)
        try:
            print(d)
        except NameError:
            print("NameError")
            pass
    except KeyboardInterrupt:
        print("KeyBoardInterrupt")
        str_bytes = bytes(b's')
        c = ser.write(str_bytes)
        ser.close()
        sys.exit()
"""
print(data_list)
print("a0 is " + str(start))
print(data_list[start + 2 : start + 5])
channel1 = 0
for i in range(3):
    channel1 <<= 8#8ビットずらす
    channel1 |= ord(data_list[start + 2 + i])#文字を文字コードに変換
if channel1 > 0x7fffff:channel1 = -(channel1 & 0x7fffff)
print(channel1)#符号付き整数max 8388607==2.5V
str_bytes = bytes(b's')
ser.write(str_bytes)
ser.close()

#1