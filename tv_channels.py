#kennex
# TV Channels

import pygame, time, sys
import numpy as np
import room
import random
import gf

ws_cnt = 0



i_python_logo = 'images/python.png' # Python Logo
i_diamond = 'images/diamond.png' # Diamond
i_bricks_scene = 'images/bricks_scene.png' # Bricks Scene
i_cam3_view = 'images/cam3_view.png' # View for Camera 3
i_gnarski_logo = 'images/gnarski_logo.png' # Gnarski Logo

python_logo = pygame.image.load(i_python_logo)
diamond = pygame.image.load(i_diamond)
bricks_scene = pygame.image.load(i_bricks_scene)
camera3_view = pygame.image.load(i_cam3_view)
gnarski_logo = pygame.image.load(i_gnarski_logo)

# Sounds
safe_init_sound = pygame.mixer.Sound('sounds/safe_init.wav')
safe_on_sound = pygame.mixer.Sound('sounds/safe_on.wav')


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()






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

"""def whitespace(surface, rect):

    pixel_size = 4
    pixel_length = rect.h / pixel_size
    pixel_height = rect.w / pixel_size
    start = rect.x

    pixel_grid = [[1]*int(pixel_height) for n in range(int(pixel_length))]

    colors = [(255, 255, 255), (205, 205, 205), (155, 155, 155), (100, 100, 100)]

    for row in pixel_grid:
        for col in row:
            color = random.randint(0, 3)
            surface.fill(colors[color], ((rect.x, rect.y), (pixel_size, pixel_size)))
            rect.x += pixel_size
        rect.y += pixel_size
        rect.x = start"""




def falling_numbers(gs, surface, rect):

    if gs.current_room_view == 1:
        gs.text = 'What was that noise?'
    gs.current_tv_screen_color = gs.white

    range_num = 16
    factor = rect.h / (range_num + 2)
    start = rect.x

    number_grid = [range(1, range_num) for n in range(14)]
    colors = [(gs.white), (gs.black), (gs.red), (gs.blue)]

    for row in number_grid:
        for col in row:
            color = random.randint(0, 2)
            text_image = gs.verdana16.render(str(col), True, colors[color])
            surface.blit(text_image, (rect.x, rect.y))

            rect.x += text_image.get_width() + factor
        rect.y += text_image.get_height()
        rect.x = start

def secret_channel_code(gs, screen, rect):
    """Will give code to turn on Safe"""
    text_image = gs.arial60.render(str(gs.turn_safe_on_channel), True, gs.black)
    text_rect = text_image.get_rect(center = rect.center)
    screen.blit(text_image, text_rect)

def message_channel(gs, screen, rect):
    """Will display a message to the screen."""
    gs.current_tv_screen_color = gs.off_white
    text_image = gs.arial60.render('Press Play', True, gs.black)
    text_rect = text_image.get_rect(center = rect.center)
    screen.blit(text_image, text_rect)


def safe_turned_on(gs, screen, rect):
    """Will give code to turn on Safe"""
    #tv_rect = pygame.Rect(x, y, h, w)
    text_image = None
    text_rect = None

    if gs.safe_uncovered:
        while gs.safe_on_sound_var == 0:
            pygame.mixer.Sound.play(safe_on_sound)
            gs.safe_on_sound_var = 1
        gs.current_tv_screen_color = gs.good_green
        text_image = gs.arial60.render('SAFE ON', True, gs.black)
        text_rect = text_image.get_rect(center = rect.center)
        gs.safe_on = True
    else:
        gs.current_tv_screen_color = gs.bad_red
        text_image = gs.arial60.render('SAFE COVERED', True, gs.black)
        text_rect = text_image.get_rect(center = rect.center)
        if gs.close_remote:
            gs.current_channel = gs.channel_code

    screen.blit(text_image, text_rect)

def show_text_on_tv(gs, screen, x, y, text):
    screen_text = gs.verdana16.render(str(text), True, gs.green)
    screen.blit(screen_text, ((x + 3), y))

