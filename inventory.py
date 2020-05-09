#kennex

import pygame
import pygame.font
from pygame.math import Vector2
import gf

pygame.font.init()
pygame.mixer.init()

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
i_papers = 'images/papers_1top.png' # Papers
i_red_book = 'images/red_book.png' # Red Book
i_blue_book = 'images/blue_book.png' # Blue Book
i_yellow_book = 'images/yellow_book.png' # Yellow Book
i_shirt = 'images/shirt_no_hang.png' # Shirt
i_screwdriver = 'images/flathead.png' # Screwdriver
i_egg = 'images/egg.png' # Screwdriver

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
yellow_book = pygame.image.load(i_yellow_book)
shirt = pygame.image.load(i_shirt)
screwdriver = pygame.image.load(i_screwdriver)
egg_inv = pygame.image.load(i_egg)

sur_inv_desk_drawer = pygame.Surface((218, 94), pygame.SRCALPHA)
sur_inv_desk_drawer.fill((254, 254, 254, 0))



# Load Sounds
key_sound = pygame.mixer.Sound('sounds/key_jingle.wav')
flip_page_sound = pygame.mixer.Sound('sounds/flip_page.wav')
shirt_sound = pygame.mixer.Sound('sounds/pick_shirt.wav')


# Game Screen
g_red_key_taped = 'images/red_key_rotated_tape.png' # Red Key with Tape
g_ripped_tape = 'images/ripped_tape.png' # Ripped Tape

red_key_taped = pygame.image.load(g_red_key_taped)
ripped_tape = pygame.image.load(g_ripped_tape)
  


