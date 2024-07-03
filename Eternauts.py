#Operational Imports (These come from python modules that I either imported at the beginning or were auto-imported for some reason.)
import pygame
from pygame import font
import chunks
pygame.init()

#Input and Event Imports:
from pygame.locals import VIDEORESIZE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, K_t, K_r, K_s, K_c, K_p, K_LSHIFT

#Display Initialization
pygame.display.set_caption("Eternauts Physics Engine 1.2")
display = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
screen_width, screen_height = pygame.display.get_window_size()

#HUD Initialization
font.init()
font_size = 20
wod_font = font.SysFont(None,font_size)

#World
gravity = 1

#The player
class player(pygame.sprite.Sprite):
    def __init__(self,spawn_loc_x,spawn_loc_y):
        super(player,self).__init__()
        self.color = ((255,255,255))
        self.joints = {'body':[spawn_loc_x-chunks.block_size*0.5,spawn_loc_y-chunks.block_size*0.5],
                       'right_arm':[spawn_loc_x+chunks.block_size*0.5,spawn_loc_y-chunks.block_size*0.5],
                       'left_arm':[spawn_loc_x-chunks.block_size*1.5,spawn_loc_y-chunks.block_size*0.5]}
        #Each of the player's parts needs to bounce off things individually, but once that bounce gets too big, it should also affect the rest of the player's parts.
        self.rects = {'body':pygame.Rect(self.joints['body'][0],self.joints['body'][1],chunks.block_size,chunks.block_size),
                      'right_arm':pygame.Rect(self.joints['right_arm'][0],self.joints['right_arm'][1],chunks.block_size,chunks.block_size),
                      'left_arm':pygame.Rect(self.joints['left_arm'][0],self.joints['left_arm'][1],chunks.block_size,chunks.block_size)}
        self.run_strength = chunks.block_size/2
        self.fly_endurance = chunks.block_size*2
        self.fly_strength = self.fly_endurance
        self.flexibility = 3 #how far away a body part can be before starting to drag back into place.
        self.magic_reach = self.rects['body'].x*2,self.rects['body'].y*2

    def draw(self, display):
        for sr in self.rects: #sr stands for self_rect
            pygame.draw.rect(display,player_1.color,self.rects[sr])

    def move(self,keypressed,all_blocks,movement_x,movement_y):
        run_speed = self.run_strength
        fly_speed = self.fly_strength
        lb = False
        tb = False
        rb = False
        bb = False
        #I need to come up with some clean collision framework. For one thing, the player will have multiple body parts, so each part has to react differently, and then they have to react as a whole as well.
        #For another thing, the collisions have to make physical sense. Like if your momentum is going left and then you collide with something, your momentum should flip directions.
        for sr in self.rects: 
            srlb = pygame.Rect(self.rects[sr].left-1,self.rects[sr].top,1,self.rects[sr].height) #self_rect_left_boundary
            srtb = pygame.Rect(self.rects[sr].left,self.rects[sr].top+1,self.rects[sr].width,1)
            srrb = pygame.Rect(self.rects[sr].right,self.rects[sr].top,1,self.rects[sr].height)
            srbb = pygame.Rect(self.rects[sr].left,self.rects[sr].bottom,self.rects[sr].width,1)
            for block in all_blocks['solid']['all']:
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
                    #print(f'Ground block top: {block.top}, Self block bottom boundary: {srbb.bottom}')
            #Second, if a player's rect is embedded, reduce its speed.
            if (lb and rb) or (tb and bb):
                run_speed = self.run_strength*0.25
            if not bb:
                self.fly_strength -= 1
                print(f'fly_speed: {self.fly_strength}')
            elif bb:
                self.fly_strength = self.fly_endurance
                #print(f'{lb,tb,rb,bb}')
            #I'm not sure why, but you have to check the blocks again after the boundaries have been established, instead of immediately checking them against the same block that establishes the boundaries.            
            for block in all_blocks['solid']['all']:
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

        if not bb:
            movement_x = movement_x*0.7
            movement_y = movement_y*0.7
        elif bb:
            movement_x = movement_x*0.5
            movement_y = movement_y*0.5

        if keypressed[K_LEFT] and (not lb or keypressed[K_LSHIFT]):
            if not bb:
                movement_x += -run_speed
            elif bb:
                movement_x = -run_speed            
        if keypressed[K_RIGHT] and (not rb or keypressed[K_LSHIFT]):
            if not bb:
                movement_x += run_speed
            elif bb:
                movement_x = run_speed
        if keypressed[K_DOWN] and (not bb or keypressed[K_LSHIFT]):
            movement_y = -run_speed
        if keypressed[K_UP] and (not tb or keypressed[K_LSHIFT]) and fly_speed > 0:
            movement_y = run_speed
        elif (not keypressed[K_UP] and self.fly_strength <= 0) or not bb: #There's something wrong with this statement
            movement_y = -run_speed
        return movement_x,movement_y

