import pygame

pygame.init()
pygame.font.init()
import time


def credits_screen(gs, screen):
    #screen.fill((gs.black))



    game_over_text = gs.arial60.render(str("to be continued..."), True, gs.black)
    fade_surface_alpha = pygame.Surface(game_over_text.get_size(), pygame.SRCALPHA)
    alpha = 0

    #credits_surface = pygame.Surface(game_over_text.get_size(), pygame.SRCALPHA)
    fade(gs, screen, fade_surface_alpha, game_over_text, 2, alpha)
    #screen.blit(game_over_text, (gs.screen_width//2, gs.screen_height//2))

def fade(gs, screen, fs_alpha, text, time, alpha):
    """Function to fade the screen"""

    start_ticks = pygame.time.get_ticks()
    seconds = (pygame.time.get_ticks() - start_ticks)/1000

    screen.fill(gs.white)

    gs.game_started = False
    gs.game_ended = True

    while gs.game_ended:
        if seconds > time:
            if alpha >= 0 and alpha <= 254:
                alpha = max(alpha+2, 0)
                fade_surface = text.copy()
                fs_alpha.fill((0, 0, 0, alpha))
                fade_surface.blit(fs_alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                if alpha >= 254:
                    alpha = 255

            screen.blit(fade_surface, (gs.screen_width//2, gs.screen_height//2))

        pygame.display.flip()
        pygame.time.Clock().tick(60)


def credits_text(gs, screen):
    credits = "This isn't done yet... Going to add these things:" \
              "-Special Thanks to Gnarski" \
              "-"
    credits = mt.multiline_text(credits, 210, gs.cambria22)
    text_height = gs.cambria22.get_height()

    line_spacing = 200

    for line in credits:
        text_image = gs.cambria22.render(line, True, gs.black)
        screen.blit(text_image, (465, line_spacing))
        line_spacing += text_height





