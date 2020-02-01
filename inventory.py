#kennex

import pygame, sys
import pygame.font
from pygame.sprite import Sprite
from pygame.math import Vector2
import gf

pygame.init()

inv_items_stable = []  # List of inventory that do not move
inv_items_spaces = []  # List of inventory squares
inv_items = []  # List of actual inventory items

# Load All Images
# Inventory
i_door_key = 'images/door_key.png' # Door Key >> Gold Key
i_red_key = 'images/red_key.png' # File Cabinet Key 1 >> Red Key
i_purple_key = 'images/purple_key.png' # File Cabinet Key 2 >> Purple Key
i_green_key = 'images/green_key.png' # Desk Drawer Key >> Green Key
i_remote = 'images/remote.png' # Remote
i_batteries = 'images/batteries.png' # Batteries
i_power_cord = 'images/power_cord.png' # Power Cord
i_papers = 'images/papers.png' # Papers
i_red_book = 'images/red_book.png' # Red Book
i_blue_book = 'images/blue_book.png' # Blue Book
i_shirt = 'images/shirt_no_hang.png' # Shirt
i_screwdriver = 'images/flathead.png' # Screwdriver

door_key = pygame.image.load(i_door_key)
red_key = pygame.image.load(i_red_key)
purple_key = pygame.image.load(i_purple_key)
green_key = pygame.image.load(i_green_key)
remote = pygame.image.load(i_remote)
batteries = pygame.image.load(i_batteries)
power_cord = pygame.image.load(i_power_cord)
papers = pygame.image.load(i_papers)
red_book = pygame.image.load(i_red_book)
blue_book = pygame.image.load(i_blue_book)
shirt = pygame.image.load(i_shirt)
screwdriver = pygame.image.load(i_screwdriver)

sur_inv_desk_drawer = pygame.Surface((218, 94), pygame.SRCALPHA)
sur_inv_desk_drawer.fill((254, 254, 254, 0))

# Game Screen
g_red_key_taped = 'images/red_key_rotated_tape.png' # Red Key with Tape
g_ripped_tape = 'images/ripped_tape.png' # Ripped Tape

red_key_taped = pygame.image.load(g_red_key_taped)
ripped_tape = pygame.image.load(g_ripped_tape)
  




"""
inv_items.append(door_key)
inv_items.append(red_key)
inv_items.append(purple_key)
inv_items.append(green_key)
inv_items.append(remote)
inv_items.append(batteries)
inv_items.append(power_cord)
inv_items.append(papers)
inv_items.append(camera_manual)
inv_items.append(chair_manual)
"""



