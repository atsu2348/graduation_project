#!/usr/bin/env python

from time import sleep
import serial
import sys
import json
import math
import requests
import pandas as pd
from datetime import datetime
import time
import ntplib

"""問題点
このUbuntuPCには複数のPythonが入っている
具体的には純正のpython2,python3、Anacondaのpython3
pythonと入力:python3[Anaconda]
python <file_name>と入力:python3[純正]
python2と入力:python2[純正]
python3と入力:python3[Anaconda]
sudo pythonと入力:python2[純正]
sudo python <file_name>と入力:python2[純正]<-今回の問題点
sudo python2と入力:python2[純正]
sudo python3と入力:python3[純正]
という状態になっている
なので、.bashrcにpython_condaを設定することで、どの場合においてもAnacondaのpython3が実行されるようにした"""

#NTPからの時間
def ntp_time():
    x = ntplib.NTPClient()
    response = x.request('ntp.nict.jp')
    response2 = response.tx_time
    time = datetime.fromtimestamp(response2)
    time = time.strftime('%Y-%m-%d %H:%M:%S.%f')#str型に変換
    return time
'''
def ntp_time():
    j = json.loads(requests.get('http://ntp-a1.nict.go.jp/cgi-bin/json').text)
    n = float(j['st'])
    n += 0.5 # 遅延分修正
    h = (int( n / 3600 % 24) + 9) % 24  # JST = GMT + 9H
    m = int(n / 60 % 60)
    s = int(n % 60)
    ms = n % 1
    ms = ms * 1000000
    time = datetime.time(int(h),int(m),int(s),int(ms))
    #ms = round(ms)
    #time = str(h).rjust(2,'0') + ":" + str(m).rjust(2,'0') + ":" + str(s).rjust(2,'0') + "." + str(int(ms))
    return time
'''

# ser = serial.Serial('COM4', 115200, timeout=5)#Windows
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=None)  # Ubuntu
#ser = serial.Serial('/dev/ttyACM0', 115200, timeout=None)  # Arduino
# sudo python user.py -p /dev/ttyUSB0
# sudo screen /dev/ttyUSB0 115200
# sudo cat /dev/ttyUSB0 |od -tx1 -v
# A5 4A 0F 10832399
# A5 4A 1D 10832413
# OPENBCI_PACKET_SIZE 33 #Packet Size

#初回のみ
#sleep(0.5)
#str_bytes = bytes(b'<')
#ser.write(str_bytes)
sleep(0.5)
str_bytes = bytes(b'b')
ser.write(str_bytes)
#ser.write(bytes(raw_input('>>>')))#入力待ちしたいときに使う
raw_data = ser.read(33)#パケットサイズが33のため
data_list = [d for d in raw_data]#raw_data分のdata_listを作成
try:
    print(data_list)
    start = data_list.index(160)#a0の位置を記録
except:
    print("Error")
    str_bytes = bytes(b's')
    ser.write(str_bytes)
    ser.close()
    sys.exit()

#channel情報
print("a0 is " + str(start))
channel = [0 for i in range(8)]
for i in range(8):
    for j in range(3):
        channel[i] <<= 8#8ビットずらす
        try:
            channel[i] |= data_list[start + 2 + i * 3+ j]#文字を文字コードに変換
        except ValueError:
            print("a0が先頭にありません")
            str_bytes = bytes(b's')
            ser.write(str_bytes)
            ser.close()
            sys.exit()
        except IndexError:
            print("channelの計算時にエラーが出ました")
            str_bytes = bytes(b's')
            ser.write(str_bytes)
            ser.close()
            sys.exit()
        if channel[i] > 0x7fffff:
            channel[i] = -(channel[i] & 0x7fffff)#符号付き整数max 8388607==2.5V
    print("channel[" + str(i + 1) + "]: " + str(channel[i]))
print(type(data_list))

#timestamp情報
#T3 = data_list[start + 28]
#T2 = data_list[start + 29]
#T1 = data_list[start + 30]
#T0 = data_list[start + 31]
Time_for_bci = 0
for i in range(4):
    Time_for_bci |= data_list[start + 28]
    Time_for_bci <<= 8
    Time_for_bci |= data_list[start + 29]
    Time_for_bci <<= 8
    Time_for_bci |= data_list[start + 30]
    Time_for_bci <<= 8
    Time_for_bci |= data_list[start + 31]
print("Timestamp: " + str(Time_for_bci) + "ms")#BCI_timestampコマンド送信時からの時刻(ms)

#NTP時刻情報
Time_for_ntp = ntp_time()
print("NTP_Time: " + str(Time_for_ntp))

#ファイル作成
data_list_ntp_add = []
data_list_ntp_add = data_list
data_list_ntp_add.insert(0,Time_for_bci)
data_list_ntp_add.insert(0,Time_for_ntp)
df = pd.DataFrame({"NTP_Time":[Time_for_ntp],"OpenBCI_Time":[Time_for_bci],"channel1":[channel[0]],"channel2":[channel[1]],"channel3":[channel[2]],"channel4":[channel[3]],"channel5":[channel[4]],"channel6":[channel[5]],"channel7":[channel[6]],"channel[8]":[channel[7]]})
print(data_list_ntp_add)
print(type(data_list_ntp_add))
df.to_csv("testfile3.csv")
print("Export to csvfile")

sleep(0.5)
str_bytes = bytes(b's')
ser.write(str_bytes)
ser.close()

