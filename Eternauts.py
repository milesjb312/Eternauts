#Operational Imports (These come from python modules that I either imported at the beginning or were auto-imported for some reason.)
import pygame
from pygame import font
import chunks
pygame.init()

#Input and Event Imports:
from pygame.locals import VIDEORESIZE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, K_t, K_r, K_s, K_c, K_p

#Display Initialization
pygame.display.set_caption("Eternauts Physics Engine 1.2")
display = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
screen_width, screen_height = pygame.display.get_window_size()

#HUD Initialization
font.init()
font_size = 20
wod_font = font.SysFont(None,font_size)

#The player
class player(pygame.sprite.Sprite):
    def __init__(self,spawn_loc_x,spawn_loc_y):
        super(player,self).__init__()
        self.Surface = pygame.Surface((30,30))
        self.Surface.fill((255,255,255))
        self.rect = self.Surface.get_rect()
        self.rect = self.Surface.get_rect()
        self.rect.center = (spawn_loc_x,spawn_loc_y)
        self.fly_strength = chunks.block_size*2/3
        self.fly_endurance = chunks.block_size/3
        self.fly_time = self.fly_endurance
        self.bounce_book = {'bounce_x':0,'bounce_y':0}
        self.bouncing = False
        self.digging = False
        self.swimming = False
        self.run_strength = chunks.block_size/2

    def update_collision_rects(self):
        self.rect_inf_top = pygame.Rect(self.rect.left,self.rect.top-self.rect.height/10,self.rect.width,self.rect.height/10)
        self.rect_inf_right = pygame.Rect(self.rect.right,self.rect.top,self.rect.width/10,self.rect.height)
        self.rect_inf_bottom = pygame.Rect(self.rect.left,self.rect.bottom,self.rect.width,self.rect.height/10)
        self.rect_inf_left = pygame.Rect(self.rect.left-self.rect.width/10,self.rect.top,self.rect.width/10,self.rect.height)  

    def draw(self, display):
        display.blit(player_1.Surface, player_1.rect)
        pygame.draw.rect(display, (200,0,0),player_1.rect_inf_top)
        pygame.draw.rect(display, (200,0,0),player_1.rect_inf_right)
        pygame.draw.rect(display, (200,0,0),player_1.rect_inf_bottom)
        pygame.draw.rect(display, (200,0,0),player_1.rect_inf_left)

#Render HUD
def render_hud():
    wod_text = f'WOD:{wod[0],wod[1]}'
    wod_text_surface = wod_font.render(wod_text,True,(255,255,255))
    hud_surface = pygame.Surface((wod_text_surface.get_width(),wod_text_surface.get_height()))
    hud_surface.fill((0,0,0))
    hud_surface.blit(wod_text_surface,(0,0))
    return hud_surface

#GAME ENGINE:
#import save_and_load

#TIME
#This is just some code specific to pygame that allows you to manage a game easily.
running = True
clock = pygame.time.Clock()

#SPACE
#Movement
'''
Movement works first by establishing what bounds are around the player. Then, based on which bounds are currently being occupied,
the movement state of the player is determined, between swimming, running, or flying. That state is passed to the main game loop,
which will run whichever movement function should currently be active.
'''
#This allows you to update the wod (standing for world origin distance), making it appear as though the player is moving.
#All objects' locations are defined based on their own wod.