def camera_one(gs, screen, x, y):
    sur_cam_one = pygame.Surface((gs.gw_width, gs.gw_height), pygame.SRCALPHA)
    sur_cam_one.fill((254, 254, 254, 0))
    sur_cam_one.fill(gs.off_white)

    # Door Settings
    main_door = pygame.Rect(390, 160, 225, 440)
    floor_rect = pygame.Rect(0, 600, 1065, 150)
    sign = pygame.Rect(225, 220, 135, 55)
    sign_number_border = pygame.Rect(sign.bottomleft[0], sign.bottomleft[1], 135, 68)

    # Door
    pygame.draw.rect(sur_cam_one, gs.door, main_door)
    pygame.draw.rect(sur_cam_one, gs.black, main_door, 3)
    pygame.draw.circle(sur_cam_one, gs.dark_gray, (425-3, 390+5), 15)
    pygame.draw.circle(sur_cam_one, gs.yellow, (425, 390), 15)
    pygame.draw.circle(sur_cam_one, gs.black, (425, 390), 16, 2)
    pygame.draw.circle(sur_cam_one, gs.black, (425, 390), 4, 1)

    pygame.draw.rect(sur_cam_one, gs.outer_floor, floor_rect)
    pygame.draw.line(sur_cam_one, gs.black, (0, 600), (1065, 600), 3)

    pygame.draw.rect(sur_cam_one, gs.white, sign)
    pygame.draw.rect(sur_cam_one, gs.white, sign_number_border)
    pygame.draw.rect(sur_cam_one, gs.black, sign, 2)
    pygame.draw.rect(sur_cam_one, gs.black, sign_number_border, 2)

    sign_word = gs.cambria30.render('SUBJECT', True, gs.black)
    sign_number = gs.cambria48.render(str(gs.door_number), True, gs.black)
    sign_word_rect = sign_word.get_rect(center=sign.center)
    sign_number_rect = sign_number.get_rect(center=sign_number_border.center)
    sur_cam_one.blit(sign_word, sign_word_rect)
    sur_cam_one.blit(sign_number, sign_number_rect)

    new_surface = gf.aspect_scale_wh(sur_cam_one, 470, 296)
    screen.blit(new_surface, (x, y))

def camera_three(gs, screen, x, y, w, h):
    screen.blit(gf.aspect_scale_wh(camera3_view, w, h), (x, y))
    text_image = gs.cambria20.render(str(gs.konar_number), True, gs.black)
    sign_rect = pygame.Rect(437, 225, 37, 19)
    text_rect = text_image.get_rect(center = sign_rect.center)
    if gs.current_room_view == 1:
        screen.blit(text_image, text_rect)

def view_diamonds(gs, screen):
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

def check_channels_for_events(gs):
    if gs.current_channel == str(7):
        gs.safe_initialized = True
        while gs.tv_sound_play_var == 0:
            pygame.mixer.Sound.play(safe_init_sound) # todo turn down sound file in audition
            gs.tv_sound_play_var = 1
    else:
        gs.safe_initialized = False
        gs.tv_sound_play_var = 0

def blue_book_hint(gs, screen, rect):
    size = 40
    pub_grid_piece = pygame.Rect(500, 250, size, size)
    pub_grid_piece.centerx = rect.centerx - 150
    pub_grid_piece.centery = rect.centery

    width = size
    height = size
    grid = [(((pub_grid_piece.x - width)/size), ((pub_grid_piece.y - height)/size)), # Grid 1 // index 0
            (((pub_grid_piece.x + width)/size), ((pub_grid_piece.y - height)/size)), # Grid 3 // index 1
            ((pub_grid_piece.x/size), ((pub_grid_piece.y - height)/size)), # Grid 2 >> 2 is after 3 because of how the grid calcs // index 2
            (((pub_grid_piece.x - width)/size), (pub_grid_piece.y/size)), # Grid 4 // index 3
            ((pub_grid_piece.x/size), (pub_grid_piece.y/size)), # Grid 5 *** Same as grid piece // index 4
            (((pub_grid_piece.x + width)/size), (pub_grid_piece.y/size)), # Grid 6 // index 5
            (((pub_grid_piece.x - width)/size), ((pub_grid_piece.y + height)/size)), # Grid 7 // index 6
            ((pub_grid_piece.x/size), ((pub_grid_piece.y + height)/size)), # Grid 8 // index 7
            (((pub_grid_piece.x + width)/size), ((pub_grid_piece.y + height)/size)), # Grid 9 // index 8
            ]

    index = 0

    for column, row in grid:

        x = column * width
        y = row * height
        dist = 150
        current_grid = pygame.Rect(x, y, width, height)
        current_grid2 = pygame.Rect(x+dist, y, width, height)
        current_grid3 = pygame.Rect(x+(dist*2), y, width, height)
        if index == 0:
            pygame.draw.rect(screen, gs.red, current_grid)
            pygame.draw.rect(screen, gs.black, current_grid, 3)

            pygame.draw.rect(screen, gs.red, current_grid2)
            pygame.draw.rect(screen, gs.black, current_grid2, 3)

            text_image = gs.cambria30.render('X  2', True, gs.black)
            text_image_rect = text_image.get_rect()
            text_image_rect.center = current_grid3.center
            screen.blit(text_image, text_image_rect)



        elif index == 1:
            pygame.draw.rect(screen, gs.green, current_grid)
            pygame.draw.rect(screen, gs.black, current_grid, 3)

            pygame.draw.rect(screen, gs.green, current_grid2)
            pygame.draw.rect(screen, gs.black, current_grid2, 3)

            pygame.draw.rect(screen, gs.blue_book_color, current_grid3)
            pygame.draw.rect(screen, gs.black, current_grid3, 3)

        elif index == 2:
            pygame.draw.rect(screen, gs.blue_book_color, current_grid)
            pygame.draw.rect(screen, gs.black, current_grid, 3)

            text_image = gs.cambria30.render('X', True, gs.black)
            text_image_rect = text_image.get_rect()
            text_image_rect.center = current_grid2.center
            screen.blit(text_image, text_image_rect)

            text_image = gs.cambria30.render('=', True, gs.black)
            text_image_rect = text_image.get_rect()
            text_image_rect.center = current_grid3.center
            screen.blit(text_image, text_image_rect)

        else:
            pygame.draw.rect(screen, gs.black, current_grid, 3)

        index += 1


