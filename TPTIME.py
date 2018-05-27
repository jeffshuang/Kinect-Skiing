#TP TIME
#Jeffrey Huang
#jshuang

#hi youngchk the 112 ta :)


from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math
import random
import time
import pyaudio

from Coin import Coin
from Rock import Rock
from Snow import Snow
from KosbieHead import Kosbie


#from Microsfot PyKinectBodyGameDemo
SKELETON_COLORS =[pygame.color.THECOLORS["white"], 
                  pygame.color.THECOLORS["white"], 
                  pygame.color.THECOLORS["white"], 
                  pygame.color.THECOLORS["white"], 
                  pygame.color.THECOLORS["white"], 
                  pygame.color.THECOLORS["white"], 
                  pygame.color.THECOLORS["white"]]

#ensures that all skeletons are white




def distanceFormula(x1,y1,x2,y2):
    #finds distance
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return d

def isInCircle(x1,y1,r,x2,y2):
    #sees if point is in given circle
    d=distanceFormula(x1,y1,x2,y2)
    if d<=r:
        return True
    else:
        return False 

def findLineAngle(x1,y1,x2,y2,x3,y3):
        #pt 1 to 2 is hyptoneuse
        #pt 1 to 3 is other side
        s=distanceFormula(x1,y1,x3,y3)
        h=distanceFormula(x1,y1,x2,y2)
        angle=math.asin(s/h)
        return angle
    
