#!/usr/bin/python

import ROOT
from ProcessTools import *


# read
fname = 'ToSort/AllFlights_but6.root'

rfile = ROOT.TFile(fname,'read')
hist = rfile.Get('histo')
hist.SetStats(0);

# process
newhist = RemoveSpikes(hist)
ghlist.append(newhist)

# draw

can = ROOT.TCanvas("process", "process", 0, 0, 1600, 800)
gcans.append(can)
can.Divide(2,1)

ROOT.gStyle.SetPalette(56);
ROOT.gStyle.SetOptTitle(0);


can.cd(1)
ROOT.gPad.SetLogz(1)
hist.Draw("colz")
can.cd(2)
ROOT.gPad.SetLogz(1)
newhist.Draw("colz")

ROOT.gApplication.Run() 
