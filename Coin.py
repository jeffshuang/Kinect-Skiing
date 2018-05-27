#implements Coin class

import pygame
import math
import random

class Coin(pygame.sprite.Sprite):

    def __init__(self, left,right, x_velocity=0):
        super().__init__()
        self.factor=.5
        self.x=random.randint(left,right)
        self.y=350
        self.radius=250
        self.yspeed=20
        n=random.randint(0,1)
        if self.x<1020:
            self.xspeed=-6
        elif self.x>1070:
            self.xspeed=6
        else:
            self.xspeed=0
       # if n==0:
        #    self.xspeed=6
        #if n==1:
         #   self.xspeed=-6
        self.image=pygame.image.load('images/coin.png')
        #image from wii.wikia.com
        self.imagecopy=self.image.copy()
        self.width,self.height=self.image.get_size()
        self.image=pygame.transform.scale(self.imagecopy, 
                (int(self.width * self.factor), int(self.height * self.factor)))
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

        #check this
        self.image=self.image.convert_alpha()


    #from PyGame Dots Demo (Lukas Peraza)
    def getRect(self):  
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)
        self.image=pygame.transform.scale(self.imagecopy, (int(self.width * self.factor), int(self.height * self.factor)))

    def update(self, screenWidth, screenHeight):
        self.x += self.xspeed
        self.y += self.yspeed
        self.factor+=.01
        #self.radius=self.factor*150
        self.radius+=1
        if self.y>screenHeight+200:
            self.kill()
        self.getRect()

    def updatePosition(self,x,y):
        self.x+=x
        self.y+=y
        self.getRect()

    def updateVelocity(self,x,y):
        self.xspeed+=x
        self.yspeed+=y
        self.getRect()

       

  
    




