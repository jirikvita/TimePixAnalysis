#!/usr/bin/python

# jk 30.1.2019

import os, sys
from ConvTool import *
#sdirs = ['FrkGvaJan2019/', 'PrgFrkJan2019/']
sdirs = ['ZurPrgFeb2019/', 'GvaZurFeb2019/']




###################################

for sdir in sdirs:
    for tfile in os.popen('cd {} ; ls *.txt'.format(sdir)):
        txt = tfile[:-1]
        txtfile = open(sdir + txt, 'read')
        sum = 0.
        for line in txtfile.readlines():
            for item in line.split():
                if len(item) > 0 :
                    sum = sum + makefloat(item)
        txtfile.close()
        base = txt
        base = base.replace('.txt', '')
        intfile = open(sdir + base + '.int', 'write')
        #print txt, sum
        intfile.write('{}\n'.format(sum))
        intfile.close()
