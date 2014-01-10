#!/usr/bin/python

import pygame, sys, json
from pygame.locals import *
from random import randint

# ani format
#   "start": {"x":0, "y":0},
#   "end":  {"x":100, "y":10},
#   "axis": {"x":0, "y":0},

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

bg = pygame.image.load("pic/bg.png")
img = pygame.image.load(imgName)#.convert()
#ani = json.load(open(aniName))
ani = json.load(open(aniName))
print ani

iw = img.get_width()
ih = img.get_height()
print 'Item size (%u, %u)' % (iw, ih)

clock = pygame.time.Clock()

x = (screenw - iw) / 2
y = (screenh - ih) / 2
r = 0

i = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if i >= len(ani['sequence']):
        i = 0
        x = (screenw - iw) / 2
        y = (screenh - ih) / 2
        r = 0

    #screen.fill((0,0,0))
    screen.blit(bg, [0,0])
    if r != 0:
        nimg = pygame.transform.rotate(img, r)
        screen.blit(nimg, [x, y])
    else:
        screen.blit(img, [x, y])
    pygame.display.flip()

    clock.tick(2)

    action = ani['sequence'][i]
    x += action['dx']
    y += action['dy']
    r += action['dr']

    i = i + 1

pygame.quit ()

