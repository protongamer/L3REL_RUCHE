#Written by Enzo N. - 2021
#That Code is OpenIoB (internet of bee)
#Beta v1.0

import pygame, time, os, sys, os.path
import busio
import board
import adafruit_rfm9x
from digitalio import DigitalInOut, Direction, Pull
from pygame.locals import *
from datetime import date
from hive_core import *


############################################
#
# TODO list:
#
# LORA WAN SUPPORT:
#
# -GET AND STORE DATA TO THE RPI
# -SYNC HIVES
# 
#
#
#



############################################################################
## Before doing everything --> Read CFG file first
cfgSweep = 0
cfgStr = ""

file = open("data/parameters.cfg", "r+")
cfgStr = file.readlines()
file.close()

#read CFG

#an another god like tool
for cfgSweep in range(len(cfgStr)):

    #check if first character is not "#" to mean that is not a comment
    if(cfgStr[cfgSweep][0] != "#"):
        i = 0
        local_state = 0
        local_str = ""
        for i in range(len(cfgStr[cfgSweep])):
            if(cfgStr[cfgSweep][i] == "M"):
                local_state = 1 #mean we need to set MAX_HIVE value
                
            if(cfgStr[cfgSweep][i] == "A"):
                local_state = 2 #mean we need to set MAX_HIVE value
                
            if(cfgStr[cfgSweep][i] == "0" or cfgStr[cfgSweep][i] == "1" or cfgStr[cfgSweep][i] == "2" or
            cfgStr[cfgSweep][i] == "3" or cfgStr[cfgSweep][i] == "4" or cfgStr[cfgSweep][i] == "5" or
            cfgStr[cfgSweep][i] == "6" or cfgStr[cfgSweep][i] == "7" or cfgStr[cfgSweep][i] == "8" or
            cfgStr[cfgSweep][i] == "9" or cfgStr[cfgSweep][i] == "."):
                
                local_str = local_str + cfgStr[cfgSweep][i]
        
        if(local_state == 1):
            MAX_HIVE = int(local_str)
        if(local_state == 2):
            SERVER_ADRESS = int(local_str)
            #print("string value : ", local_str)
            
        #print(cfgStr[cfgSweep]) #DEBUG
        
        

##############################################
#Then setup the RFM95 board (Lora radio)

#CS = DigitalInOut(board.D16) #Setup Chip Select pin Connected to Pin10 of the Dragino Shield
#RESET = DigitalInOut(board.D12) #Setup Reset pin Connected to Pin9 of the Dragino Shield
#spi = busio.SPI(board.SCK_1, MOSI = board.MOSI_1, MISO = board.MISO_1) #Use SPI1 here (We already use SPI0 for PITFT !)
#rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RF_FREQ) #setup rfm9x structure to SPI1
#rfm9x.tx_power = 23 #power send to 23dBm

##############################################


#os.putenv('SDL_FBDEV', '/dev/fb1')
#os.putenv('SDL_MOUSEDRV', 'TLSIB')
#os.putenv('SLD_MOUSEDEV', '/dev/input/touchscreen')


#######################################################################################
#Functions

#######################
def setButton(posBX, posBY, width, height, pic):
    
    
    #set state mous pressed
    state = False
    
    #set variables of mouse position(local function)
    local_MX = 0
    local_MY = 0
    
    
    #display button
    screen.blit(pic, (posBX,posBY))
    
    
    #check if mouse pressed on button
    if (pygame.mouse.get_pressed() == (True,False,False)):
        (local_mX,local_mY) = pygame.mouse.get_pos()
        #print((local_mX,local_mY))
        if (local_mX > posBX and local_mX < posBX+width and local_mY > posBY and local_mY < posBY+height):
            state = True
    
    #print(state)

    return state
    
    
    

########################
def fillScreen(arg):
    pygame.draw.rect(screen,arg, ([0,0],[720,480]))


########################
def drawBar(coordinates, level):
    
    (bar_x, bar_y) = GFX_BAR_SIZE
    
    bar_x = level
    
    pygame.draw.rect(screen, GFX_COLOR_BAR1, (coordinates, GFX_BAR_SIZE));
    pygame.draw.rect(screen, GFX_COLOR_BAR2, (coordinates, (bar_x, bar_y)));


