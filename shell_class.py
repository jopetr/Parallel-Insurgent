import pygame
import math
from random import random as random

class Shell:
    
    '''
    Private
    Loads images for obstacle from path
    '''
    def __load_components(self):
        raw_ims = []
        path = "shell/"
        raw_ims.append(pygame.image.load(path+"shell.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"shell_trail.png").convert_alpha())
        self.raw_ims = raw_ims

        explosion_images = []
        explosion_images.append(pygame.image.load(path+"images/explosion0.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion1.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion2.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion3.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion4.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion5.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion6.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion7.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion8.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion9.png").convert_alpha())
        explosion_images.append(pygame.image.load(path+"images/explosion10.png").convert_alpha())

        self.explosion_ims = explosion_images
    
    '''
    Updates rects and ims to correspond to scale and position
    '''
    def update(self, scale, rate, opponent_center, opponent_width, val):
        # Angles
        self.rate = rate
        x, y = self.pos
        x-=rate
        rects = []
        ims = []
        
        width = 1440
        height = 800

        if len(self.trail_rotation)<10:
            if len(self.trail_rotation)<(self.start_pos[0]-x)/(scale*0.2):
                new_trail = [round(random()*360)]
                for i in range(len(self.trail_rotation)):
                    new_trail.append(self.trail_rotation[i])
                self.trail_rotation = new_trail
        else:
            new_trail = [round(random()*360)]
            for i in range(len(self.trail_rotation)-1):
                new_trail.append(self.trail_rotation[i])
            self.trail_rotation = new_trail

        for i in range(len(self.trail_rotation)):
            im = pygame.transform.scale(self.raw_ims[1], (scale, scale))
            im = pygame.transform.rotate(im, self.trail_rotation[i])
            alpha = 255*(1-(i)/9)
            im.set_alpha(alpha)
            rect = im.get_rect()
            rect.center = (x+(i+1)*scale*0.2, y)
            ims.append(im)
            rects.append(rect)


        self.pos = (x,y)
        if x<=-width*0.1:
            self.done = True

        # Shell
        im = pygame.transform.scale(self.raw_ims[0], (scale, scale))
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
        min_x = x-scale/2
        max_x = x+scale/2
        min_y = y-scale/4
        max_y = y+scale/4
        
        if (min_o_x>min_x and max_o_x<max_x and min_o_y>min_y and max_o_y<max_y):
            self.hit = True
            
    '''
    Updates rects and ims of obstacle to correspond to collision animation
    '''
    def hit_update(self, scale, val):
        x, y = self.pos
        x -= self.rate*0.4
        self.pos = (x,y)
        
            
        
        rects = []
        ims = []

        

        # Bomb
        im = pygame.transform.scale(self.raw_ims[1], (scale, scale))
        if val>2:
            alpha = 255*(1-(val - 3)/11)
            im.set_alpha(alpha)
        rect = im.get_rect()
        rect.center = (x, y)
        ims.append(im)
        rects.append(rect)

        # Explosion
        if val>2:
            explosion_val = math.floor(val-3)
            explosion_scale = scale*3
            im = pygame.transform.scale(self.explosion_ims[explosion_val], (explosion_scale, explosion_scale))
            im = pygame.transform.rotate(im, self.explosion_angle)
            rect = im.get_rect()
            rect.center = (x, y)
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
    def __init__(self, start_pos):
        
        self.components = self.__load_components()
        self.hit = False
        self.explosion_angle = random()*360
        self.start_pos = start_pos
        self.pos = start_pos
        self.trail_rotation = []
        self.done = False
        self.rate = 0
        
