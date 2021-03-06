#!/usr/bin/python

#
# predictmulti2.py
# Run a Monte Carlo simulation to estimate the number of observable pulsars in
#   the Galactic Centre region in a given survey, for a given set of population
#   sizes.
#
# Usage: predictmulti2.py -r <n-rep> -f <freq> -s <s-min> -T <tsys> -G <gain>
#                         -t <tobs> -b <bw> -S <snr-min>
#   n-rep - number of realizations
#   freq - frequency of the survey
#   s-min - flux density limit of survey, in mJy
#   tsys - system temperature, in K
#   G - gain of the system, in K Jy^-1
#   tobs - observation duration, in s
#   bw - bandwidth, in MHz
#   snr-min - minimum SNR
#
# Example: predictmulti2.py -r 10000 -f 4.85 -s 0.050 -T 305 -G 2
#                           -t 23400 -b 800 -S 6 > predict.out
#   Use plotpredict.py to plot the contents of predict.out.
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

def nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# get command-line arguments
# 0                  1  2       3  4      5  6       7  8      9  10     11 12     13 14   15 16
# ./predictmulti2.py -r <n-rep> -f <freq> -s <s-min> -T <tsys> -G <gain> -t <tobs> -b <bw> -S <snr-min>
nRep = int(sys.argv[2])                 # number of realizations
freq = float(sys.argv[4])               # frequency of the survey, in GHz
Smin = float(sys.argv[6])               # flux density limit of survey, in mJy
Tsys = float(sys.argv[8])               # system temperature, in K
G = float(sys.argv[10])                 # gain of the system, in K Jy^-1
tobs = float(sys.argv[12])              # observation duration, in s
BW = float(sys.argv[14])                # bandwidth, in MHz
SNRMin = float(sys.argv[16])            # minimum SNR

# constant
nPol = 2

talpha = -3.8
tau = 1.3 * (freq / 1.0)**talpha        # in s

delta = 0.1                             # duty cycle, 10%

R = 1e6                                 # radius, in cm; 10 km = 10^6 cm
I = 1e45                                # moment of inertia, in g cm^2
c = 2.99792458e10                       # speed of light, in cm s^-1
K = (8 * np.pi**2 * R**6) / (3 * I * c**3)

P0mean = 0.300                          # s
sigmaP0 = 0.150                         # s
# limits of left-truncated gaussian (truncated at 0.0 on left, no truncation
# (large value) on right
a, b = (0.0 - P0mean) / sigmaP0, (10000.0 - P0mean) / sigmaP0

logBmean = 12.65                        # log (B/G)
sigmalogB = 0.55                        # log (B/G)

tmax = 1e9          # years

BP2lim = 0.17 * 1e12                    # B/P^2, in G s^-2

L0 = 0.18                               # mJy kpc^2
ep = -1.5
epdot = 0.5
sigmaLcorr = 0.8

# need to scale luminosities using mean spectral index, from Bates et al. (2013)
# convert Smin at freq to Smin at 1.4 GHz
alpha = -1.41
jc = np.log10(Smin) - (alpha * np.log10(freq))
Smin = alpha * np.log10(1.4) + jc
Smin = 10**Smin

D = 8.25                                # kpc, Genzel et al. (2010)
Lmin = Smin * D**2

#NmaxArray = np.rint(np.logspace(np.log10(38), np.log10(18750), num=10))
xmin = 5000
xstep = 5000
xmax = 80000
nsteps = ((xmax - xmin) / xstep) + 1
NmaxArray = np.rint(np.linspace(xmin, xmax, num=nsteps))

