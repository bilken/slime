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
attack = 'strike'

if len(sys.argv) == 2:
    attack = sys.argv[1]

a = Animations(aFile)
myform = a.forms['homonid']
#myform = a.forms['upper']
myset = a.sets['hero']

def drawChain(myform, myset, currentForm, tip, angleOffset):
    if currentForm not in myform:
        return
    for v in myform[currentForm]:
        o = myset[v]
        if a.done(o):
            a.begin(o, attack)

        rimg = a.get(o, angleOffset)

        rect = rimg.get_rect()
        rect.center = tip

        screen.blit(rimg, rect)

        newTip = tuple(map(operator.add, tip, a.tip(o, angleOffset)))
        newOffset = angleOffset + a.angle(o)

        drawChain(myform, myset, v, newTip, newOffset)


r = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50,50,50))

    tip = [screenw / 2, screenh / 2]
    angleOffset = 0

    drawChain(myform, myset, 'start', tip, angleOffset)

    pygame.display.flip()

    clock.tick(6)

pygame.quit()

