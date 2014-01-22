#!/usr/bin/python

import pygame, sys, os, json, math, operator
from pygame.locals import *

if len(sys.argv) < 2:
    print 'Usage: ass/path/path.set formName'
    exit(-1)


s = json.load(open(sys.argv[1]))
formName = sys.argv[2]

f = json.load(open('ass/forms.json'))

w = s['width']
h = s['height']
name = s['name']
spath = os.path.basename(sys.argv[1])

pygame.init()

screenw = 640
screenh = 480
screen = pygame.display.set_mode((screenw, screenh))
pygame.display.set_caption('edit %s' % (name))

clock = pygame.time.Clock()

def redraw():
    screen.fill((50,50,50))

    x = (screenw  - w * 2) / 2
    y = (screenh - h * 2) / 2

    vislist = []
    for k,v in sorted(s['items'].items(), key=lambda x: x[1]['z'], reverse=True):
        print v
        #v = s['items'][k]
        if 'file' not in v:
            continue
        fname = '%s/%s' % (spath, v['file'])
        if not os.path.isfile(fname):
            fname = v['file']
        img = pygame.image.load(fname).convert_alpha()
        ix = v['x'] * 2
        iy = v['y'] * 2
        i2 = pygame.transform.scale2x(img)
        screen.blit(i2, (x + ix, y + iy))
        r = Rect(x + ix, y + iy, i2.get_width(), i2.get_height())
        pygame.draw.rect(screen, (255,0,0), r, 1)
        vislist.append((v, r))

    pygame.display.flip()

    return vislist

changed = True
running = True
vislist = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for v, r in vislist:
                if r.collidepoint(x, y):
                    print v['name']

    if changed:
        vislist = redraw()
        changed = False

    clock.tick(30)

pygame.quit()