#THIS IS WHERE I NEED TO WORK NEXT TO MAKE IT SO THAT THE GAME CHECKS WHETHER YOU'RE RUNNING INTO SOLIDS OR LIQUIDS.
#This is like the biggest physics driver of the game, to be honest.
def check_bounds(player_rect,player_rect_inf,player_rect_inf_top,player_rect_inf_right,player_rect_inf_bottom,player_rect_inf_left,all_blocks,bounce_book,bouncing,digging,swimming,movement_x,movement_y):
    #This function returns: top_bound,right_bound,bottom_bound,left_bound,bouncing,digging,swimming,top_wet
    close_solid_blocks = [block for block in all_blocks['solid'] if player_rect_inf.colliderect(block)]
    close_liquid_blocks = [block for block in all_blocks['liquid'] if player_rect_inf.colliderect(block)]
    #close_gas_blocks = [block for block in all_blocks['gas'] if player_rect_inf.colliderect(block)]
    #colliding_blocks = []

    #initial values
    bouncing = bouncing
    digging = digging
    swimming = swimming
    bounce_rect = None
    top_bound = False
    right_bound = False
    left_bound = False
    bottom_bound = False
    top_wet = False
    right_wet = False
    left_wet = False
    bottom_wet = False

    #Check all the solid blocks for collisions
    for block in close_solid_blocks:
        #Check whether a player is hitting something on the side
        if (player_rect_inf_top.colliderect(block)):
            top_bound = True
        if (player_rect_inf_right.colliderect(block)):
            right_bound = True
        if (player_rect_inf_left.colliderect(block)):
            left_bound = True
        if (player_rect_inf_bottom.colliderect(block)):
            bottom_bound = True
        #If a player is hitting something just on the side, then adjust the bounce_book.
        bounce_rect = player_rect.clip(block)
        if bottom_bound and top_bound:
            bounce_book['bounce_y'] = 0
        elif top_bound and not bottom_bound:
            bounce_book['bounce_y'] = -abs(bounce_rect.height)
        elif bottom_bound and not top_bound:
            bounce_book['bounce_y'] = abs(bounce_rect.height)
        if right_bound and left_bound:
            bounce_book['bounce_x'] = 0
        elif right_bound and not left_bound:
            bounce_book['bounce_x'] = -abs(bounce_rect.width)
        elif left_bound and not right_bound:
            bounce_book['bounce_x'] = abs(bounce_rect.width)

        #If a player is buried somewhat in a block, then dig. Otherwise, if they're just hitting a block, bounce.
        #Definitely take another look at these conditionals
        if player_rect.colliderect(block) and (abs(bounce_rect.width) >= player_rect.width/2 or abs(bounce_rect.height) >= player_rect.height/2):
            digging = True
            bouncing = False
        elif player_rect.colliderect(block) and abs(bounce_rect.width) < player_rect.width/2 and abs(bounce_rect.height) < player_rect.height/2 and (movement_x != 0 or movement_y != 0):
            bouncing = True
        if not top_bound and not right_bound and not left_bound and not player_rect.colliderect(block):
            digging = False
            bouncing = False

    #Check all liquid blocks for collisions
    for block in close_liquid_blocks:
        if (player_rect_inf_top.colliderect(block)):
            top_wet = True
        if (player_rect_inf_bottom.colliderect(block)):
            bottom_wet = True
        if (player_rect_inf_right.colliderect(block)):
            right_wet = True
        if (player_rect_inf_left.colliderect(block)):
            left_wet = True
        if player_rect.colliderect(block) or (top_wet and right_wet) or (top_wet and left_wet) or (bottom_wet and right_wet) or (bottom_wet and left_wet):
            swimming = True
        if not top_wet and not right_wet and not left_wet and not player_rect.colliderect(block):
            swimming = False

        """
    for block in close_gas_blocks:
        if (player_rect_inf_top.colliderect(block)):
            top_bound = True
        if (player_rect_inf_bottom.colliderect(block)):
            bottom_bound = True
        if (player_rect_inf_right.colliderect(block)):
            right_bound = True
        if (player_rect_inf_left.colliderect(block)):
            left_bound = True
        if player_rect.colliderect(block) or (top_bound and right_bound) or (top_bound and left_bound) or (bottom_bound and right_bound) or (bottom_bound and left_bound):
            breathing = True
        """

    return top_bound,right_bound,bottom_bound,left_bound,bouncing,digging,swimming,top_wet

def bounce(bounce_book,player_rect,movement_x=None,movement_y=None):
    movement_x = movement_x
    movement_y = movement_y
    if movement_x != 0 and movement_y == 0:
        if bounce_book['bounce_x'] != 0:
            movement_x = bounce_book['bounce_x']
        elif bounce_book['bounce_x'] == 0:
            if bounce_book['bounce_y'] < player_rect.height/2:
                movement_y = -bounce_book['bounce_y']
#    elif movement_x != 0 and movement_y != 0:
    if movement_y != 0:
        if bounce_book['bounce_y'] != 0:
            movement_y = bounce_book['bounce_y']
        elif bounce_book['bounce_y'] == 0:
            if bounce_book['bounce_x'] < player_rect.width/2:
                movement_x = bounce_book['bounce_x']
    return movement_x,movement_y
    
def dig(top_bound,right_bound,bottom_bound,left_bound,run_strength,keypressed=None,movement_x=None,movement_y=None):
    movement_x = 0
    movement_y = 0
    if keypressed[K_LEFT]:
        if not left_bound:
            movement_x = -run_strength
        elif left_bound:
            movement_x = -run_strength/2
    if keypressed[K_RIGHT]:
        if not right_bound:
            movement_x = run_strength
        elif right_bound:
            movement_x = run_strength/2
    if keypressed[K_DOWN]:
        if not bottom_bound:
            movement_y = -run_strength
        elif bottom_bound:
            movement_y = -run_strength/2
    if keypressed[K_UP]:
        if not top_bound:
            movement_y = run_strength
        elif top_bound:
            movement_y = run_strength/2

    return movement_x,movement_y


def run(right_bound,bottom_bound,left_bound,run_strength,fly_endurance,fly_time,keypressed=None,movement_x=None):    
    movement_x = 0
    movement_y = 0
    fly_time = fly_endurance

    if keypressed[K_LEFT]:
        if not left_bound:
            movement_x = -1*run_strength
    if keypressed[K_RIGHT]:
        if not right_bound:
            movement_x = run_strength
    if bottom_bound:
        movement_y = 0
        if keypressed[K_UP]:
            movement_y += 8
    return movement_x,movement_y,fly_time

