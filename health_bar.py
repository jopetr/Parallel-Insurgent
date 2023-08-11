import pygame
import math
from random import random as random

class HealthBar:
    
    '''
    Private
    Loads images for health bar from path
    '''
    def __load_components(self):
        ims = []
        ims.append(pygame.image.load("healthbar/healthbar0.png").convert())
        ims.append(pygame.image.load("healthbar/healthbar1.png").convert())
        self.raw_ims = ims
    
    '''
    Updates rects and ims to correspond to scale and position
    '''
    def update(self, scale, pos, health):
        if health<0:
            health = 0
        elif health>1:
            health = 1

        self.health = health
        
        x, y = pos
        
        rects = []
        ims = []
        im = pygame.transform.scale(self.raw_ims[1], (scale, scale/40))
        rect = im.get_rect()
        rect.center = (x, y)

        ims.append(im)
        rects.append(rect)

        im = pygame.transform.scale(self.raw_ims[0], (scale*health, scale/40))
        rect = im.get_rect()
        rect.center = (x-((1-health)*scale/2), y)

        ims.append(im)
        rects.append(rect)

        self.ims = ims
        self.rects = rects

        
            
   

    

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
        self.components = self.__load_components()
        self.health = 1