Nnd = np.zeros(len(NmaxArray))
Nbeam = np.zeros(len(NmaxArray))
mean = np.zeros(len(NmaxArray))
std = np.zeros(len(NmaxArray))
ci68ll = np.zeros(len(NmaxArray))
ci68med = np.zeros(len(NmaxArray))
ci68ul = np.zeros(len(NmaxArray))
ci99ll = np.zeros(len(NmaxArray))
ci99med = np.zeros(len(NmaxArray))
ci99ul = np.zeros(len(NmaxArray))
for j in range(len(NmaxArray)):
    Nmax = NmaxArray[j]

    nObs = np.zeros(nRep)
    i = 0
    while i < nRep:
        # Monte Carlo simulation, following Faucher-Giguere & Kaspi (2006)

        # generate the birth period distribution
        P0 = sigmaP0 * sps.truncnorm.rvs(a, b, size=Nmax) + P0mean

        # generate magnetic field distribution
        # create random sample from gaussian
        logB = sigmalogB * np.random.randn(Nmax) + logBmean
        B = 10**logB

        # generate age distribution
        # create uniform random sample in the interval [0.0, 1.0)
        t = np.random.random((Nmax,))
        # change random values to the range [0.0, tmax) years
        t = ((tmax - 0.0) * t) + 0.0
        # convert years to seconds
        t = t * (60 * 60 * 24 * 365)

        # evolve the pulsars (compute P(t) and Pdot)
        P = np.sqrt(P0**2 + (2 * K * B**2 * t))
        Pdot = (K * B**2) / P

        # stack everything together
        pulsars = np.column_stack((B, P, Pdot))

        # get the radio-loud pulsars (pulsars that haven't crossed the death line)
        pulsars = pulsars[pulsars[:,0] / pulsars[:,1]**2 > BP2lim]
        Nnd[j] = Nnd[j] + len(pulsars)
        if 0 == len(pulsars):
            nObs[i] = 0
            i = i + 1
            continue

        # NOTE: applying radiation beaming correction before getting the
        # radio-loud pulsars leads to a different beaming fraction, although
        # the final n_obs will remain the same. the `beaming' fraction,
        # however, makes sense only for radio-loud pulsars, so first get
        # radio-loud pulsars, and then apply beaming correctons.

        # apply radiation beaming corrections
        # compute the probability of a pulsar with period P being beamed
        # towards Earth, Faucher-Giguere & Kaspi (2006), eq. 23
        fP = 0.09 * (np.log10(pulsars[:,1]) - 1)**2 + 0.03
        # generate random numbers in the range [0.0, 1.0)
        r = np.random.random((len(pulsars),))
        pulsars = pulsars[r < fP]
        Nbeam[j] = Nbeam[j] + len(pulsars)
        if 0 == len(pulsars):
            nObs[i] = 0
            i = i + 1
            continue

        # compute the luminosity distribution for all pulsars with L > Lmin
        # compute luminosities using the power law relationship
        # log L = log(L0 * P^ep * Pdot15^epdot) + L-corr
        # (18) from Faucher-Giguere & Kaspi (2006)
        # convert Pdot to 10^-15 s s^-1
        Pdot15 = pulsars[:,2] * 1e15
        # generate a normal distribution with mean = 0.0 and std = sigmaLcorr,
        # to use dither in the standard candle luminosity
        Lcorr = sigmaLcorr * np.random.randn(len(pulsars)) + 0.0
        # generate luminosities
        log10L = np.log10(L0 * pulsars[:,1]**ep * Pdot15**epdot) + Lcorr

        # compute the scatter-broadened width
        wi = pulsars[:,1] * delta       # intrinsic width, in s
        wb = np.sqrt(wi**2 + tau**2)    # scatter-broadened width, in s; ignoring t_dm and t_samp
        # extract pulsars with P > wb (so that the SNR calculation is valid)
        wbtemp = wb
        wb = wb[pulsars[:,1] > wbtemp]
        log10L = log10L[pulsars[:,1] > wbtemp]
        pulsars = pulsars[pulsars[:,1] > wbtemp]
        if 0 == len(pulsars):
            nObs[i] = 0
            i = i + 1
            continue
        # compute signal to noise ratio
        pwf = np.sqrt((pulsars[:,1] - wb) / wb)
        SNR = (10**log10L) * G * np.sqrt(nPol * tobs * BW) * pwf / (D**2 * Tsys)
        pulsars = pulsars[SNR > SNRMin]
        if 0 == len(pulsars):
            nObs[i] = 0
            i = i + 1
            continue

        nObs[i] = len(pulsars)

        i = i + 1

    Nnd[j] = Nnd[j] / nRep
    Nbeam[j] = Nbeam[j] / nRep
    mean[j] = np.rint(np.mean(nObs))
    std[j] = np.rint(np.std(nObs))
    [ci68ll[j], ci68med[j], ci68ul[j]] = np.rint(np.percentile(nObs, [15.8655254, 50.0, 84.1344746]))
    [ci99ll[j], ci99med[j], ci99ul[j]] = np.rint(np.percentile(nObs, [0.1349898, 50.0, 99.8650102]))

    print Nmax, Nnd[j], Nbeam[j], mean[j], std[j], Nbeam[j] * 100.0 / Nnd[j], ci68ll[j], ci68med[j], ci68ul[j], ci99ll[j], ci99med[j], ci99ul[j]

# initialize tex-related stuff, and specify a font size
texInit(18)

ax1 = plt.subplot(111)
(_, _, blines) = ax1.errorbar(Nbeam, ci99med, yerr=(ci99med-ci99ll, ci99ul-ci99med), fmt="b,")
for x in blines:
    x.set_linestyle("--")
ax1.errorbar(Nbeam, ci68med, yerr=(ci68med-ci68ll, ci68ul-ci68med), fmt="b,", elinewidth=6, capsize=0)
ax1.plot(Nbeam, ci99med, "ws", markeredgecolor="b")
ax1.set_xlim(np.min(Nbeam), np.max(Nbeam))
plt.xlabel(r"$\left<N\right>$")
plt.ylabel(r"$n_{\rm obs}$")
ax1.set_ylim(0.0, np.max(ci99med+(3*std)))
ax2 = ax1.twiny()
ax2.plot(Nnd, ci99med, alpha=0)
ax2.set_ylim(0.0, np.max(ci99med+(3*std)))
ax2.set_xlim(Nnd[0], Nnd[len(Nbeam)-1])
ax2.set_xlabel(r"$\left<N_{\rm GC}\right>$")

plt.show()

