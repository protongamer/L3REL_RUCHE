####################################################
#Here is the "const" core values that we must not change, or some of them maybe




########################
#ROUTINES PARAMETERS

#skip boot sequence ?
SKIP_BOOT_SEQUENCE = False 
#How much connected hives you want for your network ?
MAX_HIVE = 5 
RF_FREQ = 868.0  #What frequency we use ? (868 MHz in French Baguette lol / 915 MHz in US for BIG BURGER !)


dataFolder = "js/data/"



########
#Parameters values (better to be in const to work 8-)

MIN_TEMPERATURE = -50.0
MAX_TEMPERATURE = 150.0
MIN_HUMIDITY = 0.0
MAX_HUMIDITY = 100.0

GFX_GRAPH_WIDTH = 300.0
GFX_GRAPH_HEIGHT = 100.0
GFX_COLOR_POINTS = (0,255,255)
GFX_COLOR_LINES = (0,255,255)
GFX_COLOR_BAR1 = (127,127,127)
GFX_COLOR_BAR2 = (0,0,255)
GFX_BAR_SIZE = (200,40)

HUMIDITY_DATA = 0
TEMPERATURE_DATA = 1

CFG_STRING_1 = "#MAIN PARAMETERS\n\n"
CFG_STRING_2 = "#Max hives[1-99]\n"
CFG_STRING_3 = "#WAN SERVER ADRESS (DEFAULT -> 0)\n"




########################



#######################
#WAN NETWORK

SERVER_ADRESS = 0
RF_FREQ = 868.0 #What frequency we use ? (868.0MHz French Baguette / 915.0MHz US Lol)

#######################


MAIN_ROOM = 0
SETUP_ROOM = 1
CFG_ROOM = 2

    
    
######################################################################
#This is the ultimate god power tool. His name ? The Parser
def parseData(index_line):
    
    PARAM_R = ""
    PARAM_D = ""
    PARAM_T = ""
    PARAM_H = ""
    index_chr = 0
    state_chr = 0

    for index_chr in range(len(index_line)):
    
        #####################################
        #Character mode reading
        if(index_line[index_chr] == "R"):
            state_chr = 1
    
        elif(index_line[index_chr] == "D"):
            state_chr = 2
    
        elif(index_line[index_chr] == "T"):
            state_chr = 3
    
        elif(index_line[index_chr] == "H"):
            state_chr = 4
    
        elif(index_line[index_chr] == " "):
            state_chr = 0
        
        elif(index_line[index_chr] == "0" or index_line[index_chr] == "1" or index_line[index_chr] == "2" or
            index_line[index_chr] == "3" or index_line[index_chr] == "4" or index_line[index_chr] == "5" or
            index_line[index_chr] == "6" or index_line[index_chr] == "7" or index_line[index_chr] == "8" or
            index_line[index_chr] == "9" or index_line[index_chr] == "." or index_line[index_chr] == "-"):
            #####################################
            #Value reading
        
            if(state_chr == 1):
                PARAM_R = PARAM_R + str(index_line[index_chr])
            
            elif(state_chr == 2):
                PARAM_D = PARAM_D + str(index_line[index_chr])
        
            elif(state_chr == 3):
                PARAM_T = PARAM_T + str(index_line[index_chr])
            
            elif(state_chr == 4):
                PARAM_H = PARAM_H + str(index_line[index_chr])
    return (int(PARAM_R), float(PARAM_D), float(PARAM_T), float(PARAM_H))            
    




#######################################################################################



#########################################################################################
#TOOL TO WRITE ONTO DATABASE
def databaseWrite(f_destination, parameters):

    (PARAM_R, PARAM_D, PARAM_T, PARAM_H) = parameters
    db = open(f_destination, "a")
    local_str = "R" + str(PARAM_R) + " D" + str(PARAM_D) + " T" + str(PARAM_T) + " H" + str(PARAM_H) + "\n"
    db.write(local_str)
    db.close()
    
    
    
    
def convert(_v, in_min, in_max, out_min, out_max) :
  return (_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
