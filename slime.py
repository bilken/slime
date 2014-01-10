#!/usr/bin/python

import pygame, sys
from pygame.locals import *
from random import randint

pygame.init()

bg = pygame.image.load("pic/bg.png")
sizex = bg.get_width()
sizey = bg.get_height()

screen = pygame.display.set_mode((sizex, sizey))
pygame.display.set_caption("slime")

clock = pygame.time.Clock()

black = ( 0, 0, 0)

player = pygame.image.load('pic/player.png')
x = 0
y = 0

ground = pygame.image.load('pic/ground.png')

actionBar = pygame.image.load('pic/actionbar.png')
awidth = actionBar.get_width()
aheight = actionBar.get_height()
ax = (sizex - awidth) / 2
ay = sizey - (3 * aheight / 2)

hp = pygame.image.load('pic/fullHP.png')
hpx = ax + (awidth / 2) - (hp.get_width() / 2)
hpy = ay

mp = pygame.image.load('pic/fullMP.png')
mpx = ax + (awidth / 2) - (mp.get_width() / 2)
mpy = ay + aheight - mp.get_height()

attack = pygame.image.load('pic/attack.png')
defend = pygame.image.load('pic/defend.png')

def randy(cur, max):
    range = 25
    cur = cur + randint(-range, range)
    while cur < 0 or cur > max:
        cur = cur + randint(0, max)
    return cur

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x = randy(x, sizex)
    y = randy(y, sizey)

    screen.blit(bg, [0,0])
    screen.blit(ground, [0, y + player.get_height() - ground.get_height() / 2])
    screen.blit(player, [x, y])
    screen.blit(actionBar, [ax, ay])
    screen.blit(attack, [ax + 15, ay + 10])
    screen.blit(defend, [ax + 100, ay + 10])
    screen.blit(hp, [hpx, hpy])
    screen.blit(mp, [mpx, mpy])
    pygame.display.flip()

    clock.tick(10)

pygame.quit ()

