import pygame

class Menu():
    def __init__(self, gs, screen):
        self.gs = gs
        self.screen = screen

    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

