#kennex

import pygame, sys
import pygame.font

class GameText():
    """All text that occurs during the game at the bottom of the screen."""
        
    def __init__(self, gs, screen):
        """Initialize text"""
        self.screen = screen
        self.gs = gs
        
        # Settings
        self.text_font_color = gs.white
        self.myfont = pygame.font.SysFont("Verdana", 16)
        
        # Text to display based on the point in the game
        #oneline = 'This text should easily still be centered on the green box'
       
        self.text_to_display = gs.text
        
        # Text box parameters      
        text_box_w = (gs.gw_width - (gs.gw_border * 2))/2
        text_box_h = (gs.screen_height + gs.gw_height + gs.gw_border*3)/2

        # Text image
        self.bottom_text_image = self.myfont.render(self.text_to_display, True, self.text_font_color)

        # ONE LINE - Draw text that is only one line
        self.bti_rect = self.bottom_text_image.get_rect(center=(text_box_w, text_box_h))
        
        # Draw text to screen
        self.screen.blit(self.bottom_text_image, self.bti_rect)



"""
        ptext.draw(threeline, (text_box_w, text_box_h), color=gs.blue)
        
        if self.bottom_text_image.get_width() < text_box_w:
        elif self.bottom_text_image.get_width() == text_box_w:
            # TWO LINES - Draw text that must be on two lines
            text_box_h = text_box_h + 10
            self.bti_rect = self.bottom_text_image.get_rect(center=(text_box_w, text_box_h))
            # self.bti_rect = 
            print('two lines')

        elif self.bottom_text_image.get_width() == text_box_w:
            # THREE LINES - Draw text that must be on three lines
            print('three lines')
         
        else: 
            print('false')
            
            
        twoline = '1. Display this text. 2. Display this text. 3. Display this text. 4. Display this text. \n5. Display this text. 6. Display this text. 7. Display this text. 8. Display this text. 9. Display this text.'
        threeline = '1. Display this text. 2. Display this text. 3. Display this text. 4. Display this text. \n5. Display this text. 6. Display this text. 7. Display this text. 8. Display this text. 9. Display this text. 10. Display this text. 11. Display this text. 12. Display this text. 13. Display this text. 14. Display this text. 15. Display this text. 16. Display this text. 17. Display this text. 18. Display this text. 19. Display this text. 20. Display this text.'
 
        
        
"""