class GameRunTime(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.scorefont = pygame.font.SysFont("Montserrat",40)
        self.gameoverfont = pygame.font.SysFont("Montserrat", 120)
        self.otherfont= pygame.font.SysFont("Montserrat",100)
        self.screen_width = 1920
        self.screen_height = 1080
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((960,540), 
                       pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        self._done = False
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | 
                                  PyKinectV2.FrameSourceTypes_Body)
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, 
                              self._kinect.color_frame_desc.Height), 0, 32)
        self._bodies = None
        
       
        self.bodylocation=0
        self.lowerbody=0
        self.previousbody=0

        self.left_hand=(0,0)
        self.right_hand=(1000,1000)
        self.left_leg=0
        self.right_leg=0
        self.prevleftleg=0
        self.prevrightleg=0
        self.head=0
     
        self.splashScreen=True
      
        self.isJumping=False
        self.isFalling=False

        self.isGameOver=False

        self.isPaused=False
        
        self.score=0

        self.skyr=135
        self.skyg=206
        self.skyb=202
        
     
        self.coins=pygame.sprite.Group()
        self.rocks=pygame.sprite.Group()
        self.snow=pygame.sprite.Group()
        self.trees=pygame.sprite.Group()
        self.kosbie=pygame.sprite.Group()
        
        self.time=0
        self.originaltime=time.time()
        self.skier_x=self.screen_width//2
        self.skier_y=800

      
        self.jump=0

        self.coinsound=pygame.mixer.Sound("sounds/coin.wav") 
        self.coinsound.set_volume(.5)
        #audio from themushroomkingdom.com
        self.applause=pygame.mixer.Sound("sounds/applause3.wav") 
        self.applause.set_volume(1.0)
        #audio from wavsource.com
            
     
        self.curve=0
        self.previouscurve=0

        self.curve1=0
        self.curve2=0
        self.curve3=0
        self.curve4=0


        self.ofset=0
        self.curveoffset=0

        self.curvevalues=[0,60,120,-60,-120]
   
        self.up_path_left=0
        self.up_path_right=0
        self.bot_path_left=200
        self.bot_path_right=1720

        self.highscore=0

        self.tilting=0

        self.colorIncreasing=True

        self.isYoungchk=-1
        self.rightelbow=0

        self.lives=3
        self.loselife=False
 
    def curveIn(self):
        #going more curved
        #sign negative or positive
        self.curve1+=3
        self.curve2+=3
        self.curve3+=3
        self.curve4+=3
        
        

    def curveOut(self):
        self.curve1-=3
        self.curve2-=3
        self.curve3-=3
        self.curve4-=3
        
        
     
    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        #from PyKinectBodyGame demo
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) 
            or (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred)
                 and (joint1State == PyKinectV2.TrackingState_Inferred)):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass
    
    def draw_body(self, joints, jointPoints, color):
        #from PyKinectBodyGame demo

        #KosbieHead
        #self._frame_surface.blit(
         #       pygame.image.load('images/kosbiesprite.jpg').convert_alpha(), 
          #          [jointPoints[PyKinectV2.JointType_Head].x-100,
           #             jointPoints[PyKinectV2.JointType_Head].y-300])


        # Torso
        self.draw_body_bone(joints, jointPoints, color,
                    PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, 
                    PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, 
                    PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, 
                    PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, 
                    PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, 
                    PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, 
                    PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, 
                    PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, 
                     PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

    def draw_color_frame(self, frame, target_surface):
        #from PyKinectBodyGame demo
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def draw_background(self):
        #self._frame_surface.fill([240,255,240])
        self._frame_surface.fill([211,211,211])
  
    def draw_sky(self):
         pygame.draw.polygon(self._frame_surface, [self.skyr,self.skyg,self.skyb], 
            [[0,0],[0,300],[self.screen_width,300],[self.screen_width,0]], 0)
         

         """
         #debugging purposes
         pygame.draw.circle(self._frame_surface, [0,0,0], [200,1080-10],10,0)
         pygame.draw.circle(self._frame_surface, [0,0,0], [1720,1080-10],10,0)
         pygame.draw.circle(self._frame_surface, [0,0,0], [800,300],10,0)
         pygame.draw.circle(self._frame_surface, [0,0,0], [1120,300],10,0)
         """

    def draw_mountains(self):
       pygame.draw.polygon(self._frame_surface, (99,99,99), 
              [(125+self.ofset,300),(425+self.ofset,50),(725+self.ofset,300)]) 
       pygame.draw.polygon(self._frame_surface, (112,112,112), 
               [(0+self.ofset,300),(150+self.ofset,100),(300+self.ofset,300)])
       
       pygame.draw.polygon(self._frame_surface, (99,99,99), 
               [(1400+self.ofset,300),(1600+self.ofset,200),(1800+self.ofset,300)])
       pygame.draw.polygon(self._frame_surface, (112,112,112), 
               [(1000+self.ofset,300),(1250+self.ofset,100),(1500+self.ofset,300)])

       pygame.draw.polygon(self._frame_surface, (122,122,122), 
               [(2100+self.ofset,300),(2400+self.ofset,150),(2700+self.ofset,300)])
       pygame.draw.polygon(self._frame_surface, (99,99,99), 
               [(2000+self.ofset,300),(2150+self.ofset,200),(2300+self.ofset,300)])

       pygame.draw.polygon(self._frame_surface, (112,112,112), 
              [(-500+self.ofset,300),(-400+self.ofset,200),(-300+self.ofset,300)])
       pass

    def draw_person(self):
       if self.isYoungchk==-1:
            pygame.draw.circle(self._frame_surface, [0,0,0], 
           [self.skier_x+self.tilting, int(self.skier_y-self.jump)],100, 0)

       if self.isYoungchk==1:
           youngchk = pygame.image.load("images/youngchk.png") 
           #image from David Diao edited by Vicky Ye
           youngchk =  pygame.transform.scale(youngchk
                              , (200,200));
           self._frame_surface.blit(youngchk, [self.skier_x-90+self.tilting, 
                 int(self.skier_y-self.jump)-100])

       pygame.draw.circle(self._frame_surface, [0,0,0], 
                          [self.skier_x, int(self.skier_y+350-self.jump)],200,0)
    
    def draw_hands(self,x1,y1,x2,y2):
        handimageleft=pygame.image.load('images/hand.png')
        width,height=handimageleft.get_size()
        handimageleft=pygame.transform.scale(handimageleft, (int(width * .5), 
                                                             int(height * .5)))
        handimageright=pygame.transform.flip(handimageleft,True,False)

        handimageleft=handimageleft.convert_alpha()
        handimageright=handimageright.convert_alpha()
        try:
            self._frame_surface.blit(handimageleft, [x1,y1])
            self._frame_surface.blit(handimageright, [x2,y2])
        except:
            pass

    def draw_lives(self):
        heart=pygame.image.load('images/heart.png')
        #image from scratch.mit.edu
        heart=pygame.transform.scale(heart, (50,50))
        if self.lives>0:
            self._frame_surface.blit(heart, [50,50])
        if self.lives>1:
            self._frame_surface.blit(heart, [150,50])
        if self.lives>2:
            self._frame_surface.blit(heart, [250,50])


    def draw_path(self):
        
       
        pygame.draw.polygon(self._frame_surface, [255,250,239], 
            [[520+self.curve1+self.ofset+self.curveoffset,664],
             [1400+self.curve1+self.ofset+self.curveoffset,664],
             [1720+self.ofset+self.curveoffset,1080],
             [200+self.ofset+self.curveoffset,1080]], 0)
   

        pygame.draw.polygon(self._frame_surface, [255,250,239], 
            [[680+2*self.curve2+self.ofset+self.curveoffset,456],
             [1240+2*self.curve2+self.ofset+self.curveoffset,456],
             [1400+self.curve1+self.ofset+self.curveoffset,664],
             [520+self.curve1+self.ofset+self.curveoffset,664]], 0)

        pygame.draw.polygon(self._frame_surface, [255,250,239], 
            [[760+3*self.curve3+self.ofset+self.curveoffset,352],
             [1160+3*self.curve3+self.ofset+self.curveoffset,352],
             [1240+2*self.curve2+self.ofset+self.curveoffset, 456],
             [680+2*self.curve2+self.ofset+self.curveoffset,456]], 0)
        
        pygame.draw.polygon(self._frame_surface, [255,250,239], 
            [[800+4*self.curve4+self.ofset+self.curveoffset,300],
             [1120+4*self.curve4+self.ofset+self.curveoffset,300],[
                 1160+3*self.curve3+self.ofset+self.curveoffset, 352],
             [760+3*self.curve3+self.ofset+self.curveoffset,352]], 0)
        
     
    def draw_score(self):
        self._frame_surface.blit(self.scorefont.render("Score: %s" % str(self.score)
                      , True, (0,0,0)), (self.screen_width/4*3+200, 50))
        self._frame_surface.blit(self.scorefont.render("Highscore: %s" % str(self.highscore)
                      , True, (0,0,0)), (self.screen_width/4*3+200, 150))

    def draw_time(self):
        self._frame_surface.blit(self.scorefont.render("Time: %s" % str(self.time)
                      , True, (0,0,0)), (self.screen_width/4*3+200, 100))


    def getHighScore(self):
        try:
            file=open("highscores.txt","r")
            highscore=int(file.read())
            file.close
        except:
            print("FJALJAL")
        self.highscore=highscore

    def saveHighScore(self,score):
        try:
            file = open("highscores.txt", "w")
            file.write(str(score))
            file.close()
        except :
            print("FJDLAJLAJLAJLDJ")
    

    

    def run(self):
        #modified Framework from PyKinectBodyGame demo (Microsoft)
        # -------- Main Program Loop -----------

        
        pygame.mixer.music.load('sounds/Shelter.ogg')
            #music from Porter Robinson Soundcloud
        pygame.mixer.music.play(-1)
      
        while not self._done:
            # --- Main event loop
            
            
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                          pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                
              
            
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            if self.splashScreen==True:
                #frame = self._kinect.get_last_color_frame()
                #self.draw_color_frame(frame, self._frame_surface)
                background = pygame.image.load("images/CreditsToVickyYe.png")
                 #image editing credit to vicky ye
                #original image from upscaletravel.com

               
                self._frame_surface.blit(background, [0,0])
                self._frame_surface.blit(self.gameoverfont.render("LETS PLAY" 
                      , True, (255,255,255)), (self.screen_width//2-800, 50))
                self._frame_surface.blit(self.scorefont.render
                                         ("STEP IN FRONT AND CLAP TO START GAME"
                      , True, (255,255,255)), (self.screen_width//2-800, 150))

              
                self.snow.add(Snow())
                self.snow.update(self.screen_width,self.screen_height)
                self.snow.draw(self._frame_surface)
                


            

            if self.splashScreen==False:
                #Draw Graphics
                
                if float(self.time)==0:
                    self.originaltime=time.time()
                
                self.draw_background() 
                self.getHighScore()
                self.draw_path()  

                #updates path coordinates after drawing it
                self.up_path_left=800+4*self.curve4+self.ofset+self.curveoffset
                self.up_path_right=1120+4*self.curve4+self.ofset+self.curveoffset
                self.bot_path_left=200+self.curve1+self.ofset+self.curveoffset
                self.bot_path_right=1720+self.curve1+self.ofset+self.curveoffset 
                
                self.draw_sky()
                self.draw_mountains()
                self.draw_score()
                self.draw_lives()
                self.draw_time()
             
                    #displays in
                if float(self.time)<5:
                    self._frame_surface.blit(self.scorefont.render
                           ("SQUAT AND COLLECT COINS, STAND TO JUMP OVER OBSTACLES" 
                          , True, (0,0,0)), (self.screen_width//2-500, 50))
                    self._frame_surface.blit(self.scorefont.render
                                 ("PUT HANDS ON HEAD TO PAUSE" 
                          , True, (0,0,0)), (self.screen_width//2-300, 150))
                    self._frame_surface.blit(self.scorefont.render
                            ("YOU HAVE 3 LIVES BUT IF YOU GO OFF THE PATH YOU LOSE THEM ALL" 
                          , True, (0,0,0)), (self.screen_width//2-550, 250))
                    

                if 6>float(self.time)>5:
                    
                        self._frame_surface.blit(self.gameoverfont.render
                                             ("GOOD LUCK!" 
                          , True, (0,0,0)), (self.screen_width//2-250, 300))
                  
          
                self.time="{0:.2f}".format(time.time()-self.originaltime)
              
                #increase speed as game progresses
                for coin in self.coins:
                    coin.updateVelocity(0,.01)
                
                for rock in self.rocks:
                    rock.updateVelocity(0,.01)

                #changs color of the sky
                if self.skyb==255:
                    self.colorIncreasing=False
                if self.skyb==220:
                    self.colorIncreasing=True

                if self.colorIncreasing==False:
                    self.skyb-=.25
                    self.skyr-=.25
                if self.colorIncreasing==True:  
                    self.skyb+=.25
                    self.skyr+=.25
                
                    #sprites are generated by producing a random number
                #if 0 produce sprite
                #range of random number indicates frequency

                x=random.randint(0,40)
                if x==0 and len(self.rocks)<1:
                    r=Rock(self.up_path_left+250,self.up_path_right+50)
                    self.rocks.add(r)
                self.rocks.update(self.screen_width,self.screen_height)
                self.rocks.draw(self._frame_surface)

               

                n=random.randint(0,20)
                if n==0:
                    c=Coin(self.up_path_left+150,self.up_path_right)
                    self.coins.add(c)
                    #print(self.coins)
                    #print(n)
                self.coins.update(self.screen_width,self.screen_height)
                self.coins.draw(self._frame_surface)

                self.snow.add(Snow())
                self.snow.update(self.screen_width,self.screen_height)
                self.snow.draw(self._frame_surface)
                
                z=random.randint(0,500)
                if z==0:
                    k=Kosbie(self.up_path_left+150,self.up_path_right)
                    self.kosbie.add(k)
                   
                self.kosbie.update(self.screen_width,self.screen_height)
                self.kosbie.draw(self._frame_surface)
                
                
                if float(self.time)>9 and float(self.time)%5<0.075 and self.isPaused==False:
                   i=random.randint(0,4)
                   self.previouscurve=self.curve
                   self.curve=self.curvevalues[i]
                   
                   #print(self.curve)
                if abs(self.curve1-self.curve)>4 and abs(self.curve4-self.curve)>4:
                    if self.curve>self.curve1:
                        if self.curve1!=self.curve:
                            self.curveIn()


                    if self.curve<self.curve1:
                        if self.curve1!=self.curve:
                            self.curveOut()
                        
                #curve offset is the offset from curving
                if self.curve==120:
                    self.curveoffset+=10
                if self.curve==60:
                    self.curveoffset+=5
                if self.curve==-60:
                    self.curveoffset-=5
                if self.curve==-120:
                    self.curveoffset-=10
                    

               #adjust sprite location based on curve
                if self.curve==60 and self.curveoffset!=0:
                    for coin in self.coins:
                          coin.updatePosition(4,0)
                    for rock in self.rocks:
                          rock.updatePosition(4,0)

                if self.curve==-60 and self.curveoffset!=0:
                    for coin in self.coins:
                          coin.updatePosition(-4,0)
                    for rock in self.rocks:
                          rock.updatePosition(-4,0)

                if self.curve==120 and self.curveoffset!=0:
                    for coin in self.coins:
                          coin.updatePosition(8,0)
                    for rock in self.rocks:
                          rock.updatePosition(8,0)

                if self.curve==-120 and self.curveoffset!=0:
                    for coin in self.coins:
                          coin.updatePosition(-8,0)
                    for rock in self.rocks:
                          rock.updatePosition(-8,0)
                                    
                self.draw_person()
          
            # Get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            #print(self._bodies)
            #print(self._kinect.max_body_count)
            # --- draw skeletons to _frame_surface
            if self._bodies is not None: 
                
                for i in range(0, self._kinect.max_body_count): 
                   #TEST LATER
             
                    body = self._bodies.bodies[i] 

                    if (body.is_tracked and isInCircle(self.left_hand[0], 
                                self.left_hand[1], 100, self.right_hand[0],self.right_hand[1])):
                       self.splashScreen=False

    
                    if not body.is_tracked: 
                        continue
                    
                    joints = body.joints 
                    # ---convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    if self.splashScreen==True:
                        self.draw_body(joints, joint_points, SKELETON_COLORS[i]) 
                        #temp for testing purpose
                  
                    #moving hand logic
                    #finds colorspace point of each hand
                    if (joints[PyKinectV2.JointType_HandLeft].TrackingState 
                        != PyKinectV2.TrackingState_NotTracked):
                        self.left_hand=(joint_points[PyKinectV2.JointType_HandLeft].x,
                        joint_points[PyKinectV2.JointType_HandLeft].y)
                       # print(self.left_hand)
                        pass
                    if (joints[PyKinectV2.JointType_HandRight].TrackingState 
                        != PyKinectV2.TrackingState_NotTracked):
                        self.right_hand=(joint_points[PyKinectV2.JointType_HandRight].x,
                        joint_points[PyKinectV2.JointType_HandRight].y)
                       # print("righthand:" + str(self.right_hand))

                    self.draw_hands(self.left_hand[0],self.left_hand[1]
                                    ,self.right_hand[0],self.right_hand[1])
               
                    for kosbie in self.kosbie:
                        try:
                           
                            if (kosbie.rect.collidepoint(self.left_hand) 
                                and self.isJumping==False and coin.rect.y>500): 
                                kosbie.kill()
                                self.score+=10
                                if self.lives<3:
                                    self.lives+=1
                                #self.coinsound.play()  
                            elif (kosbie.rect.collidepoint(self.right_hand) 
                                  and self.isJumping==False and coin.rect.y>500): 
                                kosbie.kill()
                                self.score+=10
                                if self.lives<3:
                                    self.lives+=1
                                self.coinsound.play()  
                            
                        except:
                            pass

                    for coin in self.coins:
                        try:
                            #print(coin.rect)
                            if (coin.rect.collidepoint(self.left_hand) 
                                and self.isJumping==False and coin.rect.y>500): 
                                coin.kill()
                                self.score+=1
                                self.coinsound.play()  
                             

                            elif (coin.rect.collidepoint(self.right_hand) 
                                  and self.isJumping==False and coin.rect.y>500): 
                                coin.kill()
                                self.score+=1
                                self.coinsound.play()  
                            
                        except:
                            pass

                    if self.score>self.highscore:
                        self.highscore=self.score
                        self.saveHighScore(self.highscore)
            


                   
                    #jumping logic
                    #tests if is jumping
                    if (joints[PyKinectV2.JointType_HipLeft].TrackingState 
                        != PyKinectV2.TrackingState_NotTracked):
                            self.prevleftleg=self.left_leg
                            self.left_leg=joints[PyKinectV2.JointType_HipLeft].Position.y
                            #print("leftleg:"+ str(self.left_leg))
                    if (joints[PyKinectV2.JointType_HipRight].TrackingState 
                        != PyKinectV2.TrackingState_NotTracked):
                            self.prevrightleg=self.right_leg
                            self.right_leg=joints[PyKinectV2.JointType_HipRight].Position.y
                            #print("BLAH",self.right_leg)
              
                    self.jump-=10
                    if self.jump<0:
                        self.jump=0

                    if self.left_leg >-.5 and self.right_leg >-.5:
                        #y coordinate of the each hip
                        #checks to make sure you are not standing up
                        #print("JUMP MAN")
                        self.isJumping=True
                   
                    #else: 
                     #   self.isJumping=False
                    #print(self.isJumping)

                    if self.isJumping==True and self.isFalling==False:
                            self.jump+=100
                            if self.jump>200:
                                self.isFalling=True
                                self.jump=200

                    if self.jump==0:
                        self.isJumping=False
                        self.isFalling=False

                    #tilting logic               
                    if (joints[PyKinectV2.JointType_SpineShoulder
                               ].TrackingState 
                        != PyKinectV2.TrackingState_NotTracked and 
                        joints[PyKinectV2.JointType_SpineMid
                               ].TrackingState 
                        != PyKinectV2.TrackingState_NotTracked):
                        self.lowerbody=joints[PyKinectV2.JointType_SpineMid].Position.x
                        self.previousbody=self.bodylocation
                        self.bodylocation=joints[PyKinectV2.JointType_SpineShoulder].Position.x

                    if (self.bodylocation-self.lowerbody)>.025 and self.previousbody>0:
                       
                        self.ofset-=15
                        if self.tilting<50:
                            self.tilting+=10
                            
                        for coin in self.coins:
                            coin.updatePosition(-5,0)
                          
                        for rock in self.rocks:
                            rock.updatePosition(-5,0)
                          
                        
                    elif (self.bodylocation-self.lowerbody)<-.025 and self.previousbody<0:
                       
                        self.ofset+=15
                        if self.tilting>-50:
                            self.tilting-=10
                        for coin in self.coins:
                            coin.updatePosition(5,0)
                           
                        for rock in self.rocks:
                            rock.updatePosition(5,0)
                          

                    else:
                        if self.tilting<0 and self.tilting!=0:
                            self.tilting+=10
                        if self.tilting>0 and self.tilting!=0:
                            self.tilting-=10
                        
                  

                    for rock in self.rocks:
                        #print(rock.rect.centery)
                        #print(abs(rock.rect.centerx-self.skier_x))
                        try:
                            #checks if rock is at bottom and if colliding when not jumping
                            if (rock.rect.centery>1050 and 
                                rock.rect.collidepoint(self.skier_x,self.skier_y+100) and self.isJumping==False):
                                 #self.isGameOver=True
                                 self.loselife=True
                                 rock.kill()
                                
                        except:
                            pass

                    #checks to make sure player is still in path'
                    #print(200+self.ofset)
                    #print(self.bot_path_left,self.bot_path_right)
                    if not self.bot_path_left<self.skier_x<self.bot_path_right:
                        #self.isGameOver=True
                        self.loselife=True
                        

                    if self.loselife==True:
                        self.lives-=1
                        self.loselife=False
                    if self.lives==0:
                        self.isGameOver=True

                    #tracks
                    if (joints[PyKinectV2.JointType_Head].TrackingState 
                        != PyKinectV2.TrackingState_NotTracked):
                        self.head=(joint_points[PyKinectV2.JointType_Head].x,
                        joint_points[PyKinectV2.JointType_Head].y)


                    if (joints[PyKinectV2.JointType_ElbowRight].TrackingState 
                        != PyKinectV2.TrackingState_NotTracked):
                        self.elbow=(joint_points[PyKinectV2.JointType_ElbowRight].x,
                        joint_points[PyKinectV2.JointType_ElbowRight].y)

                    #checks if dabbing
                    #if dabbing switch face of skier

                    if (isInCircle(self.head[0],self.head[1],150,
                                   self.elbow[0],self.elbow[1])):
                        self.isYoungchk*=-1 
                                   

                    if (isInCircle(self.head[0],self.head[1],100,
                                   self.left_hand[0],self.left_hand[1]) 
                                   and isInCircle(self.head[0],
                                    self.head[1],100,self.right_hand[0],self.right_hand[1])):
                        self.isPaused=True
                    else:
                        self.isPaused=False

                    
                    if self.isPaused==True:
                        self._frame_surface.fill([255,255,255])
                        background = pygame.image.load("images/doggo.jpg") 
                        #image fromhttp://drivethrutv.com/project/subaru-dogs-skiing/
                        #background =  pygame.transform.scale(background
                         # , (self.screen_width,self.screen_height));
                        self._frame_surface.blit(background, [0,0])
                        self._frame_surface.blit(self.otherfont.render("PAUSED", 
                                  True, (112,112,112)),
                                  (self.screen_width//2-800, self.screen_height//2))
                        self._frame_surface.blit(self.otherfont.render
                                  ("USE YOUR HANDS TO COLLECT COINS", 
                                  True, (112,112,112)), 
                                  (self.screen_width//2-800, self.screen_height//2+200))
                        self._frame_surface.blit(self.otherfont.render
                                  ("TILT AND JUMP", 
                                  True, (112,112,112)), 
                                 (self.screen_width//2-800, self.screen_height//2+300))
                        self._frame_surface.blit(self.otherfont.render
                                  ("TO STAY ON PATH AND AVOID OBSTACLES", 
                                  True, (112,112,112)), 
                                 (self.screen_width//2-800, self.screen_height//2+400))
                        self.isJumping=True


                        
            if self._bodies==None:
                self.isPaused=True

                    #game over conditions
            if self.isGameOver==True:
                self.applause.play()
                self._frame_surface.fill([255,255,255])
                background = pygame.image.load("images/lmao.jpg") 
                background =  pygame.transform.scale(background
                          , (self.screen_width,self.screen_height));
                self._frame_surface.blit(background, [0,0])

                self._frame_surface.blit(self.otherfont.render("GAME OVER :(", 
                                  True, (0,0,0)), 
                                         (self.screen_width//2-850, self.screen_height//2-100))
                self._frame_surface.blit(self.otherfont.render("CLAP TO RESTART", 
                                  True, (0,0,0)), 
                                         (self.screen_width//2-850, self.screen_height//2+300))
                if self.highscore==self.score:
                    self._frame_surface.blit(self.otherfont.render("NEW HIGH SCORE: %s" % self.highscore , 
                                  True, (0,0,0)), 
                                         (self.screen_width//2-850, self.screen_height//2+100))
                else:
                    self._frame_surface.blit(self.otherfont.render("HIGH SCORE: %s" % self.highscore, 
                                  True, (0,0,0)), 
                                         (self.screen_width//2-850, self.screen_height//2+100))
                  
                        
               
            for event in pygame.event.get():
                        #if event.type == pygame.MOUSEBUTTONDOWN:
                         #   self.isJumping=True
                          #  print('JUMPING BOI')
                        #else:
                         #   self.isJumping=False
                        if event.type == pygame.KEYUP:
                            self.__init__()
                            self.time=0
            if self.isGameOver==True and isInCircle(self.left_hand[0], 
                        self.left_hand[1], 100, self.right_hand[0],self.right_hand[1]):
                        self.__init__()
                        self.time=0
    
          
            #copy back buffer surface pixels to the screen, resize it if 
             #needed and keep aspect ratio
    #(screen size may be different from Kinect's color frame size) 
            h_to_w = (float(self._frame_surface.get_height()) 
                      / self._frame_surface.get_width())
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface
                           , (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()

averyfungame = GameRunTime()

averyfungame.run()

