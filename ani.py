#!/usr/bin/python

import pygame, sys, json, math, operator
from pygame.locals import *
from random import randint

from Slime import Animation, Animations

pygame.init()

screenw = 640
screenh = 480
screen = pygame.display.set_mode((screenw, screenh))
pygame.display.set_caption("ani")

clock = pygame.time.Clock()

aFile = 'Slime.ani'
attack = "strike"

if len(sys.argv) == 2:
    attack = sys.argv[1]

a = Animations(aFile)
order = ["hp", "mp", "sword"]
#order = ["hp"]

r = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50,50,50))

    tip = [screenw / 2, screenh / 2]
    angleOffset = 0

    for o in order:
        if a.done(o):
            a.begin(o, attack)

        rimg = a.get(o, angleOffset)

        rect = rimg.get_rect()
        rect.center = tip

        screen.blit(rimg, rect)
        tip = tuple(map(operator.add, tip, a.tip(o, angleOffset)))
        angleOffset += a.angle(o)

    pygame.display.flip()

    clock.tick(30)

pygame.quit ()

