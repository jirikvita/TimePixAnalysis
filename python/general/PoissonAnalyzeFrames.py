#!/usr/bin/python

import os, sys
from ROOT import *
from ProcessTools import *

# STEERING:
#path='ToSort/GammaAm241AlfaZdroj510s10kGamma'
#path='ToSort/Am241Gamma36s'
#path='ToSort/GammaForPoisson1kFrames'
path='ToSort/GammaForPoisson1kFrames_lessIntense'

# subdirectory with frames:
fdir = 'frames'
fullpath = '%s/%s/' % (path,fdir)


# make ROOT files from the txt:
# comment line after HACK in case you've got these already
for fname in os.popen('cd %s ; ls *.txt*???.txt' % (fullpath,) ).read().split():
    print fname
    fullname = '%s%s' % (fullpath,fname)
    cmd = 'cd %s ; python ../../../ReadToRoot.py %s' % (fullpath,fname,)
    ### HACK!!! 
    ###os.system(cmd)

# open individual ROOT files and count number of gammas:
ngamma = []
AllGammas = []
hists = []
files = []


# go through histograms, find gammas, and see how many gammas found in each frame:
# HACK!
terminate = -1
nf = 0
for fname in os.popen('cd %s ; ls *.root' % (fullpath,) ).read().split():
    print fname
    fullname = '%s%s' % (fullpath,fname)
    rfile = TFile(fullname, 'read')
    hist = rfile.Get('histo')
    hist.SetName('%s_%i' % (hist.GetName(), nf))
    gammas = GetGammas(hist)
    ng  = len(gammas)
    
    if nf == 0:
        hists.append(hist)
        ghlist.append(hist)
        files.append(rfile)
    ngamma.append(ng)
    AllGammas.append(gammas)
    if nf > 0:
        rfile.Close()

    if terminate > 0 and nf > terminate:
        break
    nf = nf + 1

# fill the histogram of how many gammas found in each frame:
nmax = max(ngamma)+1
nmin = min(ngamma)
nbins = nmax - nmin
print nbins,nmin,nmax,1.*(1.*nmax-nmin)/(1.*nbins)
name = 'GammaCounts'
title = 'Gamma Counts;n_{#gamma};frequency'
pois = TH1D(name, title, nbins, nmin-0.5, nmax-0.5)
print ngamma
for ng in ngamma:
    pois.Fill(ng)

###################
# draw:

canname = 'PoissonTest' + path
canname = canname.replace('/', '_')
can = TCanvas(canname, canname, 0, 0, 1350, 800)
can.Divide(2,1)

can.cd(1)
gPad.SetLogz(1)

# draw first histo as example:
index = 0
hists[index].Draw("colz")
DrawCircleAroundObjects(AllGammas[index])

can.cd(2)
pois.SetMarkerStyle(20)
pois.SetMarkerSize(1)
pois.SetMarkerColor(pois.GetLineColor())
pois.Draw('e1hist')

can.Print(canname + '.png')
can.Print(canname + '.eps')
can.Print(canname + '.C')


