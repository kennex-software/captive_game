#kennex

import sys, pygame, random, time, threading, pickle
from pygame.math import Vector2
import math
import datetime
from objects import GameObjects
import puzzles
import credits
#from tkinter import Tk
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import sched
from room import Room
from stable_items import Stable_Items
from inventory import Inventory
from PIL import ImageFont

pygame.init()
pygame.font.init()

root = tk.Tk()
root.wm_attributes('-topmost', 1)
root.withdraw()




def check_events(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp):
    """Response to mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #if game_objects.save_button.collidepoint(event.pos):
                #    save_settings(gs)
                #if game_objects.load_button.collidepoint(event.pos):
                #    load_settings(gs)
                if not gs.options_menu_up:
                    if not gs.won_game:
                        if not gs.stable_item_opened:
                            room_view.switch_light(gs, event)
                            if gs.lights_on:
                                room_view.move_between_views(gs, screen, game_objects, stable_item_blocks, event)
                                inventory.select_item(gs, screen, room_view, event)

                                if gs.drill_possible:
                                    room_view.drill_down_views(gs, screen, game_objects, event)

                                if gs.current_room_view == 0:   # Default View
                                    room_view.open_door(gs, event)
                                    room_view.click_tv(gs, event, game_objects)
                                    room_view.click_trash_can(gs, event)
                                    if gs.door_opened:
                                        room_view.close_door(gs, event)
                                        if room_view.main_door.collidepoint(event.pos) and gs.current_room_view == 0 and gs.room_view_drill_down == 0:
                                            gs.won_game = True
                                            gs.end_time = pygame.time.get_ticks()
                                            print('clicked door')
                                            gs.game_started = False


                                    if gs.room_view_drill_down == 0.1 and not gs.power_cord_found: # Function to click power cord when it's not found
                                        room_view.click_power_cord(gs, event)

                                if gs.current_room_view == -1:  # Left from default
                                    room_view.open_drawers(gs, screen, game_objects, event) # See open drawers for click events
                                    room_view.click_desk_wall_outlet(gs, event)
                                    if gs.power_cord_desk_1 and not gs.power_cord_desk_2:
                                        room_view.pick_power_cord_desk(gs, event)
                                    if gs.desk_drawer_removed and not gs.green_key_found:
                                        room_view.click_green_key(gs, event)
                                    if gs.desk_drawer_removed:
                                        room_view.click_hole_in_floor(gs, event)

                                if gs.current_room_view == 1:  # Right from default // View with TV
                                    room_view.click_tv(gs, event, game_objects)
                                    if gs.room_view_drill_down == 1:
                                        if not gs.remote_found: # Function to click remote when it's not found
                                            room_view.click_remote(gs, event)

                                if gs.current_room_view < -1 or gs.current_room_view > 1:  # Fourth wall
                                    room_view.click_window_wall_outlet(gs, event)
                                    if gs.power_cord_window_1 and gs.room_view_drill_down == 0:
                                        room_view.pick_power_cord_window(gs, event)
                                    if not gs.shirt_found and gs.room_view_drill_down == 0:
                                        room_view.click_shirt(gs, event)
                                    if gs.room_view_drill_down == 1:
                                        #if gs.safe_uncovered: # Function when safe is uncovered
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

                    else:
                        print("won game")
                    if gs.control_panel_on:
                        cp.check_clicked_setting(gs, screen, event)
                        if cp.selected == 1:
                            cp.dots.append(event.pos)




                print("Click Position: " + str(event.pos))
                #print(str(event.pos))

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                inventory.deselect_items(gs, event)
        elif event.type == pygame.MOUSEMOTION:
            inventory.item_grabbed(gs, event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if gs.room_view_drill_down != 0:
                    gs.room_view_drill_down = 0
                else:
                    gs.options_menu_up = True
                    gs.pause_time = pygame.time.get_ticks()
                    gs.game_started = False



def update_screen(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop
    screen.fill(gs.bg_color)
    room_view.current_view(gs, screen, stable_item_blocks)
    GameObjects(gs, screen, inventory)
    game_status_text(gs, screen)

    if gs.control_panel_on:
        cp.draw_control_panel(gs, screen)
        if cp.selected == 1:
            cp.draw_dots(gs, screen)

    
        
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def draw_item_to_screen(gs, screen, image, factor, x, y):
    """Function to pass item and draw to screen
    image = loaded image variable
    factor = scale factor
    x = x position
    y = y position
    """
    full_rect = image.get_rect()
    image_surface = (int(full_rect[2] / factor), int(full_rect[3] / factor))
    image_rect = pygame.Rect(x, y, image_surface[0], image_surface[1])

    screen.blit(pygame.transform.smoothscale(image, (int(full_rect[2] / factor), int(full_rect[3] / factor))), image_rect)
    #pygame.draw.rect(screen, gs.yellow, image_rect, 3) # todo comment this out

    return image_rect

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

def aspect_scale_wh(surface, bx, my_h):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio
     surface is the image
     bx is the width you want
     """
    mywidth = bx
    bw, bh = surface.get_size()

    wpercent = (mywidth/float(bw))
    hsize = my_h
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
    gs.prb_n1 = random.randint(1, 13) # k
    gs.prb_n2 = random.randint(1, 22) # n
    gs.prb_code = gs.prb_n1*gs.prb_n2+(2*gs.prb_n1*(3+gs.prb_n2))+(gs.prb_n1+gs.prb_n2)

    # Puzzle A
    number_list_pua = []
    range_to_shuffle = range(1, 7)
    for n in range_to_shuffle:
        number_list_pua.append(n)
    random.shuffle(number_list_pua)
    gs.pua_code = ''.join(map(str, number_list_pua))

    gs.pua_double_digits = puzzles.double_digits(gs.pua_code)

    # Puzzle B
    gs.pub_n1 = random.randint(2, 9)
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
    gs.channel_code = str(gs.prb_code) + str(gs.pub_code)


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

    # Four Digits for Safe Combination
    while len(gs.safe_combo_random) < 4:
        number = random.randint(1, 6)
        if number not in gs.safe_combo_random:
            gs.safe_combo_random.append(number)

    # Two Colors for TV
    for n in range(1, 7):
        if n not in gs.safe_combo_random:
            gs.tv_color_numbers.append(n)

    # Implement safe code in proper order
    safe_combo_temp = list(map(int, str(gs.pua_code)))

    for x in safe_combo_temp:
        if x in gs.safe_combo_random:
            gs.safe_combo.append(x)

    # Random Channel for Papers
    gs.random_channel = random.randint(44, 99)
    if gs.random_channel == gs.pub_n7:
        gs.random_channel += 3

    # Turn Safe On Channel
    random_choice = ['U', 'D', 'L', 'R', 'F', '9']
    safe_on_channel = []
    for n in range(1, 9):
        x = random.choice(random_choice)
        safe_on_channel.append(x)

    gs.turn_safe_on_channel = ''.join(safe_on_channel)


    # Problem A
    # Random Number for Subject Number
    gs.door_number = random.randint(10, 101) # this is the subject number on camera 1
    gs.konar_number = random.randint(3, 98) # this is going to be "hidden" in camera 2   // "street sign"

    gs.safe_alpha_pra_answer = int(round_down(gs.konar_number/gs.door_number*25/10))



    # Necessary game settings based on settings for development purposes
    if gs.all_items_visible == True:
        for n in range(0, 7):
            gs.moveable_items_index_list.append(n)

    if gs.all_unlocked == True:
        self.fcd1_locked = False  # Default = False
        self.fcd2_locked = False  # Default = True // Unlocked with Purple Key
        self.dd1_locked = False  # Default = True // Unlocked with Green Key
        self.dd2_locked = False  # Default = False
        self.dd3_locked = False  # Default = True // Unlocked with Red Key
        self.door_locked = False  # Default = True // Unlocked with Door Key (Gold)

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def game_status_text(gs, screen):
    """ Function to display text at the bottom bar of the game """

    # Text box parameters
    text_box_w = (gs.gw_width - (gs.gw_border * 2))/2
    text_box_h = (gs.screen_height + gs.gw_height + gs.gw_border*3)/2
    # Text image
    bottom_text_image = gs.verdana16.render(gs.text, True, gs.white)
    # ONE LINE - Draw text that is only one line
    bti_rect = bottom_text_image.get_rect(center=(text_box_w, text_box_h))

    screen.blit(bottom_text_image, bti_rect)

    """if gs.text != None and gs.text_seconds > 0:
        time_stop = datetime.datetime.now()
        print(time_stop)



        

        gs.text_seconds -= 1

    else:
        gs.text = None
        gs.text_seconds = gs.default_seconds # will display text for this many iterations, then text will do away
    """


