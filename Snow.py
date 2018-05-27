#framework from Dots Demo (Lukas Peraza)
#implements Snow Class

import pygame
import random
import math

class Snow(pygame.sprite.Sprite):
    def __init__(self):
        super(Snow, self).__init__()
        self.radius = random.randint(3,5)
        self.x= random.randint(0, 1920)
        self.y=0
        self.xSpeed = 0
        self.ySpeed = 10
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)  # make it transparent
        self.image = self.image.convert_alpha()
        
        pygame.draw.circle(self.image, (255,250,250),
                           (self.radius, self.radius), self.radius)

    #from Dots Demo
    def getRect(self):  #
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def update(self, screenWidth, screenHeight):
        self.x += self.xSpeed
        self.y += self.ySpeed
        
        if self.x < 0:
            self.x = screenWidth
        elif self.x > screenWidth:
            self. x = 0
        if self.y < 0:
            self.y = screenHeight
        elif self.y > screenHeight:
            self.y = 0
       
        self.getRect()