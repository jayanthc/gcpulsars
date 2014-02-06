#!/usr/bin/python

#
# calcsmin.py
# Calculate the flux density limit corresponding to the inner parsec, for a set
#   of surveys. For details, see Chennamangalam & Lorimer (2014).
#
# Usage: calcsmin.py
#
# Created by Jayanth Chennamangalam
#

import numpy as np
import matplotlib.pyplot as plt


def nearestIdx(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx

def calcSminInner(smin, fwhm):
    inpcbeam = 25            # arcsec
    k = 4 * np.log(2)

    x = np.linspace(-fwhm / 2, fwhm / 2, num=1000)
    s = np.exp(-(k * x**2)/(fwhm**2))
    scale = smin / np.max(s)
    s = scale * s
    s = (smin - s) + smin

    # extract the beam within 1 pc = 25 arcsec
    xloidx = nearestIdx(x, -inpcbeam / 2)
    xhiidx = nearestIdx(x, inpcbeam / 2)
    xinpc = x[xloidx: xhiidx]
    sinpc = s[xloidx: xhiidx]

    print "S_min | peak =", np.min(s), "uJy"
    print "S_min | beam =", np.mean(s), "uJy"
    print "S_min | inner parsec =", np.mean(sinpc), "uJy"

    plt.plot(x, s, 'y:')
    plt.plot(xinpc, sinpc, 'r-')
    plt.xlim(np.min(x), np.max(x))
    plt.ylim(0.0, np.max(s))
    plt.show()

# NOTE: FWHM is in arcseconds.

print "Past Surveys"
print "------------"
# Parkes, PMPS (Manchester et al. 2001, Morris et al. 2002)
print "1.374 GHz, 3518.2 uJy"
calcSminInner(3518.2, 704)
# Parkes, 7' (Johnston et al 2006)
print "3.1 GHz, 1000 uJy:"
calcSminInner(1000, 420)
# GBT, 2.5' (Deneva 2010)
print "4.85 GHz, 49.8 uJy:"
calcSminInner(49.8, 150)
# Parkes, 1.4' (Bates et al. 2011)
print "6.6 GHz, 589.6 uJy:"
calcSminInner(589.6, 192)
# Parkes, 2.4' (Johnston et al. 2006)
print "8.4 GHz, 199.5 uJy:"
calcSminInner(199.5, 144)
# GBT, 1.4" (Deneva 2010)
print "8.50 GHz, 22.6 uJy:"
calcSminInner(22.6, 84)
# GBT, 54" (Macquart et al. 2010)
print "14.4 GHz, 30.0 uJy:"
calcSminInner(30.0, 54)

print "Future GBT Surveys"
print "------------------"
print "1.45 GHz, 104.8 uJy"
calcSminInner(104.8, 427)
print "2.165 GHz, 74.4 uJy"
calcSminInner(74.4, 286)
print "5.0 GHz, 40.5 uJy"
calcSminInner(40.5, 124)
print "9.2 GHz, 16.7 uJy"
calcSminInner(16.7, 67)
print "13.7 GHz, 13.5 uJy"
calcSminInner(13.5, 45)
print "22.375 GHz, 8.2 uJy"
calcSminInner(8.2, 28)

