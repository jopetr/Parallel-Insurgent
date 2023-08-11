import pygame
import math
from random import random as random

class Obstacle:
    
    '''
    Private
    Loads images for obstacle from path
    '''
    def __load_components(self, path):
        self.raw_im = pygame.image.load(path+"im.png").convert_alpha()
        raw_ims = []
        for i in range(12):
            raw_ims.append(pygame.image.load(path+"im"+str(i)+".png").convert_alpha())
        self.raw_ims = raw_ims
    
    '''
    Updates rects and ims to correspond to scale and position
    '''
    def update(self, scale, pos, opponent_center, opponent_width):
        # Angles
        x, y = pos
        y -= scale*0.495
        rects = []
        ims = []
        im = pygame.transform.scale(self.raw_im, (scale, scale))
        rect = im.get_rect()
        rect.center = (x, y)

        ims.append(im)
        rects.append(rect)

        self.rects = rects
        self.ims = ims


        o_x, o_y = opponent_center
        min_o_x =  o_x + opponent_width/2
        max_o_x = o_x - opponent_width/2
        min_o_y = o_y + opponent_width/2
        max_o_y = o_y - opponent_width/2
        min_x = x-0.3*scale
        max_x = x+0.12*scale
        min_y = y - 0.62*scale + scale/2
        max_y = y + scale/2
        
        if (min_o_x>min_x and max_o_x<max_x and min_o_y>min_y and max_o_y<max_y):
            self.hit = True
            
    '''
    Updates rects and ims of obstacle to correspond to collision animation
    '''
    def hit_update(self, scale, pos, val):
        x, y = pos
        y -= scale*0.495
        if not self.fall_started:
            self.fall_started = True
            thresh = scale
            self.end_x = []
            self.end_val = []
            for i in range(len(self.raw_ims)):
                self.end_x.append(random()*thresh)
                self.end_val.append(0.5+random()/2)
            
        end_x = self.end_x
        end_val = self.end_val
        rects = []
        ims = []
        end_vals = [[0.36, -55], [0.28, 55], [0.57, -63], [0.64, -93], [0.48, -107], [0.33, 97], [0.58, 90], [0.62, 0], [0.36, 0], [0, 0], [0.68, -90], [0.68, -86]]
        unbound = [5, 6]
        for i in range(len(self.raw_ims)):
            if i not in unbound:
                curr = val/end_val[i]
                if curr>1:
                    curr = 1
                im = pygame.transform.scale(self.raw_ims[i], (scale, scale))
                im = pygame.transform.rotate(im, end_vals[i][1]*curr)
                rect = im.get_rect()
                rect.center = (x+end_x[i]*curr, y+end_vals[i][0]*scale*curr)
                ims.append(im)
                rects.append(rect)
            else:
                curr = val/end_val[i]
                if curr>1:
                    curr = 1
                y_curr = curr**3
                im = pygame.transform.scale(self.raw_ims[i], (scale, scale))
                im = pygame.transform.rotate(im, end_vals[i][1]*curr)
                rect = im.get_rect()
                rect.center = (x+end_x[i]*curr, y+end_vals[i][0]*scale*y_curr)
                ims.append(im)
                rects.append(rect)

        self.rects = rects
        self.ims = ims

    

    '''
    Blits character to display surface using rects and ims
    '''
    def blit(self, display_surface: pygame.Surface):
        for i in range(len(self.rects)):
            display_surface.blit(self.ims[i], self.rects[i])

    '''
    Initializes character by loading character images from given path
    '''
    def __init__(self):
        self.components = self.__load_components("obstacle0/")
        self.hit = False
        self.fall_started = False
