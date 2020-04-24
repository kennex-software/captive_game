#! python 3
# kennex
# 


import pygame
import sys
from OpenGL.GL import *
from pygame.locals import *

# set pygame screen
pygame.init()
pygame.display.set_mode((500, 500), OPENGL | DOUBLEBUF)
pygame.display.init()
info = pygame.display.Info()

#colours
MIDNIGHT = (  15,   0, 100 )
BUTTER   = ( 255, 245, 100 )

# basic opengl configuration
glViewport(0, 0, info.current_w, info.current_h)
glDepthRange(0, 1)
glMatrixMode(GL_PROJECTION)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glShadeModel(GL_SMOOTH)
glClearColor(0.0, 0.0, 0.0, 0.0)
glClearDepth(1.0)
glDisable(GL_DEPTH_TEST)
glDisable(GL_LIGHTING)
glDepthFunc(GL_LEQUAL)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
glEnable(GL_BLEND)


###
### Function to convert a PyGame Surface to an OpenGL Texture
### Maybe it's not necessary to perform each of these operations
### every time.
###
texID = glGenTextures(1)
def surfaceToTexture( pygame_surface ):
    global texID
    rgb_surface = pygame.image.tostring( pygame_surface, 'RGB')
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    surface_rect = pygame_surface.get_rect()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, surface_rect.width, surface_rect.height, 0, GL_RGB, GL_UNSIGNED_BYTE, rgb_surface)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)


# create pygame clock
clock = pygame.time.Clock()

# make an offscreen surface for drawing PyGame to
offscreen_surface = pygame.Surface((info.current_w, info.current_h))
text_font = pygame.font.Font( None, 30 ) # some default font

done = False
while not done:
    # get quit event
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    # Do all the PyGame operations to the offscreen surface
    # So any backgrounds, sprites, etc. will get drawn to the offscreen
    # rather than to the default window/screen.
    offscreen_surface.fill( MIDNIGHT )
    # write some nonsense to put something changing on the screen
    words = text_font.render( "β-Moé-Moé count: "+str( pygame.time.get_ticks() ), True, BUTTER )
    offscreen_surface.blit( words, (50, 250) )


    # prepare to render the texture-mapped rectangle
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glClearColor(0, 0, 0, 1.0)

    # draw texture openGL Texture
    surfaceToTexture( offscreen_surface )
    glBindTexture(GL_TEXTURE_2D, texID)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-1, 1)
    glTexCoord2f(0, 1); glVertex2f(-1, -1)
    glTexCoord2f(1, 1); glVertex2f(1, -1)
    glTexCoord2f(1, 0); glVertex2f(1, 1)
    glEnd()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()