import numpy as np

def charge_balance(nd_cm3, wn_um, na_cm3, wp_um, acceptor_ionization=1.0):
    qn = nd_cm3 * wn_um
    qp = na_cm3 * acceptor_ionization * wp_um
    ratio = qp / qn
    imbalance = (qn - qp) / qn
    return {"qn_arb": qn, "qp_arb": qp, "qp_over_qn": ratio, "imbalance": imbalance}

def illustrative_ionization_sweep(nd_cm3, wn_um, na_cm3, wp_um, temperatures_c, f_low, f_high):
    temps=np.asarray(temperatures_c,dtype=float)
    fractions=np.interp(temps,[temps.min(),temps.max()],[f_low,f_high])
    ratios=(na_cm3*wp_um*fractions)/(nd_cm3*wn_um)
    return fractions,ratios
