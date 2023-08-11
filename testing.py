import pygame
import math
from random import random as random
from random import randint as randint
from character_class import Character
from obstacle_class import Obstacle
from bomb_class import Bomb
from health_bar import HealthBar
from mine_class import Mine
from vessel_class import Vessel
from shell_class import Shell
from sky_class import Sky

def run_game(width: int, height: int, display_surface: pygame.Surface):
    clock = pygame.time.Clock()
    #insurgent_components = load_insurgent("phil/")
    #character = Character("phil/")
    val = -1
    test_background = pygame.image.load("black_screen.png").convert()
    test_background = pygame.transform.scale(test_background, (width, height))
    test_box_g = pygame.image.load("test_green.png").convert()
    test_box_r = pygame.image.load("test_red.png").convert()
    test_box_width = 100
    test_box_g = pygame.transform.scale(test_box_g, (test_box_width, test_box_width))
    test_box_r = pygame.transform.scale(test_box_r, (test_box_width, test_box_width))
    test_background = pygame.transform.scale(test_background, (width, height))
    test_ground = pygame.image.load("testing_ground.png").convert()
    test_ground = pygame.transform.scale(test_ground, (width, height/2))
    #bomb = Bomb()
    mine = Mine()
    health_bar = HealthBar()
    vessel = Vessel()
    shell = Shell((width/2, height/2))
    sky = Sky()
    sky_val = 0
    while True:
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
        display_surface.blit(test_background, (0,0))
        display_surface.blit(test_ground, (0, 5*height/8))
        tick = pygame.time.get_ticks()
        
        mouse_pos = pygame.mouse.get_pos()
        box_width = 50
        #x +=10
        
        im = None

        sky_val += 0.003
        sky_val%=1
        sky.blit(sky_val, display_surface)
        
        val+=0.06
        val = val%5
        
        
        uval = -1
        if val<=1:
            uval = val
        # max height: 0.5*height, min height:
        if not vessel.done:
            vessel.step(mouse_pos, box_width)
            if vessel.hit:
                print('hit')
            #update(250, (width*0.9, 0.1*height), uval, mouse_pos, box_width)
            vessel.blit(display_surface)
        else:
            print('done')
        









        '''
        val+=0.001
        val = val%1
        health_bar.update(500, (width/3, height/3), val)
        health_bar.blit(display_surface)'''
        
        #pos = (width/3, height/3)
        '''
        if shell.hit:
            im = test_box_g
            if val == -1:
                val = 0
            else:
                val+=0.5
                if val > 13:
                    val = -1
                    shell.hit = False
            shell.hit_update(mine_width, val)
        else:
            im = test_box_r
            shell.update(100, 10, mouse_pos, mine_width, val)
        
        shell.blit(display_surface)
        rect = im.get_rect()
        rect.center = mouse_pos
        display_surface.blit(im, rect)
        '''

        '''
        rects, ims = walk_animation(insurgent_components, 200, (width/2, 700-200*0.905), val)
        for i in range(len(rects)):
            display_surface.blit(ims[i], rects[i])
        '''
        
        #character.mounted_update(400, (width/2, 700), val)
        #character.blit(display_surface)
        
        
        pygame.display.flip()
        clock.tick(60)




if __name__ == "__main__":
    
    pygame.init()
    width = 1440
    height = 800
    display_surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Parallel Insurgence')
    run_game(width, height, display_surface)