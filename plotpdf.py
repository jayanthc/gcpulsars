#!/usr/bin/python

#
# plotpdf.py
# Plot the results of galcenbayes.
#
# Usage: plotpdf.py
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

fN = np.loadtxt("survey.df")
line, = plt.plot(fN[:,0], fN[:,1], linewidth=2.0, label=r"$\nu = 4.85~{\rm GHz,}~S_{\rm min} = 50~\mu{\rm Jy}$")
line.set_dashes([4, 4, 1, 4, 1, 4])
fN = np.loadtxt("sminbat11.df")
plt.plot(fN[:,0], fN[:,1], "--", linewidth=2.0, label=r"$\nu = 6.6~{\rm GHz,}~S_{\rm min} = 592~\mu{\rm Jy}$")
fN = np.loadtxt("sminjoh06.df")
plt.plot(fN[:,0], fN[:,1], "-.", linewidth=2.0, label=r"$\nu = 8.4~{\rm GHz,}~S_{\rm min} = 201~\mu{\rm Jy}$")
fN = np.loadtxt("sminden10b.df")
plt.plot(fN[:,0], fN[:,1], "-", linewidth=2.0, label=r"$\nu = 8.50~{\rm GHz,}~S_{\rm min} = 23~\mu{\rm Jy}$")
fN = np.loadtxt("sminmac10.df")
plt.plot(fN[:,0], fN[:,1], ":", linewidth=2.0, label=r"$\nu = 14.4~{\rm GHz,}~S_{\rm min} = 31~\mu{\rm Jy}$")

plt.xscale("log")
plt.ylim(0.0, 1.0)
plt.xlabel(r"$N$")
plt.ylabel(r"$P(N~|~n_{\rm np} = 0,~n_{\rm mag} = 1)$")
plt.legend(loc="upper right", fontsize=16, numpoints=1)
plt.show()

