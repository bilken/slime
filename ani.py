#!/usr/bin/python

import pygame, sys, json, math
from pygame.locals import *
from random import randint

from Slime import Animation

if len(sys.argv) != 3:
    print 'Missing arguments: yourImage.png yourAnimation.ani'
    exit(1)

pygame.init()

screenw = 640
screenh = 480
screen = pygame.display.set_mode((screenw, screenh))
pygame.display.set_caption("ani")

clock = pygame.time.Clock()

a = Animation(sys.argv[1], sys.argv[2])

r = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    r = r + 5

    screen.fill((50,50,50))

    center = [screenw / 2, screenh / 2]

    rimg = a.rotate(r)
    rect = rimg.get_rect()
    rect.center = center

    screen.blit(rimg, rect)

    pygame.display.flip()

    clock.tick(30)

pygame.quit ()

