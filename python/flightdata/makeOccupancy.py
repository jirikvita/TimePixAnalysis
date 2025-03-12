#!/usr/bin/python

# jk 30.1.2019, 7.2.2019

import os, sys
from ConvTool import *
sdirs = ['FrkGvaJan2019/', 'PrgFrkJan2019/', 'ZurPrgFeb2019/', 'GvaZurFeb2019/']



###################################

for sdir in sdirs:
    print('Working on {}'.format(sdir,))
    for tfile in os.popen('cd {} ; ls *.txt'.format(sdir)):
        txt = tfile[:-1]
        txtfile = open(sdir + txt, 'read')
        sum = 0.
        for line in txtfile.readlines():
            for item in line.split():
                if len(item) > 0 :
                    ene =  makefloat(item)
                    if ene > 0.:
                        sum = sum + 1
        txtfile.close()
        base = txt
        base = base.replace('.txt', '')
        intfile = open(sdir + base + '.occ', 'write')
        #print txt, sum
        intfile.write('{}\n'.format(sum))
        intfile.close()
