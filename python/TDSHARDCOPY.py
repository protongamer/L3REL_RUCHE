#Simple software to get the "hardcopy" (screen capture) of tektronix TDS680B over RS232 port
import serial, os

#############################################################################
#Setup

ser = serial.Serial("COM3", 9600) #setup port

#############################################################################

timeout = 3000000 #my version of time out (not good as it's supposed to be)
read = -1 
getEvent = 0 #false nothing has come, true we've got atleast a data

print("Name of the BMP file ?")
name = input()

file = open(name + ".bmp", "wb");

while (timeout > 0): #let user to start hardcopy on scope
	
	if(ser.in_waiting): #There a data in buffer ?
		getEvent = 1 #we've got one !
		read = ser.read(1) #acquire data
		file.write(read) #write this value in the file
		print("got : " + str(read[0])) #debug
		timeout = 3000000 #refresh to the start value

	timeout = timeout - 1 #countdown timeout
	
file.close()	#when finished stop and close the file

#set result of the process
if(getEvent):
	print("done")
else:
	print("timeout")