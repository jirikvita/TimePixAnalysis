#!/usr/bin/python

# jk 2016--2018

import subprocess
import os, sys
from ROOT import *
from ProcessTools import *

gStyle.SetOptTitle(0)
Draw=True

gStyle.SetPalette(1)

pdfdir = './hough_pdf/'
pngdir = './hough_png/'
Cdir = './hough_C/'

os.system('mkdir -p ' + pdfdir)
os.system('mkdir -p ' + pngdir)
os.system('mkdir -p ' + Cdir)

path = 'Spectra/'
Paths = os.popen('cd {} ; ls | grep MuSearch_ '.format(path,)).readlines()

# subdirectory with frames:
fdir = 'root'

Histos = []
Files = []
hists = []
Cans = []

j = 0

canname = 'ThetaDistribution'
thetaCan = TCanvas(canname, canname, 0, 0, 1000, 1000)
Cans.append(thetaCan)


htheta = TH1D('theta', 'theta;#theta;N', 32, 0, pi)
grMulti = TGraph()
grMulti.SetName('Multiplicity')

Nframes = 0

for lpath in Paths:
    path=lpath[:-1]
    fullpath = '{}/{}/'.format(path,fdir)
    
    #for path in Paths[2:2]:

    print '===> Processing path {}'.format(path,)
    print '     fullpath: {}'.format(fullpath,)

    gROOT.SetBatch(1)

    # make ROOT files from the txt:
    #comment line after HACK in case you've got these already
    #mypipe = subprocess.Popen('cd {} ; ls *.txt'.format(fullpath,), stdout=subprocess.PIPE)
    #fnames = mypipe.communicate().split('\n')
    ## for fname in os.popen('cd {:} ; ls *.txt*???.txt'.format(fullpath,) ).read().split():
    #for fname in fnames:
    #    print fname
    #    fullname = '{:}{:}'.format(fullpath,fname)
    #    cmd = 'cd {} ; python ../../../ReadToRoot.py {}'.format(fullpath,fname,)
    #    ### HACK!!! DONE already;) 
    #    #os.system(cmd)

    # go through histograms, find gammas, and see how many gammas found in each frame:
    # HACK!
    nf = -1
    #mypipe = subprocess.Popen('cd {} ; ls *.root | grep -v conflict'.format(fullpath), stdout=subprocess.PIPE)
    #fnames = mypipe.communicate().split('\n')
    #for fname in fnames:
    for fname in os.popen('cd {} ; ls *.root | grep -v conflict'.format(fullpath,) ).read().split():
        nf = nf+1
        # HACK
        #if nf > 6:
        #    break
        #print fname
        fullname = '{}{}'.format(fullpath,fname)
        print 'Opening {}'.format(fullname)
        rfile = TFile(fullname, 'update')
        # rfile = TFile(fullname, 'read')
        Files.append(rfile)
        hist = rfile.Get('histo') 
        
        NnonZero = 1.*GetNnonNegative(hist)
        grMulti.SetPoint(nf, nf, NnonZero)

        if NnonZero > 1000.:
            print 'WARNING: Skipping histo due to high occupancy!'
            continue
        if NnonZero < 100.:
            print 'WARNING: Skipping histo due to low occupancy!'
            continue
        Nframes = Nframes+1

        #hists.append(hist)
        #hist.SetName('{:}_{:}'.format(hist.GetName(), nf))
        #print 'Performing transform of {}'.format(hist.GetName(),)
        rfile.cd()
        
        print 'Trying to get Hough-transformed histo from file...'
        try:
            hough = rfile.Get('histo_hough') 
            n = hough.GetEntries()
            #except:
        except:
            #ReferenceError or AttributeError:
            print '   ...failed, performing the transform now...'
            hough = HoughTransf(hist)
            hough.Write()


        # TODO!
        # get also the lines
        print 'Trying to get the lines list from file...'
        try:
            grTheta = rfile.Get('gr_theta')
            nlines = grTheta.GetN()
            spikeList = MakeListFromGraph(grTheta)
            inv = rfile.Get('histo_hough_inv_hough')
            n = inv.GetEntries()
            #except:
        except:
            #ReferenceError or AttributeError:
            print '   ...failed, performing inverse transform of {}'.format(hough.GetName())
            spikeList,inv = InvHoughTransf(hough)
            nlines = len(spikeList)
            grTheta = MakeGraph(spikeList, 'gr_theta', 0)
            grR = MakeGraph(spikeList, 'gr_r', 1)
            grTheta.Write()
            grR.Write()


        # hists.append(hough)
        # Histos.append([hist,hough,inv, spikeList])

        ###################
        # draw:
        nlines= len(spikeList)
        
        if nlines > 0:
            # filling only the strongest line!!!
            htheta.Fill(abs(spikeList[0][0]))
            if Draw:
                print 'Drawing... nlines={:}'.format(nlines,)
                canname = 'HoughTest' + path
                canname = canname.replace('/', '_')
                canname = canname +'_{:}'.format(j,)
                can = TCanvas(canname, canname, 0, 0, 1200, 450)
                can.Divide(3,1)
                
                can.cd(1)
                gPad.SetLogz(1)
                hist.SetStats(0)
                hist.Draw('colz')
                
                can.cd(2)
                gPad.SetLogz(1)
                hough.SetStats(0)
                hough.Draw('colz')
                
                can.cd(3)
                #gPad.SetLogz(1)
                inv.SetStats(0)
                inv.Draw('colz')

                can.Print(pngdir + can.GetName()+'.png')
                can.Print(pdfdir + can.GetName()+'.pdf')
                ###!!! very large!!! can.Print(Cdir + can.GetName()+'.C')

    


        else:
            print '   ...no line found, not bothering printing png...'
        j=j+1
        rfile.Write()
        rfile.Close()


thetaCan.cd()
htheta.SetMarkerColor(kRed)
htheta.SetMarkerStyle(20)
htheta.SetMarkerSize(1)
htheta.Draw('e1hist')
ymax = htheta.GetMaximum()
ymin = htheta.GetMinimum()
txt = TLatex(1.7, -(ymax-ymin)*0.07+ymax, 'Exposure: {:1.1f}h'.format(Nframes*600./3600.) ) 
txt.Draw()
thetaCan.Print(thetaCan.GetName() + '.pdf')
thetaCan.Print(thetaCan.GetName() + '.png')
thetaCan.Print(thetaCan.GetName() + '.C')

canname = 'Multiplicity'
Can = TCanvas(canname, canname, 0, 0, 1000, 1000)
Cans.append(Can)

Can.cd()
grMulti.SetMarkerColor(kBlue)
grMulti.SetMarkerStyle(20)
grMulti.SetMarkerSize(1)
grMulti.Draw('AP')
Can.Print(Can.GetName() + '.pdf')
Can.Print(Can.GetName() + '.png')
Can.Print(Can.GetName() + '.C')

