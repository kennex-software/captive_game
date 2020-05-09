#kennex

import sys, pygame, random, pickle
from pygame.math import Vector2
import math
import datetime
import puzzles
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import check_steam

pygame.font.init()
root = tk.Tk()
root.wm_attributes('-topmost', 1)
root.withdraw()



def check_events(gs, screen, inventory, room_view, game_objects, stable_item_blocks, cp, steamworks):
    """Response to mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if len(gs.wasd_list) > 0:
                    gs.wasd_list = []
                if not gs.options_menu_up:
                    if not gs.won_game:
                        if not gs.stable_item_opened:
                            room_view.switch_light(gs, event, steamworks)
                            if gs.lights_on:
                                room_view.move_between_views(gs, screen, game_objects, stable_item_blocks, event)
                                inventory.select_item(gs, screen, room_view, event)


                                if gs.drill_possible:
                                    room_view.drill_down_views(gs, screen, game_objects, event, steamworks)

                                if gs.current_room_view == 0:   # Default View
                                    room_view.open_door(gs, event)
                                    room_view.click_tv(gs, event, game_objects)
                                    room_view.click_trash_can(gs, event)
                                    if gs.door_opened:
                                        room_view.close_door(gs, event, steamworks)
                                        if room_view.main_door.collidepoint(event.pos) and gs.current_room_view == 0 and gs.room_view_drill_down == 0:

                                            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                                            if gs.leave: # This is all the end of the game stuff when the user exits the room
                                                gs.won_game = True
                                                gs.end_time = get_game_clock(gs, screen)
                                                if gs.current_time < 7200000:
                                                    check_steam.check_set_achievement(steamworks, b'ACH_EXIT_TWOHOUR') # Exit the room in under 2 hours
                                                    if gs.current_time < 3600000:
                                                        check_steam.check_set_achievement(steamworks, b'ACH_EXIT_ONEHOUR') # Exit the room in under 1 hour
                                                if gs.game_clicks <= 175:
                                                    check_steam.check_set_achievement(steamworks, b'ACH_MO_CLICKS') # Escape the room in under 175 clicks
                                                gs.game_started = False
                                                check_steam.check_set_achievement(steamworks, b'ACH_EXIT_ONE') # Door Opened Achievement
                                                check_steam.check_set_stats(steamworks, gs, 1) # Add 1 to stats of times exited and check other stats

                                            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                                            else:
                                                gs.leave = True


                                    if gs.room_view_drill_down == 0.1 and not gs.power_cord_found: # Function to click power cord when it's not found
                                        room_view.click_power_cord(gs, event, steamworks)

                                if gs.current_room_view == -1:  # Left from default
                                    room_view.open_drawers(gs, screen, game_objects, event, steamworks) # See open drawers for click events
                                    room_view.click_desk_wall_outlet(gs, event)
                                    if not gs.yellow_book_found:
                                        room_view.click_yellow_book(gs, event, steamworks)
                                    if gs.power_cord_desk_1 and not gs.power_cord_desk_2:
                                        room_view.pick_power_cord_desk(gs, event)
                                    if gs.desk_drawer_removed and not gs.green_key_found:
                                        room_view.click_green_key(gs, event, steamworks)
                                    if gs.desk_drawer_removed:
                                        room_view.click_hole_in_floor(gs, event)

                                if gs.current_room_view == 1:  # Right from default // View with TV
                                    if gs.room_view_drill_down == 0:
                                        room_view.click_tv(gs, event, game_objects)
                                        if gs.tv_stand_open and not gs.egg_found:
                                            room_view.click_egg(gs, event, steamworks)
                                    if gs.room_view_drill_down == 1:
                                        if not gs.remote_found: # Function to click remote when it's not found
                                            room_view.click_remote(gs, event, steamworks)
                                            if gs.tv_stand_open and not gs.egg_found:
                                                gs.tv_stand_open = False
                                                pygame.mixer.Sound.play(tv_stand_open_sound)

                                if gs.current_room_view < -1 or gs.current_room_view > 1:  # Fourth wall
                                    if gs.room_view_drill_down == 0:
                                        room_view.click_window_wall_outlet(gs, event)
                                        if gs.power_cord_window_1:
                                            room_view.pick_power_cord_window(gs, event)
                                        if not gs.shirt_found:
                                            room_view.click_shirt(gs, event, steamworks)
                                    if gs.room_view_drill_down == 1:
                                        #if gs.safe_uncovered: # Function when safe is uncovered
                                        room_view.safe_controls(gs, screen, event, steamworks)
                                        if not gs.papers_found: # Function to click papers when they're not found
                                            room_view.click_papers(gs, event, steamworks)


                        else:
                            if gs.red_book_opened or gs.blue_book_opened or gs.yellow_book_opened:
                                stable_item_blocks.change_manual_pages(gs, event, steamworks)
                            if gs.remote_opened:
                                stable_item_blocks.remote_buttons_clicked(gs, event, steamworks)
                            if gs.papers_opened:
                                stable_item_blocks.change_papers(gs, event)
                            if gs.shirt_opened:
                                stable_item_blocks.shirt_clicks(gs, event, steamworks)
                            if gs.desk_drawer_up:
                                stable_item_blocks.pull_up_desk_drawer_clicks(gs, event)

                    else:
                        pass
                    if gs.control_panel_on:
                        cp.check_clicked_setting(gs, screen, event)
                        if cp.selected == 1:
                            cp.dots.append(event.pos)




                print("Click Position: " + str(event.pos))
                print(gs.yellow_book_opened)
                #print(str(event.pos))
                if gs.game_started:
                    gs.game_clicks += 1
                #print(gs.game_clicks)

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
                    if gs.quit_menu_up:
                        gs.quit_menu_up = False
            if event.key == pygame.K_f:
                if gs.current_channel == 'F' and gs.tv_on:
                    check_steam.check_set_achievement(steamworks, b'ACH_F') # Respects Achievement
            if event.key == pygame.K_w:
                if len(gs.wasd_list) == 0:
                    gs.wasd_list.append('w')
            if event.key == pygame.K_a:
                if len(gs.wasd_list) == 1 and 'w' in gs.wasd_list:
                    gs.wasd_list.append('a')
                else:
                    gs.wasd_list = []
            if event.key == pygame.K_s:
                if len(gs.wasd_list) == 2 and 'a' in gs.wasd_list:
                    gs.wasd_list.append('s')
                else:
                    gs.wasd_list = []
            if event.key == pygame.K_d:
                if len(gs.wasd_list) == 3 and 's' in gs.wasd_list:
                    gs.wasd_list = []
                    check_steam.check_set_achievement(steamworks, b'ACH_WRONG_CONTROLS') # Wrong Controls Achievement
                else:
                    gs.wasd_list = []
            if event.key == pygame.K_EQUALS:
                print_settings(gs)



def update_screen(gs, screen, inventory, room_view, stable_item_blocks, cp, clock, game_objects, screen_rect, tex_gl):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop



    # Fill Screen
    screen.fill(gs.bg_color)

    # Draw Room View
    room_view.current_view(gs, screen, stable_item_blocks)

    # Draw Inventory Window and Border
    draw_inventory_window(gs, screen, game_objects)

    # Draw Inventory Item
    inventory.draw_items(gs, screen)

    # Show Game Overlay
    screen.blit(game_objects_on_screen(gs, game_objects), (0,0))

    # Draw Game Text
    game_status_text(gs, screen)



    if gs.control_panel_on:
        cp.draw_control_panel(gs, screen)
        if cp.selected == 1:
            cp.draw_dots(gs, screen)

    tex_gl.update(screen_rect.width, screen_rect.height, tex_gl.screen_to_string(screen))

    # Make the most recently drawn screen visible.
    pygame.display.flip()
    clock.tick(60)

def game_objects_on_screen(gs, game_objects):
    screen_overlay = pygame.Surface((gs.gw_width, gs.gw_height), pygame.SRCALPHA)
    #GameObjects(gs, screen, inventory)

    pygame.draw.rect(screen_overlay, gs.silver, game_objects.inventory_window)
    pygame.draw.rect(screen_overlay, gs.black, game_objects.inventory_window, 3)

    # Draw Directions Windows
    if gs.lights_on:
        if not gs.room_view_drill_down: # Only shows if drill down is not current
            ### Left
            pygame.draw.rect(screen_overlay, gs.gray_transparent, game_objects.go_left)
            ### Right
            pygame.draw.rect(screen_overlay, gs.gray_transparent, game_objects.go_right)
        else:
            pygame.draw.rect(screen_overlay, gs.gray_transparent, game_objects.go_back)

    return screen_overlay



def draw_inventory_window(gs, screen, game_objects):
    pygame.draw.rect(screen, gs.silver, game_objects.inventory_window)
    pygame.draw.rect(screen, gs.black, game_objects.inventory_window, 3)

    # Draw Bottom Black Border
    pygame.draw.rect(screen, gs.black, game_objects.bottom_border)
    #pygame.draw.rect(screen_overlay, gs.black, (0, 0, gs.screen_width, gs.screen_height), 3)


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

def check_inside_clickbox(gs, bounding_points, bounding_box_positions):
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

    # Egg Channel
    gs.easter_egg_channel = str(random.randint(12030, 32030)) + 'F'

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

    # Egg Channel TV Dot Code
    list_for_channel = ['> ',
                        '> .',
                        '> ..',
                        '> ...',
                        '> ....',
                        '> .....',
                        '> ......',
                        '> .......',
                        '> ........',
                        '> .........',
                        ]

    for number in gs.easter_egg_channel:
        if number == 'F':
            gs.list_to_display_on_egg.append('> F')
        else:
            gs.list_to_display_on_egg.append(list_for_channel[int(number)])

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


def get_game_clock(gs, screen):
    """ Returns a string value of the game clock"""
    clock_output = str(datetime.timedelta(seconds = gs.current_time // 1000))
    return clock_output

def clock_timer(gs):
    if gs.game_started:
        gs.current_time = pygame.time.get_ticks() - gs.game_start_time - gs.stoppage_time



def update_settings_dictionary(gs):
    """Function to update the settings dictionary."""
    gs.settings_dictionary = {
                                'new_game': gs.new_game,
                                'game_clicks': gs.game_clicks,
                                'text': gs.text,
                                'leave': gs.leave,
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
                                'yellow_book_found': gs.yellow_book_found,
                                'desk_drawer_removed': gs.desk_drawer_removed,
                                'shirt_found': gs.shirt_found,
                                'screwdriver_found': gs.screwdriver_found,
                                'power_cord_desk_1': gs.power_cord_desk_1,
                                'power_cord_desk_2': gs.power_cord_desk_2,
                                'power_cord_window_1': gs.power_cord_window_1,
                                'moveable_items_index_list': gs.moveable_items_index_list,
                                'number_all_items_found': gs.number_all_items_found,
                                'list_to_display_on_egg': gs.list_to_display_on_egg,
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
                                'tv_stand_open_var': gs.tv_stand_open_var,
                                'current_tv_screen_color': gs.current_tv_screen_color,
                                'message_channel_play': gs.message_channel_play,
                                'tv_stand_open': gs.tv_stand_open,
                                'tv_stand_egg_found_text_var': gs.tv_stand_egg_found_text_var,
                                'easter_egg_channel': gs.easter_egg_channel,
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
                                'fc2_open_attempts': gs.fc2_open_attempts,
                                'desk_drawer_up': gs.desk_drawer_up,
                                'fcd1_locked': gs.fcd1_locked,
                                'fcd2_locked': gs.fcd2_locked,
                                'dd1_locked': gs.dd1_locked,
                                'dd2_locked': gs.dd2_locked,
                                'dd3_locked': gs.dd3_locked,
                                'door_locked': gs.door_locked,
                                'door_opened': gs.door_opened,
                                'door_number': gs.door_number,
                                'konar_number': gs.konar_number,
                                'cam_two_number': gs.cam_two_number,
                                'lights_on': gs.lights_on,
                                'lights_beginning': gs.lights_beginning,
                                'red_book_opened': gs.red_book_opened,
                                'blue_book_opened': gs.blue_book_opened,
                                'yellow_book_opened': gs.yellow_book_opened,
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
    """Function to update settings from a save file."""
    gs.new_game = gs.settings_dictionary['new_game']
    gs.game_clicks = gs.settings_dictionary['game_clicks']
    gs.text = gs.settings_dictionary['text']
    gs.leave = gs.settings_dictionary['leave']
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
    gs.yellow_book_found = gs.settings_dictionary['yellow_book_found']
    gs.desk_drawer_removed = gs.settings_dictionary['desk_drawer_removed']
    gs.shirt_found = gs.settings_dictionary['shirt_found']
    gs.screwdriver_found = gs.settings_dictionary['screwdriver_found']
    gs.egg_found = gs.settings_dictionary['egg_found']
    gs.power_cord_desk_1 = gs.settings_dictionary['power_cord_desk_1']
    gs.power_cord_desk_2 = gs.settings_dictionary['power_cord_desk_2']
    gs.power_cord_window_1 = gs.settings_dictionary['power_cord_window_1']
    gs.moveable_items_index_list = gs.settings_dictionary['moveable_items_index_list']
    gs.number_all_items_found = gs.settings_dictionary['number_all_items_found']
    gs.list_to_display_on_egg = gs.settings_dictionary['list_to_display_on_egg']
    gs.door_key_used = gs.settings_dictionary['door_key_used']
    gs.red_key_used = gs.settings_dictionary['red_key_used']
    gs.purple_key_used = gs.settings_dictionary['purple_key_used']
    gs.green_key_used = gs.settings_dictionary['green_key_used']
    gs.batteries_used = gs.settings_dictionary['batteries_used']
    gs.power_cord_used = gs.settings_dictionary['power_cord_used']
    gs.screwdriver_used = gs.settings_dictionary['screwdriver_used']
    gs.egg_used = gs.settings_dictionary['egg_used']
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
    gs.tv_stand_open_var = gs.settings_dictionary['tv_stand_open_var']
    gs.current_tv_screen_color = gs.settings_dictionary['current_tv_screen_color']
    gs.message_channel_play = gs.settings_dictionary['message_channel_play']
    gs.tv_stand_open = gs.settings_dictionary['tv_stand_open']
    gs.tv_stand_egg_found_text_var = gs.settings_dictionary['tv_stand_egg_found_text_var']
    gs.easter_egg_channel = gs.settings_dictionary['easter_egg_channel']
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
    gs.fc2_open_attempts = gs.settings_dictionary['fc2_open_attempts']
    gs.desk_drawer_up = gs.settings_dictionary['desk_drawer_up']
    gs.fcd1_locked = gs.settings_dictionary['fcd1_locked']
    gs.fcd2_locked = gs.settings_dictionary['fcd2_locked']
    gs.dd1_locked = gs.settings_dictionary['dd1_locked']
    gs.dd2_locked = gs.settings_dictionary['dd2_locked']
    gs.dd3_locked = gs.settings_dictionary['dd3_locked']
    gs.door_locked = gs.settings_dictionary['door_locked']
    gs.door_opened = gs.settings_dictionary['door_opened']
    gs.door_number = gs.settings_dictionary['door_number']
    gs.konar_number = gs.settings_dictionary['konar_number']
    gs.cam_two_number = gs.settings_dictionary['cam_two_number']
    gs.lights_on = gs.settings_dictionary['lights_on']
    gs.lights_beginning = gs.settings_dictionary['lights_beginning']
    gs.red_book_opened = gs.settings_dictionary['red_book_opened']
    gs.blue_book_opened = gs.settings_dictionary['blue_book_opened']
    gs.yellow_book_opened = gs.settings_dictionary['yellow_book_opened']
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
    """Function to save the current settings to a game save file."""
    try:
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
    except:
        print('file not saved')
        gs.save_filename = None


def load_settings(gs):
    """Function to load the settings from a previous game save file."""
    gs.quit_menu_up = False
    gs.options_menu_up = False

    try:
        filename = askopenfilename(parent=root, initialdir="./saves/", title="Load Settings", filetypes=[("Data Files", "*.dat")]) # show an "Open" dialog box and return the path to the selected file
        if filename:
            pickle_in = open(filename, 'rb')
            gs.settings_dictionary = pickle.load(pickle_in)
            pickle_in.close()
            update_settings_from_save_file(gs)
            if filename != None:
                gs.start_game_from_load = True
                print('settings loaded')
            filename = None


    except:
        print('file not loaded')
        gs.start_game_from_load = False

def default_settings(gs):
    """Function to change all of the game settings to default settings for a new game."""
    gs.new_game = True
    gs.game_clicks = 0
    gs.save_filename = None
    gs.options_menu_up = False
    gs.quit_menu_up = False
    gs.game_ended = False
    gs.leave = False
    gs.text = None
    gs.game_clicks = 0
    gs.current_text = None
    gs.frame_rate = 60
    gs.game_start_time = None
    gs.current_time = 0
    gs.save_time = 0
    gs.pause_time = 0
    gs.resume_time = 0
    gs.stoppage_time = 0
    gs.end_time = 0
    gs.won_game = False # Dfeault = False todo make false
    gs.door_key_found = False # Default = False
    gs.red_key_found = False # Default = False
    gs.purple_key_found = False # Default = False
    gs.green_key_found = False # Default = False
    gs.remote_found = False # Default = False todo make false
    gs.batteries_found = False # Default = False
    gs.power_cord_found = False # Default = False
    gs.papers_found = False # Default = False
    gs.red_book_found = False # Default = False
    gs.blue_book_found = False # Default = False
    gs.yellow_book_found = False # Default = False
    gs.desk_drawer_removed = False # Default = False
    gs.shirt_found = False # Default = False
    gs.screwdriver_found = False # Default = False
    gs.egg_found = False # Default = False
    gs.power_cord_desk_1 = False # Default = False
    gs.power_cord_desk_2 = False # Default = False
    gs.power_cord_window_1 = False # Default = False
    gs.moveable_items_index_list = []
    gs.number_all_items_found = 0
    gs.list_to_display_on_egg = []
    gs.door_key_used = False # Default = False
    gs.red_key_used = False # Default = False
    gs.purple_key_used = False # Default = False
    gs.green_key_used = False # Default = False
    gs.batteries_used = False # Default = False
    gs.power_cord_used = False # Default = False
    gs.screwdriver_used = False # Default = False
    gs.egg_used = False # Default = False
    gs.stable_item_opened = False  # Default = False
    gs.shirt_opened = False
    gs.remote_opened = False  # Default = False
    gs.close_remote = False  # Default = False
    gs.batteries_input = False  # Default = False # todo change to false
    gs.button_input_list = []
    gs.entered_buttons = None
    gs.muted = False
    gs.volume = None
    gs.tv_on = False  # Default = False todo make false
    gs.current_channel = '3' # Default = '3' todo make '3'
    gs.random_channel = None
    gs.tv_sound_play_var = 0
    gs.safe_on_sound_var = 0
    gs.tv_stand_open_var = 0
    gs.current_tv_screen_color = (82, 82, 82)
    gs.message_channel_play = False
    gs.tv_stand_open = False
    gs.tv_stand_egg_found_text_var = True
    gs.easter_egg_channel = '366F'
    gs.safe_uncovered = False # Default = false todo make false
    gs.safe_on = False  # Default = False // Nothing on the safe can be done or used until the safe is turned on todo make false
    gs.safe_initialized = False # Safe can only be opened if a certain channel is on the TV todo make false
    gs.safe_use_color = gs.black
    gs.color_number_1 = None  # This number is needed to open the safe
    gs.color_number_2 = None  # This number is needed to open the safe
    gs.safe_combo_n1 = 0  # This number is needed to open the safe
    gs.safe_combo_n2 = 0  # This number is needed to open the safe
    gs.safe_combo_n3 = 0  # This number is needed to open the safe
    gs.safe_combo_n4 = 0  # This number is needed to open the safe
    gs.safe_opened = False # Default = False todo change to false
    gs.safe_combo_random = []
    gs.safe_combo = []
    gs.safe_alpha_pra_answer = None
    gs.tv_color_numbers = []
    gs.turn_safe_on_channel = None
    gs.safe_alpha_index = 0
    gs.safe_combo_a1 = 0 # This number is needed to open the safe
    gs.fourth_wall = False  # Default = False
    gs.current_room_view = 0
    gs.drill_possible = False  # Default = False
    gs.room_view_drill_down = 0  # Default = 0
    gs.fcd1_opened = False  # Default = False
    gs.fcd2_opened = False  # Default = False
    gs.dd1_opened = False  # Default = False
    gs.dd2_opened = False  # Default = False
    gs.dd3_opened = False  # Default = False
    gs.dd3_open_attempts = 0  # Default = 0
    gs.fc2_open_attempts = 0  # Default = 0
    gs.desk_drawer_up = False
    gs.fcd1_locked = False  # Default = False
    gs.fcd2_locked = True  # Default = True // Unlocked with Purple Key
    gs.dd1_locked = True  # Default = True // Unlocked with Green Key
    gs.dd2_locked = False  # Default = False
    gs.dd3_locked = True  # Default = True // Unlocked with Red Key
    gs.door_locked = True  # Default = True // Unlocked with Door Key (Gold)
    gs.door_opened = False  # Default = False todo change to false
    gs.door_number = None
    gs.konar_number = None # Street sign in Camera 2
    gs.cam_two_number = None
    gs.lights_on = False  # Default = False todo change to false
    gs.lights_beginning = True
    gs.red_book_opened = False  # Default = False
    gs.blue_book_opened = False  # Default = False
    gs.yellow_book_opened = False  # Default = False
    gs.current_page = 1  # Default = 1
    gs.current_book = None
    gs.diary_choice = 0
    gs.papers_opened = False  # Default = False
    gs.current_paper_in_view = 1  # Default = 1
    gs.prb_n1 = 0
    gs.prb_n2 = 0
    gs.prb_code = 0
    gs.pua_code = 0
    gs.pua_double_digits = []
    gs.pub_n1 = 0
    gs.pub_n3 = 0
    gs.pub_n2 = 0
    gs.pub_n4 = 0
    gs.pub_n5 = 0
    gs.pub_n6 = 0
    gs.pub_n7 = 0
    gs.pub_n8 = 0
    gs.pub_n9 = 0
    gs.pub_code = 0
    gs.control_panel_on = False
    gs.channel_code = 0
    gs.color_codes = {'purple': [1, 'p', gs.purple],
                        'blue': [2, 'b', gs.blue],
                        'green': [3, 'g', gs.green],
                        'yellow': [4, 'y', gs.bright_yellow],
                        'orange':[5, 'o', gs.orange],
                        'red': [6, 'r', gs.red]}
    gs.settings_dictionary = {}
    gs.selected_item_index = None
    gs.selected_item = None
    gs.offset = None
    gs.item_selection_choice = False
    gs.selected_item_start_x = 0
    gs.selected_item_start_y = 0


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
    print("Easter Egg Channel: " + str(gs.easter_egg_channel))
    print("FINDCHANNEL: ???")
    print("181161693114: ???")

def scrolling_credits(gs, screen, credits_full, scrolling_centerx, scrolling_centery, delta_y):
    text_height = gs.arial48.get_height()

    line_spacing = 0
    credits_list = []
    position_list = []
    delta_y -= 30  # Default value = 20

    for line in credits_full.split('\n'):
        text_image = gs.arial48.render(line, True, gs.black)
        credits_list.append(text_image)
        position = text_image.get_rect(center=(scrolling_centerx, scrolling_centery + delta_y + line_spacing * 70))
        position_list.append(position)
        line_spacing += 1

    if scrolling_centery + delta_y + 70*(len(credits_full.split('\n'))) < 0:
        gs.won_game = False

    for i in range(line_spacing):
        screen.blit(credits_list[i], position_list[i])

def slope_function(x1, y1, x2, y2, x3, y3):
    m = (y2 - y1) / (x2 - x1) # calculate slope
    b = y1 - m * x1 # calculate y intercept
    if y3 == None:
        y3 = m * x3 + b
        return y3 # return new y
    else:
        x3 = (y3 - b) / m
        return x3 # return new x

def generate_line_sizes(gs):
    if gs.screen_width == 1440:
        # Room View 3 (TV Stand) Lines
        gs.r3_line_x2 = gs.gw_width
        gs.r3_line_y2 = slope_function(770, 600, 1070, 750, gs.gw_width, None)
        # Room View 3 (TV Stand Drill Down) Lines
        gs.r3_1_line_x2 = gs.gw_width
        gs.r3_1_line_y2 = slope_function(680, 460, 1093, 740, gs.gw_width, None)
        # Inside Closet Drill Down Lines
        gs.r4_1_line_x2 = slope_function(876, 508, 1074, 741, None, gs.full_game_window_height)
        gs.r4_1_line_y2 = gs.full_game_window_height

def found_all_items(gs, steamworks):
    gs.number_all_items_found += 1
    print('item found: ' + str(gs.number_all_items_found))
    if gs.number_all_items_found == gs.number_total_items:
        check_steam.check_set_achievement(steamworks, b'ACH_COLLECT') # Collect all items
























