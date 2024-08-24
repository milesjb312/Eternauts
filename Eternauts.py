#Operational Imports (These come from python modules that I either imported at the beginning or were auto-imported for some reason.)
import pygame
from pygame.locals import VIDEORESIZE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, K_c, K_h, K_p, K_r, K_s, K_t, K_LSHIFT,K_m

import chunks
import player_mod
import display_mod


#GAME ENGINE:
#pygame stuff...
running = True
clock = pygame.time.Clock()
gravity = chunks.chunk_size/8
window_width,window_height = pygame.display.get_window_size()

#Initializations:
wod = [0,0] #world origin distance
#All objects' locations are defined based on their own Distance to the World Origin.
player_1 = player_mod.player(window_width//2,window_height//2) #By defining the player's spawn_loc this way, I get to make sure it always stays in the center of the window.

movement_x = 0
movement_y = 0

break_block_bool = False
break_block_loc = [0,0]
window_shiftx = 0
window_shifty = 0

while running:
    #Chunks
    block_rects = chunks.make_chunks(wod,window_shiftx,window_shifty) #to this, add a variable that represents the shifting distance for changing window size
    cwod = wod[0]//chunks.pixel_total*chunks.pixel_total,-wod[1]//chunks.pixel_total*chunks.pixel_total
    #Game loop
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                print(f'Thanks for playing! Now go out and do some good!')
            #elif event.key == K_s:
                #save_and_load.save()
            #    pass
            #This next line is just for play-testing
            #elif event.key == K_m:
                #print(f'matter_shapes: {matter_shapes}')
        elif event.type == QUIT:
            running = False
        #Display Handler (moving and resizing the window)
        elif event.type == VIDEORESIZE:
            window_width,window_height = pygame.display.get_window_size()
            window_shiftx,window_shifty = display_mod.videoresize()
            player_1.center(window_width//2,window_height//2)
            #possibly reinitialize player here or just tell player to move to center

    #Movement
    keypressed = pygame.key.get_pressed()
    movement_x,movement_y = player_mod.player.move(player_1,keypressed,block_rects,gravity,movement_x,movement_y)  
    wod[0] += movement_x
    wod[1] += movement_y
    if keypressed[K_h]:
        wod[0] = 0
        wod[1] = 0

    #if keypressed[K_c]:
    #    print(f'chunk_book: {chunks.chunk_book[cwod]}')

    #Block interaction
    if event.type == pygame.MOUSEBUTTONDOWN:
        break_block_tup = pygame.mouse.get_pos()
        chunks.break_block(break_block_tup,[window_width//2,window_height//2],wod) 

    chunks.move_matter(wod,block_rects,gravity,[window_width//2,window_height//2])

    #Drawing updates
    display_mod.display.fill((10, 130, 255))#erase the last frame.
    chunks.draw_blocks(block_rects,display_mod.display)#draw all the blocks.
    chunks.draw_matter(chunks.matter_list,display_mod.display)
    player_1.draw(display_mod)#draw the player
    hud_surface = display_mod.render_hud(wod)#draw the hud
    display_mod.display.blit(hud_surface,(window_width-hud_surface.get_width(),0))
    pygame.display.flip()
    clock.tick(35)