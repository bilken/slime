#!/usr/bin/python

import pygame, sys, os, json, math, operator
from pygame.locals import *

if len(sys.argv) < 2:
    print 'Usage: ass/path/path.set formName'
    exit(-1)


s = json.load(open(sys.argv[1]))
formName = sys.argv[2]

f = json.load(open('ass/forms.json'))
if formName not in f['forms']:
    print 'Unknown form, %s' % (formName)
    exit(-1)

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

form = f['forms'][formName]
items = s['items']
imgs = {}
rects = {}
rot = {}
for k in items:
    v = items[k]
    v['pins'] = {}
    if k not in form:
        print 'Form "%s" does not have a "%s"' % (formName, k)
    if 'file' not in v:
        imgs[k] = None
        continue
    fname = '%s/%s' % (spath, v['file'])
    if not os.path.isfile(fname):
        fname = v['file']
    imgs[k] = pygame.image.load(fname)
    rects[k] = Rect(v['x'], v['y'], imgs[k].get_width(), imgs[k].get_height())
    rot[k] = 0

def SetPins(k):
    if 'n' not in form[k]:
        next
    for nk in form[k]['n']:
        c1 = rects[k].center
        c2 = rects[k].center
        if nk in rects:
            c2 = rects[nk].center
        mx = (c1[0] + c2[0]) / 2
        my = (c1[1] + c2[1]) / 2
        items[k]['pins'][nk] = {'x':mx - rects[k].x, 'y':my - rects[k].y}
        if nk in rects:
            items[nk]['pins'][k] = {'x':mx - rects[nk].x, 'y':my - rects[nk].y}
            SetPins(nk)
        else:
            items[k]['pins']['tip'] = {'x':mx , 'y':my}

for bn in form['base']['n']:
    SetPins(bn)

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
        img = imgs[k]
        if not img:
            continue

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
selected = None
vislist = []
while running:
    mpos = None
    bkey = False
    bshift = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        bshift = pygame.key.get_mods() & KMOD_SHIFT
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = event.pos
        if event.type == pygame.KEYDOWN:
            bkey = True

    if mpos:
        x, y = mpos
        coll = []
        for k, r in vislist:
            if r.collidepoint(x, y):
                coll.append((k, r))

        if not bshift:
            if len(coll) == 1:
                selected, sr = coll[0]
                print 'Selected %s' % (selected)
                changed = True
        elif len(coll) == 1 or len(coll) == 2:
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

    if bkey:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            selected = None
            for k in rot:
                rot[k] = 0
            changed = True
            print 'Nothing selected'
        if keys[pygame.K_r]:
            if selected:
                rot[selected] = rot[selected] + 5
                changed = True
                print 'Rotating %s to %d' % (selected, rot[selected])

    if changed:
        vislist = redraw()
        changed = False

    clock.tick(30)

pygame.quit()