class Inventory():
    """Setup of the inventory items and what happens when they are clicked."""
        
    def __init__(self, gs, screen, room_view):
        """Initialize inventory class"""
        super().__init__()
        self.screen = screen
        self.gs = gs
        self.room_view = room_view
        

        # Range of inventory list | Need to figure out and fix the height variables        here V   and    here V
        for y in range(7):
            inv_items_spaces.append(pygame.Rect(gs.sidebar_x+gs.item_offset_w, gs.item_offset_h+65*y, gs.inv_item_w, gs.inv_item_h))
            inv_items_stable.append(pygame.Rect(gs.inv_item_w+gs.sidebar_x+gs.item_offset_w*2, gs.item_offset_h+65*y, gs.inv_item_w, gs.inv_item_h))            

        # End Range of Inventory List ###############################
        
        # Desk Drawer
        desk_drawer_inv = pygame.Rect(2, 52, 185, 40)
        desk_drawer_back_inv = pygame.Rect(55, 2, 160, 40)
        pygame.draw.polygon(sur_inv_desk_drawer, gs.interior_drawer, ((desk_drawer_inv.topleft), (desk_drawer_inv.topright), (desk_drawer_back_inv.topright), (desk_drawer_back_inv.topleft)))
        pygame.draw.line(sur_inv_desk_drawer, gs.black, (desk_drawer_inv.topleft), (desk_drawer_back_inv.topleft), 2)
        pygame.draw.line(sur_inv_desk_drawer, gs.black, (desk_drawer_inv.bottomleft), (desk_drawer_back_inv.bottomleft), 2)
        pygame.draw.line(sur_inv_desk_drawer, gs.black, (desk_drawer_back_inv.bottomleft), (desk_drawer_back_inv.topleft), 2)
        pygame.draw.line(sur_inv_desk_drawer, gs.black, (desk_drawer_back_inv.bottomleft), (desk_drawer_back_inv.bottomright), 2)
        pygame.draw.polygon(sur_inv_desk_drawer, gs.interior_drawer, ((desk_drawer_inv.topright), (desk_drawer_inv.bottomright), (desk_drawer_back_inv.bottomright), (desk_drawer_back_inv.topright)))
        pygame.draw.line(sur_inv_desk_drawer, gs.black, (desk_drawer_inv.bottomright), (desk_drawer_back_inv.bottomright), 2)
        pygame.draw.line(sur_inv_desk_drawer, gs.black, (desk_drawer_inv.topright), (desk_drawer_back_inv.topright), 2)
        pygame.draw.line(sur_inv_desk_drawer, gs.black, (desk_drawer_back_inv.bottomright), (desk_drawer_back_inv.topright), 2)
        pygame.draw.line(sur_inv_desk_drawer, gs.black, (desk_drawer_back_inv.topleft), (desk_drawer_back_inv.topright), 2)

        pygame.draw.rect(sur_inv_desk_drawer, gs.wood, desk_drawer_inv)       
        pygame.draw.rect(sur_inv_desk_drawer, gs.black, desk_drawer_inv, 3)
        pygame.draw.circle(sur_inv_desk_drawer, gs.silver, (desk_drawer_inv.center), 7)
        pygame.draw.circle(sur_inv_desk_drawer, gs.black, (desk_drawer_inv.center), 8, 2)
        
    def draw_items(self, gs, screen):
        """Draw the items in the locations they need to be."""
        

        # Change this area's comments around to either see or not see the items in full
        """
        ### Stable Items
        if gs.remote_found == True:  # Draw Remote Inventory Item
            self.screen.blit(pygame.transform.smoothscale(remote, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[0])
        if gs.papers_found == True:  # Draw Papers Inventory Item
            self.screen.blit(pygame.transform.smoothscale(papers, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[1])   
        if gs.red_book_found == True:  # Draw Red Book Inventory Item
            self.screen.blit(pygame.transform.smoothscale(red_book, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[2])
        if gs.blue_book_found == True:  # Draw Blue Book Manual Inventory Item
            self.screen.blit(pygame.transform.smoothscale(blue_book, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[3])
        if gs.shirt_found == True: # Draw Shirt
            self.screen.blit(pygame.transform.smoothscale(shirt, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[4])
        if gs.desk_drawer_removed == True:  # Draw Desk Drawer
            sdx = inv_items_stable[5].centerx
            sdy = inv_items_stable[5].centery
            scaled_drawer = gf.aspect_scale(sur_inv_desk_drawer, int(gs.inv_item_w))
            self.screen.blit(scaled_drawer, (sdx - scaled_drawer.get_width() // 2, sdy - scaled_drawer.get_height() // 2 ))    
            
        ### Moveable Items
        if gs.door_key_found == True:  # Draw Door Key Inventory Item
            self.screen.blit(pygame.transform.smoothscale(door_key, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[0])
        if gs.red_key_found == True:  # Draw File Cabinet Key 1 Inventory Item
            self.screen.blit(pygame.transform.smoothscale(red_key, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[1])
        if gs.purple_key_found == True:  # Draw File Cabinet Key 2 Inventory Item
            self.screen.blit(pygame.transform.smoothscale(purple_key, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[2])
        if gs.green_key_found == True:  # Draw Desk Drawer Key Inventory Item
            self.screen.blit(pygame.transform.smoothscale(green_key, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[3])
        if gs.batteries_found == True:  # Draw Batteries Inventory Item
            self.screen.blit(pygame.transform.smoothscale(batteries, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[4])
        if gs.power_cord_found == True:  # Draw Power Cord Inventory Item
            self.screen.blit(pygame.transform.smoothscale(power_cord, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[5])
        if gs.screwdriver_found == True:  # Draw Screwdriver Inventory Item
            self.screen.blit(pygame.transform.smoothscale(screwdriver, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[6])



        """### Stable Items
        # Draw Remote Inventory Item
        self.screen.blit(pygame.transform.smoothscale(remote, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[0])
        # Draw Papers Inventory Item
        self.screen.blit(pygame.transform.smoothscale(papers, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[1])
        # Draw Camera Manual Inventory Item
        self.screen.blit(pygame.transform.smoothscale(red_book, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[2])
        # Draw Chair Manual Inventory Item
        self.screen.blit(pygame.transform.smoothscale(blue_book, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[3])
        # Draw Shirt
        self.screen.blit(pygame.transform.smoothscale(shirt, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_stable[4])
        # Draw Desk Drawer
        sdx = inv_items_stable[5].centerx
        sdy = inv_items_stable[5].centery
        scaled_drawer = gf.aspect_scale(sur_inv_desk_drawer, int(gs.inv_item_w))
        self.screen.blit(scaled_drawer, (sdx - scaled_drawer.get_width() // 2, sdy - scaled_drawer.get_height() // 2 ))

        # todo fix the ability to click the shirt when viewing safe in closet
        # todo fix the ability to open an open when it's not found yet in the inventory

        # settings 'S' todo remove this later
        text = 'S'
        text_image = gs.arial60.render(text, True, gs.black)
        self.screen.blit(text_image, inv_items_stable[6])
        
        ### Moveable Items
        # Draw Door Key Inventory Item
        self.screen.blit(pygame.transform.smoothscale(door_key, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[0])
        # Draw File Cabinet Key 1 Inventory Item
        self.screen.blit(pygame.transform.smoothscale(red_key, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[1])
        # Draw File Cabinet Key 2 Inventory Item
        self.screen.blit(pygame.transform.smoothscale(purple_key, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[2])
        # Draw Desk Drawer Key Inventory Item
        self.screen.blit(pygame.transform.smoothscale(green_key, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[3])
        # Draw Batteries Inventory Item
        self.screen.blit(pygame.transform.smoothscale(batteries, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[4])
        # Draw Power Cord Inventory Item
        self.screen.blit(pygame.transform.smoothscale(power_cord, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[5])
        # Draw Screwdriver Inventory Item
        self.screen.blit(pygame.transform.smoothscale(screwdriver, (int(gs.inv_item_w), int(gs.inv_item_h))), inv_items_spaces[6])


        # Draw pick boxes
        for item in inv_items_spaces:
            pygame.draw.rect(screen, gs.yellow, item, -1)  # <<<<< CHANGE THE # HERE TO -1 TO REMOVE THE ABILITY TO SEE THE BOXES
            
        for item in inv_items_stable:
            pygame.draw.rect(screen, gs.yellow, item, -1)  # <<<<< CHANGE THE # HERE TO -1 TO REMOVE THE ABILITY TO SEE THE BOXES

            
    def select_item(self, gs, screen, room_view, event):  # Referenced from gf
        """Determines which item is selected"""
        gs.sleeperticks = False
        for item in inv_items_spaces:
            if item.collidepoint(event.pos):
                gs.offset = Vector2(item.topleft) - event.pos
                gs.si = item
                gs.si_start_x = item.x
                gs.si_start_y = item.y
                index = inv_items_spaces.index(item)  # todo delete me later
                print(index)  # todo delete me later

        for item in inv_items_stable:
            if item.collidepoint(event.pos) and gs.stable_item_opened == False:
                gs.stable_item_opened = True  # Turns on stable items.  User cannot move in view until item is closed.
                index = inv_items_stable.index(item)
                #print(index)  # todo Delete me later
                if index == 0:
                    gs.remote_opened = not gs.remote_opened
                if index == 1:
                    gs.papers_opened = not gs.papers_opened
                if index == 2:
                    gs.red_book_opened = not gs.red_book_opened
                    gs.current_book = 'red_book'
                if index == 3:
                    gs.blue_book_opened = not gs.blue_book_opened
                    gs.current_book = 'blue_book'
                if index == 4:
                    gs.shirt_opened = not gs.shirt_opened
                if index == 5:
                    gs.desk_drawer_up = not gs.desk_drawer_up
                if index == 6: # todo figure out what to do with this later
                    gs.stable_item_opened = False
                    gf.print_settings(gs)

    def item_grabbed(self, gs, screen, event):  # Referenced from gf
        """Drags items around screen"""
        if gs.si:
            gs.si.topleft = event.pos + gs.offset
    
    def deselect_items(self, gs, screen, event):  # Referenced from gf
        """Returns settings for moving items back to normal state"""
        if gs.si:
            if gs.item_selection_choice == False:
                #for item in inv_items_spaces:
                gs.si.x = gs.si_start_x
                gs.si.y = gs.si_start_y
            
        gs.si = None
        gs.offset = None
        gs.sleeperticks = True


    
