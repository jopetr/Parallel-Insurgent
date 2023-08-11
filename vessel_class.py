import pygame
import math
from random import random
from shell_class import Shell

class Vessel:
    
    '''
    Private
    Loads images for character from path
    '''
    def __load_components(self):
        path = "vessel/"
        raw_ims = []
        raw_ims.append(pygame.image.load(path+"body.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"engine.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"flame.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"cannon.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"shot_blast.png").convert_alpha())
        self.raw_ims = raw_ims
    
    '''
    Private
    Calculates (x, y) position of a child object from it's parent to facilitate dependent objects
    '''
    def __child_pos(self, parent_pos, parent_angle, distance):
        x, y = parent_pos
        angle = 360-1*parent_angle+90
        child_x = distance*math.cos(2*math.pi*angle/360) + x
        child_y = distance*math.sin(2*math.pi*angle/360) + y
        child_pos = (child_x, child_y)
        return child_pos

    '''
    Updates rects and ims to correspond to scale, position, and all angles
    '''
    def step(self, opponent_center, opponent_width):
        width = 1440
        height = 800
        val = self.t
        x = width*0.9
        y = 0.1*height
        angle = -15
        waves = 2
        uval = -1
        if val<0.5:
            x += (0.5 - val)*520
            angle-=(1 - val/0.5)*30
            self.shell_val = 0
        elif val<(waves*2+0.5):
            v = (val-0.5)%2
            if v<1:
                y+=0.4*height*(v)
                self.shell_val = self.shell_val%5
                uval = -1
                if self.shell_val<=1:
                    uval = self.shell_val
                self.shell_val += 0.08
            else:
                y+=0.4*height*(2 - v)
                self.shell_val = self.shell_val%5
                uval = -1
                if self.shell_val<=1:
                    uval = self.shell_val
                self.shell_val += 0.08
        else:
            x -= (waves*2+0.5 - val)*520
            angle-=((val - waves*2 - 0.5)/0.5)*30
            
        
        self.update(250, (x,y), uval, opponent_center, opponent_width, angle)
        self.t+=0.004
        if self.t>(waves*2+1):
            self.done = True

    '''
    Updates rects and ims to correspond to scale, position, and all angles
    '''
    def over_step(self, opponent_center, opponent_width):
        self.game_over = True
        width = 1440
        height = 800
        val = self.t
        if self.t_end >=1:
            self.t_end = 1
        else:
            self.t_end += 0.01
        x = width*0.9 + 520*self.t_end
        y = 0.1*height
        angle = -15
        waves = 2
        uval = -1
        if val<0.5:
            x += (0.5 - val)*520
            angle-=(1 - val/0.5)*30
            self.shell_val = 0
        elif val<(waves*2+0.5):
            v = (val-0.5)%2
            if v<1:
                y+=0.4*height*(v)
                self.shell_val = self.shell_val%5
                uval = -1
                if self.shell_val<=1:
                    uval = self.shell_val
                self.shell_val += 0.08
            else:
                y+=0.4*height*(2 - v)
                self.shell_val = self.shell_val%5
                uval = -1
                if self.shell_val<=1:
                    uval = self.shell_val
                self.shell_val += 0.08
        else:
            x -= (waves*2+0.5 - val)*520
            angle-=((val - waves*2 - 0.5)/0.5)*30
            
        
        self.update(250, (x,y), uval, opponent_center, opponent_width, angle)
        self.t+=0.004
        if self.t>(waves*2+1):
            self.done = True

    def update(self, scale, pos, val, opponent_center, opponent_width, angle):
        
        x, y = pos
        #-25
        ims, rects = self.__update_engines(scale*0.3, (x, y+scale*0.1), angle)


        
        

        im, rect = self.__update_cannon(scale, (x-scale*0.13, y-scale*0.1), val)
        if self.game_over:
            im, rect = self.__update_cannon(scale, (x-scale*0.13, y-scale*0.1), -1)
        ims.append(im[0])
        rects.append(rect[0])
        if val!=-1 and not self.game_over:
            ims.append(im[1])
            rects.append(rect[1])
        else:
            self.shell_shot = False

        self.__update_shells(opponent_center, opponent_width, scale)

        im = pygame.transform.scale(self.raw_ims[0], (scale, scale))
        rect = im.get_rect()
        rect.center = (x, y)
        ims.append(im)
        rects.append(rect)
        
        
        self.rects = rects
        self.ims = ims

    def __update_shells(self, opponent_center, opponent_width, scale):
        
        for shell_and_val in self.shells:
            shell = shell_and_val[0]
            val = shell_and_val[1]
            if shell.hit:
                #im = test_box_g
                if val == -1:
                    val = 0
                    self.hit = True
                else:
                    val+=0.5
                    if val <= 13:
                        shell.hit_update(scale/8, val)
                shell_and_val[1] = val
            else:
                #im = test_box_r
                shell.update(scale/8, 13, opponent_center, opponent_width, val)
        
        
    
    def __update_engines(self, scale, pos, angle):
        x, y = pos
        ims = []
        rects = []

        # Flame 0

        x -= 0.67*scale
        flame_width = scale*0.8*(1+0.1*random())
        flame_length = flame_width*0.8
        im = pygame.transform.scale(self.raw_ims[2], (flame_width, flame_length))
        im = pygame.transform.rotate(im, angle)
        rect = im.get_rect()
        rect.center = self.__child_pos((x, y), angle, 0.6*scale)
        
        ims.append(im)
        rects.append(rect)

        # Engine 0

        im = pygame.transform.scale(self.raw_ims[1], (scale, scale))
        im = pygame.transform.rotate(im, angle)
        rect = im.get_rect()
        rect.center = (x, y)
        ims.append(im)
        rects.append(rect)

        # Flame 1

        x += 1.27*scale
        flame_width = scale*0.8*(1+0.1*random())
        flame_length = flame_width*0.8
        im = pygame.transform.scale(self.raw_ims[2], (flame_width, flame_length))
        im = pygame.transform.rotate(im, angle)
        rect = im.get_rect()
        rect.center = self.__child_pos((x, y), angle, 0.6*scale)
        
        ims.append(im)
        rects.append(rect)

        # Engine 1

        im = pygame.transform.scale(self.raw_ims[1], (scale, scale))
        im = pygame.transform.rotate(im, angle)
        rect = im.get_rect()
        rect.center = (x, y)
        ims.append(im)
        rects.append(rect)

        return ims, rects
    

    def __update_cannon(self, scale, pos, uval):
        x, y = pos
        val = 0
        ims = []
        rects = []
        y-=0.01*scale
        if uval!=-1:
            val = 0.5  - abs(uval-0.5)

            #Shot Blast
        
            im = pygame.transform.scale(self.raw_ims[4], (scale*0.2, scale*0.2))
            im.set_alpha((1-uval)*255)
            rect = im.get_rect()
            rect.center = (x+val*scale*0.05-scale*0.12, y)
            ims.append(im)
            rects.append(rect)

            if not self.shell_shot and not self.game_over:
                self.shells.append([Shell((x, y)), -1])
                self.shell_shot = True

        im = pygame.transform.scale(self.raw_ims[3], (scale/2, scale/2))
        rect = im.get_rect()
        rect.center = (x+val*scale*0.05, y)
        ims.append(im)
        rects.append(rect)
        return ims, rects




    '''
    Blits character to display surface using rects and ims
    '''
    def blit(self, display_surface: pygame.Surface):
        self.hit = False
        for shell in self.shells:
            if shell[1] <= 13:
                shell[0].blit(display_surface)

        for i in range(len(self.rects)):
            display_surface.blit(self.ims[i], self.rects[i])
        
    '''
    Initializes character by loading character images from given path
    '''
    def __init__(self):
        self.__load_components()
        self.shells = []
        self.shell_shot = False
        self.t = 0
        self.shell_val = 0
        self.done = False
        self.hit = False
        self.game_over = False
        self.t_end = 0
