import pygame
import math
from random import random as random

class Mine:
    
    '''
    Private
    Loads images for mine from path
    '''
    def __load_components(self, path):
        raw_ims = []
        raw_ims.append(pygame.image.load(path+"mine0.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"mine1.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"mine2.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"mine3.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"mine4.png").convert_alpha())
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
    def update(self, scale, pos, opponent_center, opponent_width):
        # Angles
        x, y = pos
        rects = []
        ims = []

        # Bomb
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
        min_x = x-0.45*scale
        max_x = x+0.45*scale
        min_y = y-0.45*scale
        max_y = y+0.45*scale
        
        if (min_o_x>min_x and max_o_x<max_x and min_o_y>min_y and max_o_y<max_y):
            self.hit = True
            
    '''
    Updates rects and ims of obstacle to correspond to collision animation
    '''
    def hit_update(self, scale, pos, val):
        x, y = pos
        
        if not self.fall_started:
            self.fall_started = True
            thresh = scale
            
        
        rects = []
        ims = []

        
        im = None
        # Bomb
        if val<4:
            im = pygame.transform.scale(self.raw_ims[round(val)], (scale, scale))
        else:
            im = pygame.transform.scale(self.raw_ims[4], (scale, scale))
        if val>4:
            alpha = 255*(1-(val - 3)/11)
            im.set_alpha(alpha)
        rect = im.get_rect()
        rect.center = (x, y)
        ims.append(im)
        rects.append(rect)

        # Explosion
        if val>4:
            explosion_val = math.floor(val-5)
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
    Blits mine to display surface using rects and ims
    '''
    def blit(self, display_surface: pygame.Surface):
        for i in range(len(self.rects)):
            display_surface.blit(self.ims[i], self.rects[i])

    '''
    Initializes mine by loading character images from given path
    '''
    def __init__(self):
        self.components = self.__load_components("mine/")
        self.hit = False
        self.fall_started = False
        self.explosion_angle = random()*360
