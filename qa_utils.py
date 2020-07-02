# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:48:55 2019

@author: shday
"""

import math
from collections import namedtuple
import pandas as pd
import numpy as np

def construct_curve(pka, a_conc):
    b_vol = np.arange(1,25,0.2)
    b_conc = 0.1
    veq = 10*a_conc/b_conc
    sol_ph = []
    for ii in b_vol:
        if ii < veq-0.1:
            sol_ph.append(pka-np.log10((veq-ii)/ii))
        elif ii > veq+0.1:
            sol_ph.append(14+np.log10(np.sqrt(10*0.1/(10+ii)*10**(pka-14))+(ii-veq)*b_conc/(ii+10)))
        else:
            sol_ph.append(14+np.log10(np.sqrt(10*0.1/(10+ii)*10**(pka-14))))
    return sol_ph
