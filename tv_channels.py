# TV Channels
# Channel 1 | Whitespace todo figure out how to create perlin noise for TV screens (maybe with import noise function)???
# Channel 2 | Whitespace todo will flash a specific color which will be needed in the game, maybe every 9 seconds or so
# Channel 3 | Color Flash todo figure out how to create perlin noise for TV screens (maybe with import noise function)???
# Channel 4 | Camera 1 todo make this a view of Camera 1 (always plugged in)
# Channel 5 | Camera 2 todo make this a view of Camera 2, if plugged in... if not, show whitespace (see channel 1)
# Channel 6 | Camera 3 todo make this a view of Camera 3 (always plugged in) make this camera the least important, but maybe a view of inside the room
# Channel 7 | # todo figure out what to make channel
# Channel 8 | Whitespace todo figure out how to create perlin noise for TV screens (maybe with import noise function)???
# Channel 9 | # todo figure out what to make channel

import pygame
import numpy as np

x = np.arange(0, 300)
y = np.arange(0, 300)
X, Y = np.meshgrid(x, y)
Z = X + Y
Z = 255*Z/Z.max()
surf = pygame.surfarray.make_surface(Z)
screen.blit(surf, (0, 0))


"""
def gray(im):
    im = 255 * (im / im.max())
    w, h = im.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 2] = ret[:, :, 1] = ret[:, :, 0] = im
    return ret

pygame.init()
display = pygame.display.set_mode((350, 350))
x = np.arange(0, 300)
y = np.arange(0, 300)
X, Y = np.meshgrid(x, y)
Z = X + Y
Z = 255 * Z / Z.max()
Z = gray(Z)
surf = pygame.surfarray.make_surface(Z)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display.blit(surf, (0, 0))
    pygame.display.update()
pygame.quit()
"""

""" 

#Perlin Noise

def perlin(x,y,seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi]+yi],xf,yf)
    n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = gradient(p[p[xi+1]+yi],xf-1,yf)
    # combine noises
    x1 = lerp(n00,n10,u)
    x2 = lerp(n01,n11,u) # FIX1: I was using n10 instead of n01
    return lerp(x1,x2,v) # FIX2: I also had to reverse x1 and x2 here

def lerp(a,b,x):
    "linear interpolation"
    return a + x * (b-a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h,x,y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y

lin = np.linspace(0,5,100,endpoint=False)
x,y = np.meshgrid(lin,lin) # FIX3: I thought I had to invert x and y here but it was a mistake

#plt.imshow(perlin(x,y,seed=100),origin='upper')
#plt.show()
"""