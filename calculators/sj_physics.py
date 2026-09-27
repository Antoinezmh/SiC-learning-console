import numpy as np

EPS0=8.8541878128e-14 # F/cm
Q=1.602176634e-19

def ideal_1d_unipolar(vb_v, eps_r=9.7, mu_n=900., ec_v_cm=2.5e6):
    eps=eps_r*EPS0
    wd_cm=2*vb_v/ec_v_cm
    nd_cm3=eps*ec_v_cm/(Q*wd_cm)
    ron=4*vb_v**2/(eps*mu_n*ec_v_cm**3)
    return {"wd_um":wd_cm*1e4,"nd_cm3":nd_cm3,"ron_ohm_cm2":ron}

def idealized_sj(vb_v, wn_um, eps_r=9.7, mu_n=900., ec_vertical=2.5e6, ec_lateral=2.0e6):
    """Idealized balanced-SJ scaling model. Not a calibrated 2-D avalanche solution."""
    eps=eps_r*EPS0
    wn_cm=wn_um*1e-4
    l_cm=vb_v/ec_vertical
    nd_max=eps*ec_lateral/(Q*wn_cm)
    ron=2*vb_v*wn_cm/(eps*mu_n*ec_lateral)
    return {"column_um":l_cm*1e4,"nd_max_cm3":nd_max,"ron_ohm_cm2":ron}

def heuristic_imbalance_bv(v_ideal, delta, aspect_ratio, k=1.0):
    """Heuristic sensitivity visualization only; NOT the Wang/Napoli/Udrea analytical solution."""
    return v_ideal/(1+k*abs(delta)*aspect_ratio)