#######################
def setGraph(coordinates, dataType, actualHive):
    
    (baseX, baseY) = coordinates #read base graph
    local_x = 0
    local_y = 0
    old_x = 0
    old_y = 0
    
    localLastValue = 0
    
    
    screen.blit(graph, coordinates) #display grid(.bmp file)
    
    
   #read buffer 
    for bufferSweep in range(len(tempStr)):
        (R_DATA,D_DATA,T_DATA,H_DATA) = parseData(tempStr[bufferSweep])
       
        
        if(R_DATA == actualHive):
        
            old_x = local_x + baseX
            old_y = local_y + baseY
        
            if( dataType == HUMIDITY_DATA ):
                local_x = convert(D_DATA, 0.0, 31.0, 0.0, GFX_GRAPH_WIDTH)
                local_y = convert(H_DATA, MIN_HUMIDITY, MAX_HUMIDITY, GFX_GRAPH_HEIGHT, 0.0)
                localLastValue = H_DATA
            
            if( dataType == TEMPERATURE_DATA ):
                local_x = convert(D_DATA, 0.0, 31.0, 0.0, GFX_GRAPH_WIDTH)
                local_y = convert(T_DATA, MIN_TEMPERATURE, MAX_TEMPERATURE, GFX_GRAPH_HEIGHT, 0.0)
                localLastValue = T_DATA
            
            ####################
            #DRAW WHEN NEEDED !
            if(bufferSweep > 0):
                    pygame.draw.line(screen,GFX_COLOR_LINES, (old_x, old_y), (int(local_x+baseX), int(local_y+baseY)))
                
            pygame.draw.circle(screen, GFX_COLOR_POINTS, (int(baseX+local_x), int(baseY+local_y)), 2)
    return localLastValue
        
    











#######################################################################################
#Variables

#mouse Pos.
mX = 0
mY = 0

#used to load text files or data files
tempStr = ""
lastTemperature = 0
lastHumidity = 0

#used to display Ruche (1,2,3,4,5,...)
TitleRuche = ""
StrTemp = ""
StrHum = ""
currentRuche = 1

#If we want to stay in the while loop
loop = True

#flags, hmmm..., that pretty good for buttons, no ?
flag1 = False
flag2 = False
flag3 = False
flag4 = False
flag5 = False

#button state ? That necessary too
button1 = False
button2 = False

tempData = [0]*MAX_HIVE
humData = [0]*MAX_HIVE
dateData = [0]*MAX_HIVE


synchronise_level = MAX_HIVE #used to sync hives

counterTimer = 0


############
#RFM95 received packet --- at this moment it should be in this order : 

#1 byte : adress
#2 bytes : temperature
#2 bytes : humidity

#packet = None



room = MAIN_ROOM


#######################################################################################

#PATH = 'C:/Users/gordon/Documents/python/ruche/'

pygame.init()

sys.stdout.write("Gimli Says NO !\n\n\n")

file = open("data/bootPrint.md", "r+")
tempStr = file.readlines()
file.close()

#Equivalent of sizeof() in c
#print(len(tempStr))

boot_line = 0

for boot_line in range(len(tempStr)):
    sys.stdout.write(tempStr[boot_line])
    
boot_line = 0

sys.stdout.write("\n\nStarting...")
time.sleep(3)

sys.stdout.write("\n")

#debug start
#for x in range(6):
#    print(x)

#init screen
#screen = pygame.display.set_mode([720,480])
screen = pygame.display.set_mode([720,480], FULLSCREEN)

#################################################################
#Load all of pics
temp = pygame.image.load('pic/heat.bmp')
logo = pygame.image.load('pic/boot_logo.png')
hum = pygame.image.load('pic/hum.bmp')
but1 = pygame.image.load('pic/exit.bmp')
but2 = pygame.image.load('pic/next.bmp')
but3 = pygame.image.load('pic/prev.bmp')
but4 = pygame.image.load('pic/setup.bmp')
but5 = pygame.image.load('pic/button.bmp')
window = pygame.image.load('pic/window.bmp')
graph = pygame.image.load('pic/graph.bmp')
text1 = pygame.image.load('pic/text_resume.png')
text2 = pygame.image.load('pic/text_cfg.png')
text3 = pygame.image.load('pic/text_sync.png')
text4 = pygame.image.load('pic/text_quit.png')


#################################################################
#Load fonts
font = pygame.font.SysFont(None, 48)
mini_font = pygame.font.SysFont(None, 36)


##################################################################
#boot sequence


if (SKIP_BOOT_SEQUENCE == False):

    screen.blit(logo, (80,120))
    pygame.display.flip()
    time.sleep(3)


####################################
#Read time

t = time.localtime()
today = date.today()
year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")








##################################################
#Load database on boot

tempStr = ""

if(os.path.exists(dataFolder + "Y" + str(year) + "M" + str(month) + ".txt")):
	file = open(dataFolder + "Y"+ str(year) + "M" + str(month) + ".txt", "r+")
	tempStr = file.readlines()
	file.close()



#index_line = tempStr[0]

R_DATA = 0
D_DATA = 0
T_DATA = .0
H_DATA = 0
    
    


#debug my god function
#print((R_DATA,D_DATA,T_DATA,H_DATA))




