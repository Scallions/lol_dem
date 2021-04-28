import pandas as pd
import numpy as np


ZERO = 1e-9

def read_data(file_path, header=None):
    return pd.read_csv(file_path, header=header, sep=r"\s+", names=["lon","lat","alt","t1","t2"],dtype = {'t1': int, 't2': int})


def vector_product(p1, p2):
    return p1[0]*p2[1] - p2[0]*p1[1]

def is_intersected(A, B, C, D):
    AC = [C[0] - A[0], C[1] - A[1]]
    AD = [D[0] - A[0], D[1] - A[1]]
    BC = [C[0] - B[0], C[1] - B[1]]
    BD = [D[0] - B[0], D[1] - B[1]]
    CA = [A[0] - C[0], A[1] - C[1]]
    CB = [B[0] - C[0], B[1] - C[1]]
    DA = [A[0] - D[0], A[1] - D[1]]
    DB = [B[0] - D[0], B[1] - D[1]]
    return (vector_product(AC, AD) * vector_product(BC, BD) <= ZERO) \
        and (vector_product(CA, CB) * vector_product(DA, DB) <= ZERO)

def find_crossover(aorbit, dorbit, a1, a2, d1, d2):
    if a1 == a2 or d1 == d2:
        return -1, -1
    if not is_intersected(aorbit[a1], aorbit[a2], dorbit[d1], dorbit[d2]):
        return -1,-1
    if a1+1 == a2 and d1+1 == d2:
        return a1,d1

    if a1+1 == a2:
        dm = (d1+d2) // 2
        # a1 a2 d1 dm 
        ar, dr = find_crossover(aorbit, dorbit, a1, a2, d1, dm)
        if ar != -1:
            return ar, dr 
        # a1 a2 dm d2
        ar, dr = find_crossover(aorbit, dorbit, a1, a2, dm, d2)
        if ar != -1:
            return ar, dr
    elif d1+1 == d2:
        am = (a1+a2) // 2
        # a1 am d1 d2
        ar, dr = find_crossover(aorbit, dorbit, a1, am, d1, d2)
        if ar != -1:
            return ar, dr 
        # am a2 d1 d2
        ar, dr = find_crossover(aorbit, dorbit, am, a2, d1, d2)
        if ar != -1:
            return ar, dr 
    else:
        am = (a1+a2)//2
        dm = (d1+d2)//2
        # a1 am d1 dm
        ar, dr = find_crossover(aorbit, dorbit, a1, am, d1, dm)
        if ar != -1:
            return ar, dr 
        # am a2 d1 dm
        ar, dr = find_crossover(aorbit, dorbit, am, a2, d1, dm)
        if ar != -1:
            return ar, dr 
        # a1 am dm d2
        ar, dr = find_crossover(aorbit, dorbit, a1, a2, d1, dm)
        if ar != -1:
            return ar, dr 
        # am a2 dm d2
        ar, dr = find_crossover(aorbit, dorbit, am, a2, dm, d2)
        if ar != -1:
            return ar, dr 
    return -1, -1

def distance_sphere(p1, p2):
    p1 = p1 *np.pi/180
    p2 = p2 *np.pi/180
    return np.arccos(np.cos(p1[1]) * np.cos(p2[1]) * np.cos(p1[0] - p2[0]) + np.sin(p1[1])*np.sin(p2[1]))

def cross_point(A, B, C, D):
    x1, y1 = A[:2]
    x2, y2 = B[:2]
    x3, y3 = C[:2]
    x4, y4 = D[:2]
    t1 = (x3 * (y4 - y3) + y1 * (x4 - x3) - y3 * (x4 - x3) - x1 * (y4 - y3)) / ((x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1))
    t2 = (x1 * (y2 - y1) + y3 * (x2 - x1) - y1 * (x2 - x1) - x3 * (y2 - y1)) / ((x4 - x3) * (y2 - y1) - (x2 - x1) * (y4 - y3))
    if 0.0 <= t1 <= 1.0 and 0.0 <= t2 <= 1.0:
        ans = [x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1)]
    else:
        return [-1,-1,-1,-1]
    dA = distance_sphere(A[:2], np.array(ans))
    dB = distance_sphere(B[:2], np.array(ans))
    dC = distance_sphere(C[:2], np.array(ans))
    dD = distance_sphere(D[:2], np.array(ans))
    h1 = (B[2] - A[2]) * dA / (dA+dB) + A[2]
    h2 = (D[2] - C[2]) * dC / (dC+dD) + C[2]
    ans.append(h1)
    ans.append(h2)
    return ans
