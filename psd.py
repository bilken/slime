#!/usr/bin/python

import sys, json, os, re
from psd_tools import PSDImage

psdName = ''
expath = ''
prefix = ''

if len(sys.argv) >= 2:
    psdName = sys.argv[1]
if len(sys.argv) >= 3:
    expath = sys.argv[2]

err = 0
if not os.path.exists(psdName):
    print 'Missing input file'
    err = -1

if not os.path.isdir(expath):
    os.makedirs(expath)

if not os.path.isdir(expath):
    print 'Missing output path'
    err = -1

if err:
    print 'Read in a psd and generate png game assets and json'
    print '  %s input.psd output/path' % (sys.argv[0])
    exit(-1)


psd = PSDImage.load(psdName)

prefix = os.path.basename(expath)

assName = '%s/%s.set' % (expath, prefix)
f = open( assName, 'w' )

print 'Writing items to %s' % (assName)

f.write( '{\n' )
f.write( '"name":"%s",\n' % (prefix) )
f.write( '"width":%d,\n' % (psd.bbox.x2 - psd.bbox.x1) )
f.write( '"height":%d,\n' % (psd.bbox.y2 - psd.bbox.y1) )
f.write( '"items":{\n' )
z = 0
for l in psd.layers:
    fname = l.name + '.png'
    ffname = '%s/%s' % (expath, fname)
    print '  Creating %s' % (ffname)
    i = l.as_PIL()
    i.save(ffname)
    #print l
    f.write( '  "%s":{"file":"%s", "x":%d, "y":%d, "z":%d},\n' % \
        (l.name, fname, l.bbox.x1 - psd.bbox.x1, l.bbox.y1 - psd.bbox.y1, z) )
    z = z + 1
f.write( '  "nope":{"z":50}\n' )
f.write( '}}\n' )

f.close()

print 'Done'

