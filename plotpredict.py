#!/usr/bin/python

#
# plotpredict.py
# Plot the results of predictmulti2.py
#
# Usage: plotpdf.py
#   To use a differently-named input file, manually edit the loadtxt()
#   argument.
#
# Usage: plotpredict.py predict.out
#
# Created by Jayanth Chennamangalam
#

import sys
import numpy as np
import scipy.stats as sps
import matplotlib as mp
import matplotlib.pyplot as plt


# function definitions
def texInit(fontsize):
    # set plotting font properties
    font = {"family" : "serif",
            "weight" : "regular",
            "size"   : fontsize}
    plt.rc("font", **font)
    # force matplotlib to use Type 1 fonts instead of Type 3
    mp.rcParams["ps.useafm"] = True
    mp.rcParams["pdf.use14corefonts"] = True
    mp.rcParams["text.usetex"] = True

# initialize tex-related stuff, and specify a font size
texInit(18)

# perform a MC simulation to get Nmax
data = np.loadtxt(sys.argv[1])
Nmax = data[:,0]
Nnd = data[:,1]
Nbeam = data[:,2]
mean = data[:,3]
std = data[:,4]
bf = data[:,5]
ci68ll = data[:,6]
ci68med = data[:,7]
ci68ul = data[:,8]
ci99ll = data[:,9]
ci99med = data[:,10]
ci99ul = data[:,11]

ax1 = plt.subplot(111)
(_, _, blines) = ax1.errorbar(Nbeam, mean, yerr=(mean-ci99ll, ci99ul-mean), fmt="b,")
for x in blines:
    x.set_linestyle("--")
ax1.errorbar(Nbeam, mean, yerr=(mean-ci68ll, ci68ul-mean), fmt="b,", elinewidth=6, capsize=0)
ax1.plot(Nbeam, mean, "ws", markeredgecolor="b")
ax1.set_xlim(np.min(Nbeam), np.max(Nbeam))
plt.xlabel(r"$\left<N\right>$")
plt.ylabel(r"$n_{\rm obs}$")
ax1.set_ylim(0.0, np.max(mean+(3*std)))
ax2 = ax1.twiny()
ax2.plot(Nnd, mean, alpha=0)
ax2.set_ylim(0.0, np.max(mean+(3*std)))
ax2.set_xlim(Nnd[0], Nnd[len(Nbeam)-1])
ax2.set_xlabel(r"$\left<N_{\rm GC}\right>$")

plt.show()

