#kennex
# TV Channels

import pygame
import numpy as np

def tv_channels(gs, screen):
    """
    Function to hold and display all information that could be found on the TV.
    channel = channel that is chosen
    """
    if gs.current_channel == str(0):  # Whitespace todo need perlin noise?
        print(gs.current_channel)
    elif gs.current_channel == str(-1):  # Whitespace todo need perlin noise?
        print(gs.current_channel)
    elif gs.current_channel == str(1):  # Whitespace todo need perlin noise?
        print(gs.current_channel)
    elif gs.current_channel == str(2):  # Flash on screen
        print(gs.current_channel)
    elif gs.current_channel == str(3):  # Default channel??
        print(gs.current_channel)
    elif gs.current_channel == str(4):  # Camera 1
        print(gs.current_channel)
    elif gs.current_channel == str(5):  # Camera 2
        print(gs.current_channel)
    elif gs.current_channel == str(6):  # Camera 3
        print(gs.current_channel)
    elif gs.current_channel == str(7):  # Whitespace
        print(gs.current_channel)
    elif gs.current_channel == str(8):  # Whitespace
        print(gs.current_channel)
    elif gs.current_channel == str(9):  # Black Screen
        print(gs.current_channel)
    elif gs.current_channel == str(gs.channel_code):
        print(gs.current_channel)
    elif gs.current_channel == str('123456789L0F'): # todo easter egg channel for fun
        print(gs.current_channel)
    elif gs.current_channel == str(456): # todo another number channel for fun from diary
        print(gs.current_channel)
    elif gs.current_channel == str(456): # todo easter egg channel for fun
        print(gs.current_channel)
    elif gs.current_channel == str(456): # todo easter egg channel for fun
        print(gs.current_channel)
    else:  # Whitespace todo perlin noise
        print("invalid channel")