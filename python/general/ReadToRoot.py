#!/usr/bin/python

# jiri kvita, june 2015, i/o 8th Feb 2026

import os, sys

import ROOT

#####################################################

def readToRoot(fname):


    infile = open(fname, 'r')

    basename = fname.replace('.txt', '')
    rname = fname.replace('.txt', '.root')

    rfile = ROOT.TFile(rname, 'recreate')
    nx = 256
    ny = 256
    #histo = ROOT.TH2D(basename, basename, nx, 0, nx, ny, 0, ny)
    histo = ROOT.TH2D("histo", "histo", nx, 0, nx, ny, 0, ny)

    i = 0
    etot = 0.
    for line in infile.readlines():
        elements = line.split()
        j = 0
        for element in elements:
            epix = float(element)
            histo.SetBinContent(j+1, i+1, epix)
            etot += epix
            j=j+1
        i=i+1

    #print('Writing histogram to %s' % (rname,))

    rfile.Write()
    rfile.Close()
    return rname, etot

#####################################################
#####################################################
#####################################################

if __name__ == "__main__":
    args = sys.argv
    print(args)

    if len (args) < 2:
        print('Usage %s file.txt' %(args[0],))
        exit(1)

    readlines(args[1])


#####################################################
