#!/usr/bin/python

# JK 12.3.2025

import ROOT

import sys, os

# see $PYTHONPATH

from mystyle import *

#########################################################
#from dose_tools import *
# timepix chip:
# chip size [cm]
d=1.4
# chip height: [cm]!
# timepix MX-10
h_mx10 = 0.03
# Advacam MiniPix
h_advacam = 0.05
rho = 2.3296 


#########################################################

# expects keV and seconds
def GetDose(h, etot, time): #mGy/y
    # Volume:
    V = d*d*h
    # Silicon: g/cm^3
    # mass in kg:
    mass = 0.001*V*rho
    elCh = 1.602e-19
    secInY = 31557600.

    dose = etot*1e3/mass*elCh*1000.  # Jouls/kg = mGy!;-)
    rate_perannum = dose / time*secInY
    return rate_perannum

from numpy import random
# see $PYTHONPATH
from mystyle import *

from math import sqrt, pow, log, exp, factorial, sin, cos

cans = []
stuff = []




#########################################################
def main(argv):
    if len(argv) < 2:
        print(f'Usage: {argv[0]} file.root')
        return
    
    fname = argv[1]
    rfile = ROOT.TFile(fname, 'read')
    histo = rfile.Get('histo')

    SetDarkStyle()
    ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)

    histo.SetStats(0)
    I = histo.Integral()

    time = -1
    tag = ''
    
    # Advacam:
    cpath = os.getcwd()
    h = -1
    camera = ''
    times = {'PrgGva20250310_10s': 458*10,
             'WarsawaTokyoOct2024': 241 * 30,
             'TokyoWarsawaOct2024': 260*30,
             }
    for dtag in times:
        if dtag in cpath:
            time = times[dtag]
            h = h_advacam
            camera = 'Advacam'
            tag = dtag + ''
    
    # MX-10:
    times = {'MucPekSept2019': 370*30,
             'PekVieSept2019': 420*30,
             'LetNY_400x30s': 400*30,
             'LetNY_333x30s': 333*30,
             }

    for dtag in times:
        if dtag in cpath:
            time = times[dtag]
            h = h_mx10
            camera = 'MX-10'
            tag = dtag + ''
    
    d = GetDose(h, I, time)

    prenom = ''
    if len(tag) > 0:
        prenom += tag + '_'
    if len(camera) > 0:
        prenom += camera + '_'

    cname = 'plot_' + prenom + fname.split('/')[-1].replace('.root','')
    can = ROOT.TCanvas(cname, cname, 0, 0, 1100, 1000)


    if time > 0 and h > 0:
        histo.SetTitle(camera + ' E={:1.0f} MeV, t={:1.0f} min, d={:1.1f} mGy/Y;;;E [keV]'.format(I/1000., time/60.,d))
    else:
        histo.SetTitle('E={:1.0f} MeV;;;E [keV]'.format(I/1000.))
                
    histo.Draw('colz')
    ROOT.gPad.SetRightMargin(0.15)
    makeWhiteAxes(histo)

    cans.append(can)
    for can in cans:
        ROOT.gPad.SetLogz(0)
        can.Print(can.GetName() + '_liny.pdf')
        can.Print(can.GetName() + '_liny.png')
        ROOT.gPad.SetLogz(1)
        can.Print(can.GetName() + '_logy.pdf')
        can.Print(can.GetName() + '_logy.png')
        ROOT.gPad.Update()

    ROOT.gApplication.Run()
    return

#########################################################
#########################################################
#########################################################

if __name__ == "__main__":
    main(sys.argv)

    #########################################################
#########################################################
#########################################################
