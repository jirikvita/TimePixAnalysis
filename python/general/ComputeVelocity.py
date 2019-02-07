#!/usr/bin/python

from math import *

MeV = 1.
GeV = 1e3

c= 299792.458 # km/s
m = 3.7 * GeV
T = 5.5 * MeV
E = m+T
p = sqrt(E*E - m*m)
beta = sqrt(T*T + 2*T*m) / (m + T)
print 'beta=%1.5f' % (p/E)
print 'beta=%1.5f, v=%f km/s' % (beta,beta*c,)

# klasicky: T = 1/2 m*v^2
beta = sqrt(2*T/m)
print 'Klasicky: beta=%1.5f' % (beta,)
print 'Klasicky: v=%1.5f km/s' % (beta*c,)
