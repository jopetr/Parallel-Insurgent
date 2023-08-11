import pygame
import math
from character_class import Character
from random import random as random
from random import randint as randint
from obstacle_class import Obstacle
from bomb_class import Bomb
from health_bar import HealthBar
from mine_class import Mine
from vessel_class import Vessel
from sky_class import Sky


def run_game(width: int, height: int, display_surface: pygame.Surface):
    clock = pygame.time.Clock()

    test_background = pygame.image.load("black_screen.png").convert()
    test_background = pygame.transform.scale(test_background, (width, height))

    sand0 = pygame.image.load("sand0.png").convert()
    sand0 = pygame.transform.scale(sand0, (width*2, height/2))
    sand1 = pygame.image.load("sand1.png").convert()
    sand1 = pygame.transform.scale(sand1, (width*2, height/2))
    game_over_im = pygame.image.load("game_over.png").convert_alpha()

    mountain_im = []
    for i in range(5):
        im = pygame.image.load("mountain"+str(i)+".png").convert_alpha()
        mountain_im.append(pygame.transform.scale(im, (100,100)))
    

    sky = pygame.image.load("sky.png").convert()


    worm_width = 100
    worm_segments = []
    for i in range(10):
        worm_segment = pygame.image.load("wormsegments/wormsegment"+str(i)+".png").convert_alpha()
        worm_segment = pygame.transform.scale(worm_segment, (worm_width/50, worm_width))
        worm_segments.append(worm_segment)
    worm_segment = pygame.image.load("wormsegment.png").convert_alpha()
    worm_segment_width = worm_width/5
    worm_segment = pygame.transform.scale(worm_segment, (worm_segment_width, worm_width))
    worm_head = []
    for i in range(5):
        im = pygame.image.load("wormhead"+str(i)+".png").convert_alpha()
        worm_head.append(pygame.transform.scale(im, (worm_width, worm_width)))
    segments = []

    dust_im = []
    dust_width = worm_width
    for i in range(5):
        im = pygame.image.load("dustclouds/dust"+str(i)+".png").convert_alpha()
        im = pygame.transform.scale(im, (dust_width, dust_width))
        dust_im.append(im)

    # Hole initialization
    hole_scale_factor = 1.15
    hole_segment = pygame.image.load("holesegment.png").convert_alpha()
    hole_segment = pygame.transform.scale(hole_segment, (worm_width/50, hole_scale_factor*worm_width))
    hole_head = pygame.image.load("holehead.png").convert_alpha()
    hole_head = pygame.transform.scale(hole_head, (worm_width, hole_scale_factor*worm_width))

    worm_head_y = height/2
    worm_head_x = width/5
    for i in range(math.ceil((worm_head_x)/(worm_width/5))):
        segments.append([worm_head_x-(worm_width/5)*i-(3*worm_width/5), height/2])
    prev_tick = -1
    head_movement_thresh = (worm_width/20)
    sand_pos = 0
    sand_y = 7*height/8
    sand_height = sand_y - height/4
    mouth_pos = 0
    mouse_down = False
    dust = []
    # Mountain Initialization
    mountains = []
    num_mountains = 15
    min_size = math.ceil(width/num_mountains)
    for i in range(num_mountains):
        mountains.append([randint(0,len(mountain_im)-1), (randint(min_size*2, min_size*3), randint(min_size, min_size*1.5)), i*min_size+min_size/2])
   
    for i in range(100):
        dust.append([False, 0, 0])
    intro = True
    intro_head_x = -1*width/2
    intro_head_y = height
    intro_ext_time = 0

    character = Character("phil/")

    while intro:
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

        tick = pygame.time.get_ticks()
        

        # Intro head x
        if intro_head_x<0:
            intro_head_x += 4
            if intro_head_x > 0:
                intro_head_x = 0
        else:
            intro_head_x = 0

        # Intro head y
        if intro_head_y>sand_height:
            intro_head_y-=1.8
            if intro_head_y<sand_height:
                intro_head_y = sand_height
        else:
            intro_head_y = sand_height
            intro_ext_time += 1
            if intro_ext_time > 170:
                intro = False
        mouse_y = intro_head_y

        worm_head_y = mouse_y
        
        
       
        # Test background
        display_surface.blit(test_background, (0,0))
        # Worm Body Animation

        sand_pos = 0
        rect = sand0.get_rect()
        rect.center = (width-sand_pos, sand_y)
        display_surface.blit(sand0, rect)
        rect = sand0.get_rect()
        rect.center = (5*width-sand_pos, sand_y)
        display_surface.blit(sand0, rect)
        rect = sand1.get_rect()
        rect.center = (3*width-sand_pos, sand_y)
        display_surface.blit(sand1, rect)

        # Hole Head
        if worm_head_y >= (sand_height - worm_width/2):
            rect = hole_head.get_rect()
            rect.center = (worm_head_x+intro_head_x, worm_head_y)
            y_upper = sand_height - hole_scale_factor*(worm_width)/2
            y_lower = sand_height
            y = worm_head_y
            if y>=y_upper and y<=y_lower:
                alpha = 255*(y - y_upper)/(y_lower - y_upper)
                hole_head.set_alpha(alpha)
            else:
                hole_head.set_alpha(255)
            display_surface.blit(hole_head, rect)

        # Hole Body
        for i in range (len(segments)):
            if segments[i][1] >= (sand_height - worm_width/2):
                pos_diff = 0
                if i==0:
                    pos_diff = (segments[i][1] - worm_head_y)/10
                else:
                    pos_diff = (segments[i][1] - segments[i-1][1])/10

                for j in range(10):
                    scale_factor_y = pos_diff
                    scaled_hole_segment = pygame.transform.scale(hole_segment, (worm_width/50, hole_scale_factor*(worm_width+scale_factor_y)))
                    rect = scaled_hole_segment.get_rect()
                    (x, y) = segments[i]
                    x = x - (worm_width/10) + j*worm_width/50 + worm_width/100
                    rect.center = (x+intro_head_x, y - j*pos_diff)
                    y_upper = sand_height - hole_scale_factor*(worm_width+scale_factor_y)/2
                    y_lower = sand_height
                    y = worm_head_y
                    if y>=y_upper and y<=y_lower:
                        alpha = 255*(y - y_upper)/(y_lower - y_upper)
                        scaled_hole_segment.set_alpha(alpha)
                    display_surface.blit(scaled_hole_segment, rect)
            

        # Sky
        rect = sky.get_rect()
        rect.center = (width/2, sand_height/2)
        display_surface.blit(sky, rect)

        # Dune Mountains

        for i in range(num_mountains-1, -1, -1):
            im = pygame.transform.scale(mountain_im[mountains[i][0]], mountains[i][1])
            rect = im.get_rect()
            rect.center = (mountains[i][2], sand_height-mountains[i][1][1]/2)
            display_surface.blit(im, rect)


        # Character
        character_y = sand_height
        character_x = tick/20
        if character_x >= worm_head_x - worm_width/2:
            character_x = worm_head_x - worm_width/2
            character_y = sand_height - worm_width/2
        else:
            character.walk_update(50, (character_x, character_y), (tick/1200)%1.0)
            character.blit(display_surface)

        # Dust
        for i in range(len(segments)):
            (x, y) = segments[i]
            if y<(sand_height+worm_width/2) and (intro_head_x)>-1*width/8:
                x0 = x - intro_head_x
                ind = 28 - round((x0 - worm_head_x)/(-10))
                if ind>0 and not dust[ind][0]:
                    dust[ind] = [True, randint(0,len(dust_im)-1), randint(100, 150), ind*3]

        
        

        for i in range(len(dust)):
            if dust[i][0]:
                im = pygame.transform.scale(dust_im[dust[i][1]], (dust[i][2], dust[i][2]))
                rect = im.get_rect()
                alpha = dust[i][3]
                if alpha<=100:
                    im.set_alpha((100-alpha)/2)
                else:
                    im.set_alpha(0)
                dust[i][3] += 1
                rect.center = (worm_head_x-10*i, sand_height-(dust[i][2]/2)+(hole_scale_factor-1)*worm_width)
                display_surface.blit(im, rect)
        

        
        # Worm Head
        rect = worm_head[mouth_pos].get_rect()
        rect.center = (worm_head_x+intro_head_x, worm_head_y)
        display_surface.blit(worm_head[mouth_pos], rect)

        # Worm Body
        for i in range (len(segments)):
            pos_diff = 0
            if i==0:
                pos_diff = (segments[i][1] - worm_head_y)/10
            else:
                pos_diff = (segments[i][1] - segments[i-1][1])/10
            
            for j in range(10):
                scale_factor_y = pos_diff
                scaled_worm_segment = pygame.transform.scale(worm_segments[j], (worm_width/50, worm_width+scale_factor_y))
                rect = scaled_worm_segment.get_rect()
                (x, y) = segments[i]
                x = x - (worm_width/10) + j*worm_width/50 + worm_width/100+intro_head_x
                rect.center = (x, y - j*pos_diff)
                display_surface.blit(scaled_worm_segment, rect)

        # Mounted character
        if character_x >= worm_head_x - worm_width/2 and intro_ext_time>0:
            character.mounted_update(50, (character_x, character_y), 0)
            character.blit(display_surface)

        # Segment Position update
        for i in range(len(segments)-1, -1, -1):
            if i==0:
                segments[i][1] = worm_head_y
            else:
                segments[i][1] = segments[i-1][1] + i/3
        pygame.display.flip()
        clock.tick(60)



    start = 10**4*0.2
    end = 7.2*10**4

    obstacles = []
    bombs = []
    mines = []
    vessels = []

    for i in range(5):
        obstacles.append([Obstacle(),start+random()*7.2*10**4, 0])
    
    
    for i in range(20):
        bombs.append([Bomb(), start+random()*7.2*10**4, random()*(sand_height-200), -1])

    
    for i in range(50):
        mines.append([Mine(), start+random()*7.2*10**4, (sand_height+100)+random()*300, -1])
    
    
    for i in range(1):
        vessels.append([Vessel(), start])
    
    health = 1
    health_bar = HealthBar()

    head_movement_thresh = 0
    disp_x = 0

    final_mouse_y = 0
    while health>0:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

        tick = pygame.time.get_ticks()
        
        # Open/Close mouth
        if mouse_down and mouth_pos<4:
            mouth_pos+=1
        elif not mouse_down and mouth_pos>0:
            mouth_pos-=1


        mouse_y = pygame.mouse.get_pos()[1]
        thresh = 5
        if head_movement_thresh < (thresh*worm_width/20):
            head_movement_thresh += worm_width/2000
        else:
            head_movement_thresh = (thresh*worm_width/20)
            
        worm_head_y_diff = worm_head_y
        if mouse_y >= (worm_head_y + head_movement_thresh):
            worm_head_y = worm_head_y + head_movement_thresh
            if head_movement_thresh >= (thresh*worm_width/20):
                head_movement_thresh += 1
                if head_movement_thresh > (thresh*worm_width/10):
                    head_movement_thresh = (thresh*worm_width/10)
        elif mouse_y <= (worm_head_y - head_movement_thresh):
            worm_head_y = worm_head_y - head_movement_thresh
            if head_movement_thresh >= (thresh*worm_width/20):
                head_movement_thresh +=1
                if head_movement_thresh > (thresh*worm_width/10):
                    head_movement_thresh = (thresh*worm_width/10)
        else:
            worm_head_y = mouse_y
            head_movement_thresh = (worm_width/20)
        
        worm_head_y_diff -= worm_head_y
        
       
        # Test background
        display_surface.blit(test_background, (0,0))
        # Worm Body Animation
        disp_x+=10
        # Sand
        sand_pos += 10
        if sand_pos >= width*4:
            sand_pos = 0
        rect = sand0.get_rect()
        rect.center = (width-sand_pos, sand_y)
        display_surface.blit(sand0, rect)
        rect = sand0.get_rect()
        rect.center = (5*width-sand_pos, sand_y)
        display_surface.blit(sand0, rect)
        rect = sand1.get_rect()
        rect.center = (3*width-sand_pos, sand_y)
        display_surface.blit(sand1, rect)

        # Hole Head
        if worm_head_y >= (sand_height - worm_width/2):
            rect = hole_head.get_rect()
            rect.center = (worm_head_x, worm_head_y)
            y_upper = sand_height - hole_scale_factor*(worm_width)/2
            y_lower = sand_height
            y = worm_head_y
            if y>=y_upper and y<=y_lower:
                alpha = 255*(y - y_upper)/(y_lower - y_upper)
                hole_head.set_alpha(alpha)
            else:
                hole_head.set_alpha(255)
            display_surface.blit(hole_head, rect)

        # Hole Body
        for i in range (len(segments)):
            if segments[i][1] >= (sand_height - worm_width/2):
                pos_diff = 0
                if i==0:
                    pos_diff = (segments[i][1] - worm_head_y)/10
                else:
                    pos_diff = (segments[i][1] - segments[i-1][1])/10

                for j in range(10):
                    scale_factor_y = pos_diff
                    scaled_hole_segment = pygame.transform.scale(hole_segment, (worm_width/50, hole_scale_factor*(worm_width+scale_factor_y)))
                    rect = scaled_hole_segment.get_rect()
                    (x, y) = segments[i]
                    y_upper = sand_height - hole_scale_factor*(worm_width+scale_factor_y)/2
                    y_lower = sand_height
                    if y>=y_upper and y<=y_lower:
                        alpha = 255*(y - y_upper)/(y_lower - y_upper)
                        scaled_hole_segment.set_alpha(alpha)
                    x = x - (worm_width/10) + j*worm_width/50 + worm_width/100
                    rect.center = (x, y - j*pos_diff)
                    display_surface.blit(scaled_hole_segment, rect)
            

        # Sky
        rect = sky.get_rect()
        rect.center = (width/2, sand_height/2)
        display_surface.blit(sky, rect)

        # Dune Mountains

        for i in range(num_mountains-1, -1, -1):
            im = pygame.transform.scale(mountain_im[mountains[i][0]], mountains[i][1])
            rect = im.get_rect()
            rect.center = (mountains[i][2], sand_height-mountains[i][1][1]/2)
            display_surface.blit(im, rect)
            if mountains[i][2] < -1*mountains[i][1][0]/2:
                scale = (randint(min_size*2, min_size*3), randint(min_size, min_size*1.5))
                mountains[i] = [randint(0,len(mountain_im)-1), scale, width+scale[0]/2]
            else:
                mountains[i][2] -= 2


        # Obstacles
        
        for i in range(len(obstacles)):
            if obstacles[i][1] <= width*1.2 and obstacles[i][1] >= -0.4*width:
                ob = obstacles[i][0]
                x = obstacles[i][1]
                y = sand_height
                val = obstacles[i][2]
                
                if not ob.hit:
                    ob.update(300, (x,y), (worm_head_x, worm_head_y), worm_width)
                    ob.blit(display_surface)
                    if ob.hit:
                        health -= 0.1
                else:
                    val+=0.09
                    if val > 1:
                        val = 1

                    ob.hit_update(300, (x,y), val)
                    ob.blit(display_surface)
                    obstacles[i][2] = val
            obstacles[i][1]-=10

        # Vessels

        for i in range(len(vessels)):
            if vessels[i][1] <= width and not vessels[i][0].done:
                vessels[i][0].step((worm_head_x, worm_head_y), worm_width)
                if vessels[i][0].hit:
                    health -= 0.1
                vessels[i][0].blit(display_surface)
            vessels[i][1]-=10

        # Bombs 

        for i in range(len(bombs)):
            if bombs[i][1] <= width*1.2 and bombs[i][1] >= -0.4*width:
                bomb = bombs[i][0]
                x = bombs[i][1]
                y = bombs[i][2]
                val = bombs[i][3]
                
                if not bomb.hit:
                    bomb.update(100, (x,y), (worm_head_x, worm_head_y), worm_width)
                    bomb.blit(display_surface)
                    if bomb.hit:
                        health -= 0.2
                else:
                    if val == -1:
                        val = 0
                    elif val>13:
                        val = 13

                    bomb.hit_update(100, (x,y), val)
                    bomb.blit(display_surface)
                    val+=0.5
                    bombs[i][3] = val
            bombs[i][1]-=10

        # Mines

        for i in range(len(mines)):
            if mines[i][1] <= width*1.2 and mines[i][1] >= -0.4*width:
                mine = mines[i][0]
                x = mines[i][1]
                y = mines[i][2]
                val = mines[i][3]
                
                if not mine.hit:
                    mine.update(100, (x,y), (worm_head_x, worm_head_y), worm_width)
                    mine.blit(display_surface)
                    if mine.hit:
                        health -= 0.2
                else:
                    if val == -1:
                        val = 0
                    elif val>15:
                        val = 15

                    mine.hit_update(100, (x,y), val)
                    mine.blit(display_surface)
                    val+=0.5
                    mines[i][3] = val
            mines[i][1]-=10
        
        # Dust
        if worm_head_y < (sand_height + (worm_width/2)) and worm_head_y >= (sand_height - (worm_width/2)):
            dust[0] = [True, randint(0,len(dust_im)-1), randint(100, 150), 0]
        else:
            dust[0] = [False, 0, 0, 0]

        
        

        for i in range(len(dust)):
            if dust[i][0]:
                im = pygame.transform.scale(dust_im[dust[i][1]], (dust[i][2], dust[i][2]))
                rect = im.get_rect()
                alpha = dust[i][3]
                if i>0:
                    im.set_alpha((100-i)/2)
                else:
                    im.set_alpha(155)
                dust[i][3] += 1
                rect.center = (worm_head_x-i*10, sand_height-(dust[i][2]/2)+(hole_scale_factor-1)*worm_width)
                display_surface.blit(im, rect)
        
        new_dust = [[False, 0, 0, 0]]
        for i in range(0, len(dust)-1):
            new_dust.append(dust[i])
        dust = new_dust.copy()
        
        # Worm Head
        rect = worm_head[mouth_pos].get_rect()
        rect.center = (worm_head_x, worm_head_y)
        display_surface.blit(worm_head[mouth_pos], rect)

        # Worm Body
        for i in range (len(segments)):
            pos_diff = 0
            if i==0:
                pos_diff = (segments[i][1] - worm_head_y)/10
            else:
                pos_diff = (segments[i][1] - segments[i-1][1])/10
            
            for j in range(10):
                scale_factor_y = pos_diff
                scaled_worm_segment = pygame.transform.scale(worm_segments[j], (worm_width/50, worm_width+scale_factor_y))
                rect = scaled_worm_segment.get_rect()
                (x, y) = segments[i]
                x = x - (worm_width/10) + j*worm_width/50 + worm_width/100
                rect.center = (x, y - j*pos_diff)
                display_surface.blit(scaled_worm_segment, rect)
        # Character
        character_x = worm_head_x - worm_width/2
        character_y = worm_head_y - worm_width/2
        character.mounted_update(50, (character_x, character_y), worm_head_y_diff)
        character.blit(display_surface)

        # Segment Position update
        for i in range(len(segments)-1, -1, -1):
            if i==0:
                segments[i][1] = worm_head_y
            else:
                segments[i][1] = segments[i-1][1]

        # Health Bar

        health_bar.update(400, (width/2, 60), health)
        health_bar.blit(display_surface)

        pygame.display.flip()
        clock.tick(60)

        final_mouse_y = mouse_y
    t_end = 0
    

    sky = Sky()
    while True:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()  
            

        tick = pygame.time.get_ticks()
        
        # Open/Close mouth
        if mouth_pos<4 and t_end>=0.5:
            mouth_pos=round((t_end-0.5)*10)

        
        t_end += 0.01
        if t_end >= 1:
            t_end = 1
            
        

        mouse_y = sand_height - (sand_height-final_mouse_y)*(1-t_end)
        thresh = 5
        if head_movement_thresh < (thresh*worm_width/20):
            head_movement_thresh += worm_width/2000
        else:
            head_movement_thresh = (thresh*worm_width/20)
            
        worm_head_y_diff = worm_head_y
        if mouse_y >= (worm_head_y + head_movement_thresh):
            worm_head_y = worm_head_y + head_movement_thresh
            if head_movement_thresh >= (thresh*worm_width/20):
                head_movement_thresh += 1
                if head_movement_thresh > (thresh*worm_width/10):
                    head_movement_thresh = (thresh*worm_width/10)
        elif mouse_y <= (worm_head_y - head_movement_thresh):
            worm_head_y = worm_head_y - head_movement_thresh
            if head_movement_thresh >= (thresh*worm_width/20):
                head_movement_thresh +=1
                if head_movement_thresh > (thresh*worm_width/10):
                    head_movement_thresh = (thresh*worm_width/10)
        else:
            worm_head_y = mouse_y
            head_movement_thresh = (worm_width/20)
        
        worm_head_y_diff -= worm_head_y
        
       
        # Test background
        display_surface.blit(test_background, (0,0))
        # Worm Body Animation
        disp_x+=10
        # Sand
        sand_pos += 10*(1-t_end)
        if sand_pos >= width*4:
            sand_pos = 0
        rect = sand0.get_rect()
        rect.center = (width-sand_pos, sand_y)
        display_surface.blit(sand0, rect)
        rect = sand0.get_rect()
        rect.center = (5*width-sand_pos, sand_y)
        display_surface.blit(sand0, rect)
        rect = sand1.get_rect()
        rect.center = (3*width-sand_pos, sand_y)
        display_surface.blit(sand1, rect)

        # Hole Head
        if worm_head_y >= (sand_height - worm_width/2):
            rect = hole_head.get_rect()
            rect.center = (worm_head_x, worm_head_y)
            y_upper = sand_height - hole_scale_factor*(worm_width)/2
            y_lower = sand_height
            y = worm_head_y
            if y>=y_upper and y<=y_lower:
                alpha = 255*(y - y_upper)/(y_lower - y_upper)
                hole_head.set_alpha(alpha)
            else:
                hole_head.set_alpha(255)
            display_surface.blit(hole_head, rect)

        # Hole Body
        for i in range (len(segments)):
            if segments[i][1] >= (sand_height - worm_width/2):
                pos_diff = 0
                if i==0:
                    pos_diff = (segments[i][1] - worm_head_y)/10
                else:
                    pos_diff = (segments[i][1] - segments[i-1][1])/10

                for j in range(10):
                    scale_factor_y = pos_diff
                    scaled_hole_segment = pygame.transform.scale(hole_segment, (worm_width/50, hole_scale_factor*(worm_width+scale_factor_y)))
                    rect = scaled_hole_segment.get_rect()
                    (x, y) = segments[i]
                    y_upper = sand_height - hole_scale_factor*(worm_width+scale_factor_y)/2
                    y_lower = sand_height
                    if y>=y_upper and y<=y_lower:
                        alpha = 255*(y - y_upper)/(y_lower - y_upper)
                        scaled_hole_segment.set_alpha(alpha)
                    x = x - (worm_width/10) + j*worm_width/50 + worm_width/100
                    rect.center = (x, y - j*pos_diff)
                    display_surface.blit(scaled_hole_segment, rect)
            

        # Sky
        sky.blit(t_end, display_surface)

        # Dune Mountains

        for i in range(num_mountains-1, -1, -1):
            im = pygame.transform.scale(mountain_im[mountains[i][0]], mountains[i][1])
            rect = im.get_rect()
            rect.center = (mountains[i][2], sand_height-mountains[i][1][1]/2)
            display_surface.blit(im, rect)
            if mountains[i][2] < -1*mountains[i][1][0]/2:
                scale = (randint(min_size*2, min_size*3), randint(min_size, min_size*1.5))
                mountains[i] = [randint(0,len(mountain_im)-1), scale, width+scale[0]/2]
            else:
                mountains[i][2] -= 2*(1-t_end)


        # Obstacles
        
        for i in range(len(obstacles)):
            if obstacles[i][1] <= width*1.2 and obstacles[i][1] >= -0.4*width:
                ob = obstacles[i][0]
                x = obstacles[i][1]
                y = sand_height
                val = obstacles[i][2]
                
                if not ob.hit:
                    ob.update(300, (x,y), (worm_head_x, worm_head_y), worm_width)
                    ob.blit(display_surface)
                    if ob.hit:
                        health -= 0.1
                else:
                    val+=0.09
                    if val > 1:
                        val = 1

                    ob.hit_update(300, (x,y), val)
                    if t_end<1:
                        ob.blit(display_surface)
                    obstacles[i][2] = val
            obstacles[i][1]-=10*(1-t_end)

        # Vessels

        for i in range(len(vessels)):
            if vessels[i][1] <= width and not vessels[i][0].done:
                vessels[i][0].over_step((worm_head_x, worm_head_y), worm_width)
                vessels[i][0].blit(display_surface)
            vessels[i][1]-=10*(1-t_end)

        # Bombs 

        for i in range(len(bombs)):
            if bombs[i][1] <= width*1.2 and bombs[i][1] >= -0.4*width:
                bomb = bombs[i][0]
                x = bombs[i][1]
                y = bombs[i][2]
                val = bombs[i][3]
                
                if not bomb.hit:
                    bomb.update(100, (x,y), (worm_head_x, worm_head_y), worm_width)
                    bomb.blit(display_surface)
                    if bomb.hit:
                        health -= 0.2
                else:
                    if val == -1:
                        val = 0
                    elif val>13:
                        val = 13

                    bomb.hit_update(100, (x,y), val)
                    if t_end<1:
                        bomb.blit(display_surface)
                    val+=0.5
                    bombs[i][3] = val
            bombs[i][1]-=10*(1-t_end)

        # Mines

        for i in range(len(mines)):
            if mines[i][1] <= width*1.2 and mines[i][1] >= -0.4*width:
                mine = mines[i][0]
                x = mines[i][1]
                y = mines[i][2]
                val = mines[i][3]
                
                if not mine.hit:
                    mine.update(100, (x,y), (worm_head_x, worm_head_y), worm_width)
                    mine.blit(display_surface)
                    if mine.hit:
                        health -= 0.2
                else:
                    if val == -1:
                        val = 0
                    elif val>15:
                        val = 15

                    mine.hit_update(100, (x,y), val)
                    if t_end<1:
                        mine.blit(display_surface)
                    val+=0.5
                    mines[i][3] = val
            mines[i][1]-=10*(1-t_end)
        
        # Dust
        if worm_head_y < (sand_height + (worm_width/2)) and worm_head_y >= (sand_height - (worm_width/2)) and t_end<1:
            dust[0] = [True, randint(0,len(dust_im)-1), randint(100, 150), 0]
        else:
            dust[0] = [False, 0, 0, 0]

        
        

        for i in range(len(dust)):
            if dust[i][0]:
                im = pygame.transform.scale(dust_im[dust[i][1]], (dust[i][2], dust[i][2]))
                rect = im.get_rect()
                alpha = dust[i][3]
                if i>0:
                    im.set_alpha((100-i)/2)
                else:
                    im.set_alpha(155)
                dust[i][3] += 1
                rect.center = (worm_head_x-i*10, sand_height-(dust[i][2]/2)+(hole_scale_factor-1)*worm_width)
                display_surface.blit(im, rect)
        
        new_dust = [[False, 0, 0, 0]]
        for i in range(0, len(dust)-1):
            new_dust.append(dust[i])
        dust = new_dust.copy()
        
        # Worm Head
        rect = worm_head[mouth_pos].get_rect()
        rect.center = (worm_head_x, worm_head_y)
        display_surface.blit(worm_head[mouth_pos], rect)

        # Worm Body
        for i in range (len(segments)):
            pos_diff = 0
            if i==0:
                pos_diff = (segments[i][1] - worm_head_y)/10
            else:
                pos_diff = (segments[i][1] - segments[i-1][1])/10
            
            for j in range(10):
                scale_factor_y = pos_diff
                scaled_worm_segment = pygame.transform.scale(worm_segments[j], (worm_width/50, worm_width+scale_factor_y))
                rect = scaled_worm_segment.get_rect()
                (x, y) = segments[i]
                x = x - (worm_width/10) + j*worm_width/50 + worm_width/100
                rect.center = (x, y - j*pos_diff)
                display_surface.blit(scaled_worm_segment, rect)
        # Character
        character_x = worm_head_x - worm_width/2
        character_y = worm_head_y - worm_width/2
        character.mounted_update(50, (character_x, character_y), worm_head_y_diff)
        character.blit(display_surface)

        # Segment Position update
        for i in range(len(segments)-1, -1, -1):
            if i==0:
                segments[i][1] = worm_head_y
            else:
                segments[i][1] = segments[i-1][1]

        # Health Bar

        health_bar.update(400, (width/2, 60), health)
        health_bar.blit(display_surface)

        im = game_over_im
        im.set_alpha(t_end*255)
        rect = im.get_rect()
        rect.center = (width/2, height/2)
        display_surface.blit(im, rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    
    pygame.init()
    width = 1440
    height = 800
    display_surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Parallel Insurgence')
    run_game(width, height, display_surface)
