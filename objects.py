#kennex

import pygame, sys
#import pygame.font
from inventory import Inventory
import time
import gf

pygame.init()
pygame.font.init()

class GameObjects():
    """Class to store the objects in the game"""
    
    def __init__(self, gs, screen, inventory):
        """Initialize the game objects."""
        super().__init__()
        self.gs = gs
        self.screen = screen     
        self.inventory = inventory
        self.screen_directions = pygame.Surface((gs.gw_width, gs.gw_height), pygame.SRCALPHA)

        self.go_left = pygame.Rect(gs.gw_border, gs.gw_border, gs.gw_move_w, gs.gw_height)
        self.go_right = pygame.Rect(gs.gw_right_x, gs.gw_border, gs.gw_move_w, gs.gw_height)
        self.go_back = pygame.Rect(gs.gw_move_w+gs.gw_border*2, gs.gw_height-gs.gw_move_w, (gs.gw_width-gs.gw_move_w*2-gs.gw_border*4), gs.gw_move_w)
        #self.go_up = pygame.Rect((gs.gw_move_w+gs.gw_border*2, 0, (gs.gw_width-gs.gw_move_w*2-gs.gw_border*4), gs.gw_move_w))
    
        # Game Window Area
        # self.game_window_with_border = pygame.draw.rect(screen, gs.white, (gs.gw_border, gs.gw_border, gs.gw_width-(gs.gw_border*2), gs.gw_height))
        
        # Draw Textbox Area
        self.text_box = pygame.draw.rect(screen, gs.black, (gs.text_box_x, gs.text_box_y, gs.text_box_w, gs.text_box_h))
                  
        # Clock / Save Area
        #self.clock_controls = pygame.draw.rect(screen, gs.black, (gs.sidebar_x, gs.clock_box_y, gs.sidebar_w, gs.clock_box_h))
        
        # Inventory Window Area
        self.inventory_window = pygame.Rect(gs.sidebar_x, 0, gs.sidebar_w, gs.inventory_h)
        pygame.draw.rect(screen, gs.silver, self.inventory_window)
        pygame.draw.rect(screen, gs.black, self.inventory_window, 3)

        # Define and Draw inventory items
        inventory.draw_items(gs, screen)

        """
        # Draw Save Button
        self.save_button = pygame.Rect(0, self.inventory_window.bottom - 55, 110, 40)
        self.save_button.centerx = self.inventory_window.centerx
        pygame.draw.rect(screen, gs.gray, self.save_button)
        pygame.draw.rect(screen, gs.black, self.save_button, 2)
        self.save_text = gs.cambria30.render('SAVE', True, gs.black)
        self.save_text_rect = self.save_text.get_rect()
        self.save_text_rect.center = self.save_button.center
        screen.blit(self.save_text, self.save_text_rect)

        self.load_button = pygame.Rect(self.inventory_window.x + 80, self.inventory_window.bottom - 150, 50, 50)
        pygame.draw.rect(screen, gs.black, self.load_button)
        
        """

        # Draw the 'Change Screen' Windows
        if gs.lights_on:
            if not gs.room_view_drill_down: # Only shows if drill down is not current
                ### Left
                pygame.draw.rect(self.screen_directions, gs.gray_transparent, self.go_left)
                ### Right
                pygame.draw.rect(self.screen_directions, gs.gray_transparent, self.go_right)

            ### Top/Up
            #pygame.draw.rect(self.screen_directions, gs.gray_transparent, self.go_up, 1)

            ### Back/Bottom
            #self.go_back = pygame.Rect(gs.gw_move_w+gs.gw_border*2, gs.gw_height-gs.gw_move_w/2, (gs.gw_width-gs.gw_move_w*2-gs.gw_border*4), gs.gw_move_w)  # No longer used
            #pygame.draw.rect(self.screen_directions, gs.gray_transparent, self.go_back)  # No longer used

            else:
                pygame.draw.rect(self.screen_directions, gs.gray_transparent, self.go_back)

        screen.blit(self.screen_directions, (0,0))
        pygame.draw.rect(screen, gs.black, (0, 0, gs.screen_width, gs.screen_height), 3)


        """
        
        #### Displays clock on screen
        clock_value = gf.get_game_clock(gs, screen)
        clock_text = gs.verdana18.render(clock_value, True, gs.black)
        screen.blit(clock_text, (0,0))

        ##### Room View (top left corner)
        self.strtodisplay = "r" + str(gs.current_room_view) + " d" + str(gs.room_view_drill_down)
        self.text_image = self.viewfont.render(self.strtodisplay, True, gs.black)
        self.text_image_rect = self.text_image.get_rect()
        self.screen.blit(self.text_image, self.text_image_rect)
        
        """




