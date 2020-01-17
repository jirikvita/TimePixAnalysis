#!/usr/bin/python
# JK Mon 13 May 07:40:54 CEST 2019
# 23.5.2019: median! ;-)
# TODO: plot GPS height from logs as function of time! Remove some more outliars?!

from __future__ import print_function

import numpy as np

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt
from ConvTool import *

#!!! GPS Canon time is 1h later!!
GPSOFFSET = 3600.

cans = []
stuff = []

# timepix chip:
# chip size [cm]
d=1.4
# chip height: [cm]
h = 0.03
# Volume:
V = d*d*h
# Silicon: g/cm^3
rho = 2.3296 
# mass in kg:
mass = 0.001*V*rho
elCh = 1.602e-19
secInY = 31557600.

#########################################
# get energy from the .int file:
def GetEne(sdir, txt):
    txtfile = open(sdir + '/' + txt, 'read')
    ene = 0.
    # in principle we do not have to integrate this complicated way
    # as in .int files there is only one float on one line, but it should work;)
    for line in txtfile.readlines():
        for item in line.split():
            if len(item) > 0 :
                val =  makefloat(item)
                if val > 0.:
                    ene = ene + val
    return ene


#########################################
def GetDose(etot, time): #mGy/y
    dose = etot*1e3/mass*elCh*1000.  # Jouls/kg = mGy!;-)
    rate_perannum = dose / time*secInY
    return rate_perannum

#########################################
def GetEtoDoseSF(time): #mGy/y
    return 1e3/mass*elCh/time*secInY*1000.

##########################################
def GetSecs(hh,mm,ss):
    return hh*3600 + mm*60 + ss
##########################################

def MakeOffsetInSec(s1, s2):
    sec1 = GetSecs(int(s1.split(':')[0]), int(s1.split(':')[1]), int(s1.split(':')[2]) )
    sec2 = GetSecs(int(s2.split(':')[0]), int(s2.split(':')[1]), int(s2.split(':')[2]) )
    return sec1 - sec2

##########################################

