#! python 3
# kennex
# 

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

def _textureDeleter( textureID ):
    """Create function to clean up the texture on deletion"""
    def cleanup( ref ):
        if glDeleteTextures:
            glDeleteTextures([textureID])
    return cleanup

class Texture():
    """Holder for an OpenGL compiled texture

    This object holds onto a texture until it
    is deleted.  Provides methods for storing
    raw data or PIL images (store and fromPIL
    respectively)

    Attributes:
        components -- number of components in the image,
            if 0, then there is no currently stored image
        texture -- OpenGL textureID as returned by a call
            to glGenTextures(1), will be freed when the
            Texture object is deleted
        format -- GL_RGB/GL_RGBA/GL_LUMINANCE
    """
    def __init__(self):
        """Initialise the texture, if image is not None, store it"""

        self.texture = glGenTextures(1)
        self.cleanup = _textureDeleter(self.texture)

    def store(self, width, height, image):
        """define the texture's parameters...
            components -- number of components (3 or 4 for
                RGB and RGBA respectively)
            format -- GL_RGB, GL_RGBA, GL_LUMINANCE
            x,y -- dimensions of the image
            image -- string, data in raw (unencoded) format

        See:
            glBindTexture, glPixelStorei, glTexImage2D
        """
        # make our ID current
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        # copy the texture into the current texture ID
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)


    def __call__( self ):
        """Enable and select the texture...
        See:
            glBindTexture, glEnable(GL_TEXTURE_2D)
        """
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glEnable(GL_TEXTURE_2D)

    #__enter__ = __call__
    def __exit__( self, typ, val, tb ):
        """Disable for context-manager behaviour"""
        glDisable(GL_TEXTURE_2D)

    def update(self, width, height, image):
        """Update the texture with new data"""
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glBindTexture(GL_TEXTURE_2D, self.texture)
        #glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        # copy the texture into the current texture ID
        #glPixelStorei(GL_PACK_ALIGNMENT,1)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, image)

        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        glBindTexture(GL_TEXTURE_2D, self.texture)


        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(-1, 1)
        glTexCoord2f(0, 1); glVertex2f(-1, -1)
        glTexCoord2f(1, 1); glVertex2f(1, -1)
        glTexCoord2f(1, 0); glVertex2f(1, 1)
        glEnd()

    def screen_to_string(self, screen_to_convert):
        return pygame.image.tostring(screen_to_convert, 'RGB')
