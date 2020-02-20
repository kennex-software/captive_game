import pygame


credits_music = pygame.mixer.Sound('sounds/credits.wav')

def credits_menu():
    pygame.mixer.Sound.play(credits_music, 1)