import pygame, time


x = 0

pygame.init()

screen = pygame.display.set_mode([100,100])
screen.fill((0,50,0))
print("Hellooooooooooooo")

loop = True

while loop==True:

    pygame.draw.circle(screen, (255,0,0),(x,50),10)
    pygame.display.update()
    x = x + 1

    if(x > 75):
    	loop = False

    time.sleep(0.015)