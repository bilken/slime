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
spath = os.path.dirname(sys.argv[1])

pygame.init()

screenw = 640
screenh = 480
screen = pygame.display.set_mode((screenw, screenh))
pygame.display.set_caption('edit %s' % (name))

clock = pygame.time.Clock()

items = s['items']
for k in items:
    items[k]['pins'] = {}

# from http://www.nerdparadise.com/tech/python/pygame/blitopacity/
def blit_alpha(surf, img, xy, alpha):
    x, y = xy
    tmp = pygame.Surface((img.get_width(), img.get_height())).convert()
    tmp.blit(surf, (-x, -y))
    tmp.blit(img, (0, 0))
    tmp.set_alpha(alpha)
    surf.blit(tmp, xy)

def redraw():
    screen.fill((100,100,100, 255))

    x = (screenw  - w * 2) / 2
    y = (screenh - h * 2) / 2

    vislist = []
    #for k,v in sorted(items.items(), key=lambda x: x[1]['z'], reverse=True):
    for k in items:
        v = items[k]
        if 'file' not in v:
            continue
        fname = '%s/%s' % (spath, v['file'])
        if not os.path.isfile(fname):
            fname = v['file']
        img = pygame.image.load(fname)
        ix = v['x'] * 2
        iy = v['y'] * 2
        i2 = pygame.transform.scale2x(img).convert_alpha()
        blit_alpha(screen, i2, (x + ix, y + iy), 100)
        r = Rect(x + ix, y + iy, i2.get_width(), i2.get_height())
        pygame.draw.rect(screen, (255,0,0), r, 1)
        vislist.append((k, r))

        for nk,p in v['pins'].items():
            px = x + ix + p['x'] * 2
            py = y + iy + p['y'] * 2
            pygame.draw.circle(screen, (0, 0, 255), (px, py), 4)
            pygame.draw.circle(screen, (255, 255, 255), (px, py), 1)

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
            coll = []
            for k, r in vislist:
                if r.collidepoint(x, y):
                    coll.append((k, r))

            if len(coll) == 1 or len(coll) == 2:
                a, ar = coll[0]
                b, br = 'tip', 0
                if len(coll) == 2:
                    b, br = coll[1]
                px = (x - ar.x) / 2
                py = (y - ar.y) / 2
                items[a]['pins'][b] = {'x':px, 'y':py}
                print 'pin %s to %s' % (a, b)
                if len(coll) == 2:
                    px = (x - br.x) / 2
                    py = (y - br.y) / 2
                    items[b]['pins'][a] = {'x':px, 'y':py}
                changed = True


    if changed:
        vislist = redraw()
        changed = False

    clock.tick(30)

pygame.quit()

