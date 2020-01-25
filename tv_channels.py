#kennex
# TV Channels

import pygame
import numpy as np

def tv_channels(gs, screen, gscurrent_channel):
    """
    Function to hold and display all information that could be found on the TV.
    channel = channel that is chosen
    """
    if gs.current_channel == 1:  # Whitespace todo need perlin noise?
        print(gs.current_channel)
    elif gs.current_channel == 2:  # Flash on screen
        print(gs.current_channel)
    elif gs.current_channel == 3:  # Default channel??
        print(gs.current_channel)
    elif gs.current_channel == 4:  # Camera 1
        print(gs.current_channel)
    elif gs.current_channel == 5:  # Camera 2
        print(gs.current_channel)
    elif gs.current_channel == 6:  # Camera 3
        print(gs.current_channel)
    elif gs.current_channel == 7:  # Whitespace
        print(gs.current_channel)
    elif gs.current_channel == 8:  # Whitespace
        print(gs.current_channel)
    elif gs.current_channel == 9:  # Black Screen
        print(gs.current_channel)
    elif gs.current_channel == gs.channel_code: # todo need to also add L+F
        print(gs.current_channel)
    elif gs.current_channel == 1: # todo easter egg channel for fun
        print(gs.current_channel)
    elif gs.current_channel == 1: # todo another number channel for fun from diary
        print(gs.current_channel)
    elif gs.current_channel == 1: # todo easter egg channel for fun
        print(gs.current_channel)
    else:  # Black Screen
        print("invalid channel")