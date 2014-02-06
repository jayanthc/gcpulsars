#!/usr/bin/python

#
# plotnvsf.py
# Plot the results of galcenbayes_fixedf
#
# Usage: plotnvsf.py
#   To use a differently-named input file, manually edit the loadtxt()
#   argument.
#
# Created by Jayanth Chennamangalam
#

import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt


# set plotting font properties
font = {"family" : "serif",
        "weight" : "regular",
        "size"   : 18}
plt.rc("font", **font)
# force matplotlib to use Type 1 fonts instead of Type 3
mp.rcParams["ps.useafm"] = True
mp.rcParams["pdf.use14corefonts"] = True
mp.rcParams["text.usetex"] = True

fN = np.loadtxt("sminden10a.nvsf")
# 0 - f; 1 - mean; 2 - mode; 3 - lowerlimit; 4 - median; 5 - upperlimit
sel = 5
plt.plot(fN[:,0], fN[:,sel], "o:", label=r"$\nu = 4.85~{\rm GHz,}~S_{\rm min} = 50~\mu{\rm Jy}$")
fN = np.loadtxt("sminbat11.nvsf")
plt.plot(fN[:,0], fN[:,sel], "^:", label=r"$\nu = 6.6~{\rm GHz,}~S_{\rm min} = 592~\mu{\rm Jy}$")
fN = np.loadtxt("sminjoh06.nvsf")
plt.plot(fN[:,0], fN[:,sel], "d:", label=r"$\nu = 8.4~{\rm GHz,}~S_{\rm min} = 201~\mu{\rm Jy}$")
fN = np.loadtxt("sminden10b.nvsf")
plt.plot(fN[:,0], fN[:,sel], "s:", label=r"$\nu = 8.50~{\rm GHz,}~S_{\rm min} = 23~\mu{\rm Jy}$")
fN = np.loadtxt("sminmac10.nvsf")
plt.plot(fN[:,0], fN[:,sel], "v:", label=r"$\nu = 14.4~{\rm GHz,}~S_{\rm min} = 31~\mu{\rm Jy}$")

plt.yscale("log")
plt.ylim(40.0, 400000.0)
plt.xlabel(r"$f$")
plt.ylabel(r"$N_{\rm max}$")
plt.legend(loc="upper right", fontsize=16, numpoints=1)
plt.show()

