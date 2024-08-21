import pygame
from pygame.locals import VIDEORESIZE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, K_t, K_r, K_s, K_c, K_p, K_d, K_f

import numpy
import chunks
import display_mod

#The player
class player(pygame.sprite.Sprite):
    def __init__(self,spawn_loc_x,spawn_loc_y):
        super(player,self).__init__()
        self.color = ((255,255,255))
        self.joints = [['body',spawn_loc_x-chunks.block_size*0.5,spawn_loc_y+chunks.block_size*0.5]]
        #Each of the player's parts needs to bounce off things individually, but once that bounce gets too big, it should also affect the rest of the player's parts.
        self.rects = [pygame.Rect(self.joints[0][1],self.joints[0][2],chunks.block_size,chunks.block_size)]
        self.run_strength = chunks.block_size*3/4
        self.run_speed = self.run_strength
        self.jump_endurance = chunks.block_size*8
        self.jump_strength = self.jump_endurance
        self.jump_speed = self.jump_endurance/8
        self.fly_endurance = chunks.block_size*3
        self.fly_strength = self.fly_endurance
        self.fly_speed = chunks.block_size/8
        self.flexibility = 3 #how far away a body part can be before starting to drag back into place.
        self.magic_reach = self.rects[0].x*2,self.rects[0].y*2

    def draw(self, display):
        for sr in range(len(self.rects)): #sr stands for self_rect
            pygame.draw.rect(display_mod.display,self.color,self.rects[sr])

    def center(self,window_centerx,window_centery):
        for sr in range(len(self.rects)):
            self.rects[sr].centerx = window_centerx
            self.rects[sr].centery = window_centery

    def move(self,keypressed,block_rects,gravity,movement_x,movement_y):
        lb = False
        tb = False
        rb = False
        bb = False
        #I need to come up with some clean collision framework. For one thing, the player will have multiple body parts, so each part has to react differently, and then they have to react as a whole as well.
        #For another thing, the collisions have to make physical sense. Like if your momentum is going left and then you collide with something, your momentum should flip directions.
        for sr in range(len(self.rects)):
            srlb = pygame.Rect(self.rects[sr].left-1,self.rects[sr].top,1,self.rects[sr].height) #self_rect_left_boundary
            srtb = pygame.Rect(self.rects[sr].left,self.rects[sr].top+1,self.rects[sr].width,1)
            srrb = pygame.Rect(self.rects[sr].right,self.rects[sr].top,1,self.rects[sr].height)
            srbb = pygame.Rect(self.rects[sr].left,self.rects[sr].bottom,self.rects[sr].width,1)
            for block in block_rects['solid']['all']:
                #If the player isn't being accelerated by an outside force:
                #Should I make the player incapable of movement for a short time after collisions? Probably not
                #First, check what the player's rects are currently colliding with.
                if srlb.colliderect(block):
                    lb = True
                if srrb.colliderect(block):
                    rb = True
                if srtb.colliderect(block):
                    tb = True
                if srbb.colliderect(block):
                    bb = True
            #Second, if a player's rect is embedded, reduce its speed.
            #if (lb and rb) or (tb and bb):
            #    self.run_speed = self.run_strength*0.25
            if not bb:
                if self.fly_strength >= -gravity*100:
                    self.fly_strength -= gravity/4
                if self.jump_strength >= -gravity*100:
                    self.jump_strength -= gravity/4
            elif bb:
                self.fly_strength = self.fly_endurance
                self.jump_strength = self.jump_endurance
                #print(f'{lb,tb,rb,bb}')
            #I'm not sure why, but you have to check the blocks again after the boundaries have been established, instead of immediately checking them against the same block that establishes the boundaries.            
            for block in block_rects['solid']['all']:
                if srlb.colliderect(block):
                    if block.right > srlb.left:
                        movement_x = self.rects[sr].clip(block).width
                if srrb.colliderect(block):
                    if block.left < srrb.right:
                        movement_x = -self.rects[sr].clip(block).width
                if srtb.colliderect(block):
                    if block.bottom < srtb.top:
                        movement_y = -self.rects[sr].clip(block).height
                if srbb.colliderect(block):
                    if block.top < srbb.bottom:
                        movement_y = self.rects[sr].clip(block).height
                        #print(f'grounded 1: {self.rects[sr].clip(block).height}')

        
        if bb: #friction
            movement_x = movement_x*0.5
            movement_y = movement_y*0.5
        if not bb: #air resistance
            if keypressed[K_f] and self.fly_strength > 0:#flying
                movement_y = movement_y*0.9
            if keypressed[K_f] and self.fly_strength <= 0:#gliding with no more strength to fly
                movement_x = movement_x*0.9
                if movement_y > 0:
                    movement_y = movement_y*0.8 - gravity
                if -gravity*200 < movement_y <= 0:#falling downward
                    movement_y -= gravity
            if not keypressed[K_f]:#falling with some upward speed
                movement_x = movement_x*0.5
                if movement_y > 0:
                    movement_y = movement_y*0.5 - gravity
                if -gravity*200 < movement_y <= 0:#falling downward
                    movement_y -= gravity
        
        if keypressed[K_LEFT]:
            if not bb and not lb and keypressed[K_f] and self.fly_strength>0: #flying left
                movement_x += -self.fly_speed
            if not bb and not lb and self.jump_strength>0: #jumping left
                movement_x = -self.jump_speed
            if bb and not lb: #running left
                movement_x = -self.run_speed
            if bb and lb and keypressed[K_d]: #digging left
                movement_x = -self.run_speed*0.5

        if keypressed[K_RIGHT]:
            if not bb and not rb and keypressed[K_f] and self.fly_strength>0: #flying right
                movement_x += self.fly_speed
            if not bb and not rb and self.jump_strength>0: #jumping right
                movement_x = self.jump_speed
            if bb and not rb: #running right
                movement_x = self.run_speed
            if bb and rb and keypressed[K_d]: #digging right
                movement_x = self.run_speed*0.5

        if keypressed[K_DOWN] and (keypressed[K_d] or not bb):
            if not bb and keypressed[K_f] and not self.fly_strength<0:
                movement_y = -self.fly_speed
            if bb and keypressed[K_d]:
                movement_y = -self.run_speed*0.5

        if keypressed[K_UP]:
            if not tb and keypressed[K_f] and not self.fly_strength<0:
                movement_y += self.fly_speed
            if tb and keypressed[K_d]:
                movement_y = self.run_speed*0.5
            if bb and not tb:
                movement_y = self.jump_speed

        return movement_x,movement_y
    