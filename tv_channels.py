#kennex
# TV Channels

import pygame
import numpy as np
import room
import random
import gf


i_python_logo = 'images/python.png' # Python Logo
i_diamond = 'images/diamond.png' # Diamond

python_logo = pygame.image.load(i_python_logo)
diamond = pygame.image.load(i_diamond)

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

def whitespace(surface, x, y, h, w):
    pixel_size = 4
    pixel_length = w / pixel_size
    pixel_height = h / pixel_size
    start = x

    pixel_grid = [[1]*int(pixel_height) for n in range(int(pixel_length))]

    colors = [(255, 255, 255), (205, 205, 205), (155, 155, 155), (100, 100, 100)]

    for row in pixel_grid:
        for col in row:
            color = random.randint(0, 3)
            surface.fill(colors[color], ((x, y), (pixel_size, pixel_size)))
            x += pixel_size
        y += pixel_size
        x = start

def falling_numbers(gs, surface, x, y, h, w):
    gs.current_tv_screen_color = gs.white

    range_num = 11
    factor = h / (range_num + 1.75)
    start = x

    number_grid = [range(1, range_num) for n in range(14)]
    colors = [(gs.white), (gs.black), (gs.red), (gs.blue)]

    for row in number_grid:
        for col in row:
            color = random.randint(0, 2)
            text_image = gs.verdana16.render(str(col), True, colors[color])
            surface.blit(text_image, (x, y))

            x += text_image.get_width() + factor
        y += text_image.get_height()
        x = start

def secret_channel_code(gs, screen, x, y, h, w):
    """Will give code to turn on Safe"""
    tv_rect = pygame.Rect(x, y, h, w)
    text_image = gs.arial60.render(str(gs.turn_safe_on_channel), True, gs.black)
    text_rect = text_image.get_rect(center = tv_rect.center)
    screen.blit(text_image, text_rect)

def safe_turned_on(gs, screen, x, y, h, w):
    """Will give code to turn on Safe"""
    tv_rect = pygame.Rect(x, y, h, w)
    text_image = None
    text_rect = None

    if gs.safe_uncovered:
        gs.current_tv_screen_color = gs.good_green
        text_image = gs.arial60.render('SAFE ON', True, gs.black)
        text_rect = text_image.get_rect(center = tv_rect.center)
        gs.safe_on = True
    else:
        gs.current_tv_screen_color = gs.bad_red
        text_image = gs.arial60.render('SAFE COVERED', True, gs.black)
        text_rect = text_image.get_rect(center = tv_rect.center)
        if gs.close_remote:
            gs.current_channel = gs.channel_code

    screen.blit(text_image, text_rect)

def view_diamonds(gs, screen, x, y, h, w):
    """Will show two diamonds to the screen of varying colors.  These colors are needed for either the safe or to figure out the safe."""
    gs.current_tv_screen_color = gs.white

    if gs.current_room_view == 1:
        rect1 = pygame.Rect(310, 220, 146, 162)
        rect1 = rect1.inflate(-15, -15)
        rect2 = pygame.Rect(470, 150, 183, 203)
        rect2 = rect2.inflate(-15, -15)
        rect1_color = None
        rect2_color = None

        for v in gs.color_codes.values():
            if v[0] == gs.tv_color_numbers[1]:
                rect1_color = v[2]
        for v in gs.color_codes.values():
            if v[0] == gs.tv_color_numbers[0]:
                rect2_color = v[2]

        pygame.draw.rect(screen, rect1_color, rect1)
        pygame.draw.rect(screen, rect2_color, rect2)

        gf.draw_item_to_screen(gs, screen, diamond, 2.5, 310, 220)
        gf.draw_item_to_screen(gs, screen, diamond, 2, 470, 150)


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
    tv_y = 140
    tv_w = 296
    tv_h = 470

    if gs.current_room_view == 1:
        tv_x = 195
    else:
        tv_x = 945

    if gs.current_channel == str(7) and gs.tv_on:
        gs.safe_initialized = True
    else:
        gs.safe_initialized = False




    if gs.current_channel == str(1):  # Powered by Python
        gs.current_tv_screen_color = gs.white
        if gs.current_room_view == 1:
            draw_items_full(gs, screen, python_logo, 1.25, 195, 140)
        else:
            draw_items_partial(gs, screen, python_logo, 1.25, 195, 140)

    elif gs.current_channel == str(2):  # Flash on screen
        print(gs.current_channel)

    elif gs.current_channel == str(3):  # Default channel??
        pass

    elif gs.current_channel == str(4):  # Camera 1
        print(gs.current_channel)

    elif gs.current_channel == str(5):  # Camera 2
        print(gs.current_channel)

    elif gs.current_channel == str(6):  # Camera 3
        print(gs.current_channel)

    elif gs.current_channel == str(7):  # Whitespace
        falling_numbers(gs, screen, tv_x, tv_y, tv_h, tv_w)

    elif gs.current_channel == str(8):  # Whitespace
        whitespace(screen, tv_x, tv_y, tv_h, tv_w)

    elif gs.current_channel == str(9):  # Black Screen
        print(gs.current_channel)

    # Game Channels
    elif gs.current_channel == str(gs.channel_code): # Will Give Code to Turn On Safe
        gs.current_tv_screen_color = gs.white
        secret_channel_code(gs, screen, tv_x, tv_y, tv_h, tv_w)

    elif gs.current_channel == str(gs.random_channel): # Will Show Two Diamonds of different colors // These colors match the safe (bigger one is first)
        view_diamonds(gs, screen, tv_x, tv_y, tv_h, tv_w)

    elif gs.current_channel == str(gs.turn_safe_on_channel): # Turns on Safe
        safe_turned_on(gs, screen, tv_x, tv_y, tv_h, tv_w)

    # Easter Egg Channels
    elif gs.current_channel == str(456): # todo easter egg channel for fun
        print(gs.current_channel)

    elif gs.current_channel == str('123456789L0F'): # todo easter egg channel for fun
        print(gs.current_channel)

    elif gs.current_channel == str(456): # todo easter egg channel for fun
        print(gs.current_channel)

    elif gs.current_channel == str(181161693114): # This spells "RAPPICAN" if you put 1-26 next to the alphabet
        print("PAUL'S CHANNEL")

    else:  # Whitespace todo perlin noise
        whitespace(screen, tv_x, tv_y, tv_h, tv_w)

