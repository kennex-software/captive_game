#kennex

import pygame#, os, sys, copy, datetime
#from settings import Settings
import gf
import inventory
#import objects
#from stable_items import Stable_Items
#from pygame.locals import *
from math import pi
#from pygame.math import Vector2
#from pygame.math import Vector3
#from noise import pnoise2
#from time import monotonic as timer
#import time
import tv_channels
#import numpy as np

# Load images
hanging_shirt_load = 'images/shirt.png' # Hanging Shirt
laying_remote_load = 'images/remote_laying.png' # Laying Remote
laying_paper_load = 'images/laying_paper.png' # Laying Paper
rotated_batteries_load = 'images/batteries_rotated.png' # Rotated batteries
laying_power_cord_load = 'images/power_cord.png' # Laying power cord
red_book_rotated_load = 'images/red_book_rotated.png' # Rotated Red Book
blue_book_rotated_load = 'images/blue_book_rotated.png' # Rotated Blue Book
flathead_load = 'images/flathead_rotated.png' # Flathead
door_key_rotated_load = 'images/door_key_rotated.png' # Rotated Door Key
green_key_rotated_load = 'images/green_key_rotated.png' # Rotated Green Key
power_cord_plugged_1_load = 'images/power_cord_plugged_one.png' # First plugged power cord
power_cord_plugged_1_flip_load = 'images/power_cord_plugged_one_flip.png' # First plugged power cord
power_cord_plugged_2_load = 'images/power_cord_plugged_two.png' # Second plugged power cord
pittsburgh_load = 'images/pittsburgh.png' # View of Pittsburgh
tablevase_load = 'images/tablevase.png' # Table and Vase

hanging_shirt = pygame.image.load(hanging_shirt_load)
laying_remote = pygame.image.load(laying_remote_load)
laying_paper = pygame.image.load(laying_paper_load) # todo figure out .convert_alpha()
rotated_batteries = pygame.image.load(rotated_batteries_load)
laying_power_cord = pygame.image.load(laying_power_cord_load)
red_book_rotated = pygame.image.load(red_book_rotated_load)
blue_book_rotated = pygame.image.load(blue_book_rotated_load)
flathead = pygame.image.load(flathead_load)
door_key_rotated = pygame.image.load(door_key_rotated_load)
green_key_rotated = pygame.image.load(green_key_rotated_load)
power_cord_plugged_1 = pygame.image.load(power_cord_plugged_1_load)
power_cord_plugged_1_flip = pygame.image.load(power_cord_plugged_1_flip_load)
power_cord_plugged_2 = pygame.image.load(power_cord_plugged_2_load)
pittsburgh = pygame.image.load(pittsburgh_load)
tablevase = pygame.image.load(tablevase_load)

# Load Sounds
key_sound = pygame.mixer.Sound('sounds/key_jingle.wav')
door_open_sound = pygame.mixer.Sound('sounds/door_open.wav')
door_close_sound = pygame.mixer.Sound('sounds/door_close.wav')
paper_found_sound = pygame.mixer.Sound('sounds/pick_paper.wav')
book_found_sound = pygame.mixer.Sound('sounds/pick_book.wav')
input_battery_sound = pygame.mixer.Sound('sounds/input_battery.wav')
battery_found_sound = pygame.mixer.Sound('sounds/battery_found.wav')
drawer_open_sound = pygame.mixer.Sound('sounds/drawer_open.wav')
drawer_close_sound = pygame.mixer.Sound('sounds/drawer_close.wav')
file_cabinet_open_sound = pygame.mixer.Sound('sounds/file_cabinet_open.wav')
file_cabinet_close_sound = pygame.mixer.Sound('sounds/file_cabinet_close.wav')
item_picked = pygame.mixer.Sound('sounds/item_picked.wav')
light_sound = pygame.mixer.Sound('sounds/light_switch.wav')
shirt_sound = pygame.mixer.Sound('sounds/pick_shirt.wav')
safe_door = pygame.mixer.Sound('sounds/safe_door.wav')

pygame.init()
pygame.font.init()


