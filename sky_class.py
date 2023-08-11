import pygame
import math
from random import random as random

class Sky:
    
    '''
    Private
    Loads images for mine from path
    '''
    def __load_components(self, path):
        raw_ims = []
        raw_ims.append(pygame.image.load(path+"sky0.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"sky1.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"sun0.png").convert_alpha())
        raw_ims.append(pygame.image.load(path+"sun1.png").convert_alpha())
        self.raw_ims = raw_ims
    
    
    

    '''
    Blits sky to display surface using rects and ims
    '''
    def blit(self, val, display_surface: pygame.Surface):
        height = 800
        width = 1440
        sand_y = 7*height/8
        sand_height = sand_y - height/4
        rects = []
        ims = []

        im = self.raw_ims[0]
        rect = im.get_rect()
        rect.center = (width/2, sand_height/2)
        ims.append(im)
        rects.append(rect)

        im = self.raw_ims[1]
        im.set_alpha(val*255)
        rect = im.get_rect()
        rect.center = (width/2, sand_height/2)
        ims.append(im)
        rects.append(rect)

        im = self.raw_ims[2]
        im.set_alpha((1-val)*255)
        rect = im.get_rect()
        rect.center = (width/2, (1+val*0.6)*sand_height/2)
        ims.append(im)
        rects.append(rect)

        im = self.raw_ims[3]
        im.set_alpha((val)*255)
        rect = im.get_rect()
        rect.center = (width/2, (1+val*0.6)*sand_height/2)
        ims.append(im)
        rects.append(rect)


        for i in range(len(rects)):
            display_surface.blit(ims[i], rects[i])

    '''
    Initializes sky by loading images from given path
    '''
    def __init__(self):
        self.components = self.__load_components("sky/")
        
