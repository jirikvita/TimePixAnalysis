#!/usr/bin/python
# jk 30.5.2018, 29.1.2019, 1.2.2019, 7.2.2019

# TODO: marker color based on the time?;)

from ROOT import *
from math import sqrt
from ConvTool import *
import os, sys

stuff = []
cans = []
fits = []
    
##########################################
def ReadTimePixRateData(dirname, ftag, offset):
    data = []
    ratefilename = '{}/xls/rate.txt'.format(dirname)
    print('Will read timepix rate data from {}'.format(ratefilename))
    ratefile = open(ratefilename, 'read')
    for rawline in ratefile.readlines():
        line = rawline[:-1]
        #if line == '': continue
        #print line
        items = line.split('\t')
        #print items
        if len(items) < 2: continue
        iframe = makefloat(items[0])
        rate = makefloat(items[1])
        #print iframe, rate
        data.append([iframe, rate])

    ratefile.close()
    print('...read {} lines!'.format(len(data)))
    return data


##########################################
# quantity = occ, int standing for occupancy (number of fired pixels) and integrated energy, respectivelly;-)
def ReadTimePixTimeData(quantity, dirname, ftag, offset, debug = 0):
    data = []
    for line in os.popen('cd {} ; ls {}*.{}'.format(dirname,ftag, quantity)).readlines():
        fname = line[:-1]
        if debug: print('working on {}'.format(fname))
        infile = open(dirname + '/' + fname,'read')
        sval = infile.readline()
        val = makefloat(sval)
        infile.close()

        fname = fname.replace('.' + quantity,'.time')
        if debug: print('working on {}'.format(fname))
        infile = open(dirname + '/' + fname,'read')
        stime = infile.readline()
        time = MakeTime(stime) + offset
        
        data.append([val, time])
        
    return data

##########################################
def ReadTimePixOccTimeData(dirname, ftag, offset):
    return ReadTimePixTimeData('occ', dirname, ftag, offset)
##########################################
def ReadTimePixETimeData(dirname, ftag, offset):
    return ReadTimePixTimeData('int', dirname, ftag, offset)


