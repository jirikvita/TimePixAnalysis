#!/usr/bin/python

# jk 8.2.2026, Toyama

from ReadToRoot import *
from pathlib import Path
import matplotlib.pyplot as plt

RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
RESET  = "\033[0m"

# store total frame energy in MeV
Es = []
ifile = -1
for path in Path("./").glob("*.txt"):
    fname = path.name
    #print(fname)
    if 'dsc' in fname:
        continue
    ifile += 1
    #print(fname)
    rfname, etot = readToRoot(fname)
    Es.append(etot/1000.)
    col = RESET
    if etot > 10e3:
        col = RED
    print(col + '{:10} {:} {:}'.format(ifile, rfname, etot) + RESET)
    # hack
    #if ifile > 10:
    #    break
    
os.system('mkdir -p root')
os.system('hadd all.root *.root')
os.system('mv *.root root/')

plt.plot(Es)
plt.xlabel("Frame")
plt.ylabel("E [MeV]")
plt.title("Energy per frame")
plt.savefig('timeline.png')
plt.show()
