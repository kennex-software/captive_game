#kennex

import pygame, sys
import pygame.font
from inventory import Inventory
import time

pygame.init()

class GameObjects():
    """Class to store the objects in the game"""
    
    def __init__(self, gs, screen, inventory):
        """Initialize the game objects."""
        super().__init__()
        self.gs = gs
        self.screen = screen     
        self.inventory = inventory  
    
        # Game Window Area
        # self.game_window_with_border = pygame.draw.rect(screen, gs.white, (gs.gw_border, gs.gw_border, gs.gw_width-(gs.gw_border*2), gs.gw_height))
        
        # Draw Textbox Area
        self.text_box = pygame.draw.rect(screen, gs.black, (gs.text_box_x, gs.text_box_y, gs.text_box_w, gs.text_box_h))
                  
        # Clock / Save Area
        #self.clock_controls = pygame.draw.rect(screen, gs.black, (gs.sidebar_x, gs.clock_box_y, gs.sidebar_w, gs.clock_box_h))
        
        # Inventory Window Area
        self.inventory_window = pygame.draw.rect(screen, gs.silver, (gs.sidebar_x, 0, gs.sidebar_w, gs.inventory_h))
        
        # Define and Draw inventory items
        inventory.draw_items(gs, screen)    
        
        # Draw the 'Change Screen' Windows
        ### Left
        self.go_left = pygame.draw.rect(screen, gs.yellow, (gs.gw_border, gs.gw_border, gs.gw_move_w, gs.gw_height), 1)
        ### Right
        self.go_right = pygame.draw.rect(screen, gs.yellow, (gs.gw_right_x, gs.gw_border, gs.gw_move_w, gs.gw_height), 1)
        ### Top/Up
        self.go_up = pygame.draw.rect(screen, gs.yellow, (gs.gw_move_w+gs.gw_border*2, 0, (gs.gw_width-gs.gw_move_w*2-gs.gw_border*4), gs.gw_move_w), 1)
        ### Back/Bottom
        self.go_back = pygame.draw.rect(screen, gs.yellow, (gs.gw_move_w+gs.gw_border*2, gs.gw_height-gs.gw_move_w/2, (gs.gw_width-gs.gw_move_w*2-gs.gw_border*4), gs.gw_move_w), 1)
        
        # Room View (top left corner)
        self.viewfont = pygame.font.SysFont(None, 60)
        self.strtodisplay = "r" + str(gs.current_room_view) + " d" + str(gs.room_view_drill_down)
        self.text_image = self.viewfont.render(self.strtodisplay, True, gs.black)
        self.text_image_rect = self.text_image.get_rect()
        self.screen.blit(self.text_image, self.text_image_rect)




