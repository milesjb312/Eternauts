#Display Initialization
import pygame
from pygame import font
import pywinctl
import chunks
import player_mod
pygame.display.set_caption("Eternauts 1.2")
display = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
width,height = pygame.display.get_window_size()
window = pywinctl.getWindowsWithTitle("Eternauts 1.2")
left = window[0].left
top = window[0].top
window_shiftx = 0
window_shifty = 0

#HUD Initialization
font.init()
font_size = 20
wod_font = font.SysFont(None,font_size)

#Render HUD
def render_hud(wod):
    #wod stands for world origin distance
    wod_text = f'WOD:{round(wod[0]),round(wod[1])}'
    wod_text_surface = wod_font.render(wod_text,True,(255,255,255))
    hud_surface = pygame.Surface((wod_text_surface.get_width(),wod_text_surface.get_height()))
    hud_surface.fill((0,0,0))
    hud_surface.blit(wod_text_surface,(0,0))
    return hud_surface

def videoresize():
    global left
    global top
    global width
    global height
    global window_shiftx
    global window_shifty
    new_window = pywinctl.getWindowsWithTitle("Eternauts 1.2")
    new_left = new_window[0].left
    new_top = new_window[0].top
    new_width,new_height = pygame.display.get_window_size()
    #print(f'event.w: {eventw}, event.h: {eventh}')
    #new_window_width,new_window_height = pygame.display.get_window_size()
    window_shiftx += (new_width - width)//2
    window_shifty += -(new_height - height)//2
    left = new_left
    top = new_top
    width = new_width
    height = new_height
    print(f'window_shift: {window_shiftx,window_shifty}')
    return window_shiftx,window_shifty