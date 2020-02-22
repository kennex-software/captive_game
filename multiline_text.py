#kennex

from PIL import ImageFont
import pygame
pygame.init()
pygame.font.init()

def multiline_text(text, width, font1):
    """
    *** Required: from PIL import ImageFont if it's not pygame


    Function to create multiline text based on inputs.
    The function then removes all extra empty lists.

    text = Any amount and string of text
    width = Width of the area the text should fit into
    font = the type of font being used

    Created by Kennex on 1/22/2020

    """

#    print(text)  # remove if needed
#    print("")  # remove if needed
    text_list = text.split()

    total_size = font1.size(text)
    #total_size = font_pass.getsize(text) # normal python
    lines = ((total_size[0] + 10) // width) + 1
    line_width = 0
    line_number = 0
    all_lines = []
    final_list = []

    for line in range(lines):
        all_lines.append([])

    for word in text_list:
        size = font1.size(word)
        word_width = size[0]
        line_width += word_width

        if line_width < width:
            all_lines[line_number].append(word)
        else:
            line_number += 1
            line_width = 0
            all_lines[line_number].append(word)

    temp_list = filter(None, all_lines)
    temp_list2 = list(temp_list)

    for i in temp_list2:
        joined = " ".join(i)
        final_list.append(joined)

#    print(final_list) # remove if needed

    return final_list



"""

text = "A paragraph is a self-contained unit of a discourse in writing dealing with a particular point or idea. A paragraph consists of one or more sentences. Though not required by the syntax of any language, paragraphs are usually an expected part of formal writing, used to organize longer prose."
width = 250
font = ImageFont.truetype('times.ttf', 12)
multiline_text(text, width, font)

"""