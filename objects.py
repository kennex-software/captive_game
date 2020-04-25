#kennex

import pygame

class GameObjects():
    """Class to store the objects in the game"""
    
    def __init__(self, gs, screen, inventory):
        """Initialize the game objects."""

        self.gs = gs
        self.screen = screen     
        self.inventory = inventory

        self.go_left = pygame.Rect(gs.gw_border, gs.gw_border, gs.gw_move_w, gs.gw_height)
        self.go_right = pygame.Rect(gs.gw_right_x, gs.gw_border, gs.gw_move_w, gs.gw_height)
        self.go_back = pygame.Rect(gs.gw_move_w+gs.gw_border*2, gs.gw_height-gs.gw_move_w, (gs.gw_width-gs.gw_move_w*2-gs.gw_border*4), gs.gw_move_w)
        self.bottom_border = pygame.Rect(gs.text_box_x, gs.text_box_y, gs.text_box_w, gs.text_box_h)

        self.inventory_window = pygame.Rect(gs.sidebar_x, 0, gs.sidebar_w, gs.inventory_h)