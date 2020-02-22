#kennex

import os, pygame, sys, datetime
from settings import Settings
import gf
import puzzles
from inventory import Inventory
from objects import GameObjects
from stable_items import Stable_Items
from control_panel import Control_Panel
from room import Room
from pygame.locals import *

# Initialize pygame, settings, and screen object.
pygame.mixer.pre_init(44100,-16,2, 2048)
pygame.init()
clock = pygame.time.Clock()
gs = Settings()
screen = pygame.display.set_mode((gs.screen_width, gs.screen_height), HWSURFACE | DOUBLEBUF) # add ability to resize window
pygame.display.set_caption("Captive | Kennex")

intro_music = pygame.mixer.Sound('sounds/intro.wav')


def title_menu():

    title = gs.garamond90.render('CAPTIVE', True, gs.black)
    author = gs.verdana32.render('Kennex Presents:', True, gs.black)
    alpha_title_surface = pygame.Surface(title.get_size(), pygame.SRCALPHA)
    alpha_author_surface = pygame.Surface(author.get_size(), pygame.SRCALPHA)
    alpha_a = 0
    alpha_t = 0
    start_ticks = pygame.time.get_ticks()

    while True:
        # Events
        pygame.mixer.Sound.play(intro_music, -1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    game_menu()



        # Draw Menu
        #screen.fill(gs.white)

        screen.fill((gs.white))

        seconds = (pygame.time.get_ticks() - start_ticks)/1000

        if seconds > 2:
            if alpha_a >= 0 and alpha_a <= 254:
                alpha_a = max(alpha_a+2, 0)
                author_surface = author.copy()
                alpha_author_surface.fill((0, 0, 0, alpha_a))
                author_surface.blit(alpha_author_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                if alpha_a >= 254:
                    alpha_a = 255

            screen.blit(author_surface, (350, 290))


        if seconds > 7:

            if alpha_t >= 0 and alpha_t <= 254:
                alpha_t = max(alpha_t+2, 0)
                title_surface = title.copy()
                alpha_title_surface.fill((0, 0, 0, alpha_t))
                title_surface.blit(alpha_title_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                if alpha_t >= 254:
                    alpha_t = 255


            screen.blit(title_surface, (gs.screen_width//2, gs.screen_height//2))


        if seconds > 16:
            game_menu()

        # Update
        pygame.display.flip()
        clock.tick(30)

def game_menu():
    game_title = gs.garamond90.render('CAPTIVE', True, gs.black)
    game_title_rect = game_title.get_rect()
    game_title_rect.centerx = gs.screen_width//2

    button_color1 = gs.gray
    button_color2 = gs.gray
    button_color3 = gs.gray
    button_color4 = gs.gray
    button_color5 = gs.gray

    button1 = pygame.Rect(0, 600, 190, 80)
    button1.centerx = gs.screen_width//2
    button2 = button1.move(-button1.width - 30, 0)
    button3 = button2.move(-button2.width - 30, 0)
    button4 = button1.move(button1.width + 30, 0)
    button5 = button4.move(button4.width + 30, 0)

    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button1.collidepoint(event.pos):
                        print('scores')
                    if button2.collidepoint(event.pos):
                        print('load game')
                    if button3.collidepoint(event.pos):
                        print('run game')
                        pygame.time.delay(2000)
                        pygame.mixer.Sound.stop(intro_music)
                        run_game()
                    if button4.collidepoint(event.pos):
                        print('settings')
                    if button5.collidepoint(event.pos):
                        print('credits')



        screen.fill((gs.bg_color))
        screen.blit(game_title, (game_title_rect.x, 200))



        pygame.draw.rect(screen, button_color1, button1)
        pygame.draw.rect(screen, button_color2, button2)
        pygame.draw.rect(screen, button_color3, button3)
        pygame.draw.rect(screen, button_color4, button4)
        pygame.draw.rect(screen, button_color5, button5)

        pygame.draw.rect(screen, gs.black, button1, 3)
        pygame.draw.rect(screen, gs.black, button2, 3)
        pygame.draw.rect(screen, gs.black, button3, 3)
        pygame.draw.rect(screen, gs.black, button4, 3)
        pygame.draw.rect(screen, gs.black, button5, 3)

        b1_text = gs.arial32.render('PLAY', True, gs.black)
        b2_text = gs.arial32.render('LOAD', True, gs.black)
        b3_text = gs.arial32.render('SCORES', True, gs.black)
        b4_text = gs.arial32.render('SETTINGS', True, gs.black)
        b5_text = gs.arial32.render('CREDITS', True, gs.black)

        b1_text_rect = b1_text.get_rect(center = button3.center)
        b2_text_rect = b2_text.get_rect(center = button2.center)
        b3_text_rect = b3_text.get_rect(center = button1.center)
        b4_text_rect = b4_text.get_rect(center = button4.center)
        b5_text_rect = b5_text.get_rect(center = button5.center)

        screen.blit(b1_text, b1_text_rect)
        screen.blit(b2_text, b2_text_rect)
        screen.blit(b3_text, b3_text_rect)
        screen.blit(b4_text, b4_text_rect)
        screen.blit(b5_text, b5_text_rect)

        if button1.collidepoint(pygame.mouse.get_pos()):
            button_color1 = gs.dark_gray
            button_color2 = gs.gray
            button_color3 = gs.gray
            button_color4 = gs.gray
            button_color5 = gs.gray
        elif button2.collidepoint(pygame.mouse.get_pos()):
            button_color2 = gs.dark_gray
            button_color1 = gs.gray
            button_color3 = gs.gray
            button_color4 = gs.gray
            button_color5 = gs.gray
        elif button3.collidepoint(pygame.mouse.get_pos()):
            button_color3 = gs.dark_gray
            button_color2 = gs.gray
            button_color1 = gs.gray
            button_color4 = gs.gray
            button_color5 = gs.gray
        elif button4.collidepoint(pygame.mouse.get_pos()):
            button_color4 = gs.dark_gray
            button_color2 = gs.gray
            button_color3 = gs.gray
            button_color1 = gs.gray
            button_color5 = gs.gray
        elif button5.collidepoint(pygame.mouse.get_pos()):
            button_color5 = gs.dark_gray
            button_color2 = gs.gray
            button_color3 = gs.gray
            button_color4 = gs.gray
            button_color1 = gs.gray
        else:
            button_color1 = gs.gray
            button_color2 = gs.gray
            button_color3 = gs.gray
            button_color4 = gs.gray
            button_color5 = gs.gray





        # Update
        pygame.display.flip()
        clock.tick(30)

def run_game():



    gf.generate_codes(gs) # generates numbers for problems and puzzles

    stable_item_blocks = Stable_Items(gs, screen)
    room_view = Room(gs, screen, stable_item_blocks)
    inventory = Inventory(gs, screen, room_view)
    game_objects = GameObjects(gs, screen, inventory)
    cp = Control_Panel(gs, screen)

    gs.game_started = True


    gs.text = "What the...?  Where am I?"


    while True:
        gf.check_events(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp)
        gf.update_screen(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp)
        gf.game_clock(gs, screen, clock)

        if gs.sleeperticks:
            pygame.time.wait(100)  # Leave this at 100 or less




title_menu()
#game_menu()
#run_game()




"""
TO DO LIST

8. Need to create a logo for Kennex for the beginning.
9. Need to figure out what is going to go at the bottom of the inventory window.
14. Need to create an intro.
15. Need to create an outro.
20. Need to figure out if scaling the entire game is possible based on how it's drawn.


"""
# todo make credits
# todo make what happens after you click open door / outro
# todo make intro
# todo create stats tracker (i.e. how many times played, hours played, times escaped, etc.)
# todo add text
# todo add music
# todo figure out what other channels are needed
# todo figure out if you can scale the whole game
# todo add sound control to the remote
# todo are there ways to quickly optimize?
# todo figure out a title
# todo create a title logo
# todo create kennex logo


# menu to do's
# todo create menu
# todo what's on the menu?
# buttons, logs, settings




