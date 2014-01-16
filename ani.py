#!/usr/bin/python

import pygame, sys, json, math, operator
from pygame.locals import *
from random import randint
from time import sleep

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
myset = a.sets['nude']

def drawChain(level, myform, myset, currentForm, tip, angleOffset):
    o = None
    if currentForm in myset:
        o = myset[currentForm]
        if a.done(o):
            a.begin(o, currentForm, attack)
        rimg = a.get(o, angleOffset)
        rect = rimg.get_rect()
        rect.center = tip
        screen.blit(rimg, rect)

    if currentForm not in myform:
        return

    for v in myform[currentForm]:
        newTip = tip
        newOffset = angleOffset
        if o != None:
            newTip = tuple(map(operator.add, tip, a.tip(o, v, angleOffset)))
            newOffset = angleOffset + a.angle(o)
        drawChain(level + 1, myform, myset, v, newTip, newOffset)


r = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50,50,50))

    tip = [screenw / 2, screenh / 2]
    angleOffset = 0

    drawChain(0, myform, myset, 'base', tip, angleOffset)

    pygame.display.flip()

    clock.tick(2)

pygame.quit()

