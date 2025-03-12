#!/usr/bin/python

import os,sys, math

#inputs = ['rate',  ]
#inputs = ['etot', ]
inputs = ['rate', 'etot', 'sizes', 'ene' ]

for input in inputs:
    ncolumns = int(os.popen('cat %s.txt | wc -l' % (input,)).readline()[:-1])
    print(ncolumns)
    Lines = []
    infile = open('%s.txt' % (input,), 'r')
    for line in infile.readlines():
        nline = line[:-2]
        nnline = nline.split()
        nnnline = []
        for n in nnline:
            nnnline.append(int(n))
        Lines.append(nnnline)
    print(Lines)
    outfilename = input + '_trans.txt'
    outfile = open(outfilename, 'w')
    print('Writing transposed into a fil %s' % (outfilename,))
    for i in range(0,len(Lines[0])):
        for j in range(0,ncolumns):
            if j < ncolumns-1:
                outfile.write('%i ' % (Lines[j][i],) )
            else:
                outfile.write('%i' % (Lines[j][i],) )
        outfile.write('\n')

    infile.close()
    outfile.close()
    os.system('mv -i %s.txt %s_orig.txt' %(input,input,))
    os.system('mv -i %s_trans.txt %s.txt' %(input,input,))
    
# find highest energies:
# cat etot.txt | awk '{print $2 " " $1;};' | sort -n 

# ene:
# Energy [keV]    All particles   Dots    Small blobs     Curly tracks    Heavy blobs     Heavy tracks    Straight tracks

# rate:
# Number of frame Number of all particles Number of "Dot" Number of "Small blob"  Number of "Curly track" Number of "Heavy blob"  Number of "Heavy track" Number of "Straight track"

# etot:
# 'Number of frame',  'Energy [keV]'

# sizes:
# Size   'All particles', 'Dots', 'Small blobs', 'Curly tracks', 'Heavy blobs', 'Heavy tracks', 'Straight tracks'