##########################################
def MainCall(flightTag, offset_geiger):


    # data taken by JK using TimePix and LabQuest2 Geiger on flights on 29.1.2019 and 1.2.2019
    # INTEGRATEED txt files in FrkGvaJan2019, PrgFrkJan2019, GvaZurFeb2019, ZurPrgFeb2019
    # Unfortunatelly, I did not read the time of the Geiger datataking start for the GvaZur flight,
    #   so the Geiger data cannot be correlated to TimePix for this flight.
    # Plot correlation between dose by TimePix and counts in Geiger;-)
    # for each TimePix 30s exposure plot the several (usually 3) values from the Geiger 10s frame
    # laptop = TimePix time is shifted:
    # Canon:  22:50:26 <==> Timepix: 22:54:00
    # so TimePix time is AHEAD from GPS=Canon time by 00:03:34
    # 
    # Now, also GPS (Canon) time shift w.r.t. Geiger:
    # Prg-Frk:
    # Canon: 11:10:35   <==>  1370s elapsed of Geiger
    # Canon: 11:11:15   <==>  1410s elapsed of Geiger
    # Frk-Gva
    # Canon: 13:19:12   <==>  470s elapsed of Geiger
    # Gva-Zur
    #              NOT AVAILABLE
    # Zur-Prg
    # Canon: 12:38:46   <==>  160s elapsed of Geiger
    

    Tgei=10 # in s; Geiger acquisition time window
    Ttpx=30 # in s; TimePix acquisition time window
  
    # Note the minus sign! Timepix=laptop was 3min AHEAD of the Canon=GPS time! And this needs to be sibtracted!
    offset_timepix = - MakeTime('foo foo foo 00:03:34') 
    
    #dirname = '{}2019'.format(flightTag)
    dirname = '{}2019'.format(flightTag)
    ftag = dirname

    infilename = '{}_Geiger.txt'.format(flightTag)
    tag = infilename
    tag = tag.replace('_Geiger.txt', '')

    # Read TimePix data!
    tpxEdata = ReadTimePixETimeData(dirname, ftag, offset_timepix)
    tpxOccdata = ReadTimePixOccTimeData(dirname, ftag, offset_timepix)
    tpxRatedata = ReadTimePixRateData(dirname, ftag, offset_timepix)
    
    # Read Geiger data!
    infile = open(infilename)
    datax = []
    datay = []
    geigerdata = []
    i = 0.
    for line in infile.readlines():
        data = line[:-1].split()
        print(data)
        if len(data) == 0:
            continue
        datax.append(float(data[0]))
        datay.append(float(data[1]))
        t_geiger = i*Tgei + offset_geiger
        geigerdata.append([float(data[1]), t_geiger])
        i = i + 1


    print('*** TimePix rate data')
    print(tpxRatedata)
    print('*** TimePix E data')
    print(tpxEdata)
    print('*** Geiger data')
    print(geigerdata)

    gr = TGraphErrors()
    gr.SetName('Counts')

    ip = 0
    for x,y in zip(datax,datay,):
        #print x,y
        gr.SetPoint(ip, x, y)
        err = 0.
        if y > 0:
            err = sqrt(y)
        gr.SetPointError(ip, 0., err)
        ip = ip+1

    gr_tpxE_vs_gei = TGraphErrors()
    gr_tpxE_vs_gei.SetName('TimePixE_vs_GeigerCounts')
    SetStyle(gr_tpxE_vs_gei, kGreen+2, 1, 20)
    gr_tpxE_vs_gei.GetXaxis().SetTitle('Geiger counts')
    gr_tpxE_vs_gei.GetYaxis().SetTitle('TimePix energy [MeV]')

    gr_tpxRate_vs_gei = TGraphErrors()
    gr_tpxRate_vs_gei.SetName('TimePixRate_vs_GeigerCounts')
    SetStyle(gr_tpxRate_vs_gei, kBlue, 1, 20)
    gr_tpxRate_vs_gei.GetXaxis().SetTitle('Geiger counts')
    gr_tpxRate_vs_gei.GetYaxis().SetTitle('TimePix particle count')
    
    gr_tpxE_vs_tpxRate = TGraphErrors()
    gr_tpxE_vs_tpxRate.SetName('TimePixE_vs_TimePixRate')
    SetStyle(gr_tpxE_vs_tpxRate, kBlue, 1, 20)
    gr_tpxE_vs_tpxRate.GetXaxis().SetTitle('TimePix particle count')
    gr_tpxE_vs_tpxRate.GetYaxis().SetTitle('TimePix energy [MeV]')

    gr_tpxE_vs_tpxOcc = TGraphErrors()
    gr_tpxE_vs_tpxOcc.SetName('TimePixE_vs_TimePixOcc')
    SetStyle(gr_tpxE_vs_tpxOcc, kBlue, 1, 20)
    gr_tpxE_vs_tpxOcc.GetXaxis().SetTitle('TimePix pixel occupancy')
    gr_tpxE_vs_tpxOcc.GetYaxis().SetTitle('TimePix energy [MeV]')

    gr_tpxE_vs_iframe = TGraphErrors()
    gr_tpxE_vs_iframe.SetName('TimePixE_vs_iframe')
    SetStyle(gr_tpxE_vs_iframe, kCyan+3, 1, 20, 1, 1)
    gr_tpxE_vs_iframe.GetXaxis().SetTitle('TimePix frame')
    gr_tpxE_vs_iframe.GetYaxis().SetTitle('TimePix energy [MeV]')

    gr_tpxRate_vs_iframe = TGraphErrors()
    gr_tpxRate_vs_iframe.SetName('TimePixRate_vs_iframe')
    SetStyle(gr_tpxRate_vs_iframe, kMagenta+2, 1, 20, 1, 1)
    gr_tpxRate_vs_iframe.GetXaxis().SetTitle('TimePix frame')
    gr_tpxRate_vs_iframe.GetYaxis().SetTitle('TimePix particle count')

    # Eaver = E / N
    # eEaver = W *sqrt(N) / N^2
    # E = N*eAver
    # eE = sqrt(N)*eAver = E / sqrt(N)
    
    for i in range(0, len(tpxEdata)):
        val_tpxE = tpxEdata[i][0] / 1000. # conversion to MeV!
        val_tpxOcc = tpxOccdata[i][0]
        val_tpxRate = tpxRatedata[i][1]
        tpxEerr = 1.
        if val_tpxRate > 0:
            tpxEerr = val_tpxE / sqrt(1.*val_tpxRate)
        tpxRateErr = 1.
        if val_tpxRate > 0:
            tpxRateErr = sqrt(val_tpxRate)
        tpxOccErr = 1.
        if val_tpxOcc > 0:
            tpxOccErr = sqrt(1.*val_tpxOcc)

        print('Setting point {} of E vs Rate to {} {}'.format(i, val_tpxRate, val_tpxE))
        gr_tpxE_vs_tpxRate.SetPoint(i, val_tpxRate, val_tpxE)
        gr_tpxE_vs_tpxRate.SetPointError(i, tpxRateErr, tpxEerr)

        print('Setting point {} of E vs Occ to {} {}'.format(i, val_tpxOcc, val_tpxE))
        gr_tpxE_vs_tpxOcc.SetPoint(i, val_tpxOcc, val_tpxE)
        gr_tpxE_vs_tpxOcc.SetPointError(i, tpxOccErr, tpxEerr)

        print('Setting point {} of E vs iframe to {} {}'.format(i, i+1, val_tpxE))
        gr_tpxE_vs_iframe.SetPoint(i, i+1, val_tpxE)
        gr_tpxE_vs_iframe.SetPointError(i, 0, tpxEerr)

        print('Setting point {} of Rate vs iframe to {} {}'.format(i, i+1, val_tpxRate))
        gr_tpxRate_vs_iframe.SetPoint(i, i+1, val_tpxRate)
        gr_tpxRate_vs_iframe.SetPointError(i, 0, tpxRateErr)

        
    itpx = 0
    igei = 0
    ip2 = 0
    for i in range(0, max(len(geigerdata),len(tpxEdata)) ):

        if itpx >= len(tpxEdata):
            break
        if igei >= len(geigerdata):
            break
        
        t_tpx = tpxEdata[itpx][1]
        t_gei = geigerdata[igei][1]
        val_tpxE = tpxEdata[itpx][0] / 1000. # conversion to MeV!
        val_gei = geigerdata[igei][0]
        val_tpxRate = tpxRatedata[itpx][1]
        geiErr = 1.
        if val_gei > 0:
            geiErr = sqrt(val_gei)
        tpxEerr = 0.
        if val_tpxE > 0:
            tpxEerr = val_tpxE / sqrt(val_tpxRate)

        print('i={} itpx={} igei={} Ttpx={} Tgei={} tpxE={} GeiC={}'.format(i, itpx, igei, t_tpx, t_gei, val_tpxE, val_gei))
        
        if t_gei < t_tpx + Tgei:
            igei = igei+1
            print('   ...shifting geiger index...')
            continue
        if t_tpx + Ttpx < t_gei:
            print('   ...shifting tpx index...')
            itpx = itpx+1
            continue
        print('   OK! Setting point {}'.format(ip2))

        gr_tpxE_vs_gei.SetPoint(ip2, val_gei, val_tpxE)
        gr_tpxE_vs_gei.SetPointError(ip2, geiErr, tpxEerr)
        geiErr = 0.
        if val_gei > 0:
            geiErr = sqrt(val_gei)
        if itpx < len(tpxRatedata):
            val_tpxRate = tpxRatedata[itpx][1]
            tpxRateErr = 0.
            if val_tpxRate > 0:
                tpxRateErr = sqrt(val_tpxRate)

            gr_tpxRate_vs_gei.SetPoint(ip2, val_gei, val_tpxRate)
            gr_tpxRate_vs_gei.SetPointError(ip2, geiErr, tpxRateErr)
        ip2 = ip2 + 1
        igei = igei + 1 

        

    canname = 'DoseScatter_' + tag
    can = TCanvas(canname, canname, 0, 0, 1000, 1000)
    can.Divide(2,2)
    can.cd(3)
    gr_tpxE_vs_gei.Draw('AP')
    stuff.append(gr_tpxE_vs_gei)

    can.cd(4)
    gr_tpxRate_vs_gei.Draw('AP')
    stuff.append(gr_tpxRate_vs_gei)

    
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
    gr.GetXaxis().SetTitle('Time bin of {}s'.format(Tgei))
    gr.GetYaxis().SetTitle('Counts in {}s interval'.format(Tgei))
    leg = TLegend(0.17, 0.75, 0.37, 0.87)
    leg.SetBorderSize(0)
    leg.AddEntry(gr, tag, 'P')
    stuff.append(gr)

    rebin = 6
    can.cd(2)
    gPad.SetLogy()
    gPad.SetGridy(1)
    gPad.SetGridx(1)
    h1.GetYaxis().SetMoreLogLabels()
    h1.Rebin(rebin)
    h1.SetMinimum(2.5)
    h1.SetStats(0)
    h1.SetMarkerColor(kRed)
    h1.SetLineColor(h1.GetMarkerColor())
    h1.SetMarkerSize(1)
    h1.SetMarkerStyle(20)
    h1.GetYaxis().SetTitle('Counts in {}s interval'.format(rebin*Tgei))
    h1.GetXaxis().SetTitle('Time bin of {}s'.format(rebin*Tgei))
    hh1 = h1.DrawCopy('e1 hist')
    stuff.append(h1)
    stuff.append(hh1)

    h1.Scale(1./rebin)
    leg.AddEntry(h1, 'Rebinned {}x'.format(rebin), 'L')
    h1.SetLineColor(kRed)
    h1.SetLineWidth(3)
    can.cd(1)
    h1.Draw('hist same')
    leg.Draw()

    corr = gr_tpxE_vs_gei.GetCorrelationFactor()
    print('TimePix E vs Geiger points            : {}'.format(gr_tpxE_vs_gei.GetN(),))
    print('TimePix E vs Geiger counts correlation: {}'.format(corr,))
    can.cd(3)
    text = TLatex(0.15, 0.88, '#rho = {:1.2f}'.format(corr))
    text.SetNDC()
    text.Draw()
    stuff.append(text)

    corr = gr_tpxRate_vs_gei.GetCorrelationFactor()
    print('TimePix Rate vs Geiger points            : {}'.format(gr_tpxRate_vs_gei.GetN(),))
    print('TimePix Rate vs Geiger counts correlation: {}'.format(corr,))

    can.cd(4)
    text = TLatex(0.15, 0.88, '#rho = {:1.2f}'.format(corr))
    text.SetNDC()
    text.Draw()
    stuff.append(text)

    #gPad.Print(canname + '.png')
    #gPad.Print(canname + '.pdf')
    can.Print(canname + '.png')
    can.Print(canname + '.pdf')

    canname = 'TimePixERateScatter_' + tag
    can2 = TCanvas(canname, canname, 800, 100, 1000, 1000)
    can2.Divide(2,2)
    can2.cd(1)
    gr_tpxE_vs_tpxRate.Draw('AP')
    corr = gr_tpxE_vs_tpxRate.GetCorrelationFactor()
    text = TLatex(0.15, 0.88, '#rho = {:1.2f}'.format(corr))
    text.SetNDC()
    text.Draw()
    stuff.append(text)

    can2.cd(2)
    gr_tpxE_vs_tpxOcc.Draw('AP')
    corr = gr_tpxE_vs_tpxOcc.GetCorrelationFactor()
    text = TLatex(0.15, 0.88, '#rho = {:1.2f}'.format(corr))
    text.SetNDC()
    text.Draw()
    stuff.append(text)

    can2.cd(3)
    gr_tpxRate_vs_iframe.Draw('AP')
    can2.cd(4)
    gr_tpxE_vs_iframe.Draw('AP')

    gPad.Update()

    can2.Print(canname + '.png')
    can2.Print(canname + '.pdf')
    
    
    stuff.append([gr_tpxRate_vs_iframe, gr_tpxE_vs_iframe, gr_tpxE_vs_tpxOcc, gr_tpxE_vs_tpxRate])
    cans.append([can, can2])
    
    return gr_tpxRate_vs_gei, gr_tpxE_vs_gei

