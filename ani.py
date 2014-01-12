#!/usr/bin/python

import pygame, sys, json, math, operator
from pygame.locals import *
from random import randint

from Slime import Animation

alist = [] # chained animations

pygame.init()

screenw = 640
screenh = 480
screen = pygame.display.set_mode((screenw, screenh))
pygame.display.set_caption("ani")

clock = pygame.time.Clock()

for i in range(1, len(sys.argv), 2):
    alist.append(Animation(sys.argv[i], sys.argv[i + 1]))

if len(alist) == 0:
    print 'Missing animations: yourImage.png yourAnimation.ani [next.png next.ani ...]'
    exit(1)


r = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    r = r + 5

    screen.fill((50,50,50))

    start = [screenw / 2, screenh / 2]
    tr = r
    for a in alist:
        rimg = a.rotate(tr)
        rect = rimg.get_rect()
        rect.center = start
        screen.blit(rimg, rect)
        start = tuple(map(operator.add, start, a.tip(tr)))
        tr = -2 * tr

    pygame.display.flip()

    clock.tick(30)

pygame.quit ()

