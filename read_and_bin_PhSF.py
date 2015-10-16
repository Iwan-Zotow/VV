#!/usr/bin/env python

import math
import struct

import matplotlib.pyplot as plt

import BEAMphsf
import H1Dn

scale = BEAMphsf.make_energy_scale(5, lo = 0.01, me = 1.170001, hi = 1.330001)

#print(len(scale))
#print(scale)

(events, nof_photons, nof_electrons, nof_positrons) = BEAMphsf.load_events("C25.egsphsp1", 10000)

print(len(events), nof_photons, nof_electrons, nof_positrons)

#write_all_events("QQQ", events)

he = H1Dn.H1Dn(scale)

for e in events:
    WT = e[0]
    E  = e[1]
    he.fill(E, WT)

print(he.nof_events(), he.integral())

print(he.underflow())
print(he.overflow())

X = []
Y = []
W = []

scale = he.x()
n     = len(scale)
norm  = 1.0/he.integral()

sum = 0.0

for k in range (-1, he.size()+1):
    x = 0.0
    w = (he.lo() - x)
    if k == he.size():
        w = (scale[-1]-scale[-2])
        x = he.hi()
    elif k >= 0:
        w = (scale[k+1] - scale[k])
        x = scale[k]

    d = he[k]     # data from bin with index k
    y = d[0] / w  # first part of bin is collected weights
    y = y * norm
    X.append(x)
    Y.append(y)
    W.append(w)
    sum += y*w

print(sum)

p1 = plt.bar(X, Y, W, color='r')

plt.xlabel('Energy(MeV)')
plt.ylabel('PDF of the photons')
plt.title('Energy distribution')

plt.grid(True);
plt.tick_params(axis='x', direction='out')
plt.tick_params(axis='y', direction='out')

plt.show()
