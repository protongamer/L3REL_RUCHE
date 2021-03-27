####################################################
#Here is the "const" core values that we must not change, or some of them maybe




########################
#ROUTINES PARAMETERS

#skip boot sequence ?
SKIP_BOOT_SEQUENCE = True 
#How much connected hives you want for your network ?
MAX_HIVE = 5 


########################



#######################
#WAN NETWORK

SERVER_ADRESS = 0


MAIN_ROOM = 0
SETUP_ROOM = 1

    
    
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
            index_line[index_chr] == "9" or index_line[index_chr] == "."):
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
    return (int(PARAM_R), float(PARAM_D), float(PARAM_T), int(PARAM_H))            
    




#######################################################################################



#########################################################################################
#TOOL TO WRITE ONTO DATABASE
def databaseWrite(f_destination, parameters):

    (PARAM_R, PARAM_D, PARAM_T, PARAM_H) = parameters
    db = open(f_destination, "a")
    local_str = "R" + str(PARAM_R) + " D" + str(PARAM_D) + " T" + str(PARAM_T) + " H" + str(PARAM_H) + "\n"
    db.write(local_str)