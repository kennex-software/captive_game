#kennex

import os, pygame, sys, copy
from settings import Settings
import gf
from inventory import Inventory
#from objects import GameObjects
from stable_items import Stable_Items
from pygame.locals import *
from math import pi
from pygame.math import Vector2
from pygame.math import Vector3
#from noise import pnoise2
import tv_channels
import numpy as np

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




class Room():
    """Class to store the objects of the rooms and the views regarding them"""
    
    def __init__(self, gs, screen, stable_item_blocks):
        self.gs = gs
        self.screen = screen
        #self.game_obects = game_objects
        
        self.e_window = pygame.Rect(305, 80, 500, 600)
        self.click_window_int_frame = pygame.Rect(0, self.e_window.top, 12, self.e_window.height)

        # Safe
        self.safe = pygame.Rect(270, 130, 480, 270)
        self.safe_hole = self.safe.inflate(90, 60)
        self.safe_cover = self.safe_hole.inflate(10,10)
        self.safe_handle = pygame.Rect(700, 240, 30, 80)
        self.safe_use_color = gs.red
        self.safe_status_color_on = gs.black
        self.safe_status_color_off = gs.red

        # Safe Numbers
        self.safe_number_rect_n1 = pygame.Rect((self.safe.topleft[0] + 20), (self.safe.topleft[1] + 20), 70, 100)
        self.safe_number_rect_n2 = self.safe_number_rect_n1.move(90, 0)
        self.safe_number_rect_n3 = self.safe_number_rect_n2.move(90, 0)
        self.safe_number_rect_n4 = self.safe_number_rect_n3.move(90, 0)

        self.safe_number_n1 = 0
        self.safe_number_n2 = 0
        self.safe_number_n3 = 0
        self.safe_number_n4 = 0

        # Safe Colors
        self.safe_number_rect_c1 = self.safe_number_rect_n3.move(0, 130)
        self.safe_number_rect_c2 = self.safe_number_rect_n4.move(0, 130)

        self.safe_color_c1 = gs.black
        self.safe_color_c2 = gs.black
        self.index_color1 = gs.color_codes.get('purple')[0]
        self.index_color2 = gs.color_codes.get('purple')[0]

        # Safe Initialization
        self.safe_use_rect = self.safe_number_rect_n1.move(0, 130)
        
        # clickbox_name = [(), (), (), (), (), (), (), (), (), (), (), ()]
        
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
        self.laying_remote_surface = pygame.Rect(380, 493, 50, 70)
        self.laying_remote_rect = laying_remote.get_rect()
        screen.blit(pygame.transform.smoothscale(laying_remote, (int(self.laying_remote_rect[2]/4.5), int(self.laying_remote_rect[3]/4.5))), self.laying_remote_surface)

        # todo clickable remote


        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
        
    def room_view_four_1(self, gs, screen, stable_item_blocks):  # View inside of closet todo Figure out what to do in the closet
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
                self.safe_door = pygame.draw.polygon(screen, gs.tv_screen, ((-5, 183), (self.safe.topleft), (self.safe.bottomleft), (-5, 577)))
                pygame.draw.polygon(screen, gs.black, ((-5, 183), (self.safe.topleft), (self.safe.bottomleft), (-5, 577)), 3)

                self.back_of_safe = self.safe.inflate(-180, -190)
                pygame.draw.rect(screen, gs.tv_screen, self.back_of_safe)
                pygame.draw.rect(screen, gs.black, self.back_of_safe, 3)
                pygame.draw.line(screen, gs.black, self.safe.topleft, self.back_of_safe.topleft, 3)
                pygame.draw.line(screen, gs.black, self.safe.topright, self.back_of_safe.topright, 3)
                pygame.draw.line(screen, gs.black, self.safe.bottomleft, self.back_of_safe.bottomleft, 3)
                pygame.draw.line(screen, gs.black, self.safe.bottomright, self.back_of_safe.bottomright, 3)

                # Draw Door Key
                self.door_key_rotated_surface = pygame.Rect(521, 335, 50, 70)
                self.door_key_rotated_rect = door_key_rotated.get_rect()
                screen.blit(pygame.transform.smoothscale(door_key_rotated, (int(self.door_key_rotated_rect[2]/6), int(self.door_key_rotated_rect[3]/6))), self.door_key_rotated_surface)

                # todo click gold door key
                # todo click safe door to close it

            else:

                # Closed Safe
                pygame.draw.rect(screen, gs.safe, self.safe)
                pygame.draw.rect(screen, gs.black, self.safe, 4)


                # Handle
                pygame.draw.rect(screen, gs.gray, self.safe_handle)
                pygame.draw.rect(screen, gs.black, self.safe_handle, 3)

                # Numbers
                pygame.draw.rect(screen, gs.off_white, self.safe_number_rect_n1) # Number spot 1
                pygame.draw.rect(screen, gs.off_white, self.safe_number_rect_n2) # Number spot 2
                pygame.draw.rect(screen, gs.off_white, self.safe_number_rect_n3) # Number spot 3
                pygame.draw.rect(screen, gs.off_white, self.safe_number_rect_n4) # Number spot 4

                self.n1_image = gs.arial60.render(str(self.safe_number_n1), True, gs.black) # n1 text
                self.n2_image = gs.arial60.render(str(self.safe_number_n2), True, gs.black) # n2 text
                self.n3_image = gs.arial60.render(str(self.safe_number_n3), True, gs.black) # n3 text
                self.n4_image = gs.arial60.render(str(self.safe_number_n4), True, gs.black) # n4 text

                self.n1_rect = self.n1_image.get_rect(center=self.safe_number_rect_n1.center) # n1 rect
                self.n2_rect = self.n2_image.get_rect(center=self.safe_number_rect_n2.center) # n2 rect
                self.n3_rect = self.n3_image.get_rect(center=self.safe_number_rect_n3.center) # n3 rect
                self.n4_rect = self.n4_image.get_rect(center=self.safe_number_rect_n4.center) # n4 rect

                screen.blit(self.n1_image, self.n1_rect) # n1 blit
                screen.blit(self.n2_image, self.n2_rect) # n2 blit
                screen.blit(self.n3_image, self.n3_rect) # n3 blit
                screen.blit(self.n4_image, self.n4_rect) # n4 blit

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
                pygame.draw.rect(screen, self.safe_use_color, self.safe_use_rect) # Initiation
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








        else:  # Safe Panel not removed
            pygame.draw.rect(screen, gs.door, self.safe_cover)
            pygame.draw.rect(screen, gs.black, self.safe_cover, 2)

        # Draw Papers
        self.laying_paper_surface = pygame.Rect(380, 475, 100, 100)
        self.laying_paper_rect = laying_paper.get_rect()
        screen.blit(pygame.transform.smoothscale(laying_paper, (int(self.laying_paper_rect[2]/2), int(self.laying_paper_rect[3]/2))), self.laying_paper_surface)

        # todo clickable papers


        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)

    def safe_controls(self, gs, screen, event):
        if gs.safe_on:

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

            # Initialization todo some sort of channel or something
            elif self.safe_use_rect.collidepoint(event.pos):
                self.safe_use_color = gs.green


        
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
        
    def room_view_four_2_1(self, gs, screen, stable_item_blocks):  # View of outside window todo figure out what to do outside of the window
        # Clear Screen
        screen.fill(gs.white)


        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
        # Window
        """ Change the code here to whatever needs to happen outside of the window"""

        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)

    def room_view_zero_1(self, gs, screen, stable_item_blocks):  # View of inside trash can
        # Clear Screen
        screen.fill(gs.carpet)

        self.can_opening_rect = pygame.Rect(350, 220, 350, 350)

        pygame.draw.circle(screen, gs.dark_brown, self.can_opening_rect.center, 250)
        pygame.draw.circle(screen, gs.black, self.can_opening_rect.center, 250, 3)
        pygame.draw.circle(screen, gs.brown, self.can_opening_rect.center, 149)
        pygame.draw.circle(screen, gs.black, self.can_opening_rect.center, 150, 3)
        pygame.draw.rect(screen, gs.bg_color, (0, 0, 1190, 84))
        pygame.draw.line(screen, gs.black, (0, 84), (1190, 84), 5)

        # Draw Laying Power Cord
        self.laying_power_cord_rect = laying_power_cord.get_rect()
        self.laying_power_cord_scaled = pygame.transform.smoothscale(laying_power_cord, (int(self.laying_power_cord_rect[2]/1.5), int(self.laying_power_cord_rect[3]/1.5)))
        self.laying_power_cord_scaled_rect = self.laying_power_cord_scaled.get_rect(center = self.can_opening_rect.center)
        screen.blit(self.laying_power_cord_scaled, self.laying_power_cord_scaled_rect)

        # todo clickable power cord




        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
        
    def room_view_one(self, gs, screen, stable_item_blocks):  # View with door ; Default view
        self.light_switch = pygame.Rect(650, 325, 30, 40)
                
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
            pygame.draw.rect(screen, gs.off_white, self.light_switch)
            pygame.draw.rect(screen, gs.black, self.light_switch, 3)
            pygame.draw.rect(screen, gs.black, (660, 335, 10, 20), 1)   
            
            # Lines
            pygame.draw.line(screen, gs.black, (0, 725), (330, 600), 5)
            pygame.draw.line(screen, gs.black, (330, 600), (330,0), 5)
            pygame.draw.line(screen, gs.black, (330, 600), (1100, 600), 5)

            self.main_door = pygame.Rect(390, 160, 225, 440)

            if gs.door_opened and gs.room_view_drill_down == 0:
                # Draw Open Door Handle
                pygame.draw.circle(screen, gs.yellow, (243, 398), 15)
                pygame.draw.circle(screen, gs.black, (243, 398), 16, 2)




                # Draw open door
                self.opened_door = [(248, 101), (self.main_door.topleft), (self.main_door.bottomleft), (248, 674)]
                pygame.draw.polygon(screen, gs.door, self.opened_door)
                pygame.draw.polygon(screen, gs.black, self.opened_door, 3)
                pygame.draw.line(screen, gs.black, (250, 101), (250, 674), 8)
                pygame.draw.rect(screen, gs.white, self.main_door)
                pygame.draw.rect(screen, gs.black, self.main_door, 3)

            else:
                # Door
                pygame.draw.rect(screen, gs.door, self.main_door)
                pygame.draw.rect(screen, gs.black, self.main_door, 3)
                pygame.draw.circle(screen, gs.dark_gray, (585-3, 390+5), 15)
                pygame.draw.circle(screen, gs.yellow, (585, 390), 15)
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
            self.partial_tv_screen_glass = Rect(945, 140, 470, 296)
            pygame.draw.rect(screen, gs.tv_screen, self.partial_tv_screen_glass)

            if gs.tv_on:
                channel_text = gs.verdana16.render(str(gs.current_channel), True, gs.green)
                screen.blit(channel_text, ((self.partial_tv_screen_glass.x + 3), self.partial_tv_screen_glass.y))
                tv_channels.tv_channels(gs, screen)

            # Trash Can
            self.top_of_can = pygame.Rect(130, 555, 120, 25)
            bottom_of_can = pygame.Rect(0, 675, 90, 25)
            bottom_of_can.centerx = self.top_of_can.centerx


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
        
        pygame.draw.line(screen, gs.black, (275, 670), (275, 515), 3)
        pygame.draw.line(screen, gs.black, (275, 515), (678, 515), 3)
        pygame.draw.line(screen, gs.black, (678, 515), (678, 670), 3)
        pygame.draw.line(screen, gs.black, (84, 474), (690, 474), 3)  # Line for desk
               
        ########## Desk Drawer 3
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
            pygame.draw.polygon(screen, gs.wood, ((desk_drawer3.bottomleft), (desk_drawer3.topleft), (150, 610)))
            pygame.draw.polygon(screen, gs.carpet, ((desk_drawer3.bottomleft), (150, 610), (desk_drawer3.topright), (desk_drawer3.bottomright)))
            pygame.draw.polygon(screen, gs.black, ((desk_drawer3.bottomleft), (desk_drawer3.topleft), (150, 610)), 2)
            pygame.draw.polygon(screen, gs.black, ((desk_drawer3.bottomleft), (150, 610), (desk_drawer3.topright), (desk_drawer3.bottomright)), 2)
            pygame.draw.line(screen, gs.black, (desk_drawer3.bottomleft), (150, 610), 2)
            pygame.draw.ellipse(screen, gs.black, (216, 630, 16, 8))
            pygame.draw.ellipse(screen, gs.dark_gray, (220, 632, 8, 4))

            gs.desk_drawer_removed = True

            # Draw Green Key
            self.green_key_rotated_surface = pygame.Rect(148, 630, 50, 70)
            self.green_key_rotated_rect = green_key_rotated.get_rect()
            screen.blit(pygame.transform.smoothscale(green_key_rotated, (int(self.green_key_rotated_rect[2]/22), int(self.green_key_rotated_rect[3]/22))), self.green_key_rotated_surface)

            # todo click green key

        
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
            self.rotated_batteries_surface = pygame.Rect(174, 588, 50, 70)
            self.rotated_batteries_rect = rotated_batteries.get_rect()
            screen.blit(pygame.transform.smoothscale(rotated_batteries, (int(self.rotated_batteries_rect[2]/13), int(self.rotated_batteries_rect[3]/13))), self.rotated_batteries_surface)

            # todo click batteries
            
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
            self.flathead_surface = pygame.Rect(124, 528, 50, 70)
            self.flathead_rect = flathead.get_rect()
            screen.blit(pygame.transform.smoothscale(flathead, (int(self.flathead_rect[2]/4), int(self.flathead_rect[3]/4))), self.flathead_surface)

            # todo click flathead

        else:
            pygame.draw.rect(screen, gs.black, desk_drawer1, 3)
            pygame.draw.circle(screen, gs.silver, (desk_drawer1.center), 7)
            pygame.draw.circle(screen, gs.black, (desk_drawer1.center), 8, 2)
        
        # File Cabinets
        pygame.draw.polygon(screen, gs.file_cabinet, ((657, 420), (690, 474), (840, 474), (788, 420)))
        pygame.draw.polygon(screen, gs.black, ((657, 420), (690, 474), (840, 474), (788, 420)), 3)
               
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
            self.blue_book_rotated_surface = pygame.Rect(728, 598, 50, 70)
            self.blue_book_rotated_rect = blue_book_rotated.get_rect()
            screen.blit(pygame.transform.smoothscale(blue_book_rotated, (int(self.blue_book_rotated_rect[2]/5), int(self.blue_book_rotated_rect[3]/5))), self.blue_book_rotated_surface)


            pygame.draw.rect(screen, gs.file_cabinet, fcdo2)
            pygame.draw.rect(screen, gs.black, fcdo2, 3)   
            fcd_handle.center = fcdo2.center
            pygame.draw.rect(screen, gs.silver, fcd_handle)
            pygame.draw.rect(screen, gs.black, fcd_handle, 2)

            # todo blue book click


            
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
            self.red_book_rotated_surface = pygame.Rect(728, 500, 50, 70)
            self.red_book_rotated_rect = red_book_rotated.get_rect()
            screen.blit(pygame.transform.smoothscale(red_book_rotated, (int(self.red_book_rotated_rect[2]/5), int(self.red_book_rotated_rect[3]/5))), self.red_book_rotated_surface)

            pygame.draw.rect(screen, gs.file_cabinet, fcdo1)
            pygame.draw.rect(screen, gs.black, fcdo1, 3)
            fcd_handle.center = fcdo1.center
            pygame.draw.rect(screen, gs.silver, fcd_handle)
            pygame.draw.rect(screen, gs.black, fcd_handle, 2)

            # todo red book click

        else:
            pygame.draw.rect(screen, gs.file_cabinet, fcd1)
            pygame.draw.rect(screen, gs.black, fcd1, 3)
            fcd_handle.center = fcd1.center
            pygame.draw.rect(screen, gs.silver, fcd_handle)
            pygame.draw.rect(screen, gs.black, fcd_handle, 2) 

        # Wall Outlet
        pygame.draw.rect(screen, gs.off_white, (362, 528, 26, 42))
        pygame.draw.rect(screen, gs.black, (362, 528, 26, 42), 3)
        pygame.draw.rect(screen, gs.black, (369, 534, 12, 12), 1)
        pygame.draw.rect(screen, gs.black, (369, 552, 12, 12), 1)

        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
    
    def room_view_three(self, gs, screen, stable_item_blocks):  # View with TV / TV Stand todo need to figure out what to do with the tv
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
        self.tv_screen_glass = pygame.Rect(195, 140, 470, 296)
        pygame.draw.rect(screen, gs.black, (180, 125, 500, 326))  # border around the TV
        pygame.draw.rect(screen, gs.tv_screen, self.tv_screen_glass)

        # If TV is on, display the channel
        if gs.tv_on:
            channel_text = gs.verdana16.render(str(gs.current_channel), True, gs.green)
            screen.blit(channel_text, ((self.tv_screen_glass.x + 3), (self.tv_screen_glass.y)))

            tv_channels.tv_channels(gs, screen)




        # Click / Mouseovers
        self.clickbox_tv_stand_side = [(715, 500), (770, 500), (803, 622), (742, 628), (744, 528)]
        self.clickbox_tv_stand_side_draw = pygame.draw.polygon(screen, gs.yellow, self.clickbox_tv_stand_side, 1) # todo remove this with a comment
    
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
        pygame.draw.rect(screen, gs.off_white, (930, 528, 26, 42))
        pygame.draw.rect(screen, gs.black, (930, 528, 26, 42), 3)
        pygame.draw.rect(screen, gs.black, (937, 534, 12, 12), 1)
        pygame.draw.rect(screen, gs.black, (937, 552, 12, 12), 1)

        # Closet Items

        # Shirt in Closet
        self.shirt_surface = pygame.Rect(125, 212, 150, 235)
        screen.blit(pygame.transform.smoothscale(hanging_shirt, (150, 235)), self.shirt_surface)

        # Click / Mouseovers
        self.clickbox_closet_right = [(280, 516), (332, 530), (332, 615), (269, 574)]
        self.clickbox_closet_right_draw = pygame.draw.polygon(screen, gs.yellow, self.clickbox_closet_right, 1)

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

    def move_between_views(self, gs, screen, game_objects, stable_item_blocks, event):
        """Moves player between the various views based on the side that they clicked"""
        # Outer-Most Room Views
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
        if game_objects.go_back.collidepoint(event.pos) and gs.stable_item_opened == False:
            gs.room_view_drill_down = 0
            gs.current_room_view = int(gs.current_room_view // 1)

    def drill_down_views(self, gs, screen, game_objects, event):
        """Moves player between various drill down views on each view already"""        
        # Drill Down Views
        
        if gs.current_room_view == 0:   # Default View
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
                    gs.room_view_drill_down = 2
                    #gs.current_room_view = 4.2
            if self.click_window_int_frame.collidepoint(event.pos) and gs.room_view_drill_down == 2:
                gs.room_view_drill_down = 2.1
                #gs.current_room_view = 4.21

    def open_drawers(self, gs, screen, game_objects, event):
        """Opens drawers (file cabinets and desk drawers when the user clicks them"""
        
        # File Cabinets
        if gs.fcd2_opened == False:
            if gs.fcd1_opened == False:
                if fcd2.collidepoint(event.pos):
                    gs.fcd2_opened = True
            else:
                if fcd2.collidepoint(event.pos) and not fcdo1.collidepoint(event.pos):
                    gs.fcd2_opened = True
        elif gs.fcd2_opened:
            if fcdo2.collidepoint(event.pos):
                gs.fcd2_opened = False
        
        if gs.fcd1_opened == False:
            if fcd1.collidepoint(event.pos):
                gs.fcd1_opened = True
        elif gs.fcd1_opened:
            if fcdo1.collidepoint(event.pos):
                gs.fcd1_opened = False
        
        # Desk Drawers
        if gs.dd3_opened == False:
            if gs.dd2_opened == False:
                if desk_drawer3.collidepoint(event.pos):
                    gs.dd3_open_attempts += 1
                    gs.dd3_opened = True
            else:
                if desk_drawer3.collidepoint(event.pos) and not desk_drawer2_opened.collidepoint(event.pos):
                    gs.dd3_opened = True
                    gs.dd3_open_attempts += 1
        elif gs.dd3_opened == True:
            if desk_drawer3_opened.collidepoint(event.pos):
                gs.dd3_opened = False
                
        if gs.dd2_opened == False:
            if gs.dd1_opened == False:
                if desk_drawer2.collidepoint(event.pos):
                    gs.dd2_opened = True
            else:
                if desk_drawer2.collidepoint(event.pos) and not desk_drawer1_opened.collidepoint(event.pos):
                    gs.dd2_opened = True
        elif gs.dd2_opened == True:
            if desk_drawer2_opened.collidepoint(event.pos):
                gs.dd2_opened = False
                
        if gs.dd1_opened == False:
            if desk_drawer1.collidepoint(event.pos):
                gs.dd1_opened = True
        elif gs.dd1_opened == True:
            if desk_drawer1_opened.collidepoint(event.pos):
                gs.dd1_opened = False

    def switch_light(self, gs, event):
        if self.light_switch.collidepoint(event.pos):
            gs.lights_on = not gs.lights_on

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