def get_game_clock(gs, screen):
    """ Returns a string value of the game clock"""
    clock_output = str(datetime.timedelta(seconds = gs.current_time // 1000))
    return clock_output

def clock_timer(gs):
    if gs.game_started:
        gs.current_time = pygame.time.get_ticks() - gs.game_start_time - gs.stoppage_time



def update_settings_dictionary(gs):
    gs.settings_dictionary = {
                                'new_game': gs.new_game,
                                'text': gs.text,
                                'current_text': gs.current_text,
                                'current_time': gs.current_time,
                                'save_time': gs.save_time,
                                'pause_time': gs.pause_time,
                                'resume_time': gs.resume_time,
                                'stoppage_time': gs.stoppage_time,
                                'end_time': gs.end_time,
                                'frame_rate': gs.frame_rate,
                                'game_start_time': gs.game_start_time,
                                'won_game': gs.won_game,
                                'all_items_visible': gs.all_items_visible,
                                'door_key_found': gs.door_key_found,
                                'red_key_found': gs.red_key_found,
                                'purple_key_found': gs.purple_key_found,
                                'green_key_found': gs.green_key_found,
                                'remote_found': gs.remote_found,
                                'batteries_found': gs.batteries_found,
                                'power_cord_found': gs.power_cord_found,
                                'papers_found': gs.papers_found,
                                'red_book_found': gs.red_book_found,
                                'blue_book_found': gs.blue_book_found,
                                'desk_drawer_removed': gs.desk_drawer_removed,
                                'shirt_found': gs.shirt_found,
                                'screwdriver_found': gs.screwdriver_found,
                                'power_cord_desk_1': gs.power_cord_desk_1,
                                'power_cord_desk_2': gs.power_cord_desk_2,
                                'power_cord_window_1': gs.power_cord_window_1,
                                'moveable_items_index_list': gs.moveable_items_index_list,
                                'door_key_used': gs.door_key_used,
                                'red_key_used': gs.red_key_used,
                                'purple_key_used': gs.purple_key_used,
                                'green_key_used': gs.green_key_used,
                                'batteries_used': gs.batteries_used,
                                'power_cord_used': gs.power_cord_used,
                                'screwdriver_used': gs.screwdriver_used,
                                'stable_item_opened': gs.stable_item_opened,
                                'shirt_opened': gs.shirt_opened,
                                'remote_opened': gs.remote_opened,
                                'close_remote': gs.close_remote,
                                'batteries_input': gs.batteries_input,
                                'button_input_list': gs.button_input_list,
                                'entered_buttons': gs.entered_buttons,
                                'tv_on': gs.tv_on,
                                'current_channel': gs.current_channel,
                                'random_channel': gs.random_channel,
                                'tv_sound_play_var': gs.tv_sound_play_var,
                                'safe_on_sound_var': gs.safe_on_sound_var,
                                'current_tv_screen_color': gs.current_tv_screen_color,
                                'safe_uncovered': gs.safe_uncovered,
                                'safe_on': gs.safe_on,
                                'safe_initialized': gs.safe_initialized,
                                'safe_use_color': gs.safe_use_color,
                                'color_number_1': gs.color_number_1,
                                'color_number_2': gs.color_number_2,
                                'safe_combo_n1': gs.safe_combo_n1,
                                'safe_combo_n2': gs.safe_combo_n2,
                                'safe_combo_n3': gs.safe_combo_n3,
                                'safe_combo_n4': gs.safe_combo_n4,
                                'safe_opened': gs.safe_opened,
                                'safe_combo_random': gs.safe_combo_random,
                                'safe_combo': gs.safe_combo,
                                'safe_alpha_pra_answer': gs.safe_alpha_pra_answer,
                                'tv_color_numbers': gs.tv_color_numbers,
                                'turn_safe_on_channel': gs.turn_safe_on_channel,
                                'safe_alpha_index': gs.safe_alpha_index,
                                'safe_combo_a1': gs.safe_combo_a1,
                                'fourth_wall': gs.fourth_wall,
                                'current_room_view': gs.current_room_view,
                                'drill_possible': gs.drill_possible,
                                'room_view_drill_down': gs.room_view_drill_down,
                                'fcd1_opened': gs.fcd1_opened,
                                'fcd2_opened': gs.fcd2_opened,
                                'dd1_opened': gs.dd1_opened,
                                'dd2_opened': gs.dd2_opened,
                                'dd3_opened': gs.dd3_opened,
                                'dd3_open_attempts': gs.dd3_open_attempts,
                                'desk_drawer_up': gs.desk_drawer_up,
                                'fcd1_locked': gs.fcd1_locked,
                                'fcd2_locked': gs.fcd2_locked,
                                'dd1_locked': gs.dd1_locked,
                                'dd2_locked': gs.dd2_locked,
                                'dd3_locked': gs.dd3_locked,
                                'door_locked': gs.door_locked,
                                'all_unlocked': gs.all_unlocked,
                                'door_opened': gs.door_opened,
                                'door_number': gs.door_number,
                                'konar_number': gs.konar_number,
                                'cam_two_number': gs.cam_two_number,
                                'lights_on': gs.lights_on,
                                'lights_beginning': gs.lights_beginning,
                                'red_book_opened': gs.red_book_opened,
                                'blue_book_opened': gs.blue_book_opened,
                                'current_page': gs.current_page,
                                'current_book': gs.current_book,
                                'diary_choice': gs.diary_choice,
                                'papers_opened': gs.papers_opened,
                                'current_paper_in_view': gs.current_paper_in_view,
                                'prb_n1': gs.prb_n1,
                                'prb_n2': gs.prb_n2,
                                'prb_code': gs.prb_code,
                                'pua_code': gs.pua_code,
                                'pua_double_digits': gs.pua_double_digits,
                                'pub_n1': gs.pub_n1,
                                'pub_n3': gs.pub_n3,
                                'pub_n2': gs.pub_n2,
                                'pub_n4': gs.pub_n4,
                                'pub_n5': gs.pub_n5,
                                'pub_n6': gs.pub_n6,
                                'pub_n7': gs.pub_n7,
                                'pub_n8': gs.pub_n8,
                                'pub_n9': gs.pub_n9,
                                'pub_code': gs.pub_code

        }

def update_settings_from_save_file(gs):
    gs.new_game = gs.settings_dictionary['new_game']
    gs.text = gs.settings_dictionary['text']
    gs.current_text = gs.settings_dictionary['current_text']
    gs.current_time = gs.settings_dictionary['current_time']
    gs.save_time = gs.settings_dictionary['save_time']
    gs.pause_time = gs.settings_dictionary['pause_time']
    gs.resume_time = gs.settings_dictionary['resume_time']
    gs.stoppage_time = gs.settings_dictionary['stoppage_time']
    gs.end_time = gs.settings_dictionary['end_time']
    gs.frame_rate = gs.settings_dictionary['frame_rate']
    gs.game_start_time = gs.settings_dictionary['game_start_time']
    gs.won_game = gs.settings_dictionary['won_game']
    gs.all_items_visible = gs.settings_dictionary['all_items_visible']
    gs.door_key_found = gs.settings_dictionary['door_key_found']
    gs.red_key_found = gs.settings_dictionary['red_key_found']
    gs.purple_key_found = gs.settings_dictionary['purple_key_found']
    gs.green_key_found = gs.settings_dictionary['green_key_found']
    gs.remote_found = gs.settings_dictionary['remote_found']
    gs.batteries_found = gs.settings_dictionary['batteries_found']
    gs.power_cord_found = gs.settings_dictionary['power_cord_found']
    gs.papers_found = gs.settings_dictionary['papers_found']
    gs.red_book_found = gs.settings_dictionary['red_book_found']
    gs.blue_book_found = gs.settings_dictionary['blue_book_found']
    gs.desk_drawer_removed = gs.settings_dictionary['desk_drawer_removed']
    gs.shirt_found = gs.settings_dictionary['shirt_found']
    gs.screwdriver_found = gs.settings_dictionary['screwdriver_found']
    gs.power_cord_desk_1 = gs.settings_dictionary['power_cord_desk_1']
    gs.power_cord_desk_2 = gs.settings_dictionary['power_cord_desk_2']
    gs.power_cord_window_1 = gs.settings_dictionary['power_cord_window_1']
    gs.moveable_items_index_list = gs.settings_dictionary['moveable_items_index_list']
    gs.door_key_used = gs.settings_dictionary['door_key_used']
    gs.red_key_used = gs.settings_dictionary['red_key_used']
    gs.purple_key_used = gs.settings_dictionary['purple_key_used']
    gs.green_key_used = gs.settings_dictionary['green_key_used']
    gs.batteries_used = gs.settings_dictionary['batteries_used']
    gs.power_cord_used = gs.settings_dictionary['power_cord_used']
    gs.screwdriver_used = gs.settings_dictionary['screwdriver_used']
    gs.stable_item_opened = gs.settings_dictionary['stable_item_opened']
    gs.shirt_opened = gs.settings_dictionary['shirt_opened']
    gs.remote_opened = gs.settings_dictionary['remote_opened']
    gs.close_remote = gs.settings_dictionary['close_remote']
    gs.batteries_input = gs.settings_dictionary['batteries_input']
    gs.button_input_list = gs.settings_dictionary['button_input_list']
    gs.entered_buttons = gs.settings_dictionary['entered_buttons']
    gs.tv_on = gs.settings_dictionary['tv_on']
    gs.current_channel = gs.settings_dictionary['current_channel']
    gs.random_channel = gs.settings_dictionary['random_channel']
    gs.tv_sound_play_var = gs.settings_dictionary['tv_sound_play_var']
    gs.safe_on_sound_var = gs.settings_dictionary['safe_on_sound_var']
    gs.current_tv_screen_color = gs.settings_dictionary['current_tv_screen_color']
    gs.safe_uncovered = gs.settings_dictionary['safe_uncovered']
    gs.safe_on = gs.settings_dictionary['safe_on']
    gs.safe_initialized = gs.settings_dictionary['safe_initialized']
    gs.safe_use_color = gs.settings_dictionary['safe_use_color']
    gs.color_number_1 = gs.settings_dictionary['color_number_1']
    gs.color_number_2 = gs.settings_dictionary['color_number_2']
    gs.safe_combo_n1 = gs.settings_dictionary['safe_combo_n1']
    gs.safe_combo_n2 = gs.settings_dictionary['safe_combo_n2']
    gs.safe_combo_n3 = gs.settings_dictionary['safe_combo_n3']
    gs.safe_combo_n4 = gs.settings_dictionary['safe_combo_n4']
    gs.safe_opened = gs.settings_dictionary['safe_opened']
    gs.safe_combo_random = gs.settings_dictionary['safe_combo_random']
    gs.safe_combo = gs.settings_dictionary['safe_combo']
    gs.safe_alpha_pra_answer = gs.settings_dictionary['safe_alpha_pra_answer']
    gs.tv_color_numbers = gs.settings_dictionary['tv_color_numbers']
    gs.turn_safe_on_channel = gs.settings_dictionary['turn_safe_on_channel']
    gs.safe_alpha_index = gs.settings_dictionary['safe_alpha_index']
    gs.safe_combo_a1 = gs.settings_dictionary['safe_combo_a1']
    gs.fourth_wall = gs.settings_dictionary['fourth_wall']
    gs.current_room_view = gs.settings_dictionary['current_room_view']
    gs.drill_possible = gs.settings_dictionary['drill_possible']
    gs.room_view_drill_down = gs.settings_dictionary['room_view_drill_down']
    gs.fcd1_opened = gs.settings_dictionary['fcd1_opened']
    gs.fcd2_opened = gs.settings_dictionary['fcd2_opened']
    gs.dd1_opened = gs.settings_dictionary['dd1_opened']
    gs.dd2_opened = gs.settings_dictionary['dd2_opened']
    gs.dd3_opened = gs.settings_dictionary['dd3_opened']
    gs.dd3_open_attempts = gs.settings_dictionary['dd3_open_attempts']
    gs.desk_drawer_up = gs.settings_dictionary['desk_drawer_up']
    gs.fcd1_locked = gs.settings_dictionary['fcd1_locked']
    gs.fcd2_locked = gs.settings_dictionary['fcd2_locked']
    gs.dd1_locked = gs.settings_dictionary['dd1_locked']
    gs.dd2_locked = gs.settings_dictionary['dd2_locked']
    gs.dd3_locked = gs.settings_dictionary['dd3_locked']
    gs.door_locked = gs.settings_dictionary['door_locked']
    gs.all_unlocked = gs.settings_dictionary['all_unlocked']
    gs.door_opened = gs.settings_dictionary['door_opened']
    gs.door_number = gs.settings_dictionary['door_number']
    gs.konar_number = gs.settings_dictionary['konar_number']
    gs.cam_two_number = gs.settings_dictionary['cam_two_number']
    gs.lights_on = gs.settings_dictionary['lights_on']
    gs.lights_beginning = gs.settings_dictionary['lights_beginning']
    gs.red_book_opened = gs.settings_dictionary['red_book_opened']
    gs.blue_book_opened = gs.settings_dictionary['blue_book_opened']
    gs.current_page = gs.settings_dictionary['current_page']
    gs.current_book = gs.settings_dictionary['current_book']
    gs.diary_choice = gs.settings_dictionary['diary_choice']
    gs.papers_opened = gs.settings_dictionary['papers_opened']
    gs.current_paper_in_view = gs.settings_dictionary['current_paper_in_view']
    gs.prb_n1 = gs.settings_dictionary['prb_n1']
    gs.prb_n2 = gs.settings_dictionary['prb_n2']
    gs.prb_code = gs.settings_dictionary['prb_code']
    gs.pua_code = gs.settings_dictionary['pua_code']
    gs.pua_double_digits = gs.settings_dictionary['pua_double_digits']
    gs.pub_n1 = gs.settings_dictionary['pub_n1']
    gs.pub_n3 = gs.settings_dictionary['pub_n3']
    gs.pub_n2 = gs.settings_dictionary['pub_n2']
    gs.pub_n4 = gs.settings_dictionary['pub_n4']
    gs.pub_n5 = gs.settings_dictionary['pub_n5']
    gs.pub_n6 = gs.settings_dictionary['pub_n6']
    gs.pub_n7 = gs.settings_dictionary['pub_n7']
    gs.pub_n8 = gs.settings_dictionary['pub_n8']
    gs.pub_n9 = gs.settings_dictionary['pub_n9']
    gs.pub_code = gs.settings_dictionary['pub_code']



def save_settings(gs):

    if gs.save_filename == None:
        gs.save_time = gs.current_time - gs.game_start_time
        gs.save_filename = asksaveasfilename(parent=root, initialdir="./saves/", title="Save File", filetypes=[("Data Files", "*.dat")], defaultextension=".dat")
        update_settings_dictionary(gs)
        pickle_out = open(gs.save_filename, 'wb')
        pickle.dump(gs.settings_dictionary, pickle_out)
        pickle_out.close()
        print('game saved')
    else:
        update_settings_dictionary(gs)
        pickle_out = open(gs.save_filename, 'wb')
        pickle.dump(gs.settings_dictionary, pickle_out)
        pickle_out.close()
        print('game saved')


def load_settings(gs):

    filename = askopenfilename(parent=root, initialdir="./saves/", title="Load Settings", filetypes=[("Data Files", "*.dat")]) # show an "Open" dialog box and return the path to the selected file
    if filename:
        pickle_in = open(filename, 'rb')
        gs.settings_dictionary = pickle.load(pickle_in)
        pickle_in.close()
        update_settings_from_save_file(gs)
        filename = None
        print('settings loaded')
        gs.start_game_from_load = True


def print_settings(gs):
    # Print specific settings of the game for the use of more easily being able to design
    # Massive hints here
    print("Current Room View: " + str(gs.current_room_view))
    print("")
    print("Problem A: ")
    print("")
    print("Problem B Code: " + str(gs.prb_code))
    print("Puzzle A Code: " + str(gs.pua_code))
    print("Puzzle B Code: " + str(gs.pub_code))
    print("Safe Combo: " + str(gs.safe_combo))
    print("TV Color Numbers: " + str(gs.tv_color_numbers))
    print("Random Channel: " + str(gs.random_channel))
    print("Channel to Turn On Safe: " + str(gs.turn_safe_on_channel))
    print("Channel Code: " + str(gs.channel_code))
    print("Konar Number (street sign): " + str(gs.konar_number))
    print("Subject Number: " + str(gs.door_number))
    print("Safe Combo A1: " + str(gs.safe_combo_a1))
    print("Alpha Code: " + str(gs.safe_alpha_pra_answer) + "; " + str(gs.alphabet_list[gs.safe_alpha_pra_answer]))
    print("")
    print("Purple: " + str(gs.color_codes['purple'][0]))
    print("Blue: " + str(gs.color_codes['blue'][0]))
    print("Green: " + str(gs.color_codes['green'][0]))
    print("Yellow: " + str(gs.color_codes['yellow'][0]))
    print("Orange: " + str(gs.color_codes['orange'][0]))
    print("Red: " + str(gs.color_codes['red'][0]))
    print("")
    print("Diary Choice: " + str(gs.diary_choice))
    print("")
    print("Channel List:")
    print("1: Python // Done")
    print("2: Gnarski // Done")
    print("3: Default // Done")
    print("4: Camera 1 // Done")
    print("5: Camera 2 // Done")
    print("6: Camera 3 // Done")
    print("7: Falling Numbers // Done")
    print("8: Whitespace // Done")
    print("9: Blank // Done")
    print("12: Game Clock // Done")
    print("1234567890F: Button Presser // Done")
    print(str(gs.pub_n7) + ": Blue Book Hint // Not Done")
    print(str(gs.channel_code) + ": Code to Turn on Safe // Done")
    print(str(gs.random_channel) + ": Diamond Channel // Done")
    print(str(gs.turn_safe_on_channel) + ": Turn Safe On Channel // Done")
    print("FINDCHANNEL: ???")
    print("FINDCHANNEL: ???")
    print("181161693114: ???")












