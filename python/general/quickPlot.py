#!/usr/bin/python

import ROOT

import sys, os

from numpy import random
# see $PYTHONPATH
from mystyle import *

from math import sqrt, pow, log, exp, factorial, sin, cos

cans = []
stuff = []

# see $PYTHONPATH

from dose_tools import *

from mystyle import *


def main(argv):
    if len(argv) < 2:
        print(f'Usage: {argv[0]} file.root')
        return
    
    fname = argv[1]
    rfile = ROOT.TFile(fname, 'read')
    h = rfile.Get('histo')

    SetDarkStyle()
    ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)

    cname = 'plot_' + fname.split('/')[-1].replace('.root','')
    can = ROOT.TCanvas(cname, cname, 0, 0, 1100, 1000)
    h.SetStats(0)
    I = h.Integral()
    time = 458*10
    d = GetDose(I, time)
    
    h.SetTitle('E={:1.0f} MeV d={} mGy/Y;;;E [keV]'.format(I/1000., d))
    h.Draw('colz')
    ROOT.gPad.SetLogz(1)
    ROOT.gPad.SetRightMargin(0.15)
    makeWhiteAxes(h)

    cans.append(can)
    for can in cans:
        can.Print(can.GetName() + '.pdf')
        can.Print(can.GetName() + '.png')
        ROOT.gPad.Update()

    ROOT.gApplication.Run()
    return



if __name__ == "__main__":
    main(sys.argv)
