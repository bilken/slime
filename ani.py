#!/usr/bin/python

import pygame, sys, json, math
from pygame.locals import *
from random import randint

if len(sys.argv) != 3:
    print 'Missing arguments: yourImage.png yourAnimation.ani'
    exit(1)

imgName = sys.argv[1]
aniName = sys.argv[2]

pygame.init()

screenw = 640
screenh = 480
screen = pygame.display.set_mode((screenw, screenh))
pygame.display.set_caption("ani")

img = pygame.image.load(imgName).convert_alpha()
ani = json.load(open(aniName))
print ani

iw = img.get_width()
ih = img.get_height()
print 'Item size (%u, %u)' % (iw, ih)

clock = pygame.time.Clock()

sx = ani['base']['x']
sy = ani['base']['y']

ex = ani['tip']['x']
ey = ani['tip']['y']

i = len(ani['sequence'])

r = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if i >= len(ani['sequence']):
        i = 0

    #action = ani['sequence'][i]
    #r += math.degrees(math.atan2(dy, dx))

    r = r + 5

    screen.fill((50,50,50))

    brw = 2 * sx
    brx = 0
    if brw < iw:
        brw = 2 * ((iw / 2) - sx)
        brx = brw / 2 + sx
    brh = 2 * sy
    bry = 0
    if brh < ih:
        brh = 2 * ((ih / 2) - sy)
        bry = brh / 2 + sy
    br = pygame.Surface((brw, brh)).convert_alpha()
    br.fill((0,0,0,0))
    br.blit(img, (brx, bry))

    brmx = brw / 2
    brmy = brh / 2

    center = [screenw / 2, screenh / 2]

    rimg = pygame.transform.rotate(br, r)
    rect = rimg.get_rect()
    rect.center = center

    screen.blit(rimg, rect)

    pygame.draw.rect(screen, (200, 200, 200), (screenw / 2 - 4, screenh / 2 - 4, 8, 8))

    pygame.display.flip()

    clock.tick(30)

    i = i + 1

pygame.quit ()

