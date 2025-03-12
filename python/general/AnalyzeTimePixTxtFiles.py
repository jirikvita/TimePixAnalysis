#!/snap/bin/pyroot
# was: #!/usr/bin/python3
# Ne 19. listopadu 2023, 20:26:46 CET


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit
from scipy.stats import chisquare


from math import sqrt, pow, log, exp
import os, sys, getopt

cans = []
stuff = []

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    matplotlib.use('Agg')

    pattern = '*.txt'
    if len(sys.argv) > 1:
      pattern = argv[1]
    
    fnames = os.popen('ls {}'.format(pattern)).readlines()
    
    # energy per frame
    enes = []
    for xfname in fnames:
        fname = xfname[:-1]
        txtf = open(fname, 'r')
        etot = 0.
        for xline in txtf.readlines():
            line = xline[:-1]
            for sval in line.split():
                etot = etot + float(sval)
        enes.append(etot)
    print(enes)
    print(max(enes))
    print(enes.index(max(enes)))

    ex = range(0, len(enes))
    plt.clf()
    plt.plot(ex, enes, color='blue')
    plt.title('Total frame energy [keV]')

    plt.legend(frameon=False)
    plt.savefig('etot.png')

    plt.show()
    
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

