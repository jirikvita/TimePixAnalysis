#!/usr/bin/python
# JK Mon 13 May 07:40:54 CEST 2019
# 23.5.2019: median! ;-)
# TODO: plot GPS height from logs as function of time! Remove some more outliars?!



import numpy as np

#import ROOT
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
# timepix MX-10
#h = 0.03
# Advacam MiniPix
h = 0.05

# Volume:
V = d*d*h
# Silicon: g/cm^3
rho = 2.3296 
# mass in kg:
mass = 0.001*V*rho
elCh = 1.602e-19
secInY = 31557600.

# expects keV and seconds
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