def GetHeight(gpsfile,timeoffset,sdir,enefname,debug = 0):
    dscfname = enefname
    dscfname = dscfname.replace('.int','.txt.dsc')
    if debug: print('Will cat {:}/{:} | tail -n 6 | head -n 1'.format(sdir,dscfname))
    timenosep = ''
    timelist = []
    secs = 0
    for timelines in os.popen('cat {:}/{:} | tail -n 6 | head -n 1'.format(sdir,dscfname)):
        timeline = timelines[:-1]
        if debug: print(timeline)
        # get the time stamp without separator hhmmss:
        timelist = timeline.split()[3].split(':')[0:3]
        # need to add offset and correct for GOS time being 1h later;-)
        secs = GetSecs(int(timelist[0]),int(timelist[1]),int(float(timelist[2]))) + timeoffset - GPSOFFSET #!!!
        break
    hh = int(secs/3600)
    mm = int((secs - hh*3600) / 60)
    ss = int(secs - hh*3600 - mm *60) 
    if debug: print('New hh:mm:ss = {}:{}:{}'.format(hh,mm,ss))
    timenosep = '{}{}{}'.format(hh,mm,ss)
    timenosep_uncorr = timelist[0]+timelist[1]+timelist[2].split('.')[0]
    if debug: print('timenosep_uncorr: {:}'.format(timenosep_uncorr))
    if debug: print('timenosep_corr  : {:}'.format(timenosep))
    # get the height
    result = ''
    for results in os.popen('grep {:} {:}'.format(timenosep,gpsfile)):
        result = results[:-1].split()[1]
        if debug: print('Result: "{:}"'.format(result))
        break
    if result != '':
        return float(result)
    else:
        return -1
    
    

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

    ### https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    ### https://pymotw.com/2/getopt/
    ### https://docs.python.org/3.1/library/getopt.html
    gBatch = False
    gTag=''
    print(argv[1:])
    try:
        # options that require an argument should be followed by a colon (:).
        opts, args = getopt.getopt(argv[2:], 'hbt:', ['help','batch','tag='])

        print('Got options:')
        print(opts)
        print(args)
    except getopt.GetoptError:
        print('Parsing...')
        print ('Command line argument error!')
        print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]]'.format(argv[0]))
        sys.exit(2)
    for opt,arg in opts:
        print('Processing command line option {} {}'.format(opt,arg))
        if opt == '-h':
            print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]'.format(argv[0]))
            sys.exit()
        elif opt in ("-b", "--batch"):
            gBatch = True
        elif opt in ("-t", "--tag"):
            gTag = arg
            print('OK, using user-defined histograms tag for output pngs {:}'.format(gTag,) )

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))

    stdtime = 30.
    Ttot = 0.
    sdirs = {
        
        # timepix2!
        # Canon:  22:50:26 <==> Timepix: 22:54:00
        # so TimePix time is AHEAD from GPS=Canon time by 00:03:34
        # time offsets:   seconds taken per frame                   canon=GPS  timepix=laptop
        'PrgFrkJan2019' : [30., 'GPS_PrgFrkGva_19012900.LOG.parsed', '22:50:26', '22:54:00'],
        'FrkGvaJan2019' : [30.,'GPS_PrgFrkGva_19012900.LOG.parsed', '22:50:26', '22:54:00'],
        'GvaZurFeb2019' : [30.,'GPS_GvaZurPrg_19020100.LOG.parsed', '22:50:26', '22:54:00'],
        'ZurPrgFeb2019' : [30.,'GPS_GvaZurPrg_19020100.LOG.parsed', '22:50:26', '22:54:00'], # 00:03:34 diff
        
        # time offsets:                                       canon=GPS  timepix=laptop -- taken from 3days later
        'PrgZurFeb2019' : [30.,'GPS_PrgZurGva19021200.LOG.parsed', '21:07:29', '21:11:00'],
        'ZurGvaFeb2019' : [30.,'GPS_PrgZurGva19021200.LOG.parsed', '21:07:29', '21:11:00'],
        # time offsets:                                       canon=GPS  timepix=laptop  -- sure
        'FrkPrg15thFeb2019' : [30.,'GPS_GvaFrkPrg19021500.LOG.parsed', '21:07:29', '21:11:00'],
        'GvaFrkFeb15th2019' : [30.,'GPS_GvaFrkPrg19021500.LOG.parsed', '21:07:29', '21:11:00'], # 00:03:31 diff
        
        # PrgRom not usable, bad GPS eight till very end, 4000mn and lower
        # RomPrg usable, LOG parsed for reliable height
        # yes, this shift is correct and now works, probably b/c of summer time...
	'RomPrgMay2019' : [30.,'GPS_RomPrgFeb2019.LOG.parsed', '16:23:46', '17:27:00'], # 00:03:14 diff
        
        # timepix 1! Unclear time offset!!
        # TODO: try the usual time shift, or +/-3min as syst?
        # CURRENTLY: take and assume offset from Jan 2019 (best Bayesian prior information;-)
        # later back-extrapolate the offset knowing it in Jan/Feb 2019 and in May?;-)
        # these are December flights, so winter time:
        'LetGvaBrusPrg2017' : [30.,  'GPS_GvaBruPrg17120500.LOG.parsed', '22:50:26', '22:54:00'], #'00:00:00', '00:00:00' ],
        'LetPrgGvaDec2017'  : [120., 'GPS_PrgGva_17120300.LOG.parsed',   '22:50:26', '22:54:00'], #'00:00:00', '00:00:00'],

    }
        

    Hbins = [ i*500. for i in range(0, 25)]
    nH = len(Hbins)-1
    print(Hbins)
    
    hDoseAccum = ROOT.TH1D('AccumDoseVsHeight', 'Acum. Dose vs height;h [m];dose [mGy/y]', nH, 1.*Hbins[0], 1.*Hbins[-1] )
    hDose = ROOT.TH1D('DoseVsHeight', 'Dose vs height;h [m];dose [mGy/y]', nH, 1.*Hbins[0], 1.*Hbins[-1] )
    hDoseMedian = ROOT.TH1D('MedianDoseVsHeight', 'Median dose vs height;h [m];dose [mGy/y]', nH, 1.*Hbins[0], 1.*Hbins[-1] )
    hnFrames = ROOT.TH1D('NframesVsHeight', 'nFrames vs height;h [m];N', nH, 1.*Hbins[0], 1.*Hbins[-1] )

    gr2 = ROOT.TGraph()
    ip = 0
    
    stuff.append(hDoseAccum)
    stuff.append(hDose)
    stuff.append(hDoseMedian)
    stuff.append(hnFrames)

    # dict. between the height bin number and values of ene over time
    DoseOverHeight = {}
    
    for sdir in sdirs:

        # get energy
        for tfile in os.popen('cd {} ; ls *.int'.format(sdir)):
            txt = tfile[:-1]

            time = sdirs[sdir][0]
            # get total frame energy and compute the dose
            ene = GetEne(sdir, txt)
            dose = GetDose(ene, time)

            #try:
            # find height from GPS log;-)
            gpsfile = sdirs[sdir][1]
            timeoffset = MakeOffsetInSec(sdirs[sdir][2], sdirs[sdir][3])
            height = GetHeight(gpsfile,timeoffset,sdir,txt)
            if height > 0:
                print('Height: {} Dose: {}'.format(height, dose))
                # fill!
                hDoseAccum.Fill(height, ene)
                hnFrames.Fill(height, time/stdtime)
                heightBin = hDoseAccum.FindBin(height)
                try:
                    # try to access:
                    foo = DoseOverHeight[heightBin][0]
                    # TO CHECK THIS IS OK!!!
                    DoseOverHeight[heightBin].append(dose)
                except:
                    DoseOverHeight[heightBin] = [dose]
                
                #except:
                #print('Ooops, exception!')
                #gr2.SetPoint(ip, height, ene/time/1000.)
                gr2.SetPoint(ip, height, dose)
                ip = ip+1
                Ttot = Ttot + time
            else:
                print('   ...error getting height!')

            if ene > 3e4:
                print('WARNING, high energy recorded: E: {} h: {} '.format(ene, height))
    print(DoseOverHeight)
    # median:
    for ibin in DoseOverHeight:
        hDoseMedian.SetBinContent(ibin, np.median(DoseOverHeight[ibin]))
        hDoseMedian.SetBinError(ibin, sqrt(np.var(DoseOverHeight[ibin])) / sqrt(1.*len(DoseOverHeight[ibin])) )
    hDoseMedian.Scale(1.)
    # TODO: draw also scaled median and mean into the graph plot;-)
    
    Htot = int(Ttot)/3600
    Mtot = int(Ttot - Htot*3600)/60
    Stot = (Ttot - Htot*3600 - Mtot*60)/60.
    print('Total exposure with GPS info: {}h {}m {}s'.format(Htot, Mtot, Stot))
    # now postprocessing!
    hDoseAccum.Scale(GetEtoDoseSF(stdtime))
    ROOT.gStyle.SetOptTitle(0)

    canname = 'DoseHeight'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1000)
    cans.append(can)
    ROOT.gPad.SetTicks(1,1)
    #can.Divide(2,2)
    #can.cd(1)
    #hDoseAccum.Draw()
    #can.cd(2)
    #hnFrames.Draw()

    #can.cd(3)
    hDose.Divide(hDoseAccum,hnFrames)
    for i in range(0,hDose.GetNbinsX()):
        val = hDose.GetBinContent(i+1)
        n = hnFrames.GetBinContent(i+1)
        if n > 0:
            hDose.SetBinError(i+1, val/sqrt(n))
    hDose.Scale(1.)

    # stuff.append(hDose)
    hDose.SetMarkerStyle(20)
    hDose.SetMarkerSize(1)
    hDose.SetMarkerColor(ROOT.kBlue)
    hDose.SetLineColor(ROOT.kBlue)
    hDose.SetStats(0)

    hDoseMedian.SetMarkerStyle(21)
    hDoseMedian.SetMarkerSize(1)
    hDoseMedian.SetMarkerColor(ROOT.kRed)
    hDoseMedian.SetLineColor(ROOT.kRed)
    hDoseMedian.SetStats(0)

    
    leg = ROOT.TLegend(0.14, 0.55, 0.65, 0.88)
    leg.SetBorderSize(0)
    leg.AddEntry(hDose, 'Data mean', 'P')
    leg.AddEntry(hDoseMedian, 'Data median', 'P')
    stuff.append(leg)
    
    myfun = ROOT.TF1('fitpow', '[0]*x^[1]+[2]', 0., Hbins[-1])
    stuff.append(myfun)
    myfun.SetParameters(1., 2., 0.)
    myfun.SetLineColor(ROOT.kRed)
    myfun.SetLineStyle(2)
    hDoseMedian.Fit('fitpow')
    chi2 = myfun.GetChisquare()
    ndf = myfun.GetNDF()
    leg.AddEntry(myfun, 'Power fit, #chi^{2}/ndf = ' + '{:1.2f}'.format(chi2/ndf), 'L')

    myfun2 = ROOT.TF1('fitpol', '[0] + [1]*x + [2]*x^2', 0., Hbins[-1])
    stuff.append(myfun2)
    myfun2.SetParameters(1., -1e-6, 1e-8)
    myfun2.SetLineColor(ROOT.kRed)
    myfun2.SetLineStyle(1)
    hDoseMedian.Fit('fitpol')
    chi2 = myfun2.GetChisquare()
    ndf = myfun2.GetNDF()
    leg.AddEntry(myfun2, 'Quadratic fit, #chi^{2}/ndf = ' + '{:1.2f}'.format(chi2/ndf), 'L')

    # TODO: add also exp fit!
    myfun3 = ROOT.TF1('fitexp', '[0] + [1]*exp([2]*x)', 0., Hbins[-1])
    stuff.append(myfun3)
    myfun3.SetParameters(0.1, 1., 1e-6)
    myfun3.SetLineColor(ROOT.kRed)
    myfun3.SetLineStyle(3)
    hDoseMedian.Fit('fitexp')
    chi2 = myfun3.GetChisquare()
    ndf = myfun3.GetNDF()
    leg.AddEntry(myfun3, 'Exp. fit, #chi^{2}/ndf = ' + '{:1.2f}'.format(chi2/ndf), 'L')
    
    stuff.append(hDose.DrawCopy('e1'))
    stuff.append(hDoseMedian.DrawCopy('e1 same'))
    myfun.Draw('same')
    myfun2.Draw('same')
    leg.Draw()

    
    can.Print(canname + '.png')
    can.Print(canname + '.pdf')

    gcanname = 'DoseScatter'
    gcan = ROOT.TCanvas(gcanname, gcanname, 400, 400, 800, 800)
    gcan.cd()
    ROOT.gPad.SetTicks(1,1)
    cans.append(gcan)
    gr2.SetMarkerStyle(20)
    gr2.SetMarkerSize(0.7)
    gr2.SetMarkerColor(ROOT.kBlack)
    gr2.GetXaxis().SetTitle('h [m]')
    #gr2.GetYaxis().SetTitle('#DeltaE/#Deltat [MeV/s]')
    gr2.GetYaxis().SetTitle('dose [mGy/y]')
    
    gr2.Draw('AP')
    hDose.Draw('e1hist same')
    hDoseMedian.Draw('e1hist same')

    ROOT.gPad.RedrawAxis()
      
    gcan.Print(gcanname + '.png')
    gcan.Print(gcanname + '.pdf')

    
    ROOT.gApplication.Run()
    return

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

