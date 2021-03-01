import pygame, time, os
from pygame.locals import *


    
    






#mouse Pos.
mX = 0
mY = 0


loop = True

#PATH = 'C:/Users/gordon/Documents/python/ruche/'

pygame.init()

print("Gimli Says NO !")

time.sleep(1)

for x in range(6):
    print(x)

#init screen
screen = pygame.display.set_mode([720,480])

#Load all of my pics
temp = pygame.image.load('pic/heat.bmp')
hum = pygame.image.load('pic/hum.bmp')
but1 = pygame.image.load('pic/exit.bmp')



while loop == True:
    
    screen.blit(temp, (0,0))
    screen.blit(hum, (0,103))
    screen.blit(but1, (640,20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    
    if (pygame.mouse.get_pressed() == (True,False,False)):
        (mX, mY) = pygame.mouse.get_pos()
        if (mX > 640 and mX < 665 and mY > 20 and mY < 45):
            loop = False
        
        print((mX, mY))
        
    time.sleep(0.015)

    
    pygame.display.flip()







#if end loop, then exit
time.sleep(2)
exit()




#Functions






