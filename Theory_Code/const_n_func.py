###     const_n_func.py
###     Private functions for calculator for "Hall Effect" experiment
###     Nagel lab
###     by Chiao-Yu Tao
###     Last edited: 2016/04/01

import math
from blitzdb import Document

class Material(Document):
        class Meta(Document.Meta):
                pass

m = 9.10938356e-31 #mass of electron
q = 1.60217662e-19 #charge of electron
mu_0 = 4*math.pi*1e-7

CALC_RES = lambda w, R, t, w_else, l_else, Temp, Tref, res, Tcoeff: (R*math.pi/w+l_else/w_else)/t*res*(1+(Temp-Tref)*Tcoeff)

MODEL_LIN = lambda x: x; #linear w/R dependence
MODEL_CRC = lambda x: math.pow(x,2)/2/math.pow(math.log(1-x),2)*((1/math.pow(1-x,2))-1); #Curved resistance correction
MODEL_SCCJ = lambda x: math.log(1/(1-x)); #Superconducting-constant current density
SIG_NORMAL = lambda n, w, t, I: m/q*math.pow(I/(n*q*w*t),2) #carrier density, width, thickness, current
SIG_SC = lambda L, w, t, I: q/m*math.pow(mu_0*(L**2)*I/(w*t),2) #penetration depth, width, thickness, current

def HALL_POT(n, w, t, I, extB=0., C=1.): #calculate the magnetica Hall potential when external field is turned on or not.
    if extB == 0.:
        return C*1e-7*(I**2)/(n*q*w*t)
    elif extB > 0.:
	return I*extB/(n*q*t)

