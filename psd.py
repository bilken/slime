#!/usr/bin/python

import sys, json, os, re
from psd_tools import PSDImage

f = ''
expath = ''
prefix = ''

if len(sys.argv) >= 2:
    f = sys.argv[1]
if len(sys.argv) >= 3:
    expath = sys.argv[2]
if len(sys.argv) >= 4:
    prefix = sys.argv[3]
else:
    prefix = os.path.basename(expath)

err = 0
if not os.path.exists(f):
    print 'Missing input file'
    err = -1

if not os.path.isdir(expath):
    print 'Missing output path'
    err = -1

if err:
    print 'Read in a psd and generate png game assets and json'
    print '  %s input.psd output/path [setPrefix]' % (sys.argv[0])
    exit(-1)

psd = PSDImage.load(f)
for l in psd.layers:
    i = l.as_PIL()
    #i.save(l.name + '.png')

    print l
    m = re.match('(\d+)x(\d+)', l.size)
    print prefix, l.name, m

