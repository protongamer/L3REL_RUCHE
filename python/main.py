#Written by Enzo N. - 2021
#That Code is OpenIoB (internet of bee)
#Alpha v0.3

import pygame, time, os, sys
from pygame.locals import *
from datetime import date

from hive_core import *






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
        
        
        


#######################################################################################
#Functions


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
    
    
    

    
def fillScreen(arg):
    pygame.draw.rect(screen,arg, ([0,0],[720,480]))











#######################################################################################
#Variables

#mouse Pos.
mX = 0
mY = 0

#used to load text files or data files
tempStr = ""

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

#button state ? That necessary too
button1 = False
button2 = False

tempData = [0]*MAX_HIVE
humData = [0]*MAX_HIVE





room = 0


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
screen = pygame.display.set_mode([720,480])


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


#################################################################
#Load fonts
font = pygame.font.SysFont(None, 48)


##################################################################
#boot sequence


if (SKIP_BOOT_SEQUENCE == False):

    #define a transparent rect for boot sequence
    s = pygame.Surface((720,480))
    s.set_alpha(255)
    s.fill((0,0,0))

    for x in range(255):
        screen.blit(logo, (80,120))
        screen.blit(s,(0,0))
        s.set_alpha(255-x)
        pygame.display.flip()
        time.sleep(.005)

    time.sleep(3)



##################################################
#Load database 

tempStr = ""


file = open("data/Y2021M03.txt", "r+")
tempStr = file.readlines()
file.close()



#index_line = tempStr[0]

R_DATA = 0
D_DATA = 0
T_DATA = .0
H_DATA = 0
    
(R_DATA,D_DATA,T_DATA,H_DATA) = parseData(tempStr[0])
tempData[R_DATA-1] = T_DATA
humData[R_DATA-1] = H_DATA

(R_DATA,D_DATA,T_DATA,H_DATA) = parseData(tempStr[1])
tempData[R_DATA-1] = T_DATA
humData[R_DATA-1] = H_DATA

(R_DATA,D_DATA,T_DATA,H_DATA) = parseData(tempStr[2])
tempData[R_DATA-1] = T_DATA
humData[R_DATA-1] = H_DATA

(R_DATA,D_DATA,T_DATA,H_DATA) = parseData(tempStr[3])
tempData[R_DATA-1] = T_DATA
humData[R_DATA-1] = H_DATA

#debug my god function
#print((R_DATA,D_DATA,T_DATA,H_DATA))




print("Max hives : ", MAX_HIVE)
print("WAN ADRESS : ", SERVER_ADRESS)

databaseWrite("data/Y2021M03.txt", (3, 1, 67, 67))

while loop == True:



















    


    ######################################################
    #Routines part
    
    #get time
    t = time.localtime()
    today = date.today();
    day = today.strftime("%d/%m/%Y")
    current_time = time.strftime("%H:%M:%S",t)
    
    TitleRuche = "Ruche " + str(currentRuche)
    StrTemp = str(tempData[currentRuche-1]) + "°C"
    StrHum = str(humData[currentRuche-1]) + "%"
    
    ######################################################
    #Display part
    fillScreen((0,0,0))
    screen.blit(temp, (0,142))
    screen.blit(hum, (0,260))
    screen.blit(window, (225,20))
    screen.blit(graph, (280,142))
    screen.blit(graph, (280,280))
    #Text part
    
    displayTemp = font.render(StrTemp, True, (255,255,255))
    screen.blit(displayTemp, (95, 180))
    
    displayHum = font.render(StrHum, True, (255,255,255))
    screen.blit(displayHum, (95, 300))
    
    displayRuche = font.render(TitleRuche, True, (255,255,255))
    screen.blit(displayRuche, (280, 55))
    
    displayDay = font.render(day, True, (255,255,255))
    screen.blit(displayDay, (20, 400))
    
    displayTime = font.render(current_time, True, (255,255,255))
    screen.blit(displayTime, (20, 440))
    
    
    ######################################################
    
    
    
    
    
    
            
    #####################################################
    #set Buttons
    loop = not(setButton(680, 20, 25, 25, but1)) #exit button
    
    button1 = setButton(480, 40, 50, 50, but2) #next button
    button2 = setButton(160, 40, 50, 50, but3) #previous button
    setButton(640, 40, 50, 50, but4) #setup button
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
    
    time.sleep(0.015)
    pygame.display.flip()







#if end loop, then exit
time.sleep(1)
exit()




