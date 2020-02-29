import pygame

pygame.init()
pygame.font.init()



def credits_screen(gs, screen):
    #screen.fill((gs.black))

    #fade(gs, screen, gs.screen_width, gs.screen_height)
    screen.fill(gs.black)
    game_over_text = gs.arial60.render(str('game over...'), True, gs.white)
    screen.blit(game_over_text, (gs.screen_width//2, gs.screen_height//2))

def fade(gs, screen, width, height):
    fade = pygame.Surface((width, height))
    fade.fill((gs.black))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        #pygame.time.delay(100)

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





