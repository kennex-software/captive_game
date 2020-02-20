import pygame


def credits_screen(gs, screen):
    #screen.fill((gs.black))

    fade(gs, screen, gs.screen_width, gs.screen_height)

def fade(gs, screen, width, height):
    fade = pygame.Surface((width, height))
    fade.fill((gs.black))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(100)





