#kennex
# TV Channels

import pygame
import numpy as np
import room

i_python_logo = 'images/python.png' # Screwdriver
python_logo = pygame.image.load(i_python_logo)

def draw_items_full(gs, screen, image, factor, x, y):
    """Function to pass item and draw to screen
    image = loaded image variable
    factor = scale factor
    x = x position
    y = y position
    """
    full_rect = image.get_rect()
    image_surface = (int(full_rect[2] / factor), int(full_rect[3] / factor))
    image_rect = pygame.Rect(x, y, image_surface[0], image_surface[1])

    tv_rect = pygame.Rect(195, 140, 470, 296)
    image_rect.center = tv_rect.center

    screen.blit(pygame.transform.smoothscale(image, (int(full_rect[2] / factor), int(full_rect[3] / factor))), image_rect)
    #pygame.draw.rect(screen, gs.yellow, image_rect, 3) # todo comment this out

    #return image_rect

def draw_items_partial(gs, screen, image, factor, x, y):
    """Function to pass item and draw to screen
    image = loaded image variable
    factor = scale factor
    x = x position
    y = y position
    """
    full_rect = image.get_rect()
    image_surface = (int(full_rect[2] / factor), int(full_rect[3] / factor))
    image_rect = pygame.Rect(x, y, image_surface[0], image_surface[1])

    #tv_rect = pygame.Rect(195, 140, 470, 296)
    partial_tv_rect = pygame.Rect(945, 140, 470, 296)
    image_rect.center = partial_tv_rect.center

    screen.blit(pygame.transform.smoothscale(image, (int(full_rect[2] / factor), int(full_rect[3] / factor))), image_rect)
    #pygame.draw.rect(screen, gs.yellow, image_rect, 3) # todo comment this out

    #return image_rect

def tv_channels(gs, screen):
    """
    Function to hold and display all information that could be found on the TV.
    channel = channel that is chosen


        screen.blit(self.n4_image, self.n4_rect)
        screen.blit(pygame.transform.smoothscale(image, (int(full_rect[2] / factor), int(full_rect[3] / factor))), image_rect)
        self.door_key_clicker = self.draw_item_to_screen(gs, screen, door_key_rotated, 6, 521, 335)


    """
    tv_rect = pygame.Rect(195, 140, 470, 296)
    partial_tv_rect = pygame.Rect(945, 140, 470, 296)


    if gs.current_channel == str(0):  # Whitespace todo need perlin noise?
        print(gs.current_channel)
    elif gs.current_channel == str(-1):  # Whitespace todo need perlin noise?
        print(gs.current_channel)
    elif gs.current_channel == str(1):  # Powered by Python
        gs.current_tv_screen_color = gs.white
        if gs.current_room_view == 1:
            draw_items_full(gs, screen, python_logo, 1.25, 195, 140)
        else:
            draw_items_partial(gs, screen, python_logo, 1.25, 195, 140)
    elif gs.current_channel == str(2):  # Flash on screen
        print(gs.current_channel)
    elif gs.current_channel == str(3):  # Default channel??
        print(gs.current_channel)
    elif gs.current_channel == str(4):  # Camera 1
        print(gs.current_channel)
    elif gs.current_channel == str(5):  # Camera 2
        print(gs.current_channel)
    elif gs.current_channel == str(6):  # Camera 3
        print(gs.current_channel)
    elif gs.current_channel == str(7):  # Whitespace
        print(gs.current_channel)
    elif gs.current_channel == str(8):  # Whitespace
        print(gs.current_channel)
    elif gs.current_channel == str(9):  # Black Screen
        print(gs.current_channel)
    elif gs.current_channel == str(gs.channel_code):
        print(gs.current_channel)
    elif gs.current_channel == str('123456789L0F'): # todo easter egg channel for fun
        print(gs.current_channel)
    elif gs.current_channel == str(456): # todo another number channel for fun from diary
        print(gs.current_channel)
    elif gs.current_channel == str(456): # todo easter egg channel for fun
        print(gs.current_channel)
    elif gs.current_channel == str(456): # todo easter egg channel for fun
        print(gs.current_channel)
    else:  # Whitespace todo perlin noise
        print("invalid channel")