class Room():
    """Class to store the objects of the rooms and the views regarding them"""
    
    def __init__(self, gs, screen, stable_item_blocks):
        self.gs = gs
        self.screen = screen
        #self.game_obects = game_objects

        global fcd1
        global fcd2
        global fcdo1
        global fcdo2
        global fcd_handle

        fcd1 = pygame.Rect(690, 474, 150, 98)
        fcdo1 = fcd1.move(34, 46)
        fcd2 = fcd1.move(0, 98)
        fcdo2 = fcd1.move(34, 144)
        fcd_handle = pygame.Rect(0, 0, 44, 10)

        global desk_drawer1
        global desk_drawer2
        global desk_drawer3
        global desk_drawer1_opened
        global desk_drawer2_opened
        global desk_drawer3_opened

        desk_drawer1 = pygame.Rect(100, 492, 160, 40)
        desk_drawer2 = desk_drawer1.move(0, 59)
        desk_drawer3 = desk_drawer1.move(0, 118)
        desk_drawer1_opened = pygame.Rect(46, 543, 185, 40)
        desk_drawer2_opened = desk_drawer1_opened.move(0, 59)
        desk_drawer3_opened = desk_drawer1_opened.move(0, 118)

        # Door Settings
        self.door_handle_rect = pygame.draw.circle(screen, gs.yellow, (585, 390), 15)
        self.main_door = pygame.Rect(390, 160, 225, 440)
        self.opened_door = [(248, 101), (self.main_door.topleft), (self.main_door.bottomleft), (248, 674)]

        # Window Settings
        self.e_window = pygame.Rect(305, 80, 500, 600)
        self.click_window_int_frame = pygame.Rect(0, self.e_window.top, 12, self.e_window.height)

        # Trash Can Opening
        self.can_opening_rect = pygame.Rect(350, 220, 350, 350)

        # TV Settings
        self.tv_screen_glass = pygame.Rect(195, 140, 470, 296)
        self.partial_tv_screen_glass = pygame.Rect(945, 140, 470, 296)

        # Safe
        self.safe = pygame.Rect(270, 130, 480, 270)
        self.safe_hole = self.safe.inflate(90, 60)
        self.safe_cover = self.safe_hole.inflate(10,10)
        self.safe_handle = pygame.Rect(700, 240, 30, 80)

        # Safe Numbers
        self.safe_number_rect_n1 = pygame.Rect((self.safe.topleft[0] + 20), (self.safe.topleft[1] + 20), 70, 100)
        self.safe_number_rect_n2 = self.safe_number_rect_n1.move(90, 0)
        self.safe_number_rect_n3 = self.safe_number_rect_n2.move(90, 0)
        self.safe_number_rect_n4 = self.safe_number_rect_n3.move(90, 0)

        self.safe_number_n1 = 0
        self.safe_number_n2 = 0
        self.safe_number_n3 = 0
        self.safe_number_n4 = 0

        # Alphabet Code
        #self.safe_alpha_a1 = gs.alphabet_list[gs.safe_alpha_index]
        self.safe_alpha_rect_a1 = self.safe_number_rect_n2.move(0, 130)

        # Safe Colors
        self.safe_number_rect_c1 = self.safe_number_rect_n3.move(0, 130)
        self.safe_number_rect_c2 = self.safe_number_rect_n4.move(0, 130)

        self.safe_color_c1 = gs.black
        self.safe_color_c2 = gs.black
        self.index_color1 = gs.color_codes.get('purple')[0]
        self.index_color2 = gs.color_codes.get('purple')[0]

        # Safe Initialization
        self.safe_use_rect = self.safe_number_rect_n1.move(0, 130)

        # Clickable Power Cord Settings
        self.laying_power_cord_rect = laying_power_cord.get_rect()
        self.laying_power_cord_scaled = pygame.transform.smoothscale(laying_power_cord, (int(self.laying_power_cord_rect[2]/1.5), int(self.laying_power_cord_rect[3]/1.5)))
        self.laying_power_cord_scaled_rect = self.laying_power_cord_scaled.get_rect(center = self.can_opening_rect.center)



        self.laying_paper_clicker = gf.draw_item_to_screen(gs, screen, laying_paper, 2, 380, 475)
        self.remote_clicker = gf.draw_item_to_screen(gs, screen, laying_remote, 4.5, 380, 493)
        self.door_key_clicker = gf.draw_item_to_screen(gs, screen, door_key_rotated, 6, 521, 335)
        self.shirt_surface = pygame.Rect(125, 212, 150, 235)
        self.table_surface = pygame.Rect(0, 0, 500, 500) # todo update this accordingly

        # Wall Outlets
        self.desk_wall_outlet = pygame.Rect(362, 528, 26, 42)
        self.window_wall_outlet = pygame.Rect(930, 528, 26, 42)

        self.hole_in_floor = None

        # Trash Can
        self.top_of_can = pygame.Rect(130, 555, 120, 25)
        self.trash_can_clickbox = pygame.Rect(149, 582, 82, 101)

        # Light Switch
        self.light_switch = pygame.Rect(650, 325, 30, 40)



        """
        # Door Key
        self.door_key_rotated_full_rect = door_key_rotated.get_rect()
        self.door_key_rotated_surface = (int(self.door_key_rotated_full_rect[2] / 6), int(self.door_key_rotated_full_rect[3] / 6))
        self.door_key_rotated_rect = pygame.Rect(521, 335, self.door_key_rotated_surface[0], self.door_key_rotated_surface[1])

        # Papers
        self.laying_paper_full_rect = laying_paper.get_rect()
        self.laying_paper_surface = (int(self.laying_paper_full_rect[2] / 2), int(self.laying_paper_full_rect[3] / 2))
        self.laying_paper_rect = pygame.Rect(380, 475, self.laying_paper_surface[0], self.laying_paper_surface[1])

        # Remote
        self.laying_remote_full_rect = laying_remote.get_rect()
        self.laying_remote_surface = (int(self.laying_remote_full_rect[2] / 4.5), int(self.laying_remote_full_rect[3] / 4.5))
        self.laying_remote_rect = pygame.Rect(380, 493, self.laying_remote_surface[0], self.laying_remote_surface[1])

        # Flathead
        self.flathead_full_rect = flathead.get_rect()
        self.flathead_surface = (int(self.flathead_full_rect[2]/4), int(self.flathead_full_rect[3]/4))
        self.flathead_rect = pygame.Rect(124, 528, self.flathead_surface[0], self.flathead_surface[1])

        # Batteries
        #self.rotated_batteries_full_rect = rotated_batteries.get_rect()
        #self.rotated_batteries_surface = (int(self.rotated_batteries_full_rect[2] / 13), int(self.rotated_batteries_full_rect[3] / 13))
        #self.rotated_batteries_rect = pygame.Rect(174, 588, self.rotated_batteries_surface[0], self.rotated_batteries_surface[1])

        # Red Book

        # Blue Book

        # Green Key

        """
        # Safe Door
        self.safe_door = ((-5, 183), (self.safe.topleft), (self.safe.bottomleft), (-5, 577))
        
        # clickbox_name = [(), (), (), (), (), (), (), (), (), (), (), ()]

    def click_safe_cover(self, gs, event):
        if self.safe_cover.collidepoint(event.pos) and gs.room_view_drill_down == 1 and gs.current_room_view == 2 or gs.current_room_view == -2:
            gs.text = 'There seems to be something here...'

    def click_safe_while_off(self, gs, event):
        if self.safe.collidepoint(event.pos) and gs.room_view_drill_down == 1 and gs.current_room_view == 2 or gs.current_room_view == -2:
            gs.text = 'The safe says, "OFF".'

    def click_desk_wall_outlet(self, gs, event):
        if self.desk_wall_outlet.collidepoint(event.pos):
            gs.text = "It's a wall outlet..."

    def click_window_wall_outlet(self, gs, event):
        if self.window_wall_outlet.collidepoint(event.pos):
            gs.text = "It's a wall outlet..."


    def click_papers(self, gs, event):
        # function to be able to pick up the papers item
        if self.laying_paper_clicker.collidepoint(event.pos):
            gs.text = 'Papers with writing on them!'
            pygame.mixer.Sound.play(paper_found_sound)
            gs.papers_found = True

    def click_shirt(self, gs, event):
        # function to be able to pick up the shirt item
        if self.shirt_surface.collidepoint(event.pos):
            gs.text = "If I get out of here, I'm wearing this shirt!"
            pygame.mixer.Sound.play(shirt_sound)
            gs.shirt_found = True

    def click_flathead(self, gs, event):
        # function to be able to pick up the flathead item
        if self.flathead_clicker.collidepoint(event.pos):
            gs.text = 'A normal screwdriver!'
            pygame.mixer.Sound.play(item_picked)
            gs.screwdriver_found = True
            gs.moveable_items_index_list.append(6)

    def click_red_book(self, gs, event):
        # function to be able to pick up the red book item
        if self.red_book_clicker.collidepoint(event.pos) and not fcdo1.collidepoint(event.pos):
            gs.text = "A red book! What's inside?"
            pygame.mixer.Sound.play(book_found_sound)
            gs.red_book_found = True

    def click_blue_book(self, gs, event):
        # function to be able to pick up the blue book item
        if self.blue_book_clicker.collidepoint(event.pos) and not fcdo2.collidepoint(event.pos):
            gs.text = 'Wow! A blue book was in this drawer!'
            pygame.mixer.Sound.play(book_found_sound)
            gs.blue_book_found = True

    def click_green_key(self, gs, event):
        # function to be able to pick up the green key item
        if self.green_key_clicker.collidepoint(event.pos):
            gs.text = 'I found a green key!'
            pygame.mixer.Sound.play(key_sound)
            gs.green_key_found = True
            gs.moveable_items_index_list.append(3)

    def click_power_cord(self, gs, event):
        # function to be able to pick up the power cord item
        if self.laying_power_cord_scaled_rect.collidepoint(event.pos):
            gs.text = 'A power cord! What can this be used for?'
            pygame.mixer.Sound.play(item_picked)
            gs.power_cord_found = True
            gs.moveable_items_index_list.append(5)

    def pick_power_cord_desk(self, gs, event):
        # function to be able to pick up plugged power cord
        if self.power_cord_1_clicker.collidepoint(event.pos):
            gs.text = "Maybe it doesn't go here..."
            pygame.mixer.Sound.play(item_picked)
            gs.power_cord_used = False
            gs.power_cord_desk_1 = False
            gs.moveable_items_index_list.append(5)

    def pick_power_cord_window(self, gs, event):
        # function to be able to pick up plugged power cord
        if self.power_cord_window_clicker.collidepoint(event.pos):
            gs.text = "Maybe it doesn't go here..."
            pygame.mixer.Sound.play(item_picked)
            gs.power_cord_used = False
            gs.power_cord_window_1 = False
            gs.moveable_items_index_list.append(5)

    def click_batteries(self, gs, event):
        # function to be able to pick up the batteries item
        if self.battery_clicker.collidepoint(event.pos):
            gs.text = 'Batteries! What can these be for?'
            pygame.mixer.Sound.play(battery_found_sound)
            gs.batteries_found = True
            gs.moveable_items_index_list.append(4)

    def click_remote(self, gs, event):
        # function to be able to pick up the remote item
        if self.remote_clicker.collidepoint(event.pos):
            gs.text = 'A remote!  I can probably use this on the TV...'
            pygame.mixer.Sound.play(item_picked)
            gs.remote_found = True

    def click_hole_in_floor(self, gs, event):
        # function to be able to connect camera cable power cord
        if self.hole_in_floor.collidepoint(event.pos) and gs.power_cord_desk_1:
            gs.text = 'The power cord was able to be plugged into this hole!'
            pygame.mixer.Sound.play(light_sound)
            gs.power_cord_desk_2 = True
        elif self.hole_in_floor.collidepoint(event.pos) and gs.power_cord_desk_2:
            gs.text = 'The power cord is plugged in. What does it do?'
        elif self.hole_in_floor.collidepoint(event.pos) and not gs.power_cord_desk_1:
            gs.text = "There seems to be a hole in the floor here..."



        
    def room_view_three_1(self, gs, screen, stable_item_blocks):  # View next to TV stand
        # Clear Screen
        screen.fill(gs.bg_color)

        # Carpet
        pygame.draw.polygon(screen, gs.carpet, ((0, 460), (680, 460), (1093, 740), (0, 740)))
        
        # Lines
        pygame.draw.line(screen, gs.black, (360, 460), (680, 460), 5)
        pygame.draw.line(screen, gs.black, (680, 460), (680, 0), 5)
        pygame.draw.line(screen, gs.black, (680, 460), (1093, 740), 5)
        
        # TV Stand
        pygame.draw.polygon(screen, gs.wood, ((360, 465), (230, 686), (-3, 686), (-3, 80), (230, 80), (360, 170)))
        pygame.draw.polygon(screen, gs.black, ((360, 465), (230, 686), (-3, 686), (-3, 80), (230, 80), (360, 170)), 3)
        
        pygame.draw.rect(screen, gs.dark_wood, (-3, 123, 188, 520))
        pygame.draw.rect(screen, gs.darker_wood, (-3, 123, 188, 30))
        pygame.draw.rect(screen, gs.black, (-3, 123, 188, 520), 3)        
        
        pygame.draw.line(screen, gs.black, (230, 686), (230, 80), 3)
        pygame.draw.line(screen, gs.black, (0, 465), (184, 465), 3)
        pygame.draw.line(screen, gs.black, (0, 153), (184, 153), 3)

        # Draw Remote
        if not gs.remote_found:
            self.remote_clicker = gf.draw_item_to_screen(gs, screen, laying_remote, 4.5, 380, 493)


        #screen.blit(pygame.transform.smoothscale(laying_remote, (int(self.laying_remote_full_rect[2] / 4.5), int(self.laying_remote_full_rect[3] / 4.5))), self.laying_remote_rect)
        #pygame.draw.rect(screen, gs.yellow, self.laying_remote_rect, 3) # todo comment out later


        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
        
    def room_view_four_1(self, gs, screen, stable_item_blocks):  # View inside of closet
        # Clear Screen
        screen.fill(gs.door)
        
        # Lines
        pygame.draw.line(screen, gs.black, (876, 508), (1074, 741), 5)
        pygame.draw.line(screen, gs.black, (876, 508), (0, 508), 5)
        pygame.draw.line(screen, gs.black, (876, 508), (876, 0), 5)

        if gs.safe_uncovered:  # Safe is covered by a panel that requires a screwdriver to take off

            # Safe Hole
            pygame.draw.rect(screen, gs.dark_gray, self.safe_hole)
            pygame.draw.rect(screen, gs.black, self.safe_hole, 5)
            pygame.draw.line(screen, gs.black, self.safe_hole.topleft, ((self.safe.topleft[0]+30),(self.safe.topleft[1]+30)), 3)
            pygame.draw.line(screen, gs.black, self.safe_hole.topright, ((self.safe.topright[0]-30),(self.safe.topright[1]+30)), 3)
            pygame.draw.line(screen, gs.black, self.safe_hole.bottomleft, ((self.safe.bottomleft[0]+30),(self.safe.bottomleft[1]-40)), 3)
            pygame.draw.line(screen, gs.black, self.safe_hole.bottomright, ((self.safe.bottomright[0]-30),(self.safe.bottomright[1]-40)), 3)

            if gs.safe_opened:
                # Opened Safe
                pygame.draw.rect(screen, gs.tv_screen, self.safe)
                pygame.draw.rect(screen, gs.black, self.safe, 4)

                # Draw Opened Safe Door
                pygame.draw.polygon(screen, gs.tv_screen, self.safe_door)
                pygame.draw.polygon(screen, gs.black, ((-5, 183), (self.safe.topleft), (self.safe.bottomleft), (-5, 577)), 3)

                self.back_of_safe = self.safe.inflate(-180, -190)
                pygame.draw.rect(screen, gs.tv_screen, self.back_of_safe)
                pygame.draw.rect(screen, gs.black, self.back_of_safe, 3)
                pygame.draw.line(screen, gs.black, self.safe.topleft, self.back_of_safe.topleft, 3)
                pygame.draw.line(screen, gs.black, self.safe.topright, self.back_of_safe.topright, 3)
                pygame.draw.line(screen, gs.black, self.safe.bottomleft, self.back_of_safe.bottomleft, 3)
                pygame.draw.line(screen, gs.black, self.safe.bottomright, self.back_of_safe.bottomright, 3)

                # Draw Door Key
                if not gs.door_key_found:
                    #screen.blit(pygame.transform.smoothscale(door_key_rotated, (int(self.door_key_rotated_full_rect[2] / 6), int(self.door_key_rotated_full_rect[3] / 6))), self.door_key_rotated_rect)
                    #pygame.draw.rect(screen, gs.yellow, self.door_key_rotated_rect, 3) # todo comment this out
                    self.door_key_clicker = gf.draw_item_to_screen(gs, screen, door_key_rotated, 6, 521, 335)

            else:
                if gs.safe_on:
                    gs.safe_use_color = gs.red
                    self.safe_back_color = gs.off_white
                    self.safe_status_color_on = gs.green
                    self.safe_status_color_off = gs.black
                    if gs.safe_initialized:
                        gs.safe_use_color = gs.green
                else:
                    self.safe_status_color_on = gs.black
                    self.safe_status_color_off = gs.red
                    self.safe_back_color = gs.black
                    gs.safe_use_color = gs.black

                # Closed Safe
                pygame.draw.rect(screen, gs.safe, self.safe)
                pygame.draw.rect(screen, gs.black, self.safe, 4)

                # Handle
                pygame.draw.rect(screen, gs.gray, self.safe_handle)
                pygame.draw.rect(screen, gs.black, self.safe_handle, 3)

                # Numbers
                pygame.draw.rect(screen, self.safe_back_color, self.safe_number_rect_n1) # Number spot 1
                pygame.draw.rect(screen, self.safe_back_color, self.safe_number_rect_n2) # Number spot 2
                pygame.draw.rect(screen, self.safe_back_color, self.safe_number_rect_n3) # Number spot 3
                pygame.draw.rect(screen, self.safe_back_color, self.safe_number_rect_n4) # Number spot 4
                pygame.draw.rect(screen, self.safe_back_color, self.safe_alpha_rect_a1) # Alpha spot 1

                self.n1_image = gs.arial60.render(str(self.safe_number_n1), True, gs.black) # n1 text
                self.n2_image = gs.arial60.render(str(self.safe_number_n2), True, gs.black) # n2 text
                self.n3_image = gs.arial60.render(str(self.safe_number_n3), True, gs.black) # n3 text
                self.n4_image = gs.arial60.render(str(self.safe_number_n4), True, gs.black) # n4 text

                self.n1_rect = self.n1_image.get_rect(center=self.safe_number_rect_n1.center) # n1 rect
                self.n2_rect = self.n2_image.get_rect(center=self.safe_number_rect_n2.center) # n2 rect
                self.n3_rect = self.n3_image.get_rect(center=self.safe_number_rect_n3.center) # n3 rect
                self.n4_rect = self.n4_image.get_rect(center=self.safe_number_rect_n4.center) # n4 rect

                self.a1_image = gs.arial60.render(str(gs.alphabet_list[gs.safe_alpha_index]), True, gs.black) # a1 text
                self.a1_rect = self.a1_image.get_rect(center=self.safe_alpha_rect_a1.center) # a1 rect

                screen.blit(self.n1_image, self.n1_rect) # n1 blit
                screen.blit(self.n2_image, self.n2_rect) # n2 blit
                screen.blit(self.n3_image, self.n3_rect) # n3 blit
                screen.blit(self.n4_image, self.n4_rect) # n4 blit
                screen.blit(self.a1_image, self.a1_rect) # a1 blit



                # On / Off Settings
                self.safe_on_block = pygame.Rect(657, 170, 8, 8)
                self.safe_off_block = self.safe_on_block.move(0, 30)

                pygame.draw.circle(screen, self.safe_status_color_on, self.safe_on_block.center, 8)
                pygame.draw.circle(screen, self.safe_status_color_off, self.safe_off_block.center, 8)
                pygame.draw.circle(screen, gs.black, self.safe_on_block.center, 9, 2)
                pygame.draw.circle(screen, gs.black, self.safe_off_block.center, 9, 2)

                self.on_text = gs.arial16.render('ON', True, gs.white)
                self.off_text = gs.arial16.render('OFF', True, gs.white)

                screen.blit(self.on_text, ((self.safe_on_block.x + 20), self.safe_on_block.y - 6))
                screen.blit(self.off_text, ((self.safe_off_block.x + 20), self.safe_off_block.y - 6))

                # Initialization Block
                pygame.draw.rect(screen, gs.safe_use_color, self.safe_use_rect) # Initiation
                pygame.draw.rect(screen, self.safe_color_c1, self.safe_number_rect_c1) # Color spot 1
                pygame.draw.rect(screen, self.safe_color_c2, self.safe_number_rect_c2) # Color Spot 2

                # Borders
                pygame.draw.rect(screen, gs.black, self.safe_number_rect_n1, 2) # Number spot 1
                pygame.draw.rect(screen, gs.black, self.safe_number_rect_n2, 2) # Number spot 2
                pygame.draw.rect(screen, gs.black, self.safe_number_rect_n3, 2) # Number spot 3
                pygame.draw.rect(screen, gs.black, self.safe_number_rect_n4, 2) # Number spot 4
                pygame.draw.rect(screen, gs.black, self.safe_use_rect, 2) # Initiation
                pygame.draw.rect(screen, gs.black, self.safe_number_rect_c1, 2) # Color spot 1
                pygame.draw.rect(screen, gs.black, self.safe_number_rect_c2, 2) # Color Spot 2
                pygame.draw.rect(screen, gs.black, self.safe_alpha_rect_a1, 2) # Alpha Spot 1



        else:  # Safe Panel not removed
            pygame.draw.rect(screen, gs.door, self.safe_cover)
            pygame.draw.rect(screen, gs.black, self.safe_cover, 2)

        # Draw Papers
        if not gs.papers_found:
            #screen.blit(pygame.transform.smoothscale(laying_paper, (int(self.laying_paper_full_rect[2] / 2), int(self.laying_paper_full_rect[3] / 2))), self.laying_paper_rect)
            #pygame.draw.rect(screen, gs.black, self.laying_paper_rect, 3) # todo comment this out
            self.laying_paper_clicker = gf.draw_item_to_screen(gs, screen, laying_paper, 2, 380, 475)


        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)

    def safe_controls(self, gs, screen, event):
        if gs.safe_uncovered:
            if gs.safe_on:
                gs.text = 'The safe is on!'
                # This code will open the safe if all the conditions are met
                if gs.safe_initialized == True and gs.color_number_1 == gs.tv_color_numbers[0] and gs.color_number_2 == gs.tv_color_numbers[1] and gs.safe_combo_n1 == gs.safe_combo[0] and gs.safe_combo_n2 == gs.safe_combo[1] and gs.safe_combo_n3 == gs.safe_combo[2] and gs.safe_combo_n4 == gs.safe_combo[3] and gs.safe_combo_a1 == gs.safe_alpha_pra_answer and self.safe_handle.collidepoint(event.pos):
                    pygame.mixer.Sound.play(safe_door)
                    gs.safe_opened = True
                if gs.safe_opened == True:
                    gs.text = 'WOW! I opened the safe!'
                    if not gs.door_key_found:
                        if self.door_key_clicker.collidepoint(event.pos):
                            pygame.mixer.Sound.play(key_sound)
                            gs.text = 'I found a gold key!'
                            gs.door_key_found = True
                            gs.moveable_items_index_list.append(0)
                    if gf.check_inside_clickbox(self, self.safe_door, ((event.pos), (0, 0))):
                        pygame.mixer.Sound.play(safe_door)
                        gs.safe_opened = False
                else:
                    # Number Button 1
                    if self.safe_number_rect_n1.collidepoint(event.pos):
                        self.safe_number_n1 += 1
                        gs.safe_combo_n1 = self.safe_number_n1
                        if self.safe_number_n1 > 9:
                            self.safe_number_n1 = 0
                    # Number Button 2
                    if self.safe_number_rect_n2.collidepoint(event.pos):
                        self.safe_number_n2 += 1
                        gs.safe_combo_n2 = self.safe_number_n2
                        if self.safe_number_n2 > 9:
                            self.safe_number_n2 = 0
                    # Number Button 3
                    if self.safe_number_rect_n3.collidepoint(event.pos):
                        self.safe_number_n3 += 1
                        gs.safe_combo_n3 = self.safe_number_n3
                        if self.safe_number_n3 > 9:
                            self.safe_number_n3 = 0
                    # Number Button 4
                    if self.safe_number_rect_n4.collidepoint(event.pos):
                        self.safe_number_n4 += 1
                        gs.safe_combo_n4 = self.safe_number_n4
                        if self.safe_number_n4 > 9:
                            self.safe_number_n4 = 0
                    # Alpha Button 1
                    if self.safe_alpha_rect_a1.collidepoint(event.pos):
                        gs.safe_alpha_index += 1
                        gs.safe_combo_a1 = gs.safe_alpha_index
                        if gs.safe_alpha_index == 26:
                            gs.safe_alpha_index = 0
                            gs.safe_combo_a1 = 0
                    # Color Button 1
                    elif self.safe_number_rect_c1.collidepoint(event.pos):
                        for v in gs.color_codes.values():
                            if v[0] == self.index_color1:
                                self.safe_color_c1 = v[2]
                                gs.color_number_1 = v[0]
                        if self.index_color1 == 6:
                            self.index_color1 = 1
                        else:
                            self.index_color1 += 1
                    # Color Button 2
                    elif self.safe_number_rect_c2.collidepoint(event.pos):
                        for v in gs.color_codes.values():
                            if v[0] == self.index_color2:
                                self.safe_color_c2 = v[2]
                                gs.color_number_2 = v[0]
                        if self.index_color2 == 6:
                            self.index_color2 = 1
                        else:
                            self.index_color2 += 1
            else:
                self.click_safe_while_off(gs, event)
        else:
            self.click_safe_cover(gs, event)

    def room_view_four_2(self, gs, screen, stable_item_blocks):  # View of window
        # Clear Screen
        screen.fill(gs.bg_color)

        # Window
        window_frame = pygame.Rect(255, 50, 600, 680)
        self.click_window_int_frame.centerx = self.e_window.centerx
        
        pygame.draw.rect(screen, gs.gray, window_frame)
        pygame.draw.rect(screen, gs.black, window_frame, 3)
        pygame.draw.line(screen, gs.black, window_frame.topleft, self.e_window.topleft, 3)
        pygame.draw.line(screen, gs.black, window_frame.topright, self.e_window.topright, 3)
        pygame.draw.line(screen, gs.black, window_frame.bottomleft, self.e_window.bottomleft, 3)
        pygame.draw.line(screen, gs.black, window_frame.bottomright, self.e_window.bottomright, 3)
        pygame.draw.rect(screen, gs.off_white, self.e_window)
        pygame.draw.rect(screen, gs.black, self.click_window_int_frame, 3)
        pygame.draw.rect(screen, gs.black, self.e_window, 3)
        
        # Lines
        pygame.draw.line(screen, gs.black, (40, 0), (40, 741), 5)

        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
        
    def room_view_four_2_1(self, gs, screen, stable_item_blocks):  # View of outside window
        screen.fill(gs.white)
        # Clear Screen
        pittsburgh_scaled = gf.aspect_scale_wh(pittsburgh, int(gs.gw_width*1.05), int(gs.gw_height*1.05))
        screen.blit(pittsburgh_scaled, (-10, -10))

        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)

    def room_view_zero_1(self, gs, screen, stable_item_blocks):  # View of inside trash can
        # Clear Screen
        gs.text = None

        screen.fill(gs.carpet)

        pygame.draw.circle(screen, gs.dark_brown, self.can_opening_rect.center, 250)
        pygame.draw.circle(screen, gs.black, self.can_opening_rect.center, 250, 3)
        pygame.draw.circle(screen, gs.brown, self.can_opening_rect.center, 149)
        pygame.draw.circle(screen, gs.black, self.can_opening_rect.center, 150, 3)
        pygame.draw.rect(screen, gs.bg_color, (0, 0, 1190, 84))
        pygame.draw.line(screen, gs.black, (0, 84), (1190, 84), 5)

        # Draw Laying Power Cord
        if not gs.power_cord_found:
            screen.blit(self.laying_power_cord_scaled, self.laying_power_cord_scaled_rect)
            #pygame.draw.rect(screen, gs.yellow, self.laying_power_cord_scaled_rect, 3)

        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
        
    def room_view_one(self, gs, screen, stable_item_blocks):  # View with door ; Default view

                
        if gs.lights_on == False:

            screen.fill(gs.black)
            # Light Switch
            pygame.draw.rect(screen, gs.yellowish, self.light_switch)
            pygame.draw.rect(screen, gs.black, self.light_switch, 3)
            pygame.draw.rect(screen, gs.black, (660, 335, 10, 20), 1)

        else:



            # Carpet
            pygame.draw.polygon(screen, gs.carpet, ((0, 725), (330, 600), (1070, 600), (1070, 735), (0, 735)))

            # Light Switch            
            pygame.draw.rect(screen, gs.off_white, self.light_switch) # light switch body
            pygame.draw.rect(screen, gs.black, self.light_switch, 3) # light switch border
            pygame.draw.rect(screen, gs.black, (660, 335, 10, 20), 1) # light switch interior
            
            # Lines
            pygame.draw.line(screen, gs.black, (0, 725), (330, 600), 5)
            pygame.draw.line(screen, gs.black, (330, 600), (330,0), 5)
            pygame.draw.line(screen, gs.black, (330, 600), (1100, 600), 5)


            if gs.door_opened and gs.room_view_drill_down == 0:


                # Draw Open Door Handle
                pygame.draw.circle(screen, gs.yellow, (243, 398), 15)
                pygame.draw.circle(screen, gs.black, (243, 398), 16, 2)

                # Draw Open door
                pygame.draw.rect(screen, gs.white, self.main_door)


                pygame.draw.rect(screen, gs.dark_blue, ((self.main_door.x, self.main_door.y), (self.main_door.width, 486 - self.main_door.y)))
                pygame.draw.rect(screen, gs.the_other_gray, ((self.main_door.x, 486), (self.main_door.width, (self.main_door.y + self.main_door.height - 486))))
                pygame.draw.line(screen, gs.black, (self.main_door.x, 486), (self.main_door.x + self.main_door.width, 486), 3)

                tablevase_scaled = gf.aspect_scale(tablevase, 180) # table and vase scaled
                screen.blit(tablevase_scaled, (370, 395))

                pygame.draw.polygon(screen, gs.door, self.opened_door)
                pygame.draw.polygon(screen, gs.black, self.opened_door, 3)
                pygame.draw.line(screen, gs.black, (250, 101), (250, 674), 8)

                pygame.draw.rect(screen, gs.black, self.main_door, 3)





            else:
                # Door
                pygame.draw.rect(screen, gs.door, self.main_door)
                pygame.draw.rect(screen, gs.black, self.main_door, 3)
                pygame.draw.circle(screen, gs.dark_gray, (585-3, 390+5), 15)
                self.door_handle_rect = pygame.draw.circle(screen, gs.yellow, (585, 390), 15)
                pygame.draw.circle(screen, gs.black, (585, 390), 16, 2)
                pygame.draw.circle(screen, gs.black, (585, 390), 4, 1)
            
            # TV Stand
            pygame.draw.polygon(screen, gs.wood, ((900, 500), (870, 530), (1070, 530), (1070, 500)))
            pygame.draw.polygon(screen, gs.black, ((900, 500), (870, 530), (1070, 530), (1070, 500)), 3)
            pygame.draw.rect(screen, gs.wood, (870, 530, 620, 100))
            pygame.draw.rect(screen, gs.dark_wood, (870, 540, 600, 80))
            front_tv_stand = pygame.Rect(880, 540, 600, 80)
            back_tv_stand = pygame.Rect(910, 540, 540, 50)
            pygame.draw.rect(screen, gs.black, front_tv_stand, 3)
            pygame.draw.rect(screen, gs.black, back_tv_stand, 3)
            pygame.draw.line(screen, gs.black, front_tv_stand.bottomleft, back_tv_stand.bottomleft, 3)
            pygame.draw.line(screen, gs.black, front_tv_stand.bottomright, back_tv_stand.bottomright, 3)
            pygame.draw.rect(screen, gs.black, (870, 530, 620, 100), 3)  
            
            # TV
            pygame.draw.rect(screen, gs.black, (930, 125, 500, 326))
            pygame.draw.rect(screen, gs.current_tv_screen_color, self.partial_tv_screen_glass)

            if gs.tv_on:
                channel_text = gs.verdana16.render(str(gs.current_channel), True, gs.green)
                tv_channels.tv_channels(gs, screen)
                screen.blit(channel_text, ((self.partial_tv_screen_glass.x + 3), self.partial_tv_screen_glass.y))

            # Trash Can

            bottom_of_can = pygame.Rect(0, 675, 90, 25)

            bottom_of_can.centerx = self.top_of_can.centerx

            pygame.draw.ellipse(screen, gs.dark_gray, (bottom_of_can.x - 18, bottom_of_can.y + 2, bottom_of_can.width, bottom_of_can.height))
            pygame.draw.polygon(screen, gs.brown, ((self.top_of_can.midleft), (self.top_of_can.midright), (bottom_of_can.midright), (bottom_of_can.midleft)))

            pygame.draw.polygon(screen, gs.black, ((self.top_of_can.midleft), (self.top_of_can.midright), (bottom_of_can.midright), (bottom_of_can.midleft)), 3)
            pygame.draw.ellipse(screen, gs.brown, bottom_of_can)


            pygame.draw.ellipse(screen, gs.dark_brown, self.top_of_can)

            pygame.draw.arc(screen, gs.black, bottom_of_can, pi, 2*pi, 3)
            pygame.draw.arc(screen, gs.black, bottom_of_can, .05+pi, 2*pi+.05, 3)

            pygame.draw.ellipse(screen, gs.black, self.top_of_can, 3)

            if gs.room_view_drill_down == 0.1:
                self.room_view_zero_1(gs, screen, stable_item_blocks)



            # Required in all views if items are opened during the view.
            if gs.stable_item_opened:
                self.find_stable_item_opened(gs, screen, stable_item_blocks)

    def room_view_two(self, gs, screen, stable_item_blocks):  # View with desk / File cabinet
        # Carpet
        pygame.draw.polygon(screen, gs.carpet, ((0, 735), (160, 600), (1075, 600), (1075, 735)))
        
        # Lines
        pygame.draw.line(screen, gs.black, (0, 735), (160, 600), 5)
        pygame.draw.line(screen, gs.black, (160, 600), (160,0), 5)
        pygame.draw.line(screen, gs.black, (160, 600), (1075, 600), 5)
        
        # Desk 
        pygame.draw.polygon(screen, gs.wood, ((168, 420), (84, 474), (84, 670), (275, 670), (323, 600), (323, 515), (638, 515), (638, 600), (678, 670), (690, 670), (690, 474), (657, 420)))
        pygame.draw.polygon(screen, gs.black, ((168, 420), (84, 474), (84, 670), (275, 670), (323, 600), (323, 515), (638, 515), (638, 600), (678, 670), (690, 670), (690, 474), (657, 420)), 3)
        


        pygame.draw.line(screen, gs.black, (275, 670), (275, 515), 3)
        pygame.draw.line(screen, gs.black, (275, 515), (678, 515), 3)
        pygame.draw.line(screen, gs.black, (678, 515), (678, 670), 3)
        pygame.draw.line(screen, gs.black, (84, 474), (690, 474), 3)  # Line for desk
               
        ########## Desk DrawerDrawer 3
        if gs.dd3_open_attempts < 4:
            if gs.dd3_opened:
                pygame.draw.polygon(screen, gs.interior_drawer, ((desk_drawer3_opened.topleft), (desk_drawer3_opened.topright), (desk_drawer3.topright), (desk_drawer3.topleft)))
                pygame.draw.line(screen, gs.black, (desk_drawer3_opened.topleft), (desk_drawer3.topleft), 2)
                pygame.draw.line(screen, gs.black, (desk_drawer3_opened.bottomleft), (desk_drawer3.bottomleft), 2)
                pygame.draw.line(screen, gs.black, (desk_drawer3.bottomleft), (desk_drawer3.topleft), 2)
                pygame.draw.line(screen, gs.black, (desk_drawer3.bottomleft), (desk_drawer3.bottomright), 2)
                pygame.draw.polygon(screen, gs.interior_drawer, ((desk_drawer3_opened.topright), (desk_drawer3_opened.bottomright), (desk_drawer3.bottomright), (desk_drawer3.topright)))
                pygame.draw.line(screen, gs.black, (desk_drawer3_opened.bottomright), (desk_drawer3.bottomright), 2)
                pygame.draw.line(screen, gs.black, (desk_drawer3_opened.topright), (desk_drawer3.topright), 2)
                pygame.draw.line(screen, gs.black, (desk_drawer3.bottomright), (desk_drawer3.topright), 2)
                pygame.draw.line(screen, gs.black, (desk_drawer3.topleft), (desk_drawer3.topright), 2)
                
                pygame.draw.rect(screen, gs.wood, desk_drawer3_opened)       
                pygame.draw.rect(screen, gs.black, desk_drawer3_opened, 3)
                pygame.draw.circle(screen, gs.silver, (desk_drawer3_opened.center), 7)
                pygame.draw.circle(screen, gs.black, (desk_drawer3_opened.center), 8, 2)
                
            else:
                pygame.draw.rect(screen, gs.black, desk_drawer3, 3)
                pygame.draw.circle(screen, gs.silver, (desk_drawer3.center), 7)
                pygame.draw.circle(screen, gs.black, (desk_drawer3.center), 8, 2)
                
        else:  # This block removes Desk Drawer 3 permanently and places it in the inventory
            if not gs.desk_drawer_removed:
                gs.text = 'Wow! There is something under here!'
            pygame.draw.polygon(screen, gs.wood, ((desk_drawer3.bottomleft), (desk_drawer3.topleft), (150, 610)))
            pygame.draw.polygon(screen, gs.carpet, ((desk_drawer3.bottomleft), (150, 610), (desk_drawer3.topright), (desk_drawer3.bottomright)))
            pygame.draw.polygon(screen, gs.black, ((desk_drawer3.bottomleft), (desk_drawer3.topleft), (150, 610)), 2)
            pygame.draw.polygon(screen, gs.black, ((desk_drawer3.bottomleft), (150, 610), (desk_drawer3.topright), (desk_drawer3.bottomright)), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer3.bottomleft), (150, 610), 2)
            self.hole_in_floor = pygame.draw.ellipse(screen, gs.black, (210, 633, 16, 8))
            pygame.draw.ellipse(screen, gs.dark_gray, (214, 635, 8, 4))

            gs.desk_drawer_removed = True


            # Draw Green Key
            #self.green_key_rotated_surface = pygame.Rect(148, 630, 50, 70)
            #self.green_key_rotated_rect = green_key_rotated.get_rect()
            #screen.blit(pygame.transform.smoothscale(green_key_rotated, (int(self.green_key_rotated_rect[2]/22), int(self.green_key_rotated_rect[3]/22))), self.green_key_rotated_surface)
            if not gs.green_key_found:
                self.green_key_clicker = gf.draw_item_to_screen(gs, screen, green_key_rotated, 22, 148, 630)

        # Wall Outlet
        pygame.draw.rect(screen, gs.off_white, self.desk_wall_outlet)
        pygame.draw.rect(screen, gs.black, (362, 528, 26, 42), 3)
        pygame.draw.rect(screen, gs.black, (369, 534, 12, 12), 1)
        pygame.draw.rect(screen, gs.black, (369, 552, 12, 12), 1)

        if gs.power_cord_desk_1:
            self.power_cord_1_clicker = gf.draw_item_to_screen(gs, screen, power_cord_plugged_1, 3, 361, 548)  # THIS IS GOOD for ROOM VIEW 2

        if gs.power_cord_desk_2:
            gs.power_cord_desk_1 = False
            self.power_cord_2_clicker = gf.draw_item_to_screen(gs, screen, power_cord_plugged_2, 3, 215, 548)
        
        ########## Desk Drawer 2
        if gs.dd2_opened:
            pygame.draw.polygon(screen, gs.interior_drawer, ((desk_drawer2_opened.topleft), (desk_drawer2_opened.topright), (desk_drawer2.topright), (desk_drawer2.topleft)))
            pygame.draw.line(screen, gs.black, (desk_drawer2_opened.topleft), (desk_drawer2.topleft), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer2_opened.bottomleft), (desk_drawer2.bottomleft), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer2.bottomleft), (desk_drawer2.topleft), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer2.bottomleft), (desk_drawer2.bottomright), 2)
            pygame.draw.polygon(screen, gs.interior_drawer, ((desk_drawer2_opened.topright), (desk_drawer2_opened.bottomright), (desk_drawer2.bottomright), (desk_drawer2.topright)))
            pygame.draw.line(screen, gs.black, (desk_drawer2_opened.bottomright), (desk_drawer2.bottomright), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer2_opened.topright), (desk_drawer2.topright), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer2.bottomright), (desk_drawer2.topright), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer2.topleft), (desk_drawer2.topright), 2)
            
            pygame.draw.rect(screen, gs.wood, desk_drawer2_opened)
            pygame.draw.rect(screen, gs.black, desk_drawer2_opened, 3)
            pygame.draw.circle(screen, gs.silver, (desk_drawer2_opened.center), 7)
            pygame.draw.circle(screen, gs.black, (desk_drawer2_opened.center), 8, 2)

            # Draw Batteries
            if not gs.batteries_found:
                self.battery_clicker = gf.draw_item_to_screen(gs, screen, rotated_batteries, 13, 174, 588)
            
        else:
            pygame.draw.rect(screen, gs.black, desk_drawer2, 3)
            pygame.draw.circle(screen, gs.silver, (desk_drawer2.center), 7)
            pygame.draw.circle(screen, gs.black, (desk_drawer2.center), 8, 2)
        
        ########## Desk Drawer 1
        if gs.dd1_opened:
            pygame.draw.polygon(screen, gs.interior_drawer, ((desk_drawer1_opened.topleft), (desk_drawer1_opened.topright), (desk_drawer1.topright), (desk_drawer1.topleft)))
            pygame.draw.line(screen, gs.black, (desk_drawer1_opened.topleft), (desk_drawer1.topleft), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer1_opened.bottomleft), (desk_drawer1.bottomleft), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer1.bottomleft), (desk_drawer1.topleft), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer1.bottomleft), (desk_drawer1.bottomright), 2)
            pygame.draw.polygon(screen, gs.interior_drawer, ((desk_drawer1_opened.topright), (desk_drawer1_opened.bottomright), (desk_drawer1.bottomright), (desk_drawer1.topright)))
            pygame.draw.line(screen, gs.black, (desk_drawer1_opened.bottomright), (desk_drawer1.bottomright), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer1_opened.topright), (desk_drawer1.topright), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer1.bottomright), (desk_drawer1.topright), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer1.topleft), (desk_drawer1.topright), 2)
            
            pygame.draw.rect(screen, gs.wood, desk_drawer1_opened)
            pygame.draw.rect(screen, gs.black, desk_drawer1_opened, 3)
            pygame.draw.circle(screen, gs.silver, (desk_drawer1_opened.center), 7)
            pygame.draw.circle(screen, gs.black, (desk_drawer1_opened.center), 8, 2)

            # Draw Flathead
            #screen.blit(pygame.transform.smoothscale(flathead, (int(self.flathead_full_rect[2] / 4), int(self.flathead_full_rect[3] / 4))), self.flathead_rect)
            #pygame.draw.rect(screen, gs.yellow, self.flathead_rect, 3)
            if not gs.screwdriver_found:
                self.flathead_clicker = gf.draw_item_to_screen(gs, screen, flathead, 4, 125, 528)


        else:
            pygame.draw.rect(screen, gs.black, desk_drawer1, 3)
            pygame.draw.circle(screen, gs.silver, (desk_drawer1.center), 7)
            pygame.draw.circle(screen, gs.black, (desk_drawer1.center), 8, 2)
        
        # File Cabinets
        pygame.draw.polygon(screen, gs.file_cabinet, ((657, 420), (690, 474), (840, 474), (788, 420)))
        pygame.draw.polygon(screen, gs.black, ((657, 420), (690, 474), (840, 474), (788, 420)), 3)
               

        
        ##### File Cabinet Drawers Opened
        if gs.fcd2_opened == True:          
            
            ########## FC Drawer 2
            
            pygame.draw.line(screen, gs.black, (fcd2.topright), (fcd2.bottomright), 2)
        
            pygame.draw.polygon(screen, gs.interior_drawer, ((fcd2.topleft), (fcd2.topright), (fcdo2.topright), (fcdo2.topleft)))
            pygame.draw.line(screen, gs.black, (fcd2.topright), (fcd2.bottomright), 2)
            pygame.draw.polygon(screen, gs.interior_drawer, ((fcd2.topleft), (fcd2.bottomleft), (fcdo2.bottomleft), (fcdo2.topleft)))
            pygame.draw.polygon(screen, gs.black, ((fcd2.topleft), (fcd2.topright), (fcdo2.topright), (fcdo2.topleft)), 2)
            pygame.draw.polygon(screen, gs.black, ((fcd2.topleft), (fcd2.bottomleft), (fcdo2.bottomleft), (fcdo2.topleft)), 2)

            # Blue Book in Drawer
            #self.blue_book_rotated_surface = pygame.Rect(728, 598, 50, 70)
            #self.blue_book_rotated_rect = blue_book_rotated.get_rect()
            #screen.blit(pygame.transform.smoothscale(blue_book_rotated, (int(self.blue_book_rotated_rect[2]/5), int(self.blue_book_rotated_rect[3]/5))), self.blue_book_rotated_surface)
            if not gs.blue_book_found:
                self.blue_book_clicker = gf.draw_item_to_screen(gs, screen, blue_book_rotated, 5, 728, 598)




            pygame.draw.rect(screen, gs.file_cabinet, fcdo2)
            pygame.draw.rect(screen, gs.black, fcdo2, 3)   
            fcd_handle.center = fcdo2.center
            pygame.draw.rect(screen, gs.silver, fcd_handle)
            pygame.draw.rect(screen, gs.black, fcd_handle, 2)

        else:
            pygame.draw.rect(screen, gs.file_cabinet, fcd2)
            pygame.draw.rect(screen, gs.black, fcd2, 3)
            fcd_handle.center = fcd2.center
            pygame.draw.rect(screen, gs.silver, fcd_handle)
            pygame.draw.rect(screen, gs.black, fcd_handle, 2)
            
        if gs.fcd1_opened == True:
            ########## FC Drawer 1
            
            pygame.draw.line(screen, gs.black, (fcd1.topright), (fcd1.bottomright), 2)
            
            pygame.draw.polygon(screen, gs.interior_drawer, ((fcd1.topleft), (fcd1.topright), (fcdo1.topright), (fcdo1.topleft)))
            pygame.draw.line(screen, gs.black, (fcd1.topright), (fcd1.bottomright), 2)
            pygame.draw.polygon(screen, gs.interior_drawer, ((fcd1.topleft), (fcd1.bottomleft), (fcdo1.bottomleft), (fcdo1.topleft)))
            pygame.draw.polygon(screen, gs.black, ((fcd1.topleft), (fcd1.topright), (fcdo1.topright), (fcdo1.topleft)), 2)
            pygame.draw.polygon(screen, gs.black, ((fcd1.topleft), (fcd1.bottomleft), (fcdo1.bottomleft), (fcdo1.topleft)), 2)

            # Red Book in Drawer
            #self.red_book_rotated_surface = pygame.Rect(728, 500, 50, 70)
            #self.red_book_rotated_rect = red_book_rotated.get_rect()
            #screen.blit(pygame.transform.smoothscale(red_book_rotated, (int(self.red_book_rotated_rect[2]/5), int(self.red_book_rotated_rect[3]/5))), self.red_book_rotated_surface)
            if not gs.red_book_found:
                self.red_book_clicker = gf.draw_item_to_screen(gs, screen, red_book_rotated, 5, 728, 500)

            pygame.draw.rect(screen, gs.file_cabinet, fcdo1)
            pygame.draw.rect(screen, gs.black, fcdo1, 3)
            fcd_handle.center = fcdo1.center
            pygame.draw.rect(screen, gs.silver, fcd_handle)
            pygame.draw.rect(screen, gs.black, fcd_handle, 2)

        else:
            pygame.draw.rect(screen, gs.file_cabinet, fcd1)
            pygame.draw.rect(screen, gs.black, fcd1, 3)
            fcd_handle.center = fcd1.center
            pygame.draw.rect(screen, gs.silver, fcd_handle)
            pygame.draw.rect(screen, gs.black, fcd_handle, 2) 



        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
    
    def room_view_three(self, gs, screen, stable_item_blocks):  # View with TV / TV Stand
        #Carpet
        pygame.draw.polygon(screen, gs.carpet, ((0, 600), (770, 600), (1050, 738), (0, 738), (0,600)))
        
        # Lines
        pygame.draw.line(screen, gs.black, (0, 600), (770, 600), 5)
        pygame.draw.line(screen, gs.black, (770, 600), (1070, 750), 5)
        pygame.draw.line(screen, gs.black, (770, 600), (770, 0), 5)
        
        # TV Stand
        pygame.draw.polygon(screen, gs.wood, ((150, 500), (120, 530), (740, 530), (710, 500)))
        pygame.draw.polygon(screen, gs.black, ((150, 500), (120, 530), (740, 530), (710, 500)), 3)
        
        pygame.draw.rect(screen, gs.wood, (120, 530, 620, 100))

        pygame.draw.rect(screen, gs.dark_wood, (130, 540, 600, 80))
        front_tv_stand = pygame.Rect(130, 540, 600, 80)
        back_tv_stand = pygame.Rect(160, 540, 540, 50)
        
        pygame.draw.rect(screen, gs.black, front_tv_stand, 3)
        pygame.draw.rect(screen, gs.black, back_tv_stand, 3)
        pygame.draw.line(screen, gs.black, front_tv_stand.bottomleft, back_tv_stand.bottomleft, 3)
        pygame.draw.line(screen, gs.black, front_tv_stand.bottomright, back_tv_stand.bottomright, 3)

        pygame.draw.rect(screen, gs.black, (120, 530, 620, 100), 3)            

        # TV

        pygame.draw.rect(screen, gs.black, (180, 125, 500, 326))  # border around the TV
        pygame.draw.rect(screen, gs.current_tv_screen_color, self.tv_screen_glass)

        # If TV is on, display the channel
        if gs.tv_on:
            if not gs.button_input_list:
                channel_text = gs.verdana16.render(str(gs.current_channel), True, gs.green)
            else:
                channel_text = gs.verdana16.render(str(gs.entered_buttons), True, gs.green)
            #channel_text = gs.verdana16.render(str(gs.current_channel), True, gs.green)
            tv_channels.tv_channels(gs, screen)
            screen.blit(channel_text, ((self.tv_screen_glass.x + 3), (self.tv_screen_glass.y)))

        # Click / Mouseovers
        self.clickbox_tv_stand_side = [(715, 500), (770, 500), (803, 622), (742, 628), (744, 528)]
        #self.clickbox_tv_stand_side_draw = pygame.draw.polygon(screen, gs.yellow, self.clickbox_tv_stand_side, 1) # todo remove this with a comment
    
        if gs.room_view_drill_down == 1:
            self.room_view_three_1(gs, screen, stable_item_blocks)

        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)

    def room_view_four(self, gs, screen, stable_item_blocks):  # View with closet / window
        # Carpet
        pygame.draw.polygon(screen, gs.carpet, ((0, 810), (0, 725), (490, 600), (1075, 600), (1075, 810)))
        
        # Lines
        pygame.draw.line(screen, gs.black, (0, 725), (490, 600), 5)
        pygame.draw.line(screen, gs.black, (490, 600), (490,0), 5)
        pygame.draw.line(screen, gs.black, (490, 600), (1075, 600), 5)
        
        # Window
        window_frame = pygame.Rect(625, 105, 300, 340)
        self.window = pygame.Rect(650, 120, 250, 300)
        window_int_frame = pygame.Rect(0, self.window.top, 6, self.window.height)
        window_int_frame.centerx = self.window.centerx
        
        pygame.draw.rect(screen, gs.gray, window_frame)
        pygame.draw.rect(screen, gs.black, window_frame, 3)
        pygame.draw.line(screen, gs.black, window_frame.topleft, self.window.topleft, 3)
        pygame.draw.line(screen, gs.black, window_frame.topright, self.window.topright, 3)
        pygame.draw.line(screen, gs.black, window_frame.bottomleft, self.window.bottomleft, 3)
        pygame.draw.line(screen, gs.black, window_frame.bottomright, self.window.bottomright, 3)
        pygame.draw.rect(screen, gs.off_white, self.window)
        pygame.draw.rect(screen, gs.black, window_int_frame, 3)
        pygame.draw.rect(screen, gs.black, self.window, 3)
        
        # Closet Inside
        pygame.draw.polygon(screen, gs.door, ((80, 705), (80, 190), (364, 150), (364, 632)))
        pygame.draw.lines(screen, gs.black, False, [(332, 571), (211, 523), (80, 547)], 3)
        
        ### Closet bar
        pygame.draw.ellipse(screen, gs.dark_gray, (293, 190, 15, 20))
        pygame.draw.ellipse(screen, gs.black, (293, 190, 16, 21), 3)
        pygame.draw.line(screen, gs.black, (211, 523), (211, 172), 3)
        pygame.draw.line(screen, gs.black, (300, 200), (80, 236), 10)
        pygame.draw.line(screen, gs.silver, (300, 200), (80, 236), 6)
        
        # Closet Door Frame
        pygame.draw.polygon(screen, gs.black, ((80, 705), (80, 190), (364, 150), (364, 632)), 3)
        pygame.draw.polygon(screen, gs.dark_blue, ((364, 632), (80, 704), (80, 681), (332, 618), (332, 154), (364, 150)))
        pygame.draw.polygon(screen, gs.black, ((364, 632), (80, 704), (80, 681), (332, 618), (332, 154), (364, 150)), 3)
        pygame.draw.line(screen, gs.black, (365, 632), (332, 618), 3)
        
        # Wall Outlet
        pygame.draw.rect(screen, gs.off_white, self.window_wall_outlet)
        pygame.draw.rect(screen, gs.black, (930, 528, 26, 42), 3)
        pygame.draw.rect(screen, gs.black, (937, 534, 12, 12), 1)
        pygame.draw.rect(screen, gs.black, (937, 552, 12, 12), 1)

        if gs.power_cord_window_1:
            self.power_cord_window_clicker = gf.draw_item_to_screen(gs, screen, power_cord_plugged_1_flip, 3, 818, 548)  # 3, 660, 548

        # Closet Items

        # Shirt in Closet
        if not gs.shirt_found:
            screen.blit(pygame.transform.smoothscale(hanging_shirt, (150, 235)), self.shirt_surface)


        # Click / Mouseovers
        self.clickbox_closet_right = [(220, 460), (332, 488), (332, 615), (220, 561)]
        #self.clickbox_closet_right_draw = pygame.draw.polygon(screen, gs.yellow, self.clickbox_closet_right, 1) # todo comment this out

        if gs.room_view_drill_down == 1:
            self.room_view_four_1(gs, screen, stable_item_blocks)
            
        if gs.room_view_drill_down == 2:
            self.room_view_four_2(gs, screen, stable_item_blocks)
            
        if gs.room_view_drill_down == 2.1:
            self.room_view_four_2_1(gs, screen, stable_item_blocks)


        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)

    def current_view(self, gs, screen, stable_item_blocks):
        """ Draws items in the current game windows based on the view you are on"""
        
        if gs.current_room_view == 0:   # Default View
            gs.fourth_wall = False
            gs.drill_possible = True
            self.room_view_one(gs, screen, stable_item_blocks)

        if gs.current_room_view == -1:  # Left from default
            gs.fourth_wall = False
            gs.drill_possible = False
            self.room_view_two(gs, screen, stable_item_blocks)
            
        if gs.current_room_view == 1:  # Right from default
            gs.fourth_wall = False
            gs.drill_possible = True
            self.room_view_three(gs, screen, stable_item_blocks)
            
        if gs.current_room_view < -1 or gs.current_room_view > 1:  # Fourth wall
            gs.fourth_wall = True
            gs.drill_possible = True
            self.room_view_four(gs, screen, stable_item_blocks)

    def open_door(self, gs, event):
        """Unlocks the door to finish / win the game"""
        if self.door_handle_rect.collidepoint(event.pos) and gs.door_locked == False and not gs.door_opened:
            gs.text = "I opened the door! I'm free... I think..."
            pygame.mixer.Sound.play(door_open_sound)
            gs.door_opened = True

        elif self.door_handle_rect.collidepoint(event.pos) or self.main_door.collidepoint(event.pos) and gs.door_locked == True and not gs.door_opened:
            gs.text = 'The door is locked...'


    def close_door(self, gs, event):
        """Closes door after it's been opened"""
        if gf.check_inside_clickbox(self, self.opened_door, ((event.pos), (0, 0))):
            pygame.mixer.Sound.play(door_close_sound)
            gs.door_opened = False

    def move_between_views(self, gs, screen, game_objects, stable_item_blocks, event):
        """Moves player between the various views based on the side that they clicked"""
        # Outer-Most Room Views
        if gs.lights_on:
            if game_objects.go_left.collidepoint(event.pos) and gs.room_view_drill_down == 0 and gs.stable_item_opened == False:  # Doesn't allow player to go left/right in drill down views
                if gs.fourth_wall:
                    gs.current_room_view = 1
                    self.current_view(gs, screen, stable_item_blocks)
                else:
                    gs.current_room_view -= 1
                    self.current_view(gs, screen, stable_item_blocks)

            if game_objects.go_right.collidepoint(event.pos) and gs.room_view_drill_down == 0 and gs.stable_item_opened == False:  # Doesn't allow player to go left/right in drill down views
                if gs.fourth_wall:
                    gs.current_room_view = -1
                    self.current_view(gs, screen, stable_item_blocks)
                else:
                    gs.current_room_view += 1
                    self.current_view(gs, screen, stable_item_blocks)

            ### Back button
            if gs.room_view_drill_down and game_objects.go_back.collidepoint(event.pos) and gs.stable_item_opened == False:
                gs.room_view_drill_down = 0
                gs.current_room_view = int(gs.current_room_view // 1)
                gs.text = None

    def drill_down_views(self, gs, screen, game_objects, event):
        """Moves player between various drill down views on each view already"""        
        # Drill Down Views
        
        if gs.current_room_view == 0 and gs.lights_on:   # Default View
            if self.top_of_can.collidepoint(event.pos):
                gs.room_view_drill_down = 0.1
                #gs.current_room_view = 4.21

        if gs.current_room_view == -1:  # Left from default
            pass
            
        if gs.current_room_view == 1:  # Right from default
            if gf.check_inside_clickbox(self, self.clickbox_tv_stand_side, ((event.pos), (0, 0))):
                gs.room_view_drill_down = 1
                #gs.current_room_view = 3.1
            
        if gs.current_room_view < -1 or gs.current_room_view > 1:  # Fourth wall
            #if self.clickbox_closet_right.collidepoint(event.pos):
            if gs.room_view_drill_down == 0:
                if gf.check_inside_clickbox(self, self.clickbox_closet_right, ((event.pos), (0, 0))):
                    gs.room_view_drill_down = 1
                if self.window.collidepoint(event.pos):
                    gs.text = 'This window shows something outside...'
                    gs.room_view_drill_down = 2
                    #gs.current_room_view = 4.2
            if self.click_window_int_frame.collidepoint(event.pos) and gs.room_view_drill_down == 2:
                gs.text = 'It is a city skyline...'
                gs.room_view_drill_down = 2.1
                #gs.current_room_view = 4.21

    def open_drawers(self, gs, screen, game_objects, event):
        """Opens drawers (file cabinets and desk drawers when the user clicks them"""
        
        # File Cabinets
        if gs.fcd2_opened == False:
            if gs.fcd1_opened == False:
                if fcd2.collidepoint(event.pos):
                    if gs.fcd2_locked == False:
                        pygame.mixer.Sound.play(file_cabinet_open_sound)
                        gs.fcd2_opened = True
                    else:
                        gs.text = 'This drawer is locked.'
            else:
                if fcd2.collidepoint(event.pos) and not fcdo1.collidepoint(event.pos):
                    if gs.fcd2_locked == False:
                        pygame.mixer.Sound.play(file_cabinet_open_sound)
                        gs.fcd2_opened = True
                    else:
                        gs.text = 'This drawer is locked.'

        elif gs.fcd2_opened:
            if fcdo2.collidepoint(event.pos):
                pygame.mixer.Sound.play(file_cabinet_close_sound)
                gs.fcd2_opened = False
            if not gs.blue_book_found and gs.fcd1_opened == False:
                self.click_blue_book(gs, event)

        
        if gs.fcd1_opened == False:
            if fcd1.collidepoint(event.pos):
                pygame.mixer.Sound.play(file_cabinet_open_sound)
                gs.fcd1_opened = True
        elif gs.fcd1_opened:
            if fcdo1.collidepoint(event.pos):
                pygame.mixer.Sound.play(file_cabinet_close_sound)
                gs.fcd1_opened = False
            if not gs.red_book_found:
                self.click_red_book(gs, event)
        
        # Desk Drawers
        if gs.dd3_opened == False:
            if gs.dd2_opened == False:
                if desk_drawer3.collidepoint(event.pos):
                    if gs.dd3_locked == False:
                        pygame.mixer.Sound.play(drawer_open_sound)
                        gs.dd3_open_attempts += 1
                        gs.dd3_opened = True

                    else:
                        gs.text = 'This drawer is locked.'
            else:
                if desk_drawer3.collidepoint(event.pos) and not desk_drawer2_opened.collidepoint(event.pos):
                    if gs.dd3_locked == False:
                            pygame.mixer.Sound.play(drawer_open_sound)
                            gs.dd3_opened = True
                            gs.dd3_open_attempts += 1
                    else:
                        gs.text = 'This drawer is locked.'

        elif gs.dd3_opened == True:
            if desk_drawer3_opened.collidepoint(event.pos):
                pygame.mixer.Sound.play(drawer_close_sound)
                gs.dd3_opened = False
                
        if gs.dd2_opened == False:
            if gs.dd1_opened == False:
                if desk_drawer2.collidepoint(event.pos):
                    pygame.mixer.Sound.play(drawer_open_sound)
                    gs.dd2_opened = True
            else:
                if desk_drawer2.collidepoint(event.pos) and not desk_drawer1_opened.collidepoint(event.pos):
                    pygame.mixer.Sound.play(drawer_open_sound)
                    gs.dd2_opened = True
        elif gs.dd2_opened == True:
            if desk_drawer2_opened.collidepoint(event.pos):
                pygame.mixer.Sound.play(drawer_close_sound)
                gs.dd2_opened = False
            if not gs.batteries_found:
                self.click_batteries(gs, event) # will add batteries to inventory
                
        if gs.dd1_opened == False:
            if desk_drawer1.collidepoint(event.pos):
                if gs.dd1_locked == False:
                    pygame.mixer.Sound.play(drawer_open_sound)
                    gs.dd1_opened = True
                else:
                    gs.text = 'This drawer is locked.'
        elif gs.dd1_opened == True:
            if desk_drawer1_opened.collidepoint(event.pos):
                pygame.mixer.Sound.play(drawer_close_sound)
                gs.dd1_opened = False
            if not gs.screwdriver_found:
                self.click_flathead(gs, event) # will add flathead to inventory

    def switch_light(self, gs, event):
        if self.light_switch.collidepoint(event.pos) and gs.room_view_drill_down == 0 and gs.current_room_view == 0 and not gs.door_opened:
            pygame.mixer.Sound.play(light_sound)

            if gs.lights_on and gs.tv_on:
                gs.text = 'The light turned off and the TV turned off... Weird...'
            elif gs.lights_on:
                gs.text = 'The light turned off...'
            elif not gs.lights_on and gs.lights_beginning:
                gs.text = "I turned on the light switch!  I need to get out of here..."
                gs.lights_beginning = False
            elif not gs.lights_on and not gs.lights_beginning:
                gs.text = "I turned on the light switch!"

            gs.lights_on = not gs.lights_on
            gs.current_tv_screen_color = gs.tv_screen
            gs.tv_on = False

    def click_tv(self, gs, event, game_objects):
        if gs.current_room_view == 0:
            if self.partial_tv_screen_glass.collidepoint(event.pos) and not gs.tv_on and not game_objects.inventory_window.collidepoint(event.pos):
                gs.text = "It's a TV. I need to turn it on..."
            elif self.partial_tv_screen_glass.collidepoint(event.pos) and gs.tv_on and not game_objects.inventory_window.collidepoint(event.pos):
                gs.text = 'The TV is on.'
        if gs.current_room_view == 1:
            if self.tv_screen_glass.collidepoint(event.pos) and not gs.tv_on:
                gs.text = "It's a TV. I need to turn it on..."
            elif self.tv_screen_glass.collidepoint(event.pos) and gs.tv_on:
                gs.text = 'The TV is on.'

    def click_trash_can(self, gs, event):
        if self.trash_can_clickbox.collidepoint(event.pos):
            gs.text = "It's a trash can..."


    def find_stable_item_opened(self, gs, screen, stable_item_blocks):
        # Use this area to open all of the stable items in all views
        if gs.remote_opened:
            stable_item_blocks.draw_remote(gs, screen)

        if gs.red_book_opened:
            stable_item_blocks.draw_manual(gs, screen)

        if gs.blue_book_opened:
            stable_item_blocks.draw_manual(gs, screen)

        if gs.papers_opened:
            stable_item_blocks.draw_papers(gs, screen)

        if gs.shirt_opened:
            stable_item_blocks.open_shirt(gs, screen)

        if gs.desk_drawer_up:
            stable_item_blocks.pull_up_desk_drawer(gs, screen)

    def item_intersection(self, gs, event):
        """Looks for moveable items that intersect with the room and other items to achieve things"""
        # Door Key
        if gs.selected_item_index == 0 and self.door_handle_rect.collidepoint(gs.selected_item.center) and gs.current_room_view == 0 and gs.room_view_drill_down == 0:
            pygame.mixer.Sound.play(key_sound)
            gs.door_locked = False
            gs.door_key_used = True
            gs.moveable_items_index_list.remove(gs.selected_item_index)
            gs.text = 'The door is unlocked!'
        #elif gs.selected_item_index == 0 and not self.door_handle_rect.collidepoint(gs.selected_item.center):
        #    gs.text = "This doesn't go here..."

        # Red Key
        elif gs.selected_item_index == 1 and desk_drawer3.collidepoint(gs.selected_item.center) and gs.current_room_view == -1 and gs.room_view_drill_down == 0:
            pygame.mixer.Sound.play(key_sound)
            gs.dd3_locked = False
            gs.red_key_used = True
            gs.moveable_items_index_list.remove(gs.selected_item_index)
            gs.text = 'The drawer unlocked!'
        #elif gs.selected_item_index == 1 and not desk_drawer3.collidepoint(gs.selected_item.center):
        #    gs.text = "This doesn't go here..."

        # Purple Key
        elif gs.selected_item_index == 2 and fcd2.collidepoint(gs.selected_item.center) and gs.current_room_view == -1 and gs.room_view_drill_down == 0:
            pygame.mixer.Sound.play(key_sound)
            gs.fcd2_locked = False
            gs.purple_key_used = True
            gs.moveable_items_index_list.remove(gs.selected_item_index)
            gs.text = 'The drawer unlocked!'
        #elif gs.selected_item_index == 2 and not fcd2.collidepoint(gs.selected_item.center):
        #    gs.text = "This doesn't go here..."

        # Green Key
        elif gs.selected_item_index == 3 and desk_drawer1.collidepoint(gs.selected_item.center) and gs.current_room_view == -1 and gs.room_view_drill_down == 0:
            pygame.mixer.Sound.play(key_sound)
            gs.dd1_locked = False
            gs.green_key_used = True
            gs.moveable_items_index_list.remove(gs.selected_item_index)
            gs.text = 'The drawer unlocked!'
        #elif gs.selected_item_index == 3 and not desk_drawer1.collidepoint(gs.selected_item.center):
        #    gs.text = "This doesn't go here..."

        # Batteries
        elif gs.selected_item_index == 4 and gs.remote_found and inventory.inv_items_stable[0].collidepoint(gs.selected_item.center):
            pygame.mixer.Sound.play(input_battery_sound)
            gs.batteries_input = True
            gs.batteries_used = True
            gs.moveable_items_index_list.remove(gs.selected_item_index)
            gs.text = 'I put the batteries in the remote!'

        #elif gs.selected_item_index == 4 and not inventory.inv_items_stable[0].collidepoint(gs.selected_item.center):
        #    gs.text = "This doesn't go here..."

        # Power Cord - Desk Outlet
        elif gs.selected_item_index == 5 and self.desk_wall_outlet.collidepoint(gs.selected_item.center) and gs.current_room_view == -1 and gs.room_view_drill_down == 0:
            pygame.mixer.Sound.play(light_sound)
            gs.power_cord_desk_1 = True
            gs.power_cord_used = True
            gs.moveable_items_index_list.remove(gs.selected_item_index)
            gs.text = 'I plugged in the power cord!'

        # Power Cord - Window Outlet
        elif gs.selected_item_index == 5 and self.window_wall_outlet.collidepoint(gs.selected_item.center) and gs.room_view_drill_down == 0 and (gs.current_room_view == -2 or gs.current_room_view == 2):
            pygame.mixer.Sound.play(light_sound)
            gs.power_cord_window_1 = True
            gs.power_cord_used = True
            gs.moveable_items_index_list.remove(gs.selected_item_index)
            gs.text = 'I plugged in the power cord!'

        #elif gs.selected_item_index == 5 and not self.desk_wall_outlet.collidepoint(gs.selected_item.center) or not self.window_wall_outlet.collidepoint(gs.selected_item.center):
        #    gs.text = "This doesn't go here..."

        # Screwdriver / Flathead
        elif gs.selected_item_index == 6 and self.safe_cover.collidepoint(gs.selected_item.center) and gs.room_view_drill_down == 1 and (gs.current_room_view == -2 or gs.current_room_view == 2):
            pygame.mixer.Sound.play(safe_door)
            gs.safe_uncovered = True
            gs.screwdriver_used = True
            gs.moveable_items_index_list.remove(gs.selected_item_index)
            gs.text = 'WOW! There is a safe back here! What is the code?'
        #elif gs.selected_item_index == 6 and not self.safe_cover.collidepoint(gs.selected_item.center):
        #    gs.text = "This doesn't go here..."

        # Screwdriver in Desk Outlet
        elif gs.selected_item_index == 6 and self.desk_wall_outlet.collidepoint(gs.selected_item.center) and gs.current_room_view == -1 and gs.room_view_drill_down == 0:
            gs.text = "That wouldn't be a good idea!"

        # Screwdriver in Window Outlet
        elif gs.selected_item_index == 6 and self.window_wall_outlet.collidepoint(gs.selected_item.center) and gs.room_view_drill_down == 0 and (gs.current_room_view == -2 or gs.current_room_view == 2):
            gs.text = "That wouldn't be a good idea!"

        else:
            gs.text = "That doesn't go there."



