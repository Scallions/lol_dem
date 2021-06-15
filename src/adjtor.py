# adjustment

import numpy as np


import data

def read_exclude_orbits():
    """
    read orbits that don't used in the adjustment
    """
    orbits = ["A", "B"]
    return orbits




def crossover_adjustment():

    cross = data.read_crossover_point()

    v = np.ones((lc))
    # A = np.zeros((lc, (la+ld)*2))
    # P = np.eye(lc)
    A = sp.dok_matrix((lc, (la+ld)*2))
    # P = sp.identity(lc)
    P = np.zeros((lc,))
    for i in range(lc):
        # one
        afile = cross.iloc[i,0]
        dfile = cross.iloc[i,1]
        ar = cross.iloc[i,2]
        dr = cross.iloc[i,3]
        d = cross.iloc[i,-1]
        ai = fmap[afile]
        di = fmap[dfile]
        # at = aorbits[ai][0][ar][-2] - aorbits[ai][0][0][-2]
        # dt = dorbits[di-la][0][dr][-2] - dorbits[di-la][0][0][-2]
        at = cross.iloc[i,4] - aorbits[ai][0][0][-2]
        dt = cross.iloc[i,5] - dorbits[di-la][0][0][-2]
        v[i] = d 
        # P[i,i] = 1/(abs(d)+1e-6)
        P[i] = 1/(abs(d)+1e-6)
        A[i,2*ai] = 1
        A[i,2*ai+1] = at 
        A[i,2*di] = -1
        A[i,2*di+1] = -dt
    P = P / np.sum(P)
    P = sp.diags(P)