print("Max hives : ", MAX_HIVE)
print("WAN ADRESS : ", SERVER_ADRESS)


t = time.localtime()
today = date.today()
year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")
#current_time = time.strftime("%H:%M:%S",t)
hour = time.strftime("%H",t)
minute = time.strftime("%M",t)
seconds = (int(23)*3600) + (int(59)*60)
day = int(day) + convert(int(seconds), 0, 86400, 0.0, 1.0001)

print(year, "  d(s):", seconds, "  d:", day)

#write to database at destination
#databaseWrite(dataFolder + "Y"+ str(year) + "M" + str(month) + ".txt", (3, day, 67, 67))






while loop == True:

    fillScreen((0,0,0))
    
    ####################
    #Let's read a packet now
    #packet = None #always reset packet
    #packet = rfm9x.receive()
    #if(packet != None): #We get a packet
	
    #		if(len(packet) == 6): #check if we have 6 bytes
    #			if(packet[0] == SERVER_ADRESS): #check if packet is sent to the server
    #				print("ID : ", packet[1])
    #				print("Temperature : ", packet[2] + (packet[3]/100))
    #				print("Humidity : ", packet[4] + (packet[5]/100))
    #				hour = time.strftime("%H", t)
    #				minute = time.strftime("%M", t)
    #				seconds = (int(hour)*3600) + (int(minute)*60)
    #				day = int(day) + convert(int(seconds), 0, 86400, 0.0, 1.0001)
    #				databaseWrite(dataFolder + "Y" + str(year) + "M" + str(month) + ".txt", (packet[1], day, packet[2] + (packet[3]/100), packet[4] + (packet[5]/100)))

    #			if(len(packet) < 6):
    #				print("Error reading !")


    if(room == CFG_ROOM):
        
        button5 = setButton(240, 10, 240, 100, but5) #previous button
        screen.blit(text1, (240, 10))
    
        button1 = setButton(480, 140, 50, 50, but2) #next button
        button2 = setButton(160, 140, 50, 50, but3) #previous button
        button3 = setButton(480, 240, 50, 50, but2) #next button
        button4 = setButton(160, 240, 50, 50, but3) #previous button
        
        local_Text_1 = mini_font.render("Max hives : " + str(MAX_HIVE), True, (255,255,255))
        local_Text_2 = mini_font.render("Server address : " + str(SERVER_ADRESS), True, (255,255,255))
        screen.blit(local_Text_1, (260, 150))
        screen.blit(local_Text_2, (240, 250))
        
        
        
        if(button5):
                flag5 = True
        
        if(button5 == False and flag5 == True):
                flag5 = False
                synchronise_level = MAX_HIVE
                tempData = [0]*MAX_HIVE
                humData = [0]*MAX_HIVE
                dateData = [0]*MAX_HIVE
                db = open("data/parameters.cfg", "w")
                local_str = CFG_STRING_1 + CFG_STRING_2 + "M = " + str(MAX_HIVE) + "\n\n" + CFG_STRING_3 + "A = " + str(SERVER_ADRESS)
                db.write(local_str)
                db.close()
                room = SETUP_ROOM
                
        if(button1):
                flag1 = True
        
        if(button1 == False and flag1 == True):
                flag1 = False
                MAX_HIVE = MAX_HIVE + 1
                if(MAX_HIVE > 99):
                    MAX_HIVE = 99
                
        if(button2):
                flag2 = True
        
        if(button2 == False and flag2 == True):
                flag2 = False
                MAX_HIVE = MAX_HIVE - 1
                if(MAX_HIVE < 1):
                    MAX_HIVE = 1 
                
                
        if(button3):
                flag3 = True
        
        if(button3 == False and flag3 == True):
                flag3 = False
                SERVER_ADRESS = SERVER_ADRESS + 1
                if(SERVER_ADRESS > 255):
                    SERVER_ADRESS = 255
        
        if(button4):
                flag4 = True
        
        if(button4 == False and flag4 == True):
                flag4 = False
                SERVER_ADRESS = SERVER_ADRESS - 1
                if(SERVER_ADRESS < 0):
                    SERVER_ADRESS = 0
                
    

    if(room == SETUP_ROOM):
    
            if (synchronise_level == MAX_HIVE): #if no sync is in progress
                button3 = setButton(240, 10, 240, 100, but5) #previous button
                screen.blit(text1, (240, 10))
                button4 = setButton(240, 130, 240, 100, but5) #CFG button
                screen.blit(text2, (240, 130))
                button5 = setButton(240, 250, 240, 100, but5) #synchronise hives button
                screen.blit(text3, (240, 250))
                loop = not(setButton(240, 370, 240, 100, but5)) #quit button
                screen.blit(text4, (240, 370))
            
                if(button5):
                    synchronise_level = 1
            
                if(button4):
                    room = CFG_ROOM
            
                if(button3):
                    room = MAIN_ROOM
                    
            elif (synchronise_level <= MAX_HIVE): #sunc in progress
                print(synchronise_level)
                strAlertText = "Function not implemented yet !"
                alertText = font.render(strAlertText, True, (255,127,0))
                screen.blit(alertText, (90,100))
                drawBar((240,200), convert(synchronise_level, 0, MAX_HIVE, 0, 200))
                synchronise_level = synchronise_level + 1
                time.sleep(0.05)
                
            
            

    if(room == MAIN_ROOM):

        ######################################################
        #Routines part
    
        #get time
        t = time.localtime()
        today = date.today()
        text_day = today.strftime("%d/%m/%Y")
        #text_day = str((mX, mY)) #debug
        current_time = time.strftime("%H:%M:%S",t)
    
        TitleRuche = "Ruche " + str(currentRuche)
        #StrTemp = str(tempData[currentRuche-1]) + "°C"
        #StrHum = str(humData[currentRuche-1]) + "%"
        StrTemp = str(int(lastTemperature)) + "°C"
        StrHum = str(int(lastHumidity)) + "%"
    
        ######################################################
        #Display part
        fillScreen((0,0,0))
        screen.blit(temp, (0,142))
        screen.blit(hum, (0,260))
        screen.blit(window, (225,20))
        #screen.blit(graph, (280,142))
        #screen.blit(graph, (280,280))
        lastTemperature = setGraph((280,142), TEMPERATURE_DATA, currentRuche)
        lastHumidity = setGraph((280,280), HUMIDITY_DATA, currentRuche)
        #Text part
    
        displayTemp = font.render(StrTemp, True, (255,255,255))
        screen.blit(displayTemp, (95, 180))
    
        displayHum = font.render(StrHum, True, (255,255,255))
        screen.blit(displayHum, (95, 300))
    
        displayRuche = font.render(TitleRuche, True, (255,255,255))
        screen.blit(displayRuche, (280, 55))
    
        displayDay = font.render(text_day, True, (255,255,255))
        screen.blit(displayDay, (20, 400))
    
        displayTime = font.render(current_time, True, (255,255,255))
        screen.blit(displayTime, (20, 440))
    
    
        ######################################################
    
    
    
    
    
    
            
        #####################################################
        #set Buttons
        #loop = not(setButton(680, 20, 25, 25, but1)) #exit button
        button1 = setButton(480, 40, 50, 50, but2) #next button
        button2 = setButton(160, 40, 50, 50, but3) #previous button
        if(setButton(640, 40, 50, 50, but4)): #setup button
            room = SETUP_ROOM #goto setup room
        #setButton(640, 200, 240, 100, but5)
   
        if(button1 == True):
            flag1 = True
    
        if(button2 == True):
            flag2 = True
   
        if(button1 == False and flag1 == True):
            currentRuche = currentRuche + 1
            #if we overflow max value
            if(currentRuche > MAX_HIVE):
                currentRuche = 1        
            #useful to do it one time
            flag1 = False
        
        if(button2 == False and flag2 == True):
            currentRuche = currentRuche - 1
            #if we overflow min value
            if(currentRuche < 1):
                currentRuche = MAX_HIVE        
            #useful to do it one time
            flag2 = False
        
   
   
        ######################################################
    
    
    
    
    
    
    
    
   
        ######################################################
        #debug mouse 
    if (pygame.mouse.get_pressed() == (True,False,False)):
        (mX, mY) = pygame.mouse.get_pos()    
        #pygame.draw.circle(screen, (255,255,0), (int(convert(mY, 0.0, 320.0, 0.0, 320.0))+50, int(convert(mX, 0.0, 480.0, 320.0, 0.0))+50), 5)
        print((mX, mY))
        
    
        #######################################################
        #Debug values
    
        #tempData[0] = 11
        #tempData[1] = 32
        #tempData[2] = 17
        #tempData[3] = 20
        #tempData[4] = 25
    
        #humData[0] = 25
        #humData[1] = 28
        #humData[2] = 93
        #humData[3] = 100
        #humData[4] = 4
        
        
        #############################################
        #Other stuff
    
    
    
        #If user click on stop button(from os)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    
    
    counterTimer = counterTimer + 1
    
    if(counterTimer > 200):
    	if(os.path.exists(dataFolder + "Y" + str(year) + "M" + str(month) + ".txt")):
    		file = open(dataFolder + "Y" + str(year) + "M" + str(month) + ".txt", "r+")
    		tempStr = file.readlines()
    		file.close()
    	counterTimer = 0




    time.sleep(0.005)
    pygame.display.flip()







#if end loop, then exit
time.sleep(0.1)
exit()




