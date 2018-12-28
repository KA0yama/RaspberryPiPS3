# -*- coding:utf-8 -*-

import sys
import socket
file=open('/dev/input/js0','rb')
data = []

#variable
button_data =  [0,0]
ps3_data = [0 for i in range(8)]
ps3_data[0] =  255
ps3_data[3] = 127
ps3_data[4] = 127
ps3_data[5] = 127
ps3_data[6] = 127

#flag
start_flag = 0
select_flag = 0
up_lock = 0
down_lock = 0
left_lock = 0
right_lock = 0

#main
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.11.2", 55555))   
s.listen(1)                    
soc, addr = s.accept()          
print("Conneted by"+str(addr))
while True:
	for character in file.read(1):
		data += ['%02X' % character]
		if len(data) == 8:

			if data[6] == '01' : # Button
				if data[4] == '01' : # pushed
					if data[7] == '00' : # SELECT
						select_flag = 1
						button_data[0] += 12

					elif data[7] == '01' : # L3
						pass
						
					elif data[7] == '02' : # R3
						pass
						
					elif data[7] == '03' : # START
						start_flag = 1
						button_data[0] += 3
						
					elif data[7] == '04' : # ↑
						if start_flag == 0 :
							button_data[0] += 1
						else :
							up_lock = 1
						
					elif data[7] == '05' : # →
						if select_flag == 0 :
							button_data[0] += 4
						else :
							right_lock = 1
						
					elif data[7] == '06' : # ↓
						if start_flag == 0 :
							button_data[0] += 2
						else :
							down_lock = 1

					elif data[7] == '07' : # ←
						if select_flag == 0 :
							button_data[0] += 8
						else :
							left_lock = 1

					elif data[7] == '08' : # L2
						button_data[1] += 4
						
					elif data[7] == '09' : # R2
						button_data[1] += 16
						
					elif data[7] == '0A' : # L1
						button_data[1] += 2
						
					elif data[7] == '0B' : # R1
						button_data[1] += 8
						
					elif data[7] == '0C' : # triangle
						button_data[0] += 16
						
					elif data[7] == '0D' : # circle
						button_data[0] += 64
						
					elif data[7] == '0E' : # ×
						button_data[0] += 32
						
					elif data[7] == '0F' : # square
						button_data[1] += 1
						
					elif data[7] == '10' : # ps
						button_data[1] += 32

				elif data[4] == '00' : # repushed
					if data[7] == '00' : # SELECT
						select_flag = 0
						button_data[0] -= 12

					elif data[7] == '01' : # L3
						pass
						
					elif data[7] == '02' : # R3
						pass
						
					elif data[7] == '03' : # START
						start_flag = 0
						button_data[0] -= 3
						
					elif data[7] == '04' : # ↑
						if up_lock == 0 :
							button_data[0] -= 1
						else :
							up_lock = 0
						
					elif data[7] == '05' : # →
						if right_lock == 0 :
							button_data[0] -= 4
						else :
							right_lock = 0
						
					elif data[7] == '06' : # ↓
						if down_lock == 0 :
							button_data[0] -= 2
						else :
							down_lock = 0
						
					elif data[7] == '07' : # ←
						if left_lock == 0 :
							button_data[0] -= 8
						else :
							left_lock = 0

					elif data[7] == '08' : # L2
						button_data[1] -= 4
						
					elif data[7] == '09' : # R2
						button_data[1] -= 16
						
					elif data[7] == '0A' : # L1
						button_data[1] -= 2
						
					elif data[7] == '0B' : # R1
						button_data[1] -= 8
						
					elif data[7] == '0C' : # triangle
						button_data[0] -= 16
						
					elif data[7] == '0D' : # circle
						button_data[0] -= 64
						
					elif data[7] == '0E' : # ×
						button_data[0] -= 32
						
					elif data[7] == '0F' : # square
						button_data[1] -= 1

					elif data[7] == '10' : # ps
						button_data[1] -= 32

				ps3_data[1] =  button_data[1]
				ps3_data[2] =  button_data[0]

			if data[6] == '02' : # JoyStick

				stick_data = int(data[5],16)
				
				if stick_data > 127 :
					int_stick_data = stick_data - 127

				else :
					int_stick_data = stick_data + 127


				if data[7] == '00' :
					ps3_data[3] = int_stick_data

					if ps3_data[3] < 0 :
						ps3_data[3] = 0

				elif data[7] == '01' :
					ps3_data[4] = 254 - int_stick_data

					if ps3_data[4] < 0 :
						ps3_data[4] = 0

				elif data[7] == '02' :
					ps3_data[5] = int_stick_data

					if ps3_data[5] < 0 :
						ps3_data[5] = 0

				elif data[7] == '03' :
					
					ps3_data[6] = 254 - int_stick_data

					if ps3_data[6] < 0 :
						ps3_data[6] = 0

				else :
					pass

			if data[6] == '01' or data[6] == '02' :
				for byte in ps3_data:
					sys.stdout.write(str(byte)+' ')

				sys.stdout.write('\n')

			else :
				pass

			sys.stdout.flush()
			data = []

			soc.send(bytes(ps3_data))