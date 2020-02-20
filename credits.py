import pygame


credits_music = pygame.mixer.Sound('sounds/credits.wav') # todo change to credits.wav

def credits_menu(gs):
    gs.won_game = True
    pygame.mixer.Sound.play(credits_music, 1)