def tv_channels(gs, screen):
    """
    Function to hold and display all information that could be found on the TV.
    channel = channel that is chosen

        screen.blit(self.n4_image, self.n4_rect)
        screen.blit(pygame.transform.smoothscale(image, (int(full_rect[2] / factor), int(full_rect[3] / factor))), image_rect)
        self.door_key_clicker = self.draw_item_to_screen(gs, screen, door_key_rotated, 6, 521, 335)

    """
    #tv_rect = pygame.Rect(195, 140, 470, 296)
    #partial_tv_rect = pygame.Rect(945, 140, 470, 296)
    tv_y = 140
    tv_w = 470
    tv_h = 296

    global ws_surf


    if gs.current_room_view == 1:
        tv_x = 195
        #tv_rect = pygame.Rect(195, 140, 470, 296)
    else:
        tv_x = 945

    tv_rect = pygame.Rect(tv_x, tv_y, tv_w, tv_h)
    check_channels_for_events(gs)

    # Channels
    # Channel 1
    if gs.current_channel == str(1):  # Powered by Python
        if gs.current_room_view == 1:
            gs.text = 'Wow! This whole game was made with Python?'
        gs.current_tv_screen_color = gs.white
        if gs.current_room_view == 1:
            draw_items_full(gs, screen, python_logo, 1.25, 195, 140)
        else:
            draw_items_partial(gs, screen, python_logo, 1.25, 195, 140)

    # Channel 2
    elif gs.current_channel == str(2):  # Gnarski
        gs.current_tv_screen_color = gs.white
        if gs.current_room_view == 1:
            draw_items_full(gs, screen, gnarski_logo, 1.25, 195, 140)
            gs.text = 'Gnarski!?'
        else:
            draw_items_partial(gs, screen, gnarski_logo, 1.25, 195, 140)

    # Channel 3
    elif gs.current_channel == str(3):  # Default channel??
        if gs.current_room_view == 1:
                gs.text = 'I think this is the default channel...'

    # Channel 4
    # Cameras
    elif gs.current_channel == str(4):  # Camera 1
        camera_one(gs, screen, tv_x, tv_y)
        show_text_on_tv(gs, screen, tv_x, 415, 'CAMERA 1')
        if gs.current_room_view == 1:
            gs.text = "It's a camera? Is this outside of this room?"

    # Channel 5
    elif gs.current_channel == str(5): # Camera 2
        gs.current_tv_screen_color = gs.white
        if gs.current_room_view == 1:
            draw_items_full(gs, screen, bricks_scene, 1, 195, 140)
            if gs.current_room_view == 1:
                gs.text = 'A camera of a camera? What?'
            if gs.power_cord_desk_2:
                pygame.draw.circle(screen, gs.red, (487, 244), 3) # todo can we make this look like it's blinking slowly
            show_text_on_tv(gs, screen, tv_x, 415, 'CAMERA 2')
        else:
            draw_items_partial(gs, screen, bricks_scene, 1, 195, 140)
            show_text_on_tv(gs, screen, tv_x, 415, 'CAMERA 2')

    # Channel 6
    elif gs.current_channel == str(6):  # Camera 3 // Only on with power cord
        if gs.power_cord_desk_2:
            camera_three(gs, screen, tv_x, tv_y, tv_w, tv_h)
            show_text_on_tv(gs, screen, tv_x, 415, 'CAMERA 3')
            if gs.current_room_view == 1:
                gs.text = 'Oh! Another camera!'
        else:
            if gs.current_room_view == 1:
                gs.text = 'There seems to be nothing here...'

    # Channel 7
    elif gs.current_channel == str(7):  # Falling Numbers Channel 7
        falling_numbers(gs, screen, tv_rect)

    # Channel 8
    elif gs.current_channel == str(8):  # Whitespace
        whitespace(screen, tv_rect)
        if gs.current_room_view == 1:
            gs.text = 'This is a great channel.'

    # Channel 9
    elif gs.current_channel == str(9):  # Black Screen
        if gs.current_room_view == 1:
            gs.text = 'This channel was intentionally left blank.'

    # Channel 11
    elif gs.current_channel == str(11):
        message_channel(gs, screen, tv_rect)
        if gs.current_room_view == 1:
            gs.text = None

    # Channel 12
    elif gs.current_channel == str(12):  # Clock
        gs.current_tv_screen_color = gs.off_white
        clock_value = gf.get_game_clock(gs, screen)
        clock_text = gs.verdana55.render(clock_value, True, gs.red)
        clock_text_rect = clock_text.get_rect(center = tv_rect.center)
        screen.blit(clock_text, clock_text_rect)
        if gs.current_room_view == 1:
            gs.text = 'What is this clock?'

    # Game Channels // These channels will change on each new instance of the game
    # Channel Code
    elif gs.current_channel == str(gs.channel_code): # Will Give Code to Turn On Safe
        gs.current_tv_screen_color = gs.white
        secret_channel_code(gs, screen, tv_rect)
        if gs.current_room_view == 1:
            gs.text = 'Some odd code...'

    # Blue Book Hint
    elif gs.current_channel == str(gs.pub_n7): # Blue book hint
        gs.current_tv_screen_color = gs.white
        blue_book_hint(gs, screen, tv_rect)
        if gs.current_room_view == 1:
            gs.text = "I think I've seen this before..."

    # Will Show Two Diamonds of different colors // These colors match the safe (bigger one is first)
    elif gs.current_channel == str(gs.random_channel):
        view_diamonds(gs, screen)
        if gs.current_room_view == 1:
            gs.text = 'Diamonds? What do these mean?'

    # Safe Channel
    elif gs.current_channel == str(gs.turn_safe_on_channel): # Turns on Safe
        safe_turned_on(gs, screen, tv_rect)
        if gs.current_room_view == 1:
            gs.text = 'I turned on the safe!'




    # Easter Egg Channels
    elif gs.current_channel == str(456): # todo something
        print(gs.current_channel)

    elif gs.current_channel == str(456): # todo easter egg channel for fun
        print(gs.current_channel)

    elif gs.current_channel == str('1234567890F'): # Button Presser
        gs.current_tv_screen_color = gs.white
        text_image = gs.arial22.render("YOU LIKE TO PRESS BUTTONS, DON'T YA?", True, gs.black)
        text_rect = text_image.get_rect(center = tv_rect.center)
        screen.blit(text_image, text_rect)
        if gs.current_room_view == 1:
            gs.text = 'I DO LIKE BUTTONS! HAHA!'

    elif gs.current_channel == str(181161693114): # This spells "RAPPICAN" if you put 1-26 next to the alphabet
        if gs.current_room_view == 1:
            gs.text = "Paul's Channel..."

    else:  # Whitespace
        whitespace(screen, tv_rect)

        """        if gs.whitespace_count == 0:
            ws_surf = create_whitespace(screen, tv_rect)
        gs.whitespace_count += 1
        if gs.whitespace_count > 5: # 5 is just an example
            gs.whitespace_count = 0
        draw_whitespace(screen, create_whitespace(screen, tv_rect), tv_rect)"""


        if gs.current_room_view == 1:
            gs.text = 'It does not have a signal...'


