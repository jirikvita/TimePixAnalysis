#!/usr/bin/python
# jk 30.5.2018, 29.1.2019

from ROOT import *
from math import sqrt

gStyle.SetOptTitle(0)

stuff = []

# data taken by JK using LabQuest2 Geiger on 29.1.2019
# Done: INTEGRATEED txt files in FrkGvaJan2019 or PrgFrkJan2019
# plot correlation between dose by TimePix and counts in Geiger;-)
# for each Geiger frame, plot the several (usually 20) values from the TimePix 30s exposures
# laptop = TimePix time is shifted:
# Canon:  22:50:26 <==> Timepix: 22:54:00
# so TimePix time is ahead by 00:03:34
# 
# Now, also GPS (Canon) time shift w.r.t. Geiger:
# Prg-Frk:
# Canon: 11:10:35   <==>  1370s elapsed of Geiger
# Canon: 11:11:15   <==>  1410s elapsed of Geiger
# Frk-Gva
# Canon: 13:19:12   <==>  470s elapsed of Geiger

T=10 # in s; acquisition time window
#infilename = 'PrgFrkJan_Geiger.txt'
infilename = 'FrkGvaJan_Geiger.txt'
#infilename = 'ZurPrgFeb_Geiger.txt'
tag = infilename
tag = tag.replace('_Geiger.txt', '')


infile = open(infilename)
datax = []
datay = []
for line in infile.readlines():
    data = line[:-1].split()
    print data
    if len(data) == 0:
        continue
    datax.append(float(data[0]))
    datay.append(float(data[1]))

gr = TGraphErrors()
gr.SetName('Counts')

ip = 0
for x,y in zip(datax,datay,):
    print x,y
    gr.SetPoint(ip, x, y)
    err = 0.
    if y > 0:
        err = sqrt(y)
    gr.SetPointError(ip, 0., err)
    ip = ip+1

gStyle.SetPadTopMargin(0.05)
gStyle.SetPadRightMargin(0.05)

canname = 'GeigerScatter_' + tag
can = TCanvas(canname, canname, 0, 0, 1380, 800)
can.Divide(2,1)

xmin = datax[0]
xmax = datax[-1]
nbins = len(datax)-1
h1 = TH1D(canname + '_h', canname + '_h', nbins, xmin, xmax)
ip = 1
for y in datay:
    h1.SetBinContent(ip, y)
    ip = ip+1
h1.Scale(1.)

gr.SetMarkerColor(kBlue)
gr.SetMarkerSize(1)
gr.SetMarkerStyle(20)


can.cd(1)
gr.Draw('AP')
gr.GetXaxis().SetTitle('Time bin of {}s'.format(T))
gr.GetYaxis().SetTitle('Counts in {}s interval'.format(T))
leg = TLegend(0.67, 0.75, 0.87, 0.87)
leg.SetBorderSize(0)
leg.AddEntry(gr, tag, 'P')
stuff.append(gr)

rebin = 6
can.cd(2)
gPad.SetLogy()
h1.Rebin(rebin)
h1.SetMinimum(2.5)
h1.SetStats(0)
h1.SetMarkerColor(kRed)
h1.SetLineColor(h1.GetMarkerColor())
h1.SetMarkerSize(1)
h1.SetMarkerStyle(20)
h1.GetYaxis().SetTitle('Counts in {}s interval'.format(rebin*T))
h1.GetXaxis().SetTitle('Time bin of {}s'.format(rebin*T))
hh1 = h1.DrawCopy('e1 hist')
hh1.GetYaxis().SetMoreLogLabels(1)
#hh1.GetYaxis().SetTitleOffset(1.75)
gPad.RedrawAxis()
gPad.SetGridx(1)
gPad.SetGridy(1)
gPad.Update()
stuff.append(h1)
stuff.append(hh1)

h1.Scale(1./rebin)
leg.AddEntry(h1, 'Rebinned {}x'.format(rebin), 'L')
h1.SetLineColor(kRed)
h1.SetLineWidth(3)
can.cd(1)
h1.Draw('hist same')
leg.Draw()

#gPad.Print(canname + '.png')
#gPad.Print(canname + '.pdf')
can.Print(canname + '.png')
can.Print(canname + '.pdf')


gApplication.Run()

