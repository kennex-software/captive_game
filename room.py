#kennex

import os, pygame, sys, copy
from settings import Settings
import gf
from inventory import Inventory
#from objects import GameObjects
from stable_items import Stable_Items
from pygame.locals import *
from pygame.math import Vector2
from pygame.math import Vector3
from noise import pnoise2
#import tv_channels
import numpy as np

class Room():
    """Class to store the objects of the rooms and the views regarding them"""
    
    def __init__(self, gs, screen, stable_item_blocks):
        self.gs = gs
        self.screen = screen
        #self.game_obects = game_objects
        
        self.e_window = pygame.Rect(305, 80, 500, 600)
        self.click_window_int_frame = pygame.Rect(0, self.e_window.top, 12, self.e_window.height)
        
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

        # Required in all views if items are opened during the view.
        if gs.stable_item_opened:
            self.find_stable_item_opened(gs, screen, stable_item_blocks)
        
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
        
        # Window
        """ Change the code here to whatever needs to happen outside of the window"""

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
            
            # Door
            pygame.draw.rect(screen, gs.door, (390, 160, 225, 440))
            pygame.draw.rect(screen, gs.black, (390, 160, 225, 440), 3)
            pygame.draw.circle(screen, gs.dark_gray, (585-3, 390+5), 15)
            pygame.draw.circle(screen, gs.yellow, (585, 390), 15)            
            pygame.draw.circle(screen, gs.black, (585, 390), 16, 2)
            pygame.draw.circle(screen, gs.black, (585, 390), 4, 1)
            
            # Light Switch            
            pygame.draw.rect(screen, gs.off_white, self.light_switch)
            pygame.draw.rect(screen, gs.black, self.light_switch, 3)
            pygame.draw.rect(screen, gs.black, (660, 335, 10, 20), 1)   
            
            # Lines
            pygame.draw.line(screen, gs.black, (0, 725), (330, 600), 5)
            pygame.draw.line(screen, gs.black, (330, 600), (330,0), 5)
            pygame.draw.line(screen, gs.black, (330, 600), (1100, 600), 5)
            
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
            pygame.draw.rect(screen, gs.tv_screen, (945, 140, 470, 296))

            # Required in all views if items are opened during the view.
            if gs.stable_item_opened:
                self.find_stable_item_opened(gs, screen, stable_item_blocks)

            """
            # Plant
            top_of_pot = pygame.Rect(130, 555, 120, 25)
            bottom_of_pot = pygame.Rect(0, 675, 90, 25)
            bottom_of_pot.centerx = top_of_pot.centerx
            
            
            pygame.draw.polygon(screen, gs.brown, ((top_of_pot.midleft), (top_of_pot.midright), (bottom_of_pot.midright), (bottom_of_pot.midleft)))
            
            pygame.draw.polygon(screen, gs.black, ((top_of_pot.midleft), (top_of_pot.midright), (bottom_of_pot.midright), (bottom_of_pot.midleft)), 3)
            pygame.draw.ellipse(screen, gs.brown, bottom_of_pot)
            pygame.draw.ellipse(screen, gs.black, bottom_of_pot, 3)
            pygame.draw.ellipse(screen, gs.dark_gray, top_of_pot)
            
            
            
            pygame.draw.ellipse(screen, gs.black, top_of_pot, 3)
            
            #pygame.draw.line(screen, gs.black, (), (bottom_of_pot.midleft), 3)
            #pygame.draw.line(screen, gs.black, (top_of_pot.midright), (bottom_of_pot.midright), 3)
            """
        
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

        # TV Channels
        # Channel 1 | Whitespace todo figure out how to create perlin noise for TV screens (maybe with import noise function)???
        """lin = np.linspace(0,5,100,endpoint=False)
        x,y = np.meshgrid(lin,lin) # FIX3: I thought I had to invert x and y here but it was a mistake
        whitespace = tv_channels.perlin(x,y,seed=2)
        surf = pygame.surfarray.make_surface(whitespace)
        screen.blit(surf, (0, 0))"""
        # Channel 2 | Whitespace todo figure out how to create perlin noise for TV screens (maybe with import noise function)???
        # Channel 3 | Color Flash todo will flash a specific color which will be needed in the game, maybe every 9 seconds or so
        # Channel 4 | Camera 1 todo make this a view of Camera 1 (always plugged in)
        # Channel 5 | Camera 2 todo make this a view of Camera 2, if plugged in... if not, show whitespace (see channel 1)
        # Channel 6 | Camera 3 todo make this a view of Camera 3 (always plugged in) make this camera the least important, but maybe a view of inside the room
        # Channel 7 | # todo figure out what to make channel
        # Channel 8 | Whitespace todo figure out how to create perlin noise for TV screens (maybe with import noise function)???
        # Channel 9 | # todo figure out what to make channel


        
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
        #hanger_lines = [(125, 225), (131, 227), (131, 247), (160, 290), (92, 275), (131, 247)]

        hanger_surface = pygame.Surface((75, 80), pygame.SRCALPHA)
        hanger_lines = [(34, 3), (40, 5), (40, 25), (69, 68), (1, 53), (40, 25)]

        hanger_surface.fill(gs.transcolor)

        pygame.draw.lines(hanger_surface, gs.black, False, hanger_lines, 4)
        pygame.draw.lines(hanger_surface, gs.gray, False, hanger_lines, 2)


        self.screen.blit(hanger_surface, (200, 203))
        self.screen.blit(hanger_surface, (165, 209))
        self.screen.blit(hanger_surface, (91, 221))

        shirt_surface = pygame.Surface((110, 185), pygame.SRCALPHA)
        #shirt_lines = [(152, 445), (242, 439), (240, 273), (226, 251), (204, 253), (189, 251), (181, 240), (163, 262)]
        #pygame.draw.polygon(screen, gs.red, shirt_lines)
        
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
            gs.drill_possible = False
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

    def drill_down_views(self, gs, screen, game_objects, event):
        """Moves player between various drill down views on each view already"""        
        # Drill Down Views
        
        if gs.current_room_view == 0:   # Default View
            pass

        if gs.current_room_view == -1:  # Left from default
            pass
            
        if gs.current_room_view == 1:  # Right from default
            if gf.check_inside_clickbox(self, self.clickbox_tv_stand_side, ((event.pos), (0, 0))):
                gs.room_view_drill_down = 1
            
        if gs.current_room_view < -1 or gs.current_room_view > 1:  # Fourth wall
            #if self.clickbox_closet_right.collidepoint(event.pos):
            if gf.check_inside_clickbox(self, self.clickbox_closet_right, ((event.pos), (0, 0))):
                gs.room_view_drill_down = 1
            if self.window.collidepoint(event.pos):
                gs.room_view_drill_down = 2
            if self.click_window_int_frame.collidepoint(event.pos) and gs.room_view_drill_down == 2:
                gs.room_view_drill_down = 2.1

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



