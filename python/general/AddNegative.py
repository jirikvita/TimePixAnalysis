#!/usr/bin/python

import os, sys
from ROOT import *
from ProcessTools import *

# STEERING:
#path='ToSort/GammaAm241AlfaZdroj510s10kGamma'
#path='ToSort/Am241Gamma36s'
#path='ToSort/GammaForPoisson1kFrames'
fname='ToSort/gammaShell11071s.root'

opt='read'
#opt='append'
rfile = TFile(fname, opt)

hist0 = rfile.Get('histo')
hist0.SetStats(0)

hist=RemoveSpikes(hist0)
#ehist=hist0

neg = MakeNegative(hist)

smeared = MakeSmeared(hist, 2)
negsmear = MakeNegative(smeared)

smeared2 = MakeSmeared(hist, 4)
negsmear2 = MakeNegative(smeared2)


###################
# draw:

tag=fname.replace('.root', '').replace('/', '_')
canname = 'Negative' + tag
canname = canname.replace('/', '_')
can = TCanvas(canname, canname, 0, 0, 1350, 1200)
can.Divide(2,3)

#opt='lego2'
opt='colz'

can.cd(1)
gPad.SetLogz(1)
hist.Draw(opt)

can.cd(2)
#gPad.SetLogz(1)
neg.Draw(opt)

#opt='lego2'
can.cd(3)
#gPad.SetLogz(1)
smeared.Draw(opt)

can.cd(4)
#gPad.SetLogz(1)
negsmear.Draw(opt)


#opt='lego2'
can.cd(5)
#gPad.SetLogz(1)
smeared2.Draw(opt)

can.cd(6)
#gPad.SetLogz(1)
negsmear2.Draw(opt)

can.Print(canname + '.png')
can.Print(canname + '.eps')
can.Print(canname + '.C')

ROOT.gApplication.Run()
