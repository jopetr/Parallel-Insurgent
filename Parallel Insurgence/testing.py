import pygame
import math
from random import random as random
from random import randint as randint
from character_class import Character

'''
def load_insurgent(path):
    ims = []
    im = pygame.image.load(path+"head.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"body.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"arm00.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"arm01.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"arm10.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"arm11.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"leg00.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"leg01.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"leg10.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"leg11.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"foot0.png").convert_alpha()
    ims.append(im)
    im = pygame.image.load(path+"foot1.png").convert_alpha()
    ims.append(im)
    return ims

def child_pos(parent_pos, parent_angle, distance):
    x, y = parent_pos
    angle = 360-1*parent_angle+90
    child_x = distance*math.cos(2*math.pi*angle/360) + x
    child_y = distance*math.sin(2*math.pi*angle/360) + y
    child_pos = (child_x, child_y)
    return child_pos

def gen_insurgent_blit(insurgent_components, scale, pos, angles):
    # Angles

    body_angle = angles['body']
    head_angle = angles['head'] + body_angle
    arm00_angle = angles['arm00'] + body_angle
    arm01_angle = angles['arm01'] + arm00_angle
    arm10_angle = angles['arm10'] + body_angle
    arm11_angle = angles['arm11'] + arm10_angle
    leg00_angle = angles['leg00'] + body_angle
    leg01_angle = angles['leg01'] + leg00_angle
    foot0_angle = angles['foot0'] + leg01_angle
    leg10_angle = angles['leg10'] + body_angle
    leg11_angle = angles['leg11'] + leg10_angle
    foot1_angle = angles['foot1'] + leg11_angle

    # Rects and Images to be returned Initialization

    rects = []
    ims = []

    # Central Character Position

    x, y = pos

    # Arm 1

    arm10_im = pygame.transform.scale(insurgent_components[4], (scale, scale))
    arm10_im = pygame.transform.rotate(arm10_im, arm10_angle)
    arm10_rect = arm10_im.get_rect()
    arm10_rect.center = child_pos((x, y), body_angle, -0.17*scale)
    ims.append(arm10_im)
    rects.append(arm10_rect)

    arm11_im = pygame.transform.scale(insurgent_components[5], (scale, scale))
    arm11_im = pygame.transform.rotate(arm11_im, arm11_angle)
    arm11_rect = arm11_im.get_rect()
    arm11_rect.center = child_pos(arm10_rect.center, arm10_angle, 0.21*scale)
    ims.append(arm11_im)
    rects.append(arm11_rect)

    # Leg 1

    leg10_im = pygame.transform.scale(insurgent_components[8], (scale, scale))
    leg10_im = pygame.transform.rotate(leg10_im, leg10_angle)
    leg10_rect = leg10_im.get_rect()
    leg10_rect.center = child_pos((x, y), body_angle, 0.23*scale)
    ims.append(leg10_im)
    rects.append(leg10_rect)

    leg11_im = pygame.transform.scale(insurgent_components[9], (scale, scale))
    leg11_im = pygame.transform.rotate(leg11_im, leg11_angle)
    leg11_rect = leg11_im.get_rect()
    leg11_rect.center = child_pos(leg10_rect.center, leg10_angle, 0.3*scale)

    foot1_im = pygame.transform.scale(insurgent_components[11], (scale*0.97, scale*0.97))
    foot1_im = pygame.transform.rotate(foot1_im, foot1_angle)
    foot1_rect = foot1_im.get_rect()
    foot1_rect.center = child_pos(leg11_rect.center, leg11_angle, 0.3*scale)
    ims.append(foot1_im)
    rects.append(foot1_rect)

    ims.append(leg11_im)
    rects.append(leg11_rect)

    # Head

    head_im = pygame.transform.scale(insurgent_components[0], (0.9*scale/2, 0.9*scale/2))
    head_im = pygame.transform.rotate(head_im, head_angle)
    head_rect = head_im.get_rect()
    head_rect.center = child_pos((x, y), body_angle, -0.26*scale) #(x, y-(scale*0.26))
    ims.append(head_im)
    rects.append(head_rect)

    # Body

    body_im = pygame.transform.scale(insurgent_components[1], (scale, scale))
    body_im = pygame.transform.rotate(body_im, body_angle)
    body_rect = body_im.get_rect()
    body_rect.center = (x, y)
    ims.append(body_im)
    rects.append(body_rect)

    # Leg 0

    leg00_im = pygame.transform.scale(insurgent_components[6], (scale, scale))
    leg00_im = pygame.transform.rotate(leg00_im, leg00_angle)
    leg00_rect = leg00_im.get_rect()
    leg00_rect.center = child_pos((x, y), body_angle, 0.23*scale)
    ims.append(leg00_im)
    rects.append(leg00_rect)

    leg01_im = pygame.transform.scale(insurgent_components[7], (scale, scale))
    leg01_im = pygame.transform.rotate(leg01_im, leg01_angle)
    leg01_rect = leg01_im.get_rect()
    leg01_rect.center = child_pos(leg00_rect.center, leg00_angle, 0.3*scale)

    foot0_im = pygame.transform.scale(insurgent_components[10], (scale, scale))
    foot0_im = pygame.transform.rotate(foot0_im, foot0_angle)
    foot0_rect = foot0_im.get_rect()
    foot0_rect.center = child_pos(leg01_rect.center, leg01_angle, 0.3*scale)
    ims.append(foot0_im)
    rects.append(foot0_rect)

    ims.append(leg01_im)
    rects.append(leg01_rect)

    # Arm 0

    arm00_im = pygame.transform.scale(insurgent_components[2], (scale, scale))
    arm00_im = pygame.transform.rotate(arm00_im, arm00_angle)
    arm00_rect = arm00_im.get_rect()
    arm00_rect.center = child_pos((x, y), body_angle, -0.17*scale)
    ims.append(arm00_im)
    rects.append(arm00_rect)

    arm01_im = pygame.transform.scale(insurgent_components[3], (scale, scale))
    arm01_im = pygame.transform.rotate(arm01_im, arm01_angle)
    arm01_rect = arm01_im.get_rect()
    arm01_rect.center = child_pos(arm00_rect.center, arm00_angle, 0.21*scale)
    ims.append(arm01_im)
    rects.append(arm01_rect)
   
    return rects, ims


def walk_animation(insurgent_components, scale, pos, val):
    # subtract 0.905*scale from y position with all angles as 0 to have character touch ground perfectly
    val0 = val
    val1 = (val+0.5)%1.0
    angles = {}
    angles['body'] = 0
    angles['head'] = 0
    
    x, y = pos
    # leg 0
    if val0 < 0.5:
        curr = val0*2
        angles['leg00'] = -20 + 50*curr
    else:
        curr = (val0-0.5)*2
        angles['leg00'] = 30 - 50*curr
       
    if val0 < 0.25:
        angles['leg01'] = -40* (val0/0.25) - 20
    elif val0 < 0.5:
        angles['leg01'] = -60+30*(val0-0.25)*4
    elif val0<0.75:
        angles['leg01'] = 30*(val0-0.5)/0.25 + -30
    else:
        angles['leg01'] = -20*(val0-0.75)/0.25
    
    if val0<0.5:
        angles['foot0'] = 10
    elif val0<0.95:
        angles['foot0'] = -1*(angles['leg00']+angles['leg01'])
    else:
        angles['foot0'] = 10
    

    # leg 1
    if val1 < 0.5:
        curr = val1*2
        angles['leg10'] = -20 + 50*curr
    else:
        curr = (val1-0.5)*2
        angles['leg10'] = 30 - 50*curr
       
    if val1 < 0.25:
        angles['leg11'] = -40* (val1/0.25) - 20
    elif val1 < 0.5:
        angles['leg11'] = -60+30*(val1-0.25)*4
    elif val1<0.75:
        angles['leg11'] = 30*(val1-0.5)/0.25 + -30
    else:
        angles['leg11'] = -20*(val1-0.75)/0.25

    if val1<0.5:
        angles['foot1'] = 10
    elif val1<0.95:
        angles['foot1'] = -1*(angles['leg10']+angles['leg11'])
    else:
        angles['foot1'] = 10
        
    
    # Walking Height Adjustment

    if val < 0.25:
        curr = 1 - val*4
        y+=curr*scale/50
    elif val < 0.5:
        curr = (val - 0.25)*4
        y+= curr*scale/50
    elif val < 0.75:
        curr = 1 - (val-0.5)*4
        y+=curr*scale/50
    else:
        curr = (val - 0.75)*4
        y+= curr*scale/50

    # Arm 0

    if val1 < 0.5:
        curr = val1/0.5
        angles['arm00'] = -40+60*curr
        angles['arm01'] = 10+30*curr
    else:
        curr = 1 - (val1-0.5)*2
        angles['arm00'] = -40+60*curr
        angles['arm01'] = 10+30*curr


    # Arm 1

    if val0 < 0.5:
        curr = val0/0.5
        angles['arm10'] = -40+60*curr
        angles['arm11'] = 10+30*curr
    else:
        curr = 1 - (val0-0.5)*2
        angles['arm10'] = -40+60*curr
        angles['arm11'] = 10+30*curr
    
    return gen_insurgent_blit(insurgent_components, scale, (x, y), angles)

'''

def run_game(width: int, height: int, display_surface: pygame.Surface):
    clock = pygame.time.Clock()
    #insurgent_components = load_insurgent("phil/")
    character = Character("phil/")
    val = 0.0
    test_background = pygame.image.load("black_screen.png").convert()
    test_background = pygame.transform.scale(test_background, (width, height))
    test_ground = pygame.image.load("testing_ground.png").convert()
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

        tick = pygame.time.get_ticks()
        
        val+=0.02
        val = val%1.0
        
        '''
        rects, ims = walk_animation(insurgent_components, 200, (width/2, 700-200*0.905), val)
        for i in range(len(rects)):
            display_surface.blit(ims[i], rects[i])
        '''
        character.walk_update(400, (width/2, 700), val)
        character.blit(display_surface)
        display_surface.blit(test_ground, (0, 700))
        
        pygame.display.flip()
        clock.tick(60)




if __name__ == "__main__":
    
    pygame.init()
    width = 1440
    height = 800
    display_surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Parallel Insurgence')
    run_game(width, height, display_surface)