#Render HUD
def render_hud():
    #wod stands for world origin distance
    wod_text = f'WOD:{round(wod[0]),round(wod[1])}'
    wod_text_surface = wod_font.render(wod_text,True,(255,255,255))
    hud_surface = pygame.Surface((wod_text_surface.get_width(),wod_text_surface.get_height()))
    hud_surface.fill((0,0,0))
    hud_surface.blit(wod_text_surface,(0,0))
    return hud_surface

#GAME ENGINE:
#pygame stuff...
running = True
clock = pygame.time.Clock()

#This allows you to update the wod (standing for world origin distance), making it appear as though the player is moving.
#All objects' locations are defined based on their own wod.
#This code works a little. I need it to somehow be a lot smoother. I need to make it so that collisions slowly push you out of a block if you run into the block slowly. And I need it so that if you are embedded in a block already, there is no bounce, just resistance. How to distinguish between embedding and bouncing?

"""
#THIS PART OF THE CODE DOESN'T WORK YET
def break_block(block_rects,block_loc):
    #This part is TOUGH. I have to reverse engineer my block location generator.
    break_block_loc = [wod[0] + block_loc[0],wod[1] + block_loc[1]]
    for type,sub_type in block_rects.items():
        for block_rects_list in sub_type.values():
            for block_rect in block_rects_list:
                if (block_rect.x,block_rect.y) == break_block_loc:
                    block_rects[type[sub_type[block_rects_list]]].remove(block_rect)
"""

#Initializations:
wod = [0,0] #world origin distance
player_1 = player(screen_width//2,screen_height//2) #By defining the player's spawn_loc this way, I get to make sure it always stays in the center of the screen.

movement_x = 0
movement_y = 0

break_block_bool = False
break_block_loc = [0,0]

while running:
    #Chunks
    block_rects = chunks.make_chunks(wod,display)
    #Game Save and End Loop
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                print(f'Thanks for playing! Now go out and do some good!')
            elif event.key == K_s:
                #save_and_load.save()
                pass
            #This next line is just for play-testing
            elif event.key == K_p:
                if (wod[0]//chunks.pixel_total*chunks.pixel_total,wod[1]//chunks.pixel_total*chunks.pixel_total) in chunks.chunk_book:
                    print(f'chunk_book[cwod]:{chunks.chunk_book[(wod[0]//chunks.pixel_total*chunks.pixel_total,-wod[1]//chunks.pixel_total*chunks.pixel_total)]}')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            break_block_tup = pygame.mouse.get_pos()
            break_block_bool = True
            break_block_loc = [break_block_tup[0],break_block_tup[1]]
            break_block_loc[0] = break_block_loc[0]//chunks.block_size*chunks.block_size
            break_block_loc[1] = break_block_loc[1]//chunks.block_size*chunks.block_size
        elif event.type == QUIT:
            running = False
        
        #Display handler
        elif event.type == VIDEORESIZE:
            old_screen_width, old_screen_height,old_wod = screen_width,screen_height,wod
            screen_width,screen_height = event.w, event.h

            wod[0] = old_wod[0] - (screen_width - old_screen_width)//2
            wod[1] = old_wod[1] + (screen_height - old_screen_height)//2
            for s_rect in player_1.rects:
                player_1.rects[s_rect].centerx += (screen_width - old_screen_width)//2
                player_1.rects[s_rect].centery += (screen_height - old_screen_height)//2      

    #Drawing updates
    display.fill((10, 130, 255))
    chunks.draw_chunks(block_rects,display)
    
    #Movement
    keypressed = pygame.key.get_pressed()

    #Determine the player's current movement type.
    movement_x,movement_y = player.move(player_1,keypressed,block_rects,movement_x,movement_y)
    
    wod[0] += movement_x
    wod[1] += movement_y

    #if break_block_bool:
    #    break_block(block_rects,break_block_loc)

    #People
    player_1.draw(display)
    
    #HUD
    hud_surface = render_hud()
    display.blit(hud_surface,(screen_width-hud_surface.get_width(),0))
    
    pygame.display.flip()
    clock.tick(35)