def swim(top_wet,movement_x,movement_y,keypressed=None):
    movement_x = movement_x
    movement_y = movement_y
    if top_wet:
        movement_y += 0.5
    if keypressed[K_LEFT]:
        if not movement_x < -10:
            movement_x += -1.25
    if keypressed[K_RIGHT]:
        if not movement_x > 10:
            movement_x += 1.25
    if keypressed[K_DOWN]:
        if not movement_y < -10:
            movement_y += -1.25
    if movement_y >= 7.5:
        movement_y -= 1.25    
    if movement_y <= -7.5:
        movement_y += 1.25
    if movement_x > 0:
        movement_x -= 0.0625
    elif movement_x < 0:
        movement_x += 0.0625
    return movement_x,movement_y

def fly(top_bound,right_bound,bottom_bound,left_bound,fly_strength,fly_endurance,fly_time,movement_x,movement_y,keypressed=None):
    movement_x = movement_x
    movement_y = movement_y
    if not bottom_bound and not movement_y < -fly_strength:
        movement_y -= 5
    elif bottom_bound:
        movement_y = 0
    if keypressed[K_LEFT]:
        if not left_bound and not movement_x < fly_strength*-1:
            movement_x += -6
    if keypressed[K_RIGHT]:
        if not right_bound and not movement_x > fly_strength:
            movement_x += 6
        
    if 0 < fly_time <= fly_endurance:
        if keypressed[K_UP]:
            if not top_bound and not movement_y > fly_strength:
                movement_y += 6
                fly_time -= 1
    return movement_x,movement_y,fly_time

#Initializations:
wod = [0,0] #world origin distance
player_1 = player(screen_width//2,screen_height//2)
player_1.update_collision_rects()

movement_x = 0
movement_y = 0

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
            elif event.key == K_p:
                if (wod[0]//chunks.pixel_total*chunks.pixel_total,wod[1]//chunks.pixel_total*chunks.pixel_total) in chunks.chunk_book:
                    print(f'chunk_book[cwod]:{chunks.chunk_book[(wod[0]//chunks.pixel_total*chunks.pixel_total,-wod[1]//chunks.pixel_total*chunks.pixel_total)]}')
        elif event.type == QUIT:
            running = False
        
        #Display handler
        elif event.type == VIDEORESIZE:
            old_screen_width, old_screen_height,old_wod = screen_width,screen_height,wod
            screen_width,screen_height = event.w, event.h

            wod[0] = old_wod[0] - (screen_width - old_screen_width) //2
            wod[1] = old_wod[1] + (screen_height - old_screen_height) //2

            player_1.rect.centerx += (screen_width - old_screen_width) //2
            player_1.rect.centery += (screen_height - old_screen_height) //2
            player_1.update_collision_rects()
            

    #Drawing updates
    display.fill((10, 130, 255))
    chunks.draw_chunks(block_rects,display)
    
    #Movement
    keypressed = pygame.key.get_pressed()

    #THIS IS THE NEXT THING I NEED TO FIX! I have to make it so that, instead of bounds checking only the solid block_rects, it checks both solid and liquids.
    #Determine the player's current movement type.
    bounds = check_bounds(player_1.rect,(player_1.rect.inflate(10,10)),player_1.rect_inf_top,player_1.rect_inf_right,player_1.rect_inf_bottom,player_1.rect_inf_left,block_rects,player_1.bounce_book,player_1.bouncing,player_1.digging,player_1.swimming,movement_x,movement_y)
    #check_bounds(player_rect,player_rect_inf,player_rect_inf_top,player_rect_inf_right,player_rect_inf_bottom,player_rect_inf_left,all_blocks,bounce_book,bouncing,digging,swimming):
    #This function returns: top_bound,right_bound,bottom_bound,left_bound,bouncing,digging,swimming,top_wet
    if bounds[4]:
        movement_x,movement_y = bounce(player_1.bounce_book,player_1.rect,movement_x,movement_y)
        #print(f'bouncing,bounce_book:{player_1.bounce_book}')
    elif bounds[5]:
        movement_x,movement_y = dig(bounds[0],bounds[1],bounds[2],bounds[3],player_1.run_strength,keypressed,movement_x,movement_y)
        #print('digging')
    elif bounds[6]:
        movement_x,movement_y = swim(bounds[7],movement_x,movement_y,keypressed)
        #print('swimming')
    elif bounds[2]:    
        movement_x,movement_y,player_1.fly_time = run(bounds[1],bounds[2],bounds[3],player_1.run_strength,player_1.fly_endurance,player_1.fly_time,keypressed)
        #print('running')
    else:
        movement_x,movement_y,player_1.fly_time = fly(bounds[0],bounds[1],bounds[2],bounds[3],player_1.fly_strength,player_1.fly_endurance,player_1.fly_time,movement_x,movement_y,keypressed)
        #print('flying')
    wod[0] += movement_x
    wod[1] += movement_y
                        
    #People
    player_1.draw(display)
    
    #HUD
    hud_surface = render_hud()
    display.blit(hud_surface,(screen_width-hud_surface.get_width(),0))
    
    pygame.display.flip()
    clock.tick(35)