class Inventory():
    """Setup of the inventory items and what happens when they are clicked."""
        
    def __init__(self, gs, screen, room_view):
        """Initialize inventory class"""
        super().__init__()
        self.screen = screen
        self.gs = gs
        self.room_view = room_view

        inv_height_var = int(gs.screen_height // 12.3)

        # Range of inventory list | Need to figure out and fix the height variables        here V   and    here V
        for y in range(8):
            inv_items_spaces.append(pygame.Rect(gs.sidebar_x+gs.item_offset_w, gs.item_offset_h+ inv_height_var *y, gs.inv_item_w, gs.inv_item_h))
            inv_items_stable.append(pygame.Rect(gs.inv_item_w+gs.sidebar_x+gs.item_offset_w*2, gs.item_offset_h+ inv_height_var *y, gs.inv_item_w, gs.inv_item_h))

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

        # Scaled Images
        self.remote_inv_scaled = pygame.transform.smoothscale(remote, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.papers_inv_scaled = pygame.transform.smoothscale(papers, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.red_book_inv_scaled = pygame.transform.smoothscale(red_book, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.blue_book_inv_scaled = pygame.transform.smoothscale(blue_book, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.yellow_book_inv_scaled = pygame.transform.smoothscale(yellow_book, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.shirt_inv_scaled = pygame.transform.smoothscale(shirt, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.drawer_inv_scaled = gf.aspect_scale(sur_inv_desk_drawer, int(gs.inv_item_w))
        self.door_key_inv_scaled = pygame.transform.smoothscale(door_key, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.red_key_inv_scaled = pygame.transform.smoothscale(red_key, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.purple_key_inv_scaled = pygame.transform.smoothscale(purple_key, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.green_key_inv_scaled = pygame.transform.smoothscale(green_key, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.batteries_inv_scaled = pygame.transform.smoothscale(batteries, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.power_cord_inv_scaled = pygame.transform.smoothscale(power_cord, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.screwdriver_inv_scaled = pygame.transform.smoothscale(screwdriver, (int(gs.inv_item_w), int(gs.inv_item_h)))
        self.egg_inv_scaled = gf.aspect_scale(egg_inv, 43)

    def draw_items(self, gs, screen):
        """Draw the items in the locations they need to be."""
        # Change in settings to False to hide all items
       ### Stable Items
        if gs.remote_found == True:  # Draw Remote Inventory Item
            screen.blit(self.remote_inv_scaled, inv_items_stable[0])
        if gs.papers_found == True:  # Draw Papers Inventory Item
            screen.blit(self.papers_inv_scaled, inv_items_stable[1])
        if gs.red_book_found == True:  # Draw Red Book Inventory Item
            screen.blit(self.red_book_inv_scaled, inv_items_stable[2])
        if gs.blue_book_found == True:  # Draw Blue Book Manual Inventory Item
            screen.blit(self.blue_book_inv_scaled, inv_items_stable[3])
        if gs.shirt_found == True: # Draw Shirt
            screen.blit(self.shirt_inv_scaled, inv_items_stable[4])
        if gs.desk_drawer_removed == True:  # Draw Desk Drawer
            sdx = inv_items_stable[5].centerx
            sdy = inv_items_stable[5].centery
            screen.blit(self.drawer_inv_scaled, (sdx - self.drawer_inv_scaled.get_width() // 2, sdy - self.drawer_inv_scaled.get_height() // 2 ))
        if gs.yellow_book_found == True:  # Draw Yellow Book Manual Inventory Item
            screen.blit(self.yellow_book_inv_scaled, inv_items_stable[6])

        ### Moveable Items
        if gs.door_key_found == True and not gs.door_key_used:  # Draw Door Key Inventory Item
            screen.blit(self.door_key_inv_scaled, inv_items_spaces[0])
        if gs.red_key_found == True and not gs.red_key_used:  # Draw File Cabinet Key 1 Inventory Item
            screen.blit(self.red_key_inv_scaled, inv_items_spaces[1])
        if gs.purple_key_found == True and not gs.purple_key_used:  # Draw File Cabinet Key 2 Inventory Item
            screen.blit(self.purple_key_inv_scaled, inv_items_spaces[2])
        if gs.green_key_found == True and not gs.green_key_used:  # Draw Desk Drawer Key Inventory Item
            screen.blit(self.green_key_inv_scaled, inv_items_spaces[3])
        if gs.batteries_found == True and not gs.batteries_used:  # Draw Batteries Inventory Item
            screen.blit(self.batteries_inv_scaled, inv_items_spaces[4])
        if gs.power_cord_found == True and not gs.power_cord_used:  # Draw Power Cord Inventory Item
            screen.blit(self.power_cord_inv_scaled, inv_items_spaces[5])
        if gs.screwdriver_found == True and not gs.screwdriver_used:  # Draw Screwdriver Inventory Item
            screen.blit(self.screwdriver_inv_scaled, inv_items_spaces[6])
        if gs.egg_found == True and not gs.egg_used:  # Draw Egg Inventory Item
            sdx = inv_items_spaces[7].centerx
            sdy = inv_items_spaces[7].centery
            screen.blit(self.egg_inv_scaled, (sdx - self.egg_inv_scaled.get_width() // 2, sdy - self.egg_inv_scaled.get_height() // 2 ))



        """# Draw pick boxes
        for item in inv_items_spaces:
            pygame.draw.rect(screen, gs.black, item, 1)  # <<<<< CHANGE THE # HERE TO -1 TO REMOVE THE ABILITY TO SEE THE BOXES
            
        for item in inv_items_stable:
            pygame.draw.rect(screen, gs.black, item, 1)  # <<<<< CHANGE THE # HERE TO -1 TO REMOVE THE ABILITY TO SEE THE BOXES
        """
            
    def select_item(self, gs, screen, room_view, event):  # Referenced from gf
        """Determines which item is selected"""

        for item in inv_items_spaces:
            index = inv_items_spaces.index(item)
            if index in gs.moveable_items_index_list:
                if item.collidepoint(event.pos):
                    #print(index)
                    gs.offset = Vector2(item.topleft) - event.pos
                    gs.selected_item = item
                    gs.selected_item_index = index
                    gs.selected_item_start_x = item.x
                    gs.selected_item_start_y = item.y

        for item in inv_items_stable:
            if item.collidepoint(event.pos) and gs.stable_item_opened == False:
                index = inv_items_stable.index(item)
                if index == 0 and gs.remote_found:
                    gs.stable_item_opened = True  # Turns on stable items.  User cannot move in view until item is closed.
                    gs.remote_opened = not gs.remote_opened
                if index == 1 and gs.papers_found:
                    gs.stable_item_opened = True  # Turns on stable items.  User cannot move in view until item is closed.
                    gs.papers_opened = not gs.papers_opened
                    pygame.mixer.Sound.play(flip_page_sound)
                if index == 2 and gs.red_book_found:
                    gs.stable_item_opened = True  # Turns on stable items.  User cannot move in view until item is closed.
                    gs.red_book_opened = not gs.red_book_opened
                    pygame.mixer.Sound.play(flip_page_sound)
                    gs.current_book = 'red_book'
                if index == 3 and gs.blue_book_found:
                    gs.stable_item_opened = True  # Turns on stable items.  User cannot move in view until item is closed.
                    gs.blue_book_opened = not gs.blue_book_opened
                    pygame.mixer.Sound.play(flip_page_sound)
                    gs.current_book = 'blue_book'
                if index == 4 and gs.shirt_found:
                    gs.stable_item_opened = True  # Turns on stable items.  User cannot move in view until item is closed.
                    gs.shirt_opened = not gs.shirt_opened
                    pygame.mixer.Sound.play(shirt_sound)
                if index == 5 and gs.desk_drawer_removed:
                    gs.stable_item_opened = True  # Turns on stable items.  User cannot move in view until item is closed.
                    gs.desk_drawer_up = not gs.desk_drawer_up
                if index == 6 and gs.yellow_book_found:
                    gs.stable_item_opened = True  # Turns on stable items.  User cannot move in view until item is closed.
                    gs.yellow_book_opened = not gs.yellow_book_opened
                    pygame.mixer.Sound.play(flip_page_sound)
                    gs.current_book = 'yellow_book'


    def item_grabbed(self, gs, event):  # Referenced from gf
        """Drags items around screen"""
        if gs.selected_item:
            gs.selected_item.topleft = event.pos + gs.offset
    
    def deselect_items(self, gs, event):  # Referenced from gf
        """Returns settings for moving items back to normal state"""
        if gs.selected_item:
            if gs.item_selection_choice == False:
                self.room_view.item_intersection(gs, event)
                gs.selected_item.x = gs.selected_item_start_x
                gs.selected_item.y = gs.selected_item_start_y
            
        gs.selected_item = None
        gs.selected_item_index = None
        gs.offset = None





    