###################################
def CopyStyle(g1, g):
    g.SetLineColor(g1.GetLineColor())
    g.SetLineStyle(g1.GetLineStyle())
    g.SetLineWidth(g1.GetLineWidth())
    g.SetMarkerColor(g1.GetMarkerColor())
    g.SetMarkerSize(g1.GetMarkerSize())
    g.SetMarkerStyle(g1.GetMarkerStyle())
    g.GetXaxis().SetTitle(g1.GetXaxis().GetTitle())
    g.GetYaxis().SetTitle(g1.GetYaxis().GetTitle())
    
###################################

def MergeGraphs(grs, tag = ''):
    if len(grs) < 1:
        return
    if len(grs) < 2:
        return grs[0]
    ip = 0
    Gr = TGraphErrors()
    if tag == '':
        tag = gr.GetName() + '_merged'
    Gr.SetName(tag)
    CopyStyle(grs[0], Gr)
    x = Double(0.)
    y = Double(0.)
    ex = Double(0.)
    ey = Double(0.)
    for gr in grs:
        for i in range(0, gr.GetN()):
            gr.GetPoint(i, x, y)
            ex = gr.GetErrorX(i)
            ey = gr.GetErrorY(i)
            Gr.SetPoint(ip, x, y)
            Gr.SetPointError(ip, ex, ey)
            ip = ip + 1
    print('Merged graph points: {}'.format(ip))
    return Gr


