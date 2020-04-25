#! python 3
# kennex
#
import pygame

pygame.font.init()


class Control_Panel():
    """A class to store the control panel for the drawing editor."""

    def __init__(self, gs, screen):
        """Initialize the control panel."""
        self.gs = gs
        self.screen = screen
        self.color = gs.black
        self.selected = None
        self.dots = []

    def draw_control_panel(self, gs, screen):
        # Control Panel
        self.cp_bg = pygame.Rect(0, 0, 170, 80)
        pygame.draw.rect(screen, gs.white, self.cp_bg)
        pygame.draw.rect(screen, gs.black, self.cp_bg, 2)

        # Dot
        self.dot_text_image = gs.verdana12.render('DOT', True, gs.black)
        screen.blit(self.dot_text_image, (10, 10))
        self.dot_color = gs.black
        self.dot_text_image_rect = self.dot_text_image.get_rect()
        self.cp_button1 = pygame.Rect((self.dot_text_image_rect.right + 15), self.dot_text_image_rect.centery, 20, 20)


        # Line
        self.line_text_image = gs.verdana12.render('LINE', True, gs.black)
        screen.blit(self.line_text_image, (75, 10))
        self.line_color = gs.black
        self.line_text_image_rect = self.line_text_image.get_rect()
        self.cp_button2 = pygame.Rect((self.line_text_image_rect.right + 85), self.line_text_image_rect.centery, 20, 20)


        # Multiline
        self.mline_text_image = gs.verdana12.render('MLINE', True, gs.black)
        screen.blit(self.mline_text_image, (10, 40))
        self.mline_color = gs.black
        self.mline_text_image_rect = self.mline_text_image.get_rect()
        self.cp_button3 = pygame.Rect((self.mline_text_image_rect.right + 15), self.mline_text_image_rect.centery + 30, 20, 20)


        # Clear
        self.clear_text_image = gs.verdana12.render('CLEAR', True, gs.black)
        screen.blit(self.clear_text_image, (85, 40))
        self.clear_color = gs.black
        self.clear_text_image_rect = self.clear_text_image.get_rect()
        self.cp_button4 = pygame.Rect((self.clear_text_image_rect.right + 95), self.clear_text_image_rect.centery + 30, 20, 20)


        # Draw Buttons
        if self.selected == 1:
            self.dot_color = gs.red
        elif self.selected == 2:
            self.line_color = gs.red
        elif self.selected == 3:
            self.mline_color = gs.red
        elif self.selected == 4:
            self.dot_color = gs.black
            self.line_color = gs.black
            self.mline_color = gs.black
            self.clear_color = gs.black
            print(self.dots)
            self.selected = None
            self.dots = []

        pygame.draw.rect(screen, self.dot_color, self.cp_button1)
        pygame.draw.rect(screen, self.line_color, self.cp_button2)
        pygame.draw.rect(screen, self.mline_color, self.cp_button3)
        pygame.draw.rect(screen, self.clear_color, self.cp_button4)




    def draw_dots(self, gs, screen):
        # Draws dots to the screen until Clear is pressed
        for dot in self.dots:
            if self.dots.index(dot) > 0:
                pygame.draw.circle(screen, gs.red, dot, 5)

        #pygame.display.update()

    def draw_line(self, gs, screen, event):
        # Draws lines to the screen until Clear is pressed
        pass

    def draw_mline(self, gs, screen, event):
        # Draws multi-lines to the screen until Clear is pressed
        # Double click stops the lines
        pass



    def check_clicked_setting(self, gs, screen, event):
        # Choose which setting in control panel required
        if self.cp_button1.collidepoint(event.pos):
            self.selected = 1
        elif self.cp_button2.collidepoint(event.pos):
            self.selected = 2
        elif self.cp_button3.collidepoint(event.pos):
            self.selected = 3
        elif self.cp_button4.collidepoint(event.pos):
            self.selected = 4


