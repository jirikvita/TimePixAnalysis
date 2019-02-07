#!/usr/bin/python

# jiri kvita, june 2015

import os, sys

import ROOT

args = sys.argv
print args

if len (args) < 2:
    print 'Usage %s file.txt' %(args[0],)
    exit(1)

fname = args[1]

infile = file(fname, 'r')

basename = fname.replace('.txt', '')
rname = fname.replace('.txt', '.root')

rfile = ROOT.TFile(rname, 'recreate')
nx = 256
ny = 256
#histo = ROOT.TH2D(basename, basename, nx, 0, nx, ny, 0, ny)
histo = ROOT.TH2D("histo", "histo", nx, 0, nx, ny, 0, ny)

i = 0
for line in infile.readlines():
    elements = line.split()
    j = 0
    for element in elements:
        histo.SetBinContent(j+1, i+1, ROOT.Double(element))
        j=j+1
    i=i+1

print 'Writing histogram to %s' % (rname,)

rfile.Write()
rfile.Close()

