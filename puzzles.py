#! python 3
# kennex
#

import random
import math
import pygame

pygame.font.init()

# Digit Doubler - Used to find the digits to circle for Puzzle A
def double_digits(n):
    circled_digits = []
    for position, x in enumerate(n):
        new_number = str(x) + str(position+1)
        circled_digits.append(new_number)
    return circled_digits

# This board is used for Puzzle A
def get_board(gs, screen, n, list):

    # get the numbers
    numbers = [i for i in range(n * n)]

    numbers_string = []
    for i in range(0, len(numbers)):
        numbers_string.append(str(numbers[i]))
    #numbers_string = list(map(str, numbers))
    #print(list)

    for i in list:
        if str(i) in numbers_string:
            #print(i)
            numbers_string[int(i)] = str(i)

    # create the nested list representing the board
    rev_board = [numbers_string[i:i+n][::-1] for i in range(0, len(numbers_string), n)]

    # Generate the board to the screen
    if gs.screen_width == 1200:
        start = 378
    else:
        start = 478
    for line in reversed(rev_board):
        end = 208
        start += 30
        for number in line:
            if number in gs.pua_double_digits:
                text_image = gs.verdana16.render(number, True, gs.red)
            else:
                text_image = gs.verdana16.render(number, True, gs.black)

            screen.blit(text_image, (start, end))
            end += 35
            #print('%3s' % number, end = " ")
        #print()

