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
item = 'nudeTorso'

if len(sys.argv) == 2:
    item = sys.argv[1]

a = Animations(aFile)

r = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50,50,50))

    tip = [screenw / 2, screenh / 2]

    rimg = a.get(item, r)

    rect = rimg.get_rect()
    rect.center = tip

    screen.blit(rimg, rect)

    pygame.draw.rect(screen, (255,255,255,0), (screenw/2-2, screenh/2-2, 4, 4))

    r += 5

    pygame.display.flip()

    clock.tick(20)

pygame.quit()

