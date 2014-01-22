#!/usr/bin/python

import pygame, sys, math, operator
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
action = None

if len(sys.argv) == 2:
    attack = sys.argv[1]

a = Animations(aFile)
myform = a.forms['homonid']
myset = a.sets['nude']

def imageChain(myform, myset, currentForm, tip, angleOffset):
    o = None
    l = list()
    if currentForm in myset:
        o = myset[currentForm]
        if action:
            a.begin(o, currentForm, action)
        rimg = a.get(o, angleOffset)
        rect = rimg.get_rect()
        rect.center = tip
        zorder = 0
        if currentForm in myform:
            zorder = myform[currentForm]['z']

        if angleOffset == 0 and a.angle(o) == 0:
            r = a.rect(o).copy()
            r.x = rect.x + r.x
            r.y = rect.y + r.y
            l.append({"n":currentForm, "i":rimg, "r":rect, "z":zorder, "o":r})
        else:
            l.append({"n":currentForm, "i":rimg, "r":rect, "z":zorder})


    if currentForm not in myform:
        print 'no %s' % (currentForm)
        return l

    for v in myform[currentForm]['n']:
        newTip = tip
        newOffset = angleOffset
        if o != None:
            newTip = tuple(map(operator.add, tip, a.tip(o, v, angleOffset)))
            newOffset = angleOffset + a.angle(o)
        l = l + imageChain(myform, myset, v, newTip, newOffset)

    return l

x = 0
y = 0
yoff = 0
left = False
running = True
while running:
    mousePos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = event.pos

    keys = pygame.key.get_pressed()
    if keys[pygame.K_l]:
        left = True
        x -= 5
    if keys[pygame.K_j]:
        left = False
        x += 5
    if keys[pygame.K_SPACE]:
        if y == 0:
            yoff = 1
    if keys[pygame.K_a]:
        action = 'strike'
    if keys[pygame.K_s]:
        action = 'dive'

    if yoff:
        y = yoff * yoff - 25 * yoff + 10
        yoff = yoff + 1
        if y > 0:
            y = 0
            yoff = 0

    screen.fill((50,50,50))

    spacing = 50
    offset = x % spacing
    for w in range(offset, screenw, spacing):
        pygame.draw.line(screen, (0,0,0), (w, 0), (w, screenh))
    floor = screenh * 3 / 4
    pygame.draw.line(screen, (0,0,0), (0, floor), (screenw, floor))

    tip = [screenw / 2, floor + y]
    angleOffset = 0

    images = imageChain(myform, myset, 'base', tip, angleOffset)
    for i in sorted(images, key=lambda d: d["z"]):
        screen.blit(i["i"], i["r"])
        if 'o' in i:
            pygame.draw.rect(screen, (255,0,0), i['o'], 1)

    if mousePos:
        mx, my = mousePos
        for i in images:
            if 'o' in i and i['o'].collidepoint(mx, my):
                print i['n']

    action = None

    pygame.display.flip()

    clock.tick(30)

pygame.quit()

