#Written by Enzo N. - 2021
#That Code is OpenIoB (internet of bee)
#Beta v1.0

#this is part for transmission using RFM9x module
#This is supposed to run at the same time than main.py
#A bash script is adviced to run this script and the main.py

import time, os, sys, os.path
import busio
import board
import adafruit_rfm9x
from digitalio import DigitalInOut, Direction, Pull
from pygame.locals import *
from datetime import date
from hive_core import *


#Then setup the RFM95 board (Lora radio)

CS = DigitalInOut(board.D16) #Setup Chip Select pin Connected to Pin10 of the Dragino Shield
RESET = DigitalInOut(board.D12) #Setup Reset pin Connected to Pin9 of the Dragino Shield
spi = busio.SPI(board.SCK_1, MOSI = board.MOSI_1, MISO = board.MISO_1) #Use SPI1 here (We already use SPI0 for PITFT !)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RF_FREQ) #setup rfm9x structure to SPI1
rfm9x.tx_power = 23 #power send to 23dBm

year = 0
month = 0
day = 0
seconds = 0
minute = 0
hour = 0
loop = True

print("Why hello Dr.stanz...")
print("RFM9x ready")

send_packet = bytes([112]) #112 in ASCII -> character 'p'

while loop == True:

    #get time
    t = time.localtime()
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    ####################
    #Let's read a packet now
    packet = None #always reset packet
    packet = rfm9x.receive()
    if(packet != None): #We get a packet
	
    		if(len(packet) == 6): #check if we have 6 bytes
    			if(packet[0] == SERVER_ADRESS): #check if packet is sent to the server
    				print("ID : ", packet[1])
    				print("Temperature : ", packet[2] + (packet[3]/100))
    				print("Humidity : ", packet[4] + (packet[5]/100))
    				hour = time.strftime("%H", t)
    				minute = time.strftime("%M", t)
    				seconds = (int(hour)*3600) + (int(minute)*60)
    				day = int(day) + convert(int(seconds), 0, 86400, 0.0, 1.0001)
    				databaseWrite(dataFolder + "Y" + str(year) + "M" + str(month) + ".txt", (packet[1], day, packet[2] + (packet[3]/100), packet[4] + (packet[5]/100)))
    				#send now data
    				rfm9x.send(send_packet)
    				print(send_packet)


    			if(len(packet) < 6):
    				print("Error reading !")

