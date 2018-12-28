# -*- coding: utf-8 -*-
import socket
import serial
import time
import RPi.GPIO as GPIO

#con=serial.Serial('/dev/ttyUSB0',38400,timeout=0)
#print (con.portstr)

ps3_data = [0 for i in range(8)]
ps3_data[3] = 127
ps3_data[4] = 127
ps3_data[5] = 127
ps3_data[6] = 127


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("192.168.11.2", 55555))

while(1):

    data = soc.recv(1024)
    
    decode_data = data.hex()

    if len(decode_data) == 16 :

        for x in range(8):
            x_num = x * 2
            y_num = x * 2 + 1
            ps3_data[x] = int(decode_data[x_num],16) << 4
            ps3_data[x] += int(decode_data[y_num],16)

            print(ps3_data)
#            con.write(ps3_data)
            
    else :
        pass