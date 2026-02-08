#!/usr/bin/python

# JK 12.3.2025

import ROOT
from pathlib import Path
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

    batch=False
    if len(argv) > 2:
        if argv[2] == '-b' or argv[2] == '-B' or argv[2] == '--batch':
            batch = True

    if batch:
        ROOT.gROOT.SetBatch(1)
        
    SetDarkStyle()
    ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)

    histo.SetStats(0)
    I = histo.Integral()

    time = -1
    tag = ''
    
    # Advacam:
    cpath = os.getcwd()
    # default sensor thickness: negative: unknown
    h = -1
    camera = ''
    times = {'PrgGva20250310_10s': 458*10, 'WarsawaTokyoOct2024': 241*30,
             'TokyoWarsawaOct2024': 260*30,
             'Advacam_T9_WCTE2025_muons1': 167*60,
             'Advacam_T9_WCTE2025_muons2': 60*60,
             'Advacam_T9_WCTE2025_muons3': 60*60,
             'Advacam_T9_WCTE2025_muons4': 60*60,
             'Advacam_T9_WCTE2025_muons5': 60*60,
             'Advacam_T9_WCTE2025_muons6': 60*60,
             'Advacam_T9_WCTE2025_muons7': 180*60,
             'Advacam_T9_WCTE2025_muons8': 80*60,
             'Advacam_T9_WCTE2025_muons9': 120*60, 'radsources':
             30*32, 'T9CRbg' : 30*120, 'PrgGva20250411' : 400*15,
             # May/June 2025:
             'prggva20250526_15s' : 300*15,
             'gvaprg20250602' : 324*15,
             # November 2025
             'prggva20251120' : 530*10,
             'gvaprg20251123' : 574*10,
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
             'LetNY_80x30s': 80*30,
             # empty: 'LetNY_60x30s': 60*30,
             'Uglass8h_spect': 8*3600,
             'MX10_T9_WCTE2025_muons1': 90*30,
             'MX10_T9_WCTE2025_muons2': 120*30,
             'MX10_T9_WCTE2025_muons3': 240*30,
             'BgJuly2019_120x600s': 120*600,
             'BananDetailed_54x600s': 54*600,
             }

    for dtag in times:
        if dtag in cpath:
            time = times[dtag]
            h = h_mx10
            camera = 'MX-10'
            tag = dtag + ''

    if time < 0:
        #try to add all times from dsc files
        totalTime = 0.
        print('Will try to extract total time from the dsc files.')
        paths = []
        for path in Path("./").glob("*.txt.dsc"):
            paths.append(path)
        if len(paths) == 0:
            for path in Path("./").glob("*/*.txt.dsc"):
                paths.append(path)
        for path in paths:
            fname = path.name
            print(fname)
            infile = open(fname, 'r')
            dscLines = []
            for xline in infile.readlines():
                dscLines.append(xline[:-1])
            for iline,line in enumerate(dscLines):
                if 'Acq time' in line:
                    # the time in seconds is 2 lines later;-)
                    totalTime += float(dscLines[iline+2])
                if camera == '' and 'MiniPIX' in line:
                    camera = 'Advacam'
                    h = h_advacam
                    print(f'OK, extracted camera type as {camera}')
                if camera == '' and 'MX-10' in line:
                    camera = 'MX-10'
                    h = h_mx10
                    print(f'OK, extracted camera type as {camera}')
        print(f'OK, extracte total time of {totalTime} from the dsc times.')
        time = 1.*totalTime

    # Compute the dose
    d = GetDose(h, I, time)

    prenom = ''
    if len(tag) > 0:
        prenom += tag + '_'
    if len(camera) > 0:
        prenom += camera + '_'

    cname = 'plot_' + prenom + fname.split('/')[-1].replace('.root','')
    can = ROOT.TCanvas(cname, cname, 0, 0, 1100, 1000)


    if time > 0 and h > 0:
        histo.SetTitle(camera + ' E={:1.1f} MeV, t={:1.0f} min, d={:1.2f} mGy/Y;;;E [keV]'.format(I/1000., time/60.,d))
    else:
        histo.SetTitle('E={:1.0f} MeV;;;E [keV]'.format(I/1000.))
                
    histo.Draw('colz')
    ROOT.gPad.SetRightMargin(0.15)
    makeWhiteAxes(histo)

    cans.append(can)
    for can in cans:
        ROOT.gPad.SetLogz(0)
        #can.Print(can.GetName() + '_liny.pdf')
        can.Print(can.GetName() + '_liny.png')
        ROOT.gPad.SetLogz(1)
        #can.Print(can.GetName() + '_logy.pdf')
        can.Print(can.GetName() + '_logy.png')
        ROOT.gPad.Update()

    if not batch:
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