###################################
def FitGraph(gr):
    xmax = gr.GetXaxis().GetXmax()
    xmin = gr.GetXaxis().GetXmin()
    fitname = 'fit_gr'
    fit = TF1(fitname, '[0] + [1]*x', xmin, xmax)
    fit.SetParameters(0., 1.)
    gr.Fit(fitname)
    chi2 = fit.GetChisquare()
    ndf = fit.GetNDF()
    text1 = TLatex(0.50, 0.88, 'Fit #chi^{2}/NDF = ' + '{:1.2f}'.format(chi2/ndf))
    text1.SetNDC()
    text1.Draw()
    stuff.append(text1)
    text2 = TLatex(0.72, 0.21, 'p_{0} = ' + '{:1.2f}'.format(fit.GetParameter(0)))
    text2.SetNDC()
    text2.Draw()
    stuff.append(text2)
    text3 = TLatex(0.72, 0.15, 'p_{1} = ' + '{:1.2f}'.format(fit.GetParameter(1)))
    text3.SetNDC()
    text3.Draw()
    stuff.append(text3)
    return fit


###################################


def MakeAndPlotGlobalGraphs(Gr_tpxRate_vs_gei, Gr_tpxE_vs_gei, dofit = True):
    GlobalGr_tpxRate_vs_gei = MergeGraphs(Gr_tpxRate_vs_gei, 'GlobalTpxRateVsGeigerCounts')
    GlobalGr_tpxE_vs_gei = MergeGraphs(Gr_tpxE_vs_gei, 'GlobalTpxEVsGeigerCounts')

    canname = 'GlobalScatterTimePixGeiger'
    can = TCanvas(canname, canname, 3, 3, 1400, 750)
    can.Divide(2,1)

    can.cd(1)
    GlobalGr_tpxE_vs_gei.Draw('AP')
    corr = GlobalGr_tpxE_vs_gei.GetCorrelationFactor()
    text = TLatex(0.15, 0.88, '#rho = {:1.2f}'.format(corr))
    text.SetNDC()
    text.Draw()
    stuff.append(text)
    FitGraph(GlobalGr_tpxE_vs_gei)
    
    can.cd(2)
    GlobalGr_tpxRate_vs_gei.Draw('AP')
    corr = GlobalGr_tpxRate_vs_gei.GetCorrelationFactor()
    text = TLatex(0.15, 0.88, '#rho = {:1.2f}'.format(corr))
    text.SetNDC()
    text.Draw()
    stuff.append(text)
    FitGraph(GlobalGr_tpxRate_vs_gei)

    stuff.append([GlobalGr_tpxE_vs_gei, GlobalGr_tpxRate_vs_gei])

    can.Print(canname + '.png')
    can.Print(canname + '.pdf')
    cans.append(can)

    
    
