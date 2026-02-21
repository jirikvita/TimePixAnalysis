#!/usr/bin/python

# jk 8.2.2026, Toyama

from ReadToRoot import *
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
RESET  = "\033[0m"

# store total frame energy in MeV
Es = []
ifile = -1
suspects = {}
thr = 30e3
suspect_pngs = []
for path in Path("./").glob("*.txt"):
    fname = path.name
    #print(fname)
    if 'dsc' in fname or 'log' in fname:
        continue
    ifile += 1
    #print(fname)
    rfname, etot = readToRoot(fname)
    Es.append(etot/1000.)
    col = RESET
    if etot > thr:
        col = RED
        suspects[ifile] = etot/1000.
        suspect_pngs.append(rfname.replace('.root','.png'))
    print(col + '{:10} {:} {:}'.format(ifile, rfname, etot) + RESET)
    
    # hack
    #if ifile > 10:
    #    break

print('Moving root files...')
os.system('mkdir -p root')
os.system('hadd all.root *.root')
os.system('mv *.root root/')

print(f'Suspected frames with energy over {thr} MeV:')
print(suspects)
print('eog ', end='')
for png in suspect_pngs:
    print(png, end=' ')
print()

plt.plot(Es, color = 'blue')
plt.xlabel("frame")
plt.ylabel("E [MeV]")
plt.title("Energy per frame")
plt.savefig('timeline.png')
plt.show()


Emax = max(Es) + 1.
nb = 100
dE = Emax / nb
mean = np.mean(Es)
std = np.std(Es)
bins = np.linspace(0., Emax, nb)

#plt.figure()
#plt.hist(Es, bins=bins)
#plt.title("Histogram of energy per frame")
#plt.xlabel("E [MeV]")
#plt.ylabel("frames")
#plt.show()

# ---- Main histogram ----
fig, ax = plt.subplots()
mycol = '#00AA00'

ax.hist(Es, bins=bins, color = mycol, alpha = 0.7)
ax.set_title("Histogram of energy per frame")
ax.set_xlabel("E [MeV]")
ax.set_ylabel("frames")

## Mean line
ax.axvline(mean, linestyle="--", linewidth=1, label=f"Mean = {mean:.2f}")
## Std lines
ax.axvline(mean - std, linestyle=":", linewidth=1, label=f"-1σ = {mean-std:.2f}")
ax.axvline(mean + std, linestyle=":", linewidth=1, label=f"+1σ = {mean+std:.2f}")
ax.legend()

# Print mean and std as text inside plot
textstr = f"Mean = {mean:.3f} MeV\nStd Dev = {std:.3f} MeV"
ax.text(
    0.650, 0.48,
    textstr,
    transform=ax.transAxes,   # relative axis coordinates
    fontsize=10,
    #verticalalignment='bottom',
    #horizontalalignment='center',
    bbox=dict(boxstyle="round", alpha=0.2, facecolor="white")
)


# ---- Inset log-scale histogram ----
ax_inset = inset_axes(ax, width="35%", height="35%", loc="upper right")

ax_inset.hist(Es, bins=bins, color = mycol, alpha = 0.7)
ax_inset.set_yscale("log")
#ax_inset.set_title("Log scale", fontsize=8)
ax_inset.tick_params(labelsize=8)

plt.savefig('energy_per_frame.png')

plt.show()
