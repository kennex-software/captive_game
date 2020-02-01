#kennex

import sys, pygame, random
from pygame.math import Vector2
import math
from objects import GameObjects
import puzzles
from room import Room
from text import GameText
from stable_items import Stable_Items
from inventory import Inventory
from PIL import ImageFont

def check_events(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp):
    """Response to mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not gs.stable_item_opened:
                    room_view.switch_light(gs, event)
                    if gs.lights_on:
                        room_view.move_between_views(gs, screen, game_objects, stable_item_blocks, event)
                        inventory.select_item(gs, screen, room_view, event)

                        if gs.drill_possible:
                            room_view.drill_down_views(gs, screen, game_objects, event)

                        if gs.current_room_view == 0:   # Default View
                            if not gs.power_cord_found: # Function to click power cord when it's not found
                                room_view.click_power_cord(gs, event)

                        if gs.current_room_view == -1:  # Left from default
                            room_view.open_drawers(gs, screen, game_objects, event) # See open drawers for click events
                            if gs.desk_drawer_removed and not gs.green_key_found:
                                room_view.click_green_key(gs, event)

                        if gs.current_room_view == 1:  # Right from default
                            if gs.room_view_drill_down == 1:
                                if not gs.remote_found: # Function to click remote when it's not found
                                    room_view.click_remote(gs, event)

                        if gs.current_room_view < -1 or gs.current_room_view > 1:  # Fourth wall
                            if gs.room_view_drill_down == 1:
                                if gs.safe_uncovered: # Function when safe is uncovered
                                    room_view.safe_controls(gs, screen, event)
                                if not gs.papers_found: # Function to click papers when they're not found
                                    room_view.click_papers(gs, event)


                else:
                    if gs.red_book_opened or gs.blue_book_opened:
                        stable_item_blocks.change_manual_pages(gs, event)
                    if gs.remote_opened:
                        stable_item_blocks.remote_buttons_clicked(gs, event)
                    if gs.papers_opened:
                        stable_item_blocks.change_papers(gs, event)
                    if gs.shirt_opened:
                        stable_item_blocks.shirt_clicks(gs, event)
                    if gs.desk_drawer_up:
                        stable_item_blocks.pull_up_desk_drawer_clicks(gs, event)
                if gs.control_panel_on:
                    cp.check_clicked_setting(gs, screen, event)
                    if cp.selected == 1:
                        cp.dots.append(event.pos)




                print("Click Position: " + str(event.pos))
                #print(str(event.pos))

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                inventory.deselect_items(gs, screen, event)
        elif event.type == pygame.MOUSEMOTION:
            inventory.item_grabbed(gs, screen, event)

def update_screen(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop
    screen.fill(gs.bg_color)
    room_view.current_view(gs, screen, stable_item_blocks)
    GameObjects(gs, screen, inventory)
    GameText(gs, screen)
    if gs.control_panel_on:
        cp.draw_control_panel(gs, screen)
        if cp.selected == 1:
            cp.draw_dots(gs, screen)

    
        
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def aspect_scale(surface, bx):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio
     surface is the image
     bx is the width you want
     """
    mywidth = bx
    bw, bh = surface.get_size()

    wpercent = (mywidth/float(bw))
    hsize = int((float(bh)*float(wpercent)))
    surface = pygame.transform.smoothscale(surface, (mywidth, hsize))
    
    return surface

def check_inside_clickbox(self, bounding_points, bounding_box_positions):
    """This function will determine whether or not user clicked inside of a polygon or image"""
    """ bounding_points: nodes that make up the polygon.
        bounding_box_positions: candidate points to filter. (In my implementation created from the bounding box.
    """

    # Arrays containing the x- and y-coordinates of the polygon's vertices.
    vertx = [point[0] for point in bounding_points]
    verty = [point[1] for point in bounding_points]
    # Number of vertices in the polygon
    nvert = len(bounding_points)
    # Points that are inside
    points_inside = []

    # For every candidate position within the bounding box
    for idx, pos in enumerate(bounding_box_positions):
        testx, testy = (pos[0], pos[1])
        c = 0
        for i in range(0, nvert):
            j = i - 1 if i != 0 else nvert - 1
            if( ((verty[i] > testy ) != (verty[j] > testy))   and
                    (testx < (vertx[j] - vertx[i]) * (testy - verty[i]) / (verty[j] - verty[i]) + vertx[i]) ):
                c += 1
        # If odd, that means that we are inside the polygon
        if c % 2 == 1:
            points_inside.append(pos)
    if len(points_inside) == 1:
        return True
    else:
        return False