def whitespace(surface, rect):

    pixel_size = 4
    pixel_length = rect.h / pixel_size
    pixel_height = rect.w / pixel_size
    start = rect.x

    pixel_grid = [[1]*int(pixel_height) for n in range(int(pixel_length))]

    colors = [(255, 255, 255), (205, 205, 205), (155, 155, 155), (100, 100, 100)]

    for row in pixel_grid:
        for col in row:
            color = random.randint(0, 3)
            surface.fill(colors[color], ((rect.x, rect.y), (pixel_size, pixel_size)))
            rect.x += pixel_size
        rect.y += pixel_size
        rect.x = start

"""def create_whitespace(surface, rect):

    pixel_size = 4
    pixel_length = rect.h / pixel_size
    pixel_height = rect.w / pixel_size
    start = rect.x

    pixel_grid = [[1]*int(pixel_height) for n in range(int(pixel_length))]

    colors = [(255, 255, 255), (205, 205, 205), (155, 155, 155), (100, 100, 100)]

    for row in pixel_grid:
        for col in row:
            color = random.randint(0, 3)
            surface.fill(colors[color], (rect.x, rect.y, pixel_size, pixel_size))
            rect.x += pixel_size
        rect.y += pixel_size
        rect.x = start
    return surface

def draw_whitespace(screen, ws_surf, rect):
    screen.blit(ws_surf, rect)
"""
