import scipy.sparse as sp 
import numpy as np
import time

A = sp.coo_matrix([[1., 1., 3.]*300])
B = sp.coo_matrix([[1., 0., 0.]*300]*300000)


start = time.time()

A*B.T

end = time.time()
print("time: ", end-start)