def generate_codes(gs):
    """
    This function only occurs once at the very beginning of the game (or when a new game is started).
    These codes are necessary for the game to run and are used to complete the puzzles and game.
    """
    # Problem A

    # Problem B
    gs.prb_n1 = random.randint(1, 13)
    gs.prb_n2 = random.randint(1, 22)
    gs.prb_code = gs.prb_n1*gs.prb_n2+(2*gs.prb_n1*(3+gs.prb_n2))+(gs.prb_n1+gs.prb_n2)

    # Puzzle A
    number_list_pua = []
    range_to_shuffle = range(1, 7)
    for n in range_to_shuffle:
        number_list_pua.append(n)
    random.shuffle(number_list_pua)
    gs.pua_code = ''.join(map(str, number_list_pua))

    gs.pua_double_digits = puzzles.double_digits(gs.pua_code)

    # Generate board for Puzzle A Numbers
    #board = puzzles.get_board(10, pua_double_digits)
    #print(board)


    # Puzzle B
    gs.pub_n1 = random.randint(1, 9)
    gs.pub_n3 = random.randint(1, 6)
    gs.pub_n2 = gs.pub_n1 * gs.pub_n3 * 2
    gs.pub_n4 = gs.pub_n1 + gs.pub_n2
    gs.pub_n6 = gs.pub_n1 + gs.pub_n3
    gs.pub_n5 = gs.pub_n4 * gs.pub_n6 * 2
    gs.pub_n7 = gs.pub_n4 + gs.pub_n5
    gs.pub_n9 = gs.pub_n4 + gs.pub_n6
    gs.pub_n8 = gs.pub_n7 * gs.pub_n9 * 2
    gs.pub_code = int(str(gs.pub_n8)[-3:])


    # Channel Code
    gs.channel_code = gs.prb_code + gs.pub_code

    # Diary Choice Interger
    gs.diary_choice = random.randint(1, 3)


    # Generate color numbers
    # Shuffle List for Colors
    number_list_colors = []
    range_to_shuffle = range(1, 7)
    for n in range_to_shuffle:
        number_list_colors.append(n)
    random.shuffle(number_list_colors)

    # Randomize the colors per numbers per game
    gs.color_codes['purple'][0] = number_list_colors[0]
    gs.color_codes['blue'][0] = number_list_colors[1]
    gs.color_codes['green'][0] = number_list_colors[2]
    gs.color_codes['yellow'][0] = number_list_colors[3]
    gs.color_codes['orange'][0] = number_list_colors[4]
    gs.color_codes['red'][0] = number_list_colors[5]

def print_settings(gs):
    # Print specific settings of the game for the use of more easily being able to design
    # Massive hints here
    print("Current Room View: " + str(gs.current_room_view))
    print("")
    print("Problem A: ")
    print("")
    print("Problem B Code: " + str(gs.prb_code))
    print("")
    print("Puzzle A Code: " + str(gs.pua_code))
    print("")
    print("Puzzle B Code: " + str(gs.pub_code))
    print("")
    print("Purple: " + str(gs.color_codes['purple'][0]))
    print("Blue: " + str(gs.color_codes['blue'][0]))
    print("Green: " + str(gs.color_codes['green'][0]))
    print("Yellow: " + str(gs.color_codes['yellow'][0]))
    print("Orange: " + str(gs.color_codes['orange'][0]))
    print("Red: " + str(gs.color_codes['red'][0]))
    print("")
    print("Channel Code: " + str(gs.channel_code))
    print("")
    print("Diary Choice: " + str(gs.diary_choice))
    print("")








