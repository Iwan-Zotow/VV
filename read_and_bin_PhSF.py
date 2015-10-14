#!/usr/bin/python

import math
import matplotlib.pyplot as plt

import BEAMphsf
from H1Du import H1Du

with open("C25.egsphsp1", "rb") as phsf:
    
    m, NPPHSP, NPHOTPHSP, EKMAX, EKMIN, NINCP = BEAMphsf.read_header(phsf)
    
    print(m) # mode
    print(NPPHSP) # total nof of particle records
    print(NPHOTPHSP) # total nof of photon records
    print(EKMAX) # max kinetic energy, MeV
    print(EKMIN) # min electron kinetic energy, MeV, shall be ECUT-0.511
    print(NINCP) # nof original incident particles
    print("================ End of PhSF header ======================")

    he = H1Du(50, 0.01, 1.33)
    hx = H1Du(31, -15.5, 15.5)
    hy = H1Du(31, -15.5, 15.5)

    for i in range (0, NPPHSP):
        (LATCH, E, X, Y, U, V, W, WT, ZLAST) = BEAMphsf.read_record_long(phsf)
        if LATCH == 8388608: #8388608=2^23, this is photon, see PIRS-509, page #96
            if E<0:
                E = -E

            he.fill(E, WT)
            hx.fill(X, WT)
            hy.fill(Y, WT)

    print(he.nof_events(), he.integral())

    X = []
    Y = []

    step = he.step()
    for i in range (-1, he.size()+1):
        x = he.lo() + (float(i) + 0.5)*step
        d = he[i] # data from bin with index i
        y = d[0]  # first part of bin is collected weights
        X.append(x)
        Y.append(y)

    width = 0.8*step
    p1 = plt.bar(X, Y, width, color='r')

    plt.xlabel('Energy(MeV)')
    plt.ylabel('N of photons')
    plt.title('Energy distribution')

    plt.grid(True);
    plt.tick_params(axis='x', direction='out')
    plt.tick_params(axis='y', direction='out')

    plt.show()
