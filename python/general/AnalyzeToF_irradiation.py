#!/usr/bin/python



import ROOT

# Jiri Kvita, 25th Jan 2018

def Rotate180Deg(hist):
    # assuming square histogram, anyway...
    nx = hist.GetXaxis().GetNbins()
    ny = hist.GetYaxis().GetNbins()
    histo = hist.Clone(hist.GetName() + '_rotated')
    for i in range(1,nx+1):
        for j in range(1,ny+1):
            histo.SetBinContent(nx-i+1,ny-j+1,hist.GetBinContent(i,j))
    return histo

def FixBinContentForDraw(histo):
    nx = hist.GetXaxis().GetNbins()
    ny = hist.GetYaxis().GetNbins()
    # add 1keV to empty bins! for drawing purposes only!
    for i in range(1,nx+1):
        for j in range(1,ny+1):
            val = histo.GetBinContent(i,j)
            if val <= 0:
                histo.SetBinContent(i,j, 1.)
    return

# compute the dose from ToF bars irradiated on LHC tunnel during 2017;
# Train1 broken ToF bar measured at SLO between 19th-22nd January
# by shifting the edge of the sharp point by 1mm beyond the chip, to 5mm, 10mm etc.

ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)
ROOT.gStyle.SetOptTitle(0)
    
shifts = ['25mm', '20mm', '15mm', '10mm', '5mm', '1mm', 'Bg']
nh = len(shifts)
canname = 'ToF_irradiated'
unit = 400
#unit = 300
#can = ROOT.TCanvas(canname, canname, 0, 0, nh*unit,unit)
#can.Divide(nh,1)
can = ROOT.TCanvas(canname, canname, 0, 0, 3*unit,2*unit)
can.Divide(3,2)
can_bg = ROOT.TCanvas(canname+'_bg', canname+'_bg', 100, 100, unit,unit)
can_bg.Divide(3,2)

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
e = 1.602e-19


files = []
histos = []
texts = []

for shift in shifts:
    i = shifts.index(shift)
    hours = 15.
    name = 'Train1_{:}_15h/root/all.root'.format(shift)
    if 'Bg' in shift:
        #shift = 'Bg'
        name = 'NonirradiatedBg_Xmm_39h/root/all.root'
        hours = 39.
    rfile = ROOT.TFile(name)
    files.append(rfile)
    hist = rfile.Get('histo')
    histo = Rotate180Deg(hist) # adds 1keV to empty bins! for drawing purposes only!
    if 'Bg' in shift:
        histo.Scale(15./39.)
    FixBinContentForDraw(histo)
    histos.append(hist)
    histos.append(histo)
    etot = hist.Integral() # keV!
    dose = etot*1e3/mass*e  # Jouls/kg = Gy
    doserate = dose/hours
    rate_perannum = doserate*1e3*365.*24
    print('=== Shift : {:}'.format(shift))
    print('etot      : {:} GeV'.format(etot*1e-6))
    print('dose      : {:} muGy'.format(dose*1e6))
    print('doserate  : {:} muGy/h'.format(doserate*1e6))
    print('doserate  : {:} mGy/year'.format(rate_perannum))
    #print(': {:}'.format())
    #print(': {:}'.format())

    #can.cd(i+1)
    #ROOT.gPad.SetLogz(1)
    #hist.SetMaximum(6000.)
    #hist.SetStats(0)
    #hist.Draw('colz')
    if shift == 'Bg':
        can_bg.cd()
    else:
        can.cd(i+1)
    ROOT.gPad.SetLogz(1)
    histo.SetMaximum(6000.)
    histo.SetMinimum(1.)
    histo.SetStats(0)
    histo.Draw('colz')
    text = ROOT.TLatex(0.5, 0.93, '{:2.1f} mGy/y equiv.'.format(rate_perannum))
    text.SetNDC()
    text.SetTextColor(ROOT.kRed)
    texts.append(text)
    text.Draw()
    tag = 'd={:}, 15h'.format(shift)
    if shift == 'Bg':
        tag = 'Bckg. 39h, scaled'
    text = ROOT.TLatex(0.1, 0.93, tag)
    text.SetNDC()
    text.SetTextColor(ROOT.kBlue)
    texts.append(text)
    text.Draw()
    
can.Print(can.GetName()+'.png')
can.Print(can.GetName()+'.pdf')
can_bg.Print(can.GetName()+'.png')
can_bg.Print(can.GetName()+'.pdf')

ROOT.gApplication.Run()
