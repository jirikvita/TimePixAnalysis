#!/usr/bin/python

import ROOT

import sys, os

#from dose_tools import *
# timepix chip:
# chip size [cm]
d=1.4
# chip height: [cm]!
# timepix MX-10
#h = 0.03
# Advacam MiniPix
h = 0.05

# Volume:
V = d*d*h
# Silicon: g/cm^3
rho = 2.3296 
# mass in kg:
mass = 0.001*V*rho
elCh = 1.602e-19
secInY = 31557600.

# expects keV and seconds
def GetDose(etot, time): #mGy/y
    dose = etot*1e3/mass*elCh*1000.  # Jouls/kg = mGy!;-)
    rate_perannum = dose / time*secInY
    return rate_perannum

from numpy import random
# see $PYTHONPATH
from mystyle import *

from math import sqrt, pow, log, exp, factorial, sin, cos

cans = []
stuff = []

# see $PYTHONPATH


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

    time = -1
    
    # PrgGva20250310_10s
    #time = 458*10

    # WarsawaTokyoOct2024
    #time = 241 * 30

    # TokyoWarsawaOct2024
    #time = 260*30
    
    d = GetDose(I, time)

    if time > 0:
        h.SetTitle('E={:1.0f} MeV d={:1.1f} mGy/Y;;;E [keV]'.format(I/1000., d))
    else:
        h.SetTitle('E={:1.0f} MeV;;;E [keV]'.format(I/1000.))
                
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
