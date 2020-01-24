#kennex
# TV Channels

import pygame
import numpy as np

def tv_channels(gs, screen, channel):
    """
    Function to hold and display all information that could be found on the TV.
    channel = channel that is chosen
    """
    if channel == 1:  # Whitespace todo need perlin noise?
        print(channel)
    elif channel == 2:  # Flash on screen
        print(channel)
    elif channel == 3:  # Default channel??
        print(channel)
    elif channel == 4:  # Camera 1
        print(channel)
    elif channel == 5:  # Camera 2
        print(channel)
    elif channel == 6:  # Camera 3
        print(channel)
    elif channel == 7:  # Whitespace
        print(channel)
    elif channel == 8:  # Whitespace
        print(channel)
    elif channel == 9:  # Black Screen
        print(channel)
    elif channel == gs.channel_code: # todo need to also add L+F
        print(channel)
    elif channel == 1: # todo easter egg channel for fun
        print(channel)
    elif channel == 1: # todo another number channel for fun from diary
        print(channel)
    elif channel == 1: # todo easter egg channel for fun
        print(channel)
    else:  # Black Screen
        print("invalid channel")