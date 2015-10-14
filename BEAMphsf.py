import sys
import struct
import math

SHORT = 0
LONG  = 1

def read_header(phsf):
    """
    Read and return PhSF header

    :param phsf: open phase space file
    :type phsf: file
    :returns: header info
    :rtype: tuple
    """
    mode = phsf.read(5) # shall be MODE0 or MODE2
    #print(mode)

    m = -1
    if mode == b"MODE0":
        #print("SHORT BEAMNRC file found")
        m = SHORT
    elif mode == b"MODE2":
        #print("LONG BEAMNRC file found")
        m = LONG
    else:
        print("Unknown phase space file format")
        sys.exit()

    NPPHSP = struct.unpack('i', phsf.read(4))[0] # total nof of particle records

    NPHOTPHSP = struct.unpack('i', phsf.read(4))[0] # total nof of photon records

    EKMAX = struct.unpack('f', phsf.read(4))[0] # max kinetic energy, MeV

    EKMIN = struct.unpack('f', phsf.read(4))[0] # min electron kinetic energy, MeV, shall be ECUT-0.511

    NINCP = struct.unpack('f', phsf.read(4))[0] # nof original incident particles

    if m == LONG:
        dummy = phsf.read(7) # skip fortran garbage, for direct access of record with size 32bytes
    else: # MODE0 file
        dummy = phsf.read(3) # skip fortran garbage, for direct access of record with size 28bytes

    return (m, NPPHSP, NPHOTPHSP, EKMAX, EKMIN, NINCP)

def read_record_short(phsf):
    """
    Read MODE0 PhSF particle record

    :param phsf: open phase space file
    :returns: record tuple
    """

    LATCH = struct.unpack('i', phsf.read(4))[0]
    E = struct.unpack('f', phsf.read(4))[0]
    X = struct.unpack('f', phsf.read(4))[0]
    Y = struct.unpack('f', phsf.read(4))[0]
    U = struct.unpack('f', phsf.read(4))[0]
    V = struct.unpack('f', phsf.read(4))[0]
    W = math.sqrt(1.0 - (U*U + V*V))
    WT = struct.unpack('f', phsf.read(4))[0]
    if (WT < 0.0): # weight sign is in fact Z directional cosine sign
        WT = -WT
        W  = -W

    return (LATCH, E, X, Y, U, V, W, WT)

def read_record_long(phsf):
    """
    Read MODE2 PhSF particle record

    :param phsf: open phase space file
    :returns: record tuple
    """

    LATCH = struct.unpack('i', phsf.read(4))[0]
    E = struct.unpack('f', phsf.read(4))[0]
    X = struct.unpack('f', phsf.read(4))[0]
    Y = struct.unpack('f', phsf.read(4))[0]
    U = struct.unpack('f', phsf.read(4))[0]
    V = struct.unpack('f', phsf.read(4))[0]
    W = math.sqrt(1.0 - (U*U + V*V))
    WT = struct.unpack('f', phsf.read(4))[0]
    ZLAST = struct.unpack('f', phsf.read(4))[0]
    if (WT < 0.0): # weight sign is in fact Z directional cosine sign
        WT = -WT
        W  = -W

    return (LATCH, E, X, Y, U, V, W, WT, ZLAST)
