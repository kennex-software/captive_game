#kennex

import pygame, sys#, datetime, os
from settings import Settings
import gf
from inventory import Inventory
from objects import GameObjects
from stable_items import Stable_Items
from control_panel import Control_Panel
from room import Room
from pygame.locals import *

# Initialize pygame, settings, and screen object.
pygame.mixer.pre_init(44100,-16,2, 2048)
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
gs = Settings()
screen = pygame.display.set_mode((gs.screen_width, gs.screen_height), HWSURFACE | DOUBLEBUF) # add ability to resize window
pygame.display.set_caption("Captive | Kennex")
icon = pygame.image.load('images/key_icon.ico') # should be 32 x 32
game_logo = pygame.image.load('images/key_logo.png')
pygame.display.set_icon(icon)
stable_item_blocks = Stable_Items(gs, screen)
room_view = Room(gs, screen, stable_item_blocks)
inventory = Inventory(gs, screen, room_view)
game_objects = GameObjects(gs, screen, inventory)
cp = Control_Panel(gs, screen)

intro_music = pygame.mixer.Sound('sounds/intro.wav')
credits_music = pygame.mixer.Sound('sounds/credits.wav')

def credits():
    title = gs.arial60.render('to be continued...', True, gs.black)
    alpha_title_surface = pygame.Surface(title.get_size(), pygame.SRCALPHA)
    alpha_t = 0
    start_ticks = pygame.time.get_ticks()
    max_alpha_reached = False
    run_tbc = True
    run_credits = True
    credits_full = """
    created by : kennex
    music by : gnarski
    special thanks to : bigheadbrett for play testing
    tech with tim for inspiring me to code
    happy chuck programming for help with scrolling text
    Ted Klein Bergman for help with the tv static
    
    
    
    and you.  thanks for playing
    
    
    CAPTIVE
    """
    scrolling_centerx, scrolling_centery = screen.get_rect().centerx, screen.get_rect().centery
    delta = scrolling_centery


    while gs.won_game:

        pygame.mixer.Sound.play(credits_music, 1)
        screen.fill((gs.white))
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not run_tbc:
                        run_credits = False
                        pygame.time.wait(1000)
                        pygame.mixer.Sound.stop(credits_music)
                        game_menu()
                    if run_tbc:
                        run_tbc = False
                        run_credits = True




        seconds = (pygame.time.get_ticks() - start_ticks)/1000

        if seconds > 2 and run_tbc:
            if not max_alpha_reached:
                if alpha_t >= 0 and alpha_t <= 254:
                    alpha_t = max(alpha_t+2, 0)
                    title_surface = title.copy()
                    alpha_title_surface.fill((0, 0, 0, alpha_t))
                    title_surface.blit(alpha_title_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                    if alpha_t >= 254:
                        alpha_t = 255
                        max_alpha_reached = True

            if max_alpha_reached:
                alpha_t = max(alpha_t-2, 0)
                title_surface = title.copy()
                alpha_title_surface.fill((0, 0, 0, alpha_t))
                title_surface.blit(alpha_title_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                if alpha_t <= 1:
                    alpha_t = 0


            screen.blit(title_surface, (gs.screen_width//2, gs.screen_height//2))

        if seconds > 12 and run_tbc:
            run_tbc = False

        if not run_tbc and run_credits:
            delta -= 1
            gf.scrolling_credits(gs, screen, credits_full, scrolling_centerx, scrolling_centery, delta)

        else:
            pass




        # Update
        pygame.display.flip()
        clock.tick(30)

def title_menu():

    title = gs.cambria90.render('CAPTIVE', True, gs.black)
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
    game_title = gs.cambria150.render('CAPTIVE', True, gs.black)
    game_title_rect = game_title.get_rect()
    game_title_rect.centerx = gs.screen_width//2
    game_logo_rect = game_logo.get_rect()
    game_logo_rect.centerx = gs.screen_width//2

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
                        gf.load_settings(gs)
                        pygame.time.wait(500)
                        gs.options_menu_up = False
                        pygame.mixer.Sound.stop(intro_music)
                        gs.game_started = True
                        run_game()
                    if button3.collidepoint(event.pos):
                        print('run game')
                        pygame.time.wait(2000)
                        pygame.mixer.Sound.stop(intro_music)
                        gs.game_started = True
                        run_game()
                    if button4.collidepoint(event.pos):
                        print('settings')
                    if button5.collidepoint(event.pos):
                        sys.exit()
                        print('quit')


        gs.new_game = True
        screen.fill((gs.bg_color))
        screen.blit(game_logo, (game_logo_rect.x, game_title_rect.bottom + 175))
        screen.blit(game_title, (game_title_rect.x, 175))







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
        b5_text = gs.arial32.render('QUIT', True, gs.black)

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

def options_menu():
    gs.options_menu_up = True
    game_title = gs.cambria90.render('OPTIONS', True, gs.black)
    game_title_rect = game_title.get_rect()
    game_title_rect.centerx = gs.screen_width//2

    quit_menu = pygame.Rect(400, 325, 600, 200)
    quit_menu.centerx = gs.screen_width//2

    button_color1 = gs.gray
    button_color2 = gs.gray
    button_color3 = gs.gray
    button_color4 = gs.gray
    button_color5 = gs.gray
    q_button_save_color = gs.gray
    q_button_quit_color = gs.gray

    button1 = pygame.Rect(0, 600, 190, 80)
    button1.centerx = gs.screen_width//2
    button2 = button1.move(-button1.width - 30, 0)
    button3 = button2.move(-button2.width - 30, 0)
    button4 = button1.move(button1.width + 30, 0)
    button5 = button4.move(button4.width + 30, 0)

    q_button_save = pygame.Rect(0, 410, 190, 80)
    q_button_save.centerx = quit_menu.centerx - ((q_button_save.width // 2) + 15)
    q_button_quit = q_button_save.move(q_button_save.width + 30, 0)



    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gs.options_menu_up = False
                    gs.resume_time = pygame.time.get_ticks()
                    gs.stoppage_time = gs.stoppage_time + (gs.resume_time - gs.pause_time)
                    gs.game_started = True
                    run_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not gs.quit_menu_up:
                    if button1.collidepoint(event.pos):
                        print('load game')
                        gf.load_settings(gs)
                        pygame.time.wait(500)
                        gs.options_menu_up = False
                        gs.resume_time = pygame.time.get_ticks()
                        gs.stoppage_time = gs.stoppage_time + (gs.resume_time - gs.pause_time)
                        if gs.start_game_from_load:
                            gs.game_started = True
                            run_game()
                    if button2.collidepoint(event.pos):
                        print('save game')
                        gs.resume_time = pygame.time.get_ticks()
                        gs.stoppage_time = gs.stoppage_time + (gs.resume_time - gs.pause_time)
                        gf.save_settings(gs)
                        pygame.time.wait(500)
                        gs.options_menu_up = False
                        gs.game_started = True
                        run_game()
                    if button3.collidepoint(event.pos):
                        print('run game')
                        gs.options_menu_up = False
                        gs.resume_time = pygame.time.get_ticks()
                        gs.stoppage_time = gs.stoppage_time + (gs.resume_time - gs.pause_time)
                        gs.game_started = True
                        run_game()
                    if button4.collidepoint(event.pos):
                        print('settings')
                    if button5.collidepoint(event.pos):
                        gs.quit_menu_up = True
                        print('show quit menu')
                if event.button == 1 and gs.quit_menu_up:
                    print('quit menu up')
                    if q_button_save.collidepoint(event.pos):
                        print('save game')
                        gs.resume_time = pygame.time.get_ticks()
                        gs.stoppage_time = gs.stoppage_time + (gs.resume_time - gs.pause_time)
                        gf.save_settings(gs)
                        pygame.time.wait(500)
                        gs.options_menu_up = False
                        gs.quit_menu_up = False
                        gs.game_started = True
                        run_game()
                    if q_button_quit.collidepoint(event.pos):
                        gs.options_menu_up = False
                        gs.quit_menu_up = False
                        game_menu()







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

        b1_text = gs.arial32.render('BACK', True, gs.black)
        b2_text = gs.arial32.render('SAVE', True, gs.black)
        b3_text = gs.arial32.render('LOAD', True, gs.black)
        b4_text = gs.arial32.render('SETTINGS', True, gs.black)
        b5_text = gs.arial32.render('QUIT', True, gs.black)

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

        if not gs.quit_menu_up:
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

        if gs.quit_menu_up:
            window_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            window_surface.fill(gs.white_alpha)
            screen.blit(window_surface, (0,0))

            pygame.draw.rect(screen, gs.bg_color, quit_menu)
            pygame.draw.rect(screen, gs.black, quit_menu, 4)
            ask_to_save_text = gs.verdana18.render('Are you sure you want to quit without saving?', True, gs.black)
            ask_to_save_text_rect = ask_to_save_text.get_rect(center = (quit_menu.centerx, quit_menu.y + 40))
            screen.blit(ask_to_save_text, ask_to_save_text_rect)

            pygame.draw.rect(screen, q_button_save_color, q_button_save)
            pygame.draw.rect(screen, q_button_quit_color, q_button_quit)

            pygame.draw.rect(screen, gs.black, q_button_save, 3)
            pygame.draw.rect(screen, gs.black, q_button_quit, 3)

            q_save_text_rect = b2_text.get_rect(center = q_button_save.center)
            q_quit_text_rect = b5_text.get_rect(center = q_button_quit.center)

            screen.blit(b2_text, q_save_text_rect)
            screen.blit(b5_text, q_quit_text_rect)

            if q_button_save.collidepoint(pygame.mouse.get_pos()):
                q_button_save_color = gs.dark_gray
                q_button_quit_color = gs.gray
            elif q_button_quit.collidepoint(pygame.mouse.get_pos()):
                q_button_quit_color = gs.dark_gray
                q_button_save_color = gs.gray
            else:
                q_button_save_color = gs.gray
                q_button_quit_color = gs.gray

        # Update
        pygame.display.flip()
        clock.tick(30)

def run_game():

    if gs.new_game:
        gf.default_settings(gs)
        gf.generate_codes(gs) # generates numbers for problems and puzzles
        gf.update_settings_dictionary(gs) # Generates the ability to save the settings generated in the generate codes
        gs.text = "What the...?  Where am I?"
        gs.game_start_time = pygame.time.get_ticks()
        gs.new_game = False

    while gs.game_started:
        gf.check_events(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp)
        gf.update_screen(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp)


        #if gs.sleeperticks:
        #    pygame.time.wait(100)  # Leave this at 100 or less

        clock.tick(60)
        gf.clock_timer(gs)

    while gs.options_menu_up:
        gf.clock_timer(gs)
        options_menu()

    while gs.won_game:
        credits()


    pygame.time.wait(1000)
    pygame.mixer.Sound.stop(credits_music)
    game_menu()

#credits()
#run_game()
title_menu()
#game_menu()





"""
Batch this:

pyinstaller --onefile -w captive.py control_panel.py credits.py gf.py inventory.py multiline_text.py objects.py puzzles.py room.py scale_points_list.py settings.py stable_items.py tv_channels.py whitespace.py


"""

