#! python 3
# kennex
#

import random
import math
import pygame
import pygame.font
import ptext

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
    start = 378
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



"""
def blit_text(gs, screen, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


text = "This is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
       "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
       "This function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
       "text will disappear underneath the surface"
font = pygame.font.SysFont('Arial', 64)


"""