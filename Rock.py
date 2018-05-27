import pygame
import random
import math


#Implements Rock class

class Rock(pygame.sprite.Sprite):
  
    def __init__(self,left,right,x_velocity=0):
        
        super().__init__()
        self.x=random.randint(left,right)
        self.y=500
        self.factor=.5
        self.radius=350
        self.yspeed=random.randint(8,12)
        n=random.randint(0,2)
        if n==0:
            self.xspeed=1
        if n==1:
            self.xspeed=-1
        if n==2:
            self.xspeed=1
        self.image=pygame.image.load('images/rock.png')
        #image from clubpenguin.wikia.com
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
        self.image=pygame.transform.scale(self.imagecopy,
               (int(self.width * self.factor), int(self.height * self.factor)))

    def update(self, screenWidth, screenHeight):
        self.x += self.xspeed
        self.y += self.yspeed
        self.factor+=.0075
        if self.y>screenHeight+100:
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




