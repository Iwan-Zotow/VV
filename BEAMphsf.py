import struct


def write_all_events(filename , events):
    """
    Given the file name, write out all events
    """

    with open(filename, "wt") as f:
        for e in events:
            f.write('{0:15.4e} {1:15.4e} {2:15.4e} {3:15.4e} {4:15.4e} {5:15.4e} {6:15.4e} {7:15.4e}\n'.format(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7]))

    return None


def make_energy_scale(nof_bins_hi2me, lo, me, hi):
    """
    Out of number of bins between hi and me,
    build non-uniform energy scale
    """

    # bins in hi-to-me region
    step = (hi - me)/float(nof_bins_hi2me)

    scale = []

    # filling lo-to-me region with the same bin size
    prev = me
    while True:
        scale.append(prev)
        prev -= step
        if prev < lo:
            break

    if scale[-1] != lo:
        scale.append(lo)

    # make it ascending
    scale = sorted(scale)

    # finally fill me-to-hi
    for k in range(1, nof_bins_hi2me):
        scale.append(me + float(k)*step)

    scale.append(hi)

    return scale


def move_event(e, zstart, zend):
    """
    Move particles from current plane to plane shifted by zshift
    :param e: an event
    :param zshift: shift value, in mm
    """
    X = e[2]
    Y = e[3]
    Z = zstart

    wx = e[5]
    wy = e[6]
    wz = e[7]

    s = 0.0
    if wz != 0.0:
        s = (zend - zstart) / wz

    return (X + wx*s, Y + wy*s, zend)