###################################
###################################
###################################

def main(argv):

    gStyle.SetOptTitle(0)
    gStyle.SetPadTopMargin(0.05)
    gStyle.SetPadRightMargin(0.05)
    
    # always need to produce manually rate.txt first and move it to xls/ directory
    # also must prepare corresp. Geiger*.txt file!
    FlightData = { 'PrgFrkJan' : MakeTime('foo foo foo 11:10:35') - 1370.,
                   'FrkGvaJan' : MakeTime('foo foo foo 13:19:12') - 470.,
                   'ZurPrgFeb' : MakeTime('foo foo foo 12:38:46') - 160.,
                   'PrgRomMay' : MakeTime('foo foo foo 11:28:17.5') - 130.,
                   'RomPrgMay' : MakeTime('foo foo foo 17:30:35') - 30.
    }

    Gr_tpxRate_vs_gei = []
    Gr_tpxE_vs_gei = []

    for flightdata in FlightData:
        print('*** Processing', flightdata)
        flightTag = flightdata
        offset_geiger = FlightData[flightTag]
        gr_tpxRate_vs_gei, gr_tpxE_vs_gei = MainCall(flightTag, offset_geiger)
        Gr_tpxRate_vs_gei.append(gr_tpxRate_vs_gei)
        Gr_tpxE_vs_gei.append(gr_tpxE_vs_gei)

    MakeAndPlotGlobalGraphs(Gr_tpxRate_vs_gei, Gr_tpxE_vs_gei)
    
    gApplication.Run()
    
###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
    
###################################
###################